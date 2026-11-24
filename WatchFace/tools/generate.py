#!/usr/bin/env python3
"""Generates the Tidal watch face (Watch Face Format XML) and a matching SVG preview.

The design: a tinted, softly lit dial with a minute track. A central disc turns
once an hour and carries the minute hand. On the opposite side of that disc an
hour sub-dial orbits the centre; it counter-rotates so its markers stay upright
while its own hand shows the hour.

Run from the WatchFace/ directory:  python3 tools/generate.py
"""
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = 450
C = W / 2

# ---- dial colour themes: centre, mid, edge, sub-dial disc --------------------
THEMES = [
    ("lagoon", "Lagoon", ["#FFB2DDD5", "#FF86BFB6", "#FF4A8780", "#FF9FD0C7"]),
    ("glacier", "Glacier", ["#FFD3E0EA", "#FFA3B9CA", "#FF5C7790", "#FFBDCFDD"]),
    ("sand", "Sand", ["#FFE6DBC7", "#FFCBB99C", "#FF8A785B", "#FFDCCDB3"]),
    ("dusk", "Dusk", ["#FFCDBCDB", "#FFA290BA", "#FF5A4974", "#FFBBA8CE"]),
    ("graphite", "Graphite", ["#FF7A8186", "#FF555B60", "#FF222629", "#FF6A7176"]),
]

MARK = "#F5FFFFFF"        # indices and hands
MARK_SOFT = "#80FFFFFF"   # minute dots
RING = "#40FFFFFF"        # thin rings

# Geometry (450 canvas, scaled by the watch to 480x480 on the Ultra)
R_OUTER_RING = 214
R_TRACK_IN = 186
SUB_OFFSET = 70           # distance from centre to sub-dial centre
SUB_R = 100               # sub-dial outer radius
SUB_DISC_R = 70           # sub-dial inner disc radius
MIN_HAND = (42, 176)      # start/end radius of the minute hand
HOUR_HAND_LEN = 58
HAND = "#FFFFFFFF"        # opaque, so overlapping taper segments don't show seams
HAND_W = (8, 2.4)         # hand width at the base and at the tip
TAPER_STEPS = 18

# Glow overlays. Literal colours only: the watch does not resolve
# [CONFIGURATION] references inside gradients, so the dial is a solid theme
# colour with a fixed light-to-shadow alpha gradient on top.
DIAL_GLOW = (["#66FFFFFF", "#14FFFFFF", "#00000000", "#59000000"], [0, 0.35, 0.6, 1])
SUB_GLOW = (["#40FFFFFF", "#00FFFFFF", "#26000000"], [0, 0.55, 1])


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def taper(x, y0, y1):
    """Segments along a vertical hand from y0 (base) to y1 (tip), narrowing toward the tip."""
    segs = []
    for i in range(TAPER_STEPS):
        a, b = i / TAPER_STEPS, (i + 1) / TAPER_STEPS
        w = HAND_W[0] + (HAND_W[1] - HAND_W[0]) * (a + b) / 2
        segs.append((y0 + (y1 - y0) * a, y0 + (y1 - y0) * b, w))
    return segs


def wff_hand(x, y0, y1, ind):
    return [f'{ind}<Line startX="{f(x)}" startY="{f(a)}" endX="{f(x)}" endY="{f(b)}">'
            f'<Stroke color="{HAND}" thickness="{f(w)}" cap="ROUND"/></Line>' for a, b, w in taper(x, y0, y1)]


def svg_hand(x, y0, y1, extra=""):
    return [f'<g{extra}>'] + [f'<line x1="{f(x)}" y1="{f(a)}" x2="{f(x)}" y2="{f(b)}" stroke="#fff" '
                              f'stroke-width="{f(w)}" stroke-linecap="round"/>' for a, b, w in taper(x, y0, y1)] + ["</g>"]


def wff_glow(glow):
    cols, pos = glow
    return f'colors="{" ".join(cols)}" positions="{" ".join(f(v) for v in pos)}"'


def svg_stops(glow):
    out = []
    for c, pos in zip(*glow):
        col, op = argb_to_css(c)
        out.append(f'<stop offset="{f(pos)}" stop-color="{col}" stop-opacity="{op}"/>')
    return "".join(out)


# ---------------------------------------------------------------------------
# Shape model shared by both renderers.
# Each item: (kind, params). Kinds: line, dot, ring, pill (rotated capsule)
# ---------------------------------------------------------------------------
def track_marks():
    items = []
    for i in range(60):
        deg = i * 6
        if i == 0:
            x, y = polar(C, C, 205, 0)
            items.append(("dot", dict(cx=x, cy=y, r=4.5, color=MARK)))
        elif i in (15, 30, 45):
            items.append(("pill", dict(cx=C, cy=C, r=199, deg=deg, length=20, width=8, stroke=2.2)))
        elif i % 5 == 0:
            x1, y1 = polar(C, C, 192, deg)
            x2, y2 = polar(C, C, 207, deg)
            items.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, w=3.4, color=MARK)))
        else:
            x, y = polar(C, C, 200, deg)
            items.append(("dot", dict(cx=x, cy=y, r=1.5, color=MARK_SOFT)))
    return items


def logo_mark(cx, cy, h=14, w=2.4):
    """Anthropic "A\\" mark drawn with lines, centred on (cx, cy), h tall."""
    k = h / 13
    segs = [((-2.5, -6.5), (-8, 6.5)),      # A left leg
            ((-2.5, -6.5), (3, 6.5)),       # A right leg
            ((-6.1, 2), (1.1, 2)),          # A crossbar
            ((2.5, -6.5), (8, 6.5))]        # backslash, parallel to the right leg
    return [("line", dict(x1=cx + a[0] * k, y1=cy + a[1] * k, x2=cx + b[0] * k, y2=cy + b[1] * k, w=w, color=MARK))
            for a, b in segs]


def subdial_marks(c):
    items = []
    for h in range(12):
        deg = h * 30
        if h == 0:
            items += logo_mark(c, c - 85)
        elif h in (3, 6, 9):
            items.append(("pill", dict(cx=c, cy=c, r=85, deg=deg, length=16, width=7, stroke=2)))
        else:
            x1, y1 = polar(c, c, 79, deg)
            x2, y2 = polar(c, c, 91, deg)
            items.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, w=3, color=MARK)))
    return items


# ---------------------------------------------------------------------------
# Watch Face Format renderer
# ---------------------------------------------------------------------------
def wff_items(items, frame, ind, name):
    out = []
    plain = [it for it in items if it[0] != "pill"]
    pills = [it for it in items if it[0] == "pill"]
    if plain:
        out.append(f'{ind}<PartDraw name="{name}" x="0" y="0" width="{frame}" height="{frame}">')
        for kind, p in plain:
            if kind == "line":
                out.append(f'{ind}  <Line startX="{f(p["x1"])}" startY="{f(p["y1"])}" endX="{f(p["x2"])}" endY="{f(p["y2"])}">'
                           f'<Stroke color="{p["color"]}" thickness="{f(p["w"])}" cap="ROUND"/></Line>')
            elif kind == "dot":
                d = p["r"] * 2
                out.append(f'{ind}  <Ellipse x="{f(p["cx"] - p["r"])}" y="{f(p["cy"] - p["r"])}" width="{f(d)}" height="{f(d)}">'
                           f'<Fill color="{p["color"]}"/></Ellipse>')
        out.append(f"{ind}</PartDraw>")
    for kind, p in pills:
        # Draw an upright capsule at 12 o'clock, then rotate the whole part about the dial centre.
        L, Wd = p["length"], p["width"]
        x = p["cx"] - Wd / 2
        y = p["cy"] - p["r"] - L / 2
        out.append(f'{ind}<PartDraw name="{name}_pill" x="0" y="0" width="{frame}" height="{frame}" '
                   f'pivotX="{f(p["cx"] / frame)}" pivotY="{f(p["cy"] / frame)}" angle="{p["deg"]}">')
        out.append(f'{ind}  <RoundRectangle x="{f(x)}" y="{f(y)}" width="{f(Wd)}" height="{f(L)}" '
                   f'cornerRadiusX="{f(Wd / 2)}" cornerRadiusY="{f(Wd / 2)}">'
                   f'<Stroke color="{MARK}" thickness="{f(p["stroke"])}"/></RoundRectangle>')
        out.append(f"{ind}</PartDraw>")
    return out


def build_wff():
    cfg = lambda i: f"[CONFIGURATION.dial.{i}]"
    L = []
    L.append('<?xml version="1.0" encoding="utf-8"?>')
    L.append("<!-- Generated by tools/generate.py - edit the generator, not this file. -->")
    L.append(f'<WatchFace width="{W}" height="{W}" clipShape="CIRCLE">')
    L.append('  <Metadata key="CLOCK_TYPE" value="ANALOG"/>')
    L.append('  <Metadata key="PREVIEW_TIME" value="10:10:00"/>')
    L.append("  <UserConfigurations>")
    L.append('    <ColorConfiguration id="dial" displayName="@string/dial_color" defaultValue="lagoon">')
    for tid, _, cols in THEMES:
        L.append(f'      <ColorOption id="{tid}" displayName="@string/theme_{tid}" colors="{" ".join(cols)}"/>')
    L.append("    </ColorConfiguration>")
    L.append("  </UserConfigurations>")
    L.append('  <Scene backgroundColor="#FF000000">')

    # Dial: lit from the upper left, darker at the rim
    L.append(f'    <PartDraw name="dial" x="0" y="0" width="{W}" height="{W}">')
    L.append(f'      <Variant mode="AMBIENT" target="alpha" value="0"/>')
    L.append(f'      <Ellipse x="0" y="0" width="{W}" height="{W}"><Fill color="{cfg(1)}"/></Ellipse>')
    L.append(f'      <Ellipse x="0" y="0" width="{W}" height="{W}"><Fill color="#00000000">'
             f'<RadialGradient centerX="185" centerY="165" radius="320" {wff_glow(DIAL_GLOW)}/>'
             f"</Fill></Ellipse>")
    L.append(f'      <Ellipse x="{f(C - R_OUTER_RING)}" y="{f(C - R_OUTER_RING)}" width="{2 * R_OUTER_RING}" height="{2 * R_OUTER_RING}">'
             f'<Stroke color="{RING}" thickness="1.2"/></Ellipse>')
    L.append(f'      <Ellipse x="{f(C - R_TRACK_IN)}" y="{f(C - R_TRACK_IN)}" width="{2 * R_TRACK_IN}" height="{2 * R_TRACK_IN}">'
             f'<Stroke color="{RING}" thickness="1.2"/></Ellipse>')
    L.append("    </PartDraw>")

    # Minute track (dimmed in ambient)
    L.append(f'    <Group name="track" x="0" y="0" width="{W}" height="{W}">')
    L.append('      <Variant mode="AMBIENT" target="alpha" value="110"/>')
    L += wff_items(track_marks(), W, "      ", "track")
    L.append("    </Group>")

    # Rotating disc: turns once per hour
    L.append(f'    <Group name="disc" x="0" y="0" width="{W}" height="{W}" pivotX="0.5" pivotY="0.5">')
    L.append('      <Transform target="angle" value="[MINUTE_SECOND] * 6"/>')

    # Minute hand
    L.append(f'      <PartDraw name="minuteHand" x="0" y="0" width="{W}" height="{W}">')
    L += wff_hand(C, C - MIN_HAND[0], C - MIN_HAND[1], "        ")
    L.append("      </PartDraw>")

    # Hour sub-dial, opposite the minute hand; counter-rotates to stay upright
    S = 2 * SUB_R
    sc = SUB_R
    L.append(f'      <Group name="subdial" x="{f(C - SUB_R)}" y="{f(C + SUB_OFFSET - SUB_R)}" width="{S}" height="{S}" pivotX="0.5" pivotY="0.5">')
    L.append('        <Transform target="angle" value="0 - [MINUTE_SECOND] * 6"/>')
    L.append(f'        <PartDraw name="subdialFace" x="0" y="0" width="{S}" height="{S}">')
    L.append('          <Variant mode="AMBIENT" target="alpha" value="0"/>')
    L.append(f'          <Ellipse x="1" y="1" width="{S - 2}" height="{S - 2}"><Fill color="#14000000"/><Stroke color="{RING}" thickness="1.2"/></Ellipse>')
    d = SUB_DISC_R
    L.append(f'          <Ellipse x="{sc - d}" y="{sc - d}" width="{2 * d}" height="{2 * d}"><Fill color="{cfg(3)}"/></Ellipse>')
    L.append(f'          <Ellipse x="{sc - d}" y="{sc - d}" width="{2 * d}" height="{2 * d}"><Fill color="#00000000">'
             f'<RadialGradient centerX="{sc - 25}" centerY="{sc - 30}" radius="{2 * d}" {wff_glow(SUB_GLOW)}/>'
             f'</Fill><Stroke color="{RING}" thickness="1.2"/></Ellipse>')
    L.append("        </PartDraw>")
    L.append(f'        <Group name="subdialMarks" x="0" y="0" width="{S}" height="{S}">')
    L.append('          <Variant mode="AMBIENT" target="alpha" value="110"/>')
    L += wff_items(subdial_marks(sc), S, "          ", "subdialMarks")
    L.append("        </Group>")
    L.append(f'        <PartDraw name="hourHand" x="0" y="0" width="{S}" height="{S}" pivotX="0.5" pivotY="0.5">')
    L.append('          <Transform target="angle" value="[HOUR_0_11_MINUTE] * 30"/>')
    L += wff_hand(sc, sc, sc - HOUR_HAND_LEN, "          ")
    L.append("        </PartDraw>")
    L.append("      </Group>")
    L.append("    </Group>")
    L.append("  </Scene>")
    L.append("</WatchFace>")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# SVG preview renderer (same geometry) - used for the preview image
# ---------------------------------------------------------------------------
def argb_to_css(c):
    a = int(c[1:3], 16) / 255
    return f"#{c[3:]}", f"{a:.3f}"


def svg_items(items):
    out = []
    for kind, p in items:
        if kind == "line":
            col, op = argb_to_css(p["color"])
            out.append(f'<line x1="{f(p["x1"])}" y1="{f(p["y1"])}" x2="{f(p["x2"])}" y2="{f(p["y2"])}" '
                       f'stroke="{col}" stroke-opacity="{op}" stroke-width="{p["w"]}" stroke-linecap="round"/>')
        elif kind == "dot":
            col, op = argb_to_css(p["color"])
            out.append(f'<circle cx="{f(p["cx"])}" cy="{f(p["cy"])}" r="{p["r"]}" fill="{col}" fill-opacity="{op}"/>')
        elif kind == "pill":
            L, Wd = p["length"], p["width"]
            col, op = argb_to_css(MARK)
            out.append(f'<rect x="{f(p["cx"] - Wd / 2)}" y="{f(p["cy"] - p["r"] - L / 2)}" width="{Wd}" height="{L}" '
                       f'rx="{Wd / 2}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{p["stroke"]}" '
                       f'transform="rotate({p["deg"]} {f(p["cx"])} {f(p["cy"])})"/>')
    return out


def build_svg(theme, hh=10, mm=10, ss=0):
    cols = [argb_to_css(c)[0] for c in theme[2]]
    minute = mm + ss / 60
    m_ang = minute * 6
    h_ang = ((hh % 12) + minute / 60) * 30
    S = 2 * SUB_R
    col, op = argb_to_css(MARK)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">',
         "<defs>",
         f'<radialGradient id="g-{theme[0]}" gradientUnits="userSpaceOnUse" cx="185" cy="165" r="320">{svg_stops(DIAL_GLOW)}</radialGradient>',
         f'<radialGradient id="s-{theme[0]}" gradientUnits="userSpaceOnUse" cx="{SUB_R - 25}" cy="{SUB_R - 30}" r="{2 * SUB_DISC_R}">{svg_stops(SUB_GLOW)}</radialGradient>',
         f'<clipPath id="c-{theme[0]}"><circle cx="{C}" cy="{C}" r="{C}"/></clipPath>',
         "</defs>",
         f'<g clip-path="url(#c-{theme[0]})"><rect width="{W}" height="{W}" fill="#000"/>',
         f'<circle cx="{C}" cy="{C}" r="{C}" fill="{cols[1]}"/>',
         f'<circle cx="{C}" cy="{C}" r="{C}" fill="url(#g-{theme[0]})"/>',
         f'<circle cx="{C}" cy="{C}" r="{R_OUTER_RING}" fill="none" stroke="#fff" stroke-opacity="0.25" stroke-width="1.2"/>',
         f'<circle cx="{C}" cy="{C}" r="{R_TRACK_IN}" fill="none" stroke="#fff" stroke-opacity="0.25" stroke-width="1.2"/>']
    o += svg_items(track_marks())
    o.append(f'<g transform="rotate({f(m_ang)} {C} {C})">')
    o += svg_hand(C, C - MIN_HAND[0], C - MIN_HAND[1])
    o.append(f'<g transform="translate({f(C - SUB_R)} {f(C + SUB_OFFSET - SUB_R)}) rotate({f(-m_ang)} {SUB_R} {SUB_R})">')
    o.append(f'<circle cx="{SUB_R}" cy="{SUB_R}" r="{SUB_R - 1}" fill="#000" fill-opacity="0.08" stroke="#fff" stroke-opacity="0.25" stroke-width="1.2"/>')
    o.append(f'<circle cx="{SUB_R}" cy="{SUB_R}" r="{SUB_DISC_R}" fill="{cols[3]}"/>')
    o.append(f'<circle cx="{SUB_R}" cy="{SUB_R}" r="{SUB_DISC_R}" fill="url(#s-{theme[0]})" stroke="#fff" stroke-opacity="0.25" stroke-width="1.2"/>')
    o += svg_items(subdial_marks(SUB_R))
    o += svg_hand(SUB_R, SUB_R, SUB_R - HOUR_HAND_LEN, f' transform="rotate({f(h_ang)} {SUB_R} {SUB_R})"')
    o.append("</g></g></g></svg>")
    return "\n".join(o)


def build_strings():
    s = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>",
         '    <string name="app_name">Tidal</string>',
         '    <string name="dial_color">Dial colour</string>']
    s += [f'    <string name="theme_{tid}">{label}</string>' for tid, label, _ in THEMES]
    s.append("</resources>")
    return "\n".join(s) + "\n"


if __name__ == "__main__":
    res = ROOT / "app/src/main/res"
    (res / "raw/watchface.xml").write_text(build_wff())
    (res / "values/strings.xml").write_text(build_strings())
    for t in THEMES:
        (ROOT / f"preview/{t[0]}.svg").write_text(build_svg(t))
    print("wrote watchface.xml, strings.xml and preview SVGs")
