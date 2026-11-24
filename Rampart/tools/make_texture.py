#!/usr/bin/env python3
"""Makes Rampart's metal texture: res/drawable-nodpi/metal_texture.png (needs `pip install numpy pillow`).

One 450x450 overlay, laid over the dial colour:
  - the dial (r < R_DIAL) gets a sunburst brush: fine streaks fanning out from the centre
  - the outer ring gets a circular brush: fine streaks running round the ring
Each pixel is white or black at low alpha, so the texture lightens/darkens whatever
colour sits underneath and every dial colour option keeps working.

Run from the Rampart/ directory:  python3 tools/make_texture.py
The output is committed; generate.py does not touch it.
"""
import pathlib

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = 450
SS = 3                      # supersampling factor
R_DIAL = 192                # must match generate.py
R_EDGE = 225
DIAL_STRENGTH = 0.13        # max overlay alpha on the dial
RING_STRENGTH = 0.10        # max overlay alpha on the ring

rng = np.random.default_rng(14)


def smooth(a, k):
    """Circular box blur of a 1-D array."""
    return sum(np.roll(a, i) for i in range(-k, k + 1)) / (2 * k + 1)


def norm(a):
    a = a - a.mean()
    return a / (a.std() + 1e-9)


n = W * SS
yy, xx = np.mgrid[0:n, 0:n]
c = (n - 1) / 2
dx, dy = (xx - c) / SS, (yy - c) / SS
r = np.hypot(dx, dy)
theta = (np.arctan2(dx, -dy) / (2 * np.pi)) % 1.0           # 0 at 12 o'clock, clockwise

# --- sunburst: noise indexed by angle, varied slowly along the radius ---
fine = norm(smooth(rng.normal(size=7200), 2))
coarse = norm(smooth(rng.normal(size=900), 2))
bands = norm(rng.normal(size=(1800, 48)))                    # angle x radius bands
ai = (theta * len(fine)).astype(int) % len(fine)
ci = (theta * len(coarse)).astype(int) % len(coarse)
bi = (theta * bands.shape[0]).astype(int) % bands.shape[0]
rb = np.clip(r / R_EDGE * (bands.shape[1] - 1), 0, bands.shape[1] - 1.001)
r0 = rb.astype(int)
band = bands[bi, r0] * (1 - (rb - r0)) + bands[bi, r0 + 1] * (rb - r0)
sun = norm(0.6 * fine[ai] + 0.25 * coarse[ci] + 0.35 * band)

# --- circular brush: noise indexed by radius, varied slowly around the ring ---
rfine = norm(smooth(rng.normal(size=4000), 1))
ri = np.clip((r / R_EDGE * 3000).astype(int), 0, len(rfine) - 1)
wobble = norm(smooth(rng.normal(size=360), 6))
ring = norm(rfine[ri] + 0.4 * wobble[(theta * 360).astype(int) % 360])

# Blend: sunburst inside the dial, circular brush outside, each faded at the edges.
in_dial = np.clip(R_DIAL - r, 0, 1)
in_face = np.clip(R_EDGE - r, 0, 1)
centre_fade = np.clip(r / 14, 0, 1)                         # streaks converge to mush at the hub
amount = (sun * DIAL_STRENGTH * centre_fade * in_dial
          + ring * RING_STRENGTH * (1 - in_dial) * in_face) / 2.2
amount = np.clip(amount, -1, 1)

rgba = np.zeros((n, n, 4), dtype=np.float32)
rgba[..., :3] = np.where(amount[..., None] > 0, 255, 0)
rgba[..., 3] = np.abs(amount) * 255
img = Image.fromarray(rgba.round().astype(np.uint8), "RGBA").resize((W, W), Image.LANCZOS)
out = ROOT / "app/src/main/res/drawable-nodpi/metal_texture.png"
img.save(out, optimize=True)
print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
