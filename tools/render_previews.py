#!/usr/bin/env python3
"""Renders a watch face's preview SVGs to PNG with headless Microsoft Edge (or Chrome).

Usage (from the repo root):
  python tools/render_previews.py <face-dir>                      # all preview/*.svg -> <face-dir>/preview/all-colours.png
  python tools/render_previews.py <face-dir> --only a b --out x.png   # just preview/a.svg and preview/b.svg
  python tools/render_previews.py <face-dir> --thumb slate-yellow # picker thumbnail -> app/src/main/res/drawable-nodpi/preview.png

Options: --size N (cell size in px, default 220 for >12 faces else 450), --cols N (default fits ~2400px).
SVGs are embedded with <object>, not <img>, so previews that load images or use <foreignObject> render fully.
"""
import argparse
import math
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/usr/bin/microsoft-edge", "/usr/bin/google-chrome", "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
GAP, PAD, LABEL = 12, 14, 22


def browser():
    for b in BROWSERS:
        if os.path.exists(b):
            return b
    for name in ("msedge", "google-chrome", "chromium", "chrome"):
        if shutil.which(name):
            return shutil.which(name)
    sys.exit("No Edge or Chrome found - add its path to BROWSERS in tools/render_previews.py")


def screenshot(html, png, width, height):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="wf-render-"))
    page = tmp / "page.html"
    page.write_text(html, encoding="utf-8")
    png = pathlib.Path(png).resolve()
    png.parent.mkdir(parents=True, exist_ok=True)
    if png.exists():
        png.unlink()
    subprocess.run([browser(), "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                    "--hide-scrollbars", f"--user-data-dir={tmp / 'profile'}", "--virtual-time-budget=3000",
                    f"--window-size={width},{height}", f"--screenshot={png}", page.as_uri()],
                   check=False, capture_output=True, timeout=120)
    # On Windows the Edge launcher can exit before its child process writes the screenshot.
    deadline = time.time() + 60
    while time.time() < deadline and not (png.exists() and png.stat().st_size > 0):
        time.sleep(0.5)
    time.sleep(1)
    shutil.rmtree(tmp, ignore_errors=True)
    if not png.exists():
        sys.exit(f"Rendering failed: {png} was not written")
    print(f"wrote {png}")


def obj(svg, size):
    return (f"<object type='image/svg+xml' data='{svg.resolve().as_uri()}' "
            f"style='width:{size}px;height:{size}px;display:block'></object>")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("face", type=pathlib.Path)
    ap.add_argument("--only", nargs="+", help="preview names (without .svg) in the order to show them")
    ap.add_argument("--out", type=pathlib.Path)
    ap.add_argument("--size", type=int)
    ap.add_argument("--cols", type=int)
    ap.add_argument("--thumb", help="render this preview as the watch picker thumbnail instead of a sheet")
    a = ap.parse_args()

    prev = a.face / "preview"
    if a.thumb:
        svg = prev / f"{a.thumb}.svg"
        html = f"<html><body style='margin:0;background:#000'>{obj(svg, 450)}</body></html>"
        screenshot(html, a.out or a.face / "app/src/main/res/drawable-nodpi/preview.png", 450, 450)
        return

    svgs = [prev / f"{n}.svg" for n in a.only] if a.only else sorted(prev.glob("*.svg"))
    missing = [s for s in svgs if not s.exists()]
    if missing or not svgs:
        sys.exit(f"Missing previews: {missing or prev}")
    size = a.size or (220 if len(svgs) > 12 else 450)
    cols = a.cols or max(1, min(len(svgs), (2400 - 2 * PAD + GAP) // (size + GAP)))
    rows = math.ceil(len(svgs) / cols)
    cells = "".join(f"<div>{obj(s, size)}<p>{s.stem}</p></div>" for s in svgs)
    html = ("<html><body style='margin:0;background:#111;color:#bbb;font:13px sans-serif'>"
            f"<div style='display:grid;grid-template-columns:repeat({cols},{size}px);gap:{GAP}px;padding:{PAD}px;"
            f"text-align:center'>{cells}</div><style>p{{margin:4px 0 0}}</style></body></html>")
    width = 2 * PAD + cols * size + (cols - 1) * GAP
    height = 2 * PAD + rows * (size + LABEL) + (rows - 1) * GAP
    screenshot(html, a.out or prev / "all-colours.png", width, height)


if __name__ == "__main__":
    main()
