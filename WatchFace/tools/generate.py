#!/usr/bin/env python3
"""Generates the Tidal watch face (Watch Face Format XML) and matching SVG previews.

The design: a tinted, softly lit dial with a minute track. A central disc turns
once an hour and carries the minute hand. On the opposite side of that disc an
hour sub-dial orbits the centre; it counter-rotates so its markers stay upright
while its own hand shows the hour.

Settings on the watch (long-press -> Customise):
  Colour - the dial colour theme
  Style  - Classic (tinted dial), Dark (near-black, tinted glow, coloured hands),
           Noir (pure black, markings and hands in the theme colour)
  Logo   - the mark at 12 on the hour dial: Anthropic, Claude or a plain dot

Run from the WatchFace/ directory:  python3 tools/generate.py
"""
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = 450
C = W / 2

# ---- dial colour themes: accent (light), dial, edge, sub-dial disc ------------
# Slot 0 is the light accent used for hands/markings in Dark and Noir styles.
THEMES = [
    ("lagoon", "Lagoon", ["#FFB2DDD5", "#FF86BFB6", "#FF4A8780", "#FF9FD0C7"]),
    ("glacier", "Glacier", ["#FFD3E0EA", "#FFA3B9CA", "#FF5C7790", "#FFBDCFDD"]),
    ("sand", "Sand", ["#FFE6DBC7", "#FFCBB99C", "#FF8A785B", "#FFDCCDB3"]),
    ("dusk", "Dusk", ["#FFCDBCDB", "#FFA290BA", "#FF5A4974", "#FFBBA8CE"]),
    ("graphite", "Graphite", ["#FFB8BEC2", "#FF555B60", "#FF222629", "#FF6A7176"]),
    ("ocean", "Ocean", ["#FFB5D3F2", "#FF5E8FC4", "#FF2C4F7C", "#FF7FA7D6"]),
    ("rose", "Rose", ["#FFF4D3D8", "#FFD79AA6", "#FF8C5563", "#FFE6B3BC"]),
    ("sage", "Sage", ["#FFDCE6CF", "#FFA9B894", "#FF5F6E4C", "#FFC2CFB0"]),
    ("ember", "Ember", ["#FFF6D0B4", "#FFD98C62", "#FF8E4A2C", "#FFE8AA84"]),
    ("midnight", "Midnight", ["#FFAFBCEB", "#FF2E3B6B", "#FF121833", "#FF43528A"]),
]

STYLES = [("classic", "Classic"), ("dark", "Dark"), ("noir", "Noir")]
LOGOS = [("anthropic", "Anthropic"), ("claude", "Claude"), ("dot", "Dot")]

WHITE = "#F5FFFFFF"
RING = "#40FFFFFF"        # thin rings


def cfg(i):
    """A colour from the selected theme. Rendered as a [CONFIGURATION] reference on the watch."""
    return ("cfg", i)


# Per style: what each part of the face is painted with.
STYLE = {
    "classic": dict(base=cfg(1), tint=None, glow=["#8CFFFFFF", "#1FFFFFFF", "#00000000", "#7A000000"],
                    sub_base=cfg(3), sub_tint=None, sub_glow=["#5CFFFFFF", "#00FFFFFF", "#36000000"],
                    mark=WHITE, dots="#80FFFFFF", hand="#FFFFFFFF", ring=RING, sub_well="#14000000"),
    "dark": dict(base="#FF0B0C0D", tint=(cfg(2), 120), glow=["#40FFFFFF", "#0FFFFFFF", "#00000000", "#A6000000"],
                 sub_base="#FF0B0C0D", sub_tint=(cfg(1), 110), sub_glow=["#36FFFFFF", "#00FFFFFF", "#47000000"],
                 mark="#E6FFFFFF", dots="#59FFFFFF", hand=cfg(0), ring="#2EFFFFFF", sub_well="#40000000"),
    "noir": dict(base="#FF000000", tint=None, glow=None,
                 sub_base="#FF000000", sub_tint=None, sub_glow=None,
                 mark=cfg(0), dots="#66FFFFFF", hand=cfg(0), ring="#33FFFFFF", sub_well="#FF000000"),
}
GLOW_POS = [0, 0.35, 0.6, 1]
SUB_GLOW_POS = [0, 0.55, 1]

# Geometry (450 canvas, scaled by the watch to 480x480 on the Ultra)
R_OUTER_RING = 214
R_TRACK_IN = 186
SUB_OFFSET = 70           # distance from centre to sub-dial centre
SUB_R = 100               # sub-dial outer radius
SUB_DISC_R = 70           # sub-dial inner disc radius
MIN_HAND = (42, 176)      # start/end radius of the minute hand
HOUR_HAND_LEN = 58
HAND_W = (8, 2.4)         # hand width at the base and at the tip
TAPER_STEPS = 18


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


# ---- colours: literal "#AARRGGBB" or cfg(i) ----------------------------------
def wcol(c):
    return f"[CONFIGURATION.dial.{c[1]}]" if isinstance(c, tuple) else c


def scol(c, theme):
    """(css colour, opacity) for the SVG preview."""
    if isinstance(c, tuple):
        c = theme[2][c[1]]
    return f"#{c[3:]}", f"{int(c[1:3], 16) / 255:.3f}"


def taper(y0, y1):
    """Segments along a vertical hand from y0 (base) to y1 (tip), narrowing toward the tip."""
    segs = []
    for i in range(TAPER_STEPS):
        a, b = i / TAPER_STEPS, (i + 1) / TAPER_STEPS
        w = HAND_W[0] + (HAND_W[1] - HAND_W[0]) * (a + b) / 2
        segs.append((y0 + (y1 - y0) * a, y0 + (y1 - y0) * b, w))
    return segs


def hand_items(x, y0, y1, color):
    return [("line", dict(x1=x, y1=a, x2=x, y2=b, w=w, color=color)) for a, b, w in taper(y0, y1)]


# ---------------------------------------------------------------------------
# Shape model shared by both renderers.
# Each item: (kind, params). Kinds: line, dot, pill (rotated capsule)
# ---------------------------------------------------------------------------
def track_marks(st):
    items = []
    for i in range(60):
        deg = i * 6
        if i == 0:
            x, y = polar(C, C, 205, 0)
            items.append(("dot", dict(cx=x, cy=y, r=4.5, color=st["mark"])))
        elif i in (15, 30, 45):
            items.append(("pill", dict(cx=C, cy=C, r=199, deg=deg, length=20, width=8, stroke=2.2, color=st["mark"])))
        elif i % 5 == 0:
            x1, y1 = polar(C, C, 192, deg)
            x2, y2 = polar(C, C, 207, deg)
            items.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, w=3.4, color=st["mark"])))
        else:
            x, y = polar(C, C, 200, deg)
            items.append(("dot", dict(cx=x, cy=y, r=1.5, color=st["dots"])))
    return items


def subdial_marks(c, st):
    """Hour markers, without the 12 o'clock mark (that is the configurable logo)."""
    items = []
    for h in range(1, 12):
        deg = h * 30
        if h in (3, 6, 9):
            items.append(("pill", dict(cx=c, cy=c, r=85, deg=deg, length=16, width=7, stroke=2, color=st["mark"])))
        else:
            x1, y1 = polar(c, c, 79, deg)
            x2, y2 = polar(c, c, 91, deg)
            items.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, w=3, color=st["mark"])))
    return items


def logo_mark(logo, cx, cy, color, h=14):
    """The 12 o'clock mark on the hour dial, centred on (cx, cy), about h tall."""
    k = h / 13
    if logo == "anthropic":
        # "A\" drawn with lines
        segs = [((-2.5, -6.5), (-8, 6.5)), ((-2.5, -6.5), (3, 6.5)), ((-6.1, 2), (1.1, 2)), ((2.5, -6.5), (8, 6.5))]
        return [("line", dict(x1=cx + a[0] * k, y1=cy + a[1] * k, x2=cx + b[0] * k, y2=cy + b[1] * k, w=2.4, color=color))
                for a, b in segs]
    if logo == "claude":
        # spark: uneven rays around a small centre
        k = 17 / 13
        angles = [0, 28, 62, 88, 121, 148, 181, 209, 238, 272, 300, 331]
        lengths = [7.4, 5.6, 7.0, 5.3, 7.3, 5.9, 6.8, 5.2, 7.2, 5.7, 7.0, 5.4]
        out = []
        for a, ln in zip(angles, lengths):
            x1, y1 = polar(cx, cy, 1.3 * k, a)
            x2, y2 = polar(cx, cy, ln * k, a)
            out.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, w=1.9, color=color)))
        return out
    return [("dot", dict(cx=cx, cy=cy, r=3.6, color=color))]


# ---------------------------------------------------------------------------
# Watch Face Format renderer
# ---------------------------------------------------------------------------
def wff_draw(items, frame, ind, name):
    """Plain lines/dots go into one PartDraw; each pill gets its own rotated PartDraw."""
    out = []
    plain = [it for it in items if it[0] != "pill"]
    pills = [it for it in items if it[0] == "pill"]
    if plain:
        out.append(f'{ind}<PartDraw name="{name}" x="0" y="0" width="{frame}" height="{frame}">')
        for kind, p in plain:
            if kind == "line":
                out.append(f'{ind}  <Line startX="{f(p["x1"])}" startY="{f(p["y1"])}" endX="{f(p["x2"])}" endY="{f(p["y2"])}">'
                           f'<Stroke color="{wcol(p["color"])}" thickness="{f(p["w"])}" cap="ROUND"/></Line>')
            elif kind == "dot":
                d = p["r"] * 2
                out.append(f'{ind}  <Ellipse x="{f(p["cx"] - p["r"])}" y="{f(p["cy"] - p["r"])}" width="{f(d)}" height="{f(d)}">'
                           f'<Fill color="{wcol(p["color"])}"/></Ellipse>')
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
                   f'<Stroke color="{wcol(p["color"])}" thickness="{f(p["stroke"])}"/></RoundRectangle>')
        out.append(f"{ind}</PartDraw>")
    return out


def wff_disc(ind, name, x, y, size, base, tint, glow, glow_pos, gcx, gcy, gr, ring=None, ambient_hide=True):
    """A filled circle: solid base, optional theme tint at partial alpha, optional literal-colour glow."""
    L = [f'{ind}<PartDraw name="{name}" x="{f(x)}" y="{f(y)}" width="{f(size)}" height="{f(size)}">']
    if ambient_hide:
        L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="0"/>')
    L.append(f'{ind}  <Ellipse x="0" y="0" width="{f(size)}" height="{f(size)}"><Fill color="{wcol(base)}"/></Ellipse>')
    L.append(f"{ind}</PartDraw>")
    if tint:
        L.append(f'{ind}<PartDraw name="{name}Tint" x="{f(x)}" y="{f(y)}" width="{f(size)}" height="{f(size)}" alpha="{tint[1]}">')
        if ambient_hide:
            L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="0"/>')
        L.append(f'{ind}  <Ellipse x="0" y="0" width="{f(size)}" height="{f(size)}"><Fill color="{wcol(tint[0])}"/></Ellipse>')
        L.append(f"{ind}</PartDraw>")
    if glow or ring:
        L.append(f'{ind}<PartDraw name="{name}Glow" x="{f(x)}" y="{f(y)}" width="{f(size)}" height="{f(size)}">')
        if ambient_hide:
            L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="0"/>')
        if glow:
            L.append(f'{ind}  <Ellipse x="0" y="0" width="{f(size)}" height="{f(size)}"><Fill color="#FFFFFFFF">'
                     f'<RadialGradient centerX="{f(gcx)}" centerY="{f(gcy)}" radius="{f(gr)}" colors="{" ".join(glow)}" '
                     f'positions="{" ".join(f(v) for v in glow_pos)}"/></Fill></Ellipse>')
        if ring:
            L.append(f'{ind}  <Ellipse x="0" y="0" width="{f(size)}" height="{f(size)}"><Stroke color="{ring}" thickness="1.2"/></Ellipse>')
        L.append(f"{ind}</PartDraw>")
    return L


def wff_face(style, ind):
    st = STYLE[style]
    L = []
    # Dial: lit from the upper left, darker at the rim
    L += wff_disc(ind, "dial", 0, 0, W, st["base"], st["tint"], st["glow"], GLOW_POS, 185, 165, 320)
    L.append(f'{ind}<PartDraw name="rings" x="0" y="0" width="{W}" height="{W}">')
    L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="0"/>')
    for r in (R_OUTER_RING, R_TRACK_IN):
        L.append(f'{ind}  <Ellipse x="{f(C - r)}" y="{f(C - r)}" width="{2 * r}" height="{2 * r}">'
                 f'<Stroke color="{st["ring"]}" thickness="1.2"/></Ellipse>')
    L.append(f"{ind}</PartDraw>")

    # Minute track (dimmed in ambient)
    L.append(f'{ind}<Group name="track" x="0" y="0" width="{W}" height="{W}">')
    L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="110"/>')
    L += wff_draw(track_marks(st), W, ind + "  ", "track")
    L.append(f"{ind}</Group>")

    # Rotating disc: turns once per hour
    L.append(f'{ind}<Group name="disc" x="0" y="0" width="{W}" height="{W}" pivotX="0.5" pivotY="0.5">')
    L.append(f'{ind}  <Transform target="angle" value="[MINUTE_SECOND] * 6"/>')
    L += wff_draw(hand_items(C, C - MIN_HAND[0], C - MIN_HAND[1], st["hand"]), W, ind + "  ", "minuteHand")

    # Hour sub-dial, opposite the minute hand; counter-rotates to stay upright
    S = 2 * SUB_R
    sc = SUB_R
    i2 = ind + "    "
    L.append(f'{ind}  <Group name="subdial" x="{f(C - SUB_R)}" y="{f(C + SUB_OFFSET - SUB_R)}" width="{S}" height="{S}" pivotX="0.5" pivotY="0.5">')
    L.append(f'{i2}<Transform target="angle" value="0 - [MINUTE_SECOND] * 6"/>')
    L.append(f'{i2}<PartDraw name="subdialWell" x="0" y="0" width="{S}" height="{S}">')
    L.append(f'{i2}  <Variant mode="AMBIENT" target="alpha" value="0"/>')
    L.append(f'{i2}  <Ellipse x="1" y="1" width="{S - 2}" height="{S - 2}"><Fill color="{st["sub_well"]}"/>'
             f'<Stroke color="{st["ring"]}" thickness="1.2"/></Ellipse>')
    L.append(f"{i2}</PartDraw>")
    d = SUB_DISC_R
    L += wff_disc(i2, "subdialDisc", sc - d, sc - d, 2 * d, st["sub_base"], st["sub_tint"], st["sub_glow"], SUB_GLOW_POS,
                  d - 25, d - 30, 2 * d, ring=st["ring"])
    L.append(f'{i2}<Group name="subdialMarks" x="0" y="0" width="{S}" height="{S}">')
    L.append(f'{i2}  <Variant mode="AMBIENT" target="alpha" value="110"/>')
    L += wff_draw(subdial_marks(sc, st), S, i2 + "  ", "subdialMarks")
    L.append(f'{i2}  <ListConfiguration id="logo">')
    for lid, _ in LOGOS:
        L.append(f'{i2}    <ListOption id="{lid}">')
        L += wff_draw(logo_mark(lid, sc, sc - 85, st["mark"]), S, i2 + "      ", f"logo_{lid}")
        L.append(f"{i2}    </ListOption>")
    L.append(f"{i2}  </ListConfiguration>")
    L.append(f"{i2}</Group>")
    L.append(f'{i2}<Group name="hourHand" x="0" y="0" width="{S}" height="{S}" pivotX="0.5" pivotY="0.5">')
    L.append(f'{i2}  <Transform target="angle" value="[HOUR_0_11_MINUTE] * 30"/>')
    L += wff_draw(hand_items(sc, sc, sc - HOUR_HAND_LEN, st["hand"]), S, i2 + "  ", "hourHand")
    L.append(f"{i2}</Group>")
    L.append(f"{ind}  </Group>")
    L.append(f"{ind}</Group>")
    return L


def build_wff():
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
    L.append('    <ListConfiguration id="style" displayName="@string/style" defaultValue="classic">')
    for sid, _ in STYLES:
        L.append(f'      <ListOption id="{sid}" displayName="@string/style_{sid}"/>')
    L.append("    </ListConfiguration>")
    L.append('    <ListConfiguration id="logo" displayName="@string/logo" defaultValue="anthropic">')
    for lid, _ in LOGOS:
        L.append(f'      <ListOption id="{lid}" displayName="@string/logo_{lid}"/>')
    L.append("    </ListConfiguration>")
    L.append("  </UserConfigurations>")
    L.append('  <Scene backgroundColor="#FF000000">')
    L.append('    <ListConfiguration id="style">')
    for sid, _ in STYLES:
        L.append(f'      <ListOption id="{sid}">')
        L.append(f'        <Group name="{sid}" x="0" y="0" width="{W}" height="{W}">')
        L += wff_face(sid, "          ")
        L.append("        </Group>")
        L.append("      </ListOption>")
    L.append("    </ListConfiguration>")
    L.append("  </Scene>")
    L.append("</WatchFace>")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# SVG preview renderer (same geometry)
# ---------------------------------------------------------------------------
def svg_items(items, theme):
    out = []
    for kind, p in items:
        col, op = scol(p["color"], theme)
        if kind == "line":
            out.append(f'<line x1="{f(p["x1"])}" y1="{f(p["y1"])}" x2="{f(p["x2"])}" y2="{f(p["y2"])}" '
                       f'stroke="{col}" stroke-opacity="{op}" stroke-width="{f(p["w"])}" stroke-linecap="round"/>')
        elif kind == "dot":
            out.append(f'<circle cx="{f(p["cx"])}" cy="{f(p["cy"])}" r="{p["r"]}" fill="{col}" fill-opacity="{op}"/>')
        elif kind == "pill":
            L, Wd = p["length"], p["width"]
            out.append(f'<rect x="{f(p["cx"] - Wd / 2)}" y="{f(p["cy"] - p["r"] - L / 2)}" width="{Wd}" height="{L}" '
                       f'rx="{Wd / 2}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{p["stroke"]}" '
                       f'transform="rotate({p["deg"]} {f(p["cx"])} {f(p["cy"])})"/>')
    return out


def svg_stops(glow, pos):
    out = []
    for c, p in zip(glow, pos):
        col, op = scol(c, None)
        out.append(f'<stop offset="{f(p)}" stop-color="{col}" stop-opacity="{op}"/>')
    return "".join(out)


def svg_disc(cx, cy, r, base, tint, glow_id, theme, ring=None):
    col, op = scol(base, theme)
    o = [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{col}" fill-opacity="{op}"/>']
    if tint:
        tc, _ = scol(tint[0], theme)
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{tc}" fill-opacity="{tint[1] / 255:.3f}"/>')
    if glow_id:
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#{glow_id})"/>')
    if ring:
        rc, rop = scol(ring, None)
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{rc}" stroke-opacity="{rop}" stroke-width="1.2"/>')
    return o


def build_svg(theme, style, logo, hh=10, mm=10, ss=0):
    st = STYLE[style]
    minute = mm + ss / 60
    m_ang = minute * 6
    h_ang = ((hh % 12) + minute / 60) * 30
    rc, rop = scol(st["ring"], None)
    key = f"{style}-{theme[0]}"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">', "<defs>"]
    if st["glow"]:
        o.append(f'<radialGradient id="g-{key}" gradientUnits="userSpaceOnUse" cx="185" cy="165" r="320">{svg_stops(st["glow"], GLOW_POS)}</radialGradient>')
    if st["sub_glow"]:
        o.append(f'<radialGradient id="s-{key}" gradientUnits="userSpaceOnUse" cx="{SUB_R - 25}" cy="{SUB_R - 30}" r="{2 * SUB_DISC_R}">'
                 f'{svg_stops(st["sub_glow"], SUB_GLOW_POS)}</radialGradient>')
    o += [f'<clipPath id="c-{key}"><circle cx="{C}" cy="{C}" r="{C}"/></clipPath>', "</defs>",
          f'<g clip-path="url(#c-{key})"><rect width="{W}" height="{W}" fill="#000"/>']
    o += svg_disc(C, C, C, st["base"], st["tint"], st["glow"] and f"g-{key}", theme)
    for r in (R_OUTER_RING, R_TRACK_IN):
        o.append(f'<circle cx="{C}" cy="{C}" r="{r}" fill="none" stroke="{rc}" stroke-opacity="{rop}" stroke-width="1.2"/>')
    o += svg_items(track_marks(st), theme)
    o.append(f'<g transform="rotate({f(m_ang)} {C} {C})">')
    o += svg_items(hand_items(C, C - MIN_HAND[0], C - MIN_HAND[1], st["hand"]), theme)
    o.append(f'<g transform="translate({f(C - SUB_R)} {f(C + SUB_OFFSET - SUB_R)}) rotate({f(-m_ang)} {SUB_R} {SUB_R})">')
    wc, wop = scol(st["sub_well"], None)
    o.append(f'<circle cx="{SUB_R}" cy="{SUB_R}" r="{SUB_R - 1}" fill="{wc}" fill-opacity="{wop}" stroke="{rc}" stroke-opacity="{rop}" stroke-width="1.2"/>')
    o += svg_disc(SUB_R, SUB_R, SUB_DISC_R, st["sub_base"], st["sub_tint"], st["sub_glow"] and f"s-{key}", theme, ring=st["ring"])
    o += svg_items(subdial_marks(SUB_R, st), theme)
    o += svg_items(logo_mark(logo, SUB_R, SUB_R - 85, st["mark"]), theme)
    o.append(f'<g transform="rotate({f(h_ang)} {SUB_R} {SUB_R})">')
    o += svg_items(hand_items(SUB_R, SUB_R, SUB_R - HOUR_HAND_LEN, st["hand"]), theme)
    o.append("</g></g></g></g></svg>")
    return "\n".join(o)


def build_strings():
    s = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>",
         '    <string name="app_name">Tidal</string>',
         '    <string name="dial_color">Dial colour</string>',
         '    <string name="style">Style</string>',
         '    <string name="logo">Logo</string>']
    s += [f'    <string name="theme_{tid}">{label}</string>' for tid, label, _ in THEMES]
    s += [f'    <string name="style_{sid}">{label}</string>' for sid, label in STYLES]
    s += [f'    <string name="logo_{lid}">{label}</string>' for lid, label in LOGOS]
    s.append("</resources>")
    return "\n".join(s) + "\n"


if __name__ == "__main__":
    res = ROOT / "app/src/main/res"
    (res / "raw/watchface.xml").write_text(build_wff())
    (res / "values/strings.xml").write_text(build_strings())
    prev = ROOT / "preview"
    for old in prev.glob("*.svg"):
        old.unlink()
    for sid, _ in STYLES:
        for t in THEMES:
            (prev / f"{sid}-{t[0]}.svg").write_text(build_svg(t, sid, "anthropic"))
    for lid, _ in LOGOS:
        (prev / f"logo-{lid}.svg").write_text(build_svg(THEMES[0], "classic", lid))
    print("wrote watchface.xml, strings.xml and preview SVGs")
