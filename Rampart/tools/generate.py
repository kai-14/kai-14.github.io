#!/usr/bin/env python3
"""Generates the Rampart watch face (Watch Face Format XML) and matching SVG previews.

The design: a dark, brushed dial inside a heavy black chapter ring. Blocky
"teeth" step in from the ring at every hour, each with a lume bar, with the
hour numerals on the ring outside them. Skeleton sword hands, a bright seconds
hand and a day-date window at 3.

Settings on the watch (long-press -> Customise):
  Dial    - dial colour
  Seconds - seconds hand colour
  Logo    - mark below 12: none, Anthropic or Claude
  Tilt shine - the metal sheen turns as you tilt your wrist (uses the motion sensor)

Metal look: a brushed texture image (tools/make_texture.py -> res/drawable-nodpi/metal_texture.png)
over the dial colour, sweep-gradient sheens on the dial and ring, and bevel highlights on the
teeth and hands. Gradients need an opaque Fill/Stroke colour: Android multiplies the gradient by
the paint's alpha, so a transparent colour hides the gradient completely.

Run from the Rampart/ directory:  python3 tools/generate.py
"""
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = 450
C = W / 2

DIALS = [("slate", "Slate", "#FF4A4D50"), ("carbon", "Carbon", "#FF26282A"), ("olive", "Olive", "#FF4B4F3C"),
         ("navy", "Navy", "#FF2C3A52"), ("ash", "Ash", "#FF7A7D80")]
ACCENTS = [("yellow", "Yellow", "#FFF2C230"), ("orange", "Orange", "#FFFF8A2A"), ("red", "Red", "#FFE8413A"),
           ("lime", "Lime", "#FFB6E23C"), ("ice", "Ice", "#FF8FD8FF"), ("white", "White", "#FFF0F0F0")]
LOGOS = [("none", "None"), ("anthropic", "Anthropic"), ("claude", "Claude")]

DIAL = ("dial", 0)
ACCENT = ("accent", 0)
CASE = "#FF0C0D0E"          # chapter ring
TOOTH_FILL = "#A30A0B0C"     # teeth: translucent dark metal, so the brushing and sheen show through
NUMERAL = "#FFE4E6E8"
LUME = "#FFCFD6C8"
TICK = "#FFD3CFBC"           # pale cream ticks, two between each pair of hours
SILVER = "#FFD5D9DD"
HAND_CORE = "#FF0D0E0F"
PRINT = "#FFB4B8BC"
DIAL_GLOW = (["#38FFFFFF", "#0DFFFFFF", "#00000000", "#80000000"], [0, 0.4, 0.7, 1])

R_EDGE = 225
R_DIAL = 192                 # visible dial radius between the teeth
TOOTH = (150, 222, 50)       # inner radius, outer radius, width
R_NUM = 204                  # numerals in line with the minute ticks
R_LUME = 166                 # lume bar on the inner part
TICKS = (197, 212)
LIGHT = (-0.6, -0.8)         # direction the light comes from (upper left)
BEVEL = ["#8CFFFFFF", "#1FFFFFFF", "#00FFFFFF"]
HAND_METAL = ["#FFF8FAFB", "#FFCDD2D7", "#FF8A9198"]
TILT = ("clamp([ACCELEROMETER_ANGLE_X], -40, 40) * {a} + clamp([ACCELEROMETER_ANGLE_Y], -40, 40) * {b}")
HOUR_HAND = (112, 14)        # length, max width
MIN_HAND = (166, 13)
SEC_HAND = (36, 186)         # tail, length


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def polar(r, deg, cx=C, cy=C):
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def wcol(c):
    return f"[CONFIGURATION.{c[0]}.{c[1]}]" if isinstance(c, tuple) else c


def scol(c, pick):
    if isinstance(c, tuple):
        c = pick[c[0]]
    return f"#{c[3:]}", f"{int(c[1:3], 16) / 255:.3f}"


# ---------------------------------------------------------------------------
# Shape model. Kinds:
#   line  x1 y1 x2 y2 w color cap
#   dot   cx cy r color
#   rrect upright rounded rect centred on (C, C - r), rotated by deg about C
#   text  cx cy size text color (static); or source= "day"/"date"
# ---------------------------------------------------------------------------
def line(x1, y1, x2, y2, w, color, cap="ROUND", grad=None):
    """grad: (sx, sy, ex, ey, colors, positions) - a linear gradient along the stroke, in local coords."""
    return ("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, w=w, color=color, cap=cap, grad=grad))


def rot(x, y, deg, cx=C, cy=C):
    a = math.radians(deg)
    dx, dy = x - cx, y - cy
    return cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)


def sheen(bright, dark, phase, n=24, power=1.0):
    """Sweep-gradient stops for a bow-tie of light: bright at phase and phase+180 degrees."""
    cols, pos = [], []
    for i in range(n + 1):
        b = math.cos(2 * math.radians(i * 360 / n - phase))
        a = (abs(b) ** power) * (bright if b > 0 else dark)
        cols.append(f"#{round(a * 255):02X}{'FFFFFF' if b > 0 else '000000'}")
        pos.append(i / n)
    return cols, pos


DIAL_SHEEN = sheen(0.22, 0.16, 315)
RING_SHEEN = sheen(0.15, 0.0, 300, power=2.0)


def tooth_bevel(deg):
    """Highlight along the inner end and sides of a tooth, lit from LIGHT whatever the tooth's angle."""
    r0, _, tw = TOOTH
    rad, x0, x1 = 11, C - tw / 2, C + tw / 2
    yi, yo = C - r0, C - (R_DIAL + 6)
    pts = [(x0, yo), (x0, yi - rad)]
    for k in range(1, 5):                                   # inner-left corner
        a = math.radians(90 * k / 4)
        pts.append((x0 + rad - rad * math.cos(a), yi - rad + rad * math.sin(a)))
    pts.append((x1 - rad, yi))
    for k in range(1, 5):                                   # inner-right corner
        a = math.radians(90 * k / 4)
        pts.append((x1 - rad + rad * math.sin(a), yi - rad * (1 - math.cos(a))))
    pts.append((x1, yo))
    # Light direction in this tooth's local (unrotated) frame
    lx, ly = rot(C + LIGHT[0], C + LIGHT[1], -deg)
    lx, ly = lx - C, ly - C
    tc = (C, C - (r0 + R_DIAL) / 2)
    g = (tc[0] + lx * 34, tc[1] + ly * 34, tc[0] - lx * 34, tc[1] - ly * 34, BEVEL, [0, 0.45, 1])
    return [line(a[0], a[1], b[0], b[1], 1.6, "#FFFFFFFF", grad=g) for a, b in zip(pts, pts[1:])]


def teeth():
    """One group per hour: the tooth block and its lume bar."""
    out = []
    r0, r1, tw = TOOTH
    for h in range(12):
        out.append([("rrect", dict(r=(r0 + r1) / 2, h=r1 - r0, w=tw, rad=11, deg=h * 30, fill=TOOTH_FILL, stroke=None, sw=0)),
                    ("rrect", dict(r=R_LUME, h=9, w=21, rad=2, deg=h * 30, fill=LUME, stroke=None, sw=0))]
                   + tooth_bevel(h * 30))
    return out


def minute_ticks():
    items = []
    for h in range(12):
        for off in (10, 20):
            x1, y1 = polar(TICKS[0], h * 30 + off)
            x2, y2 = polar(TICKS[1], h * 30 + off)
            items.append(line(x1, y1, x2, y2, 2.2, TICK))
    return items


def numerals():
    out = []
    for h in range(1, 13):
        x, y = polar(R_NUM, h * 30)
        out.append(("text", dict(cx=x, cy=y, size=24, text=str(h), color=NUMERAL, angle=h * 30)))
    return out


def sword(length, wmax, color_body=SILVER, color_core=HAND_CORE, steps=36):
    """Skeleton sword hand pointing up from (C, C): silver silhouette, black core, crisp outline."""
    tail, neck, shoulder = 14, 16, 0.8 * length

    def width(d):  # d = distance from pivot toward the tip (negative = tail)
        if d <= shoulder:
            return 6 + (wmax - 6) * max(d, 0) / shoulder
        return wmax * (length - d) / (length - shoulder)

    g = (C - wmax / 2, C, C + wmax / 2, C, HAND_METAL, [0, 0.5, 1])
    items = []
    span = length + tail
    for i in range(steps):
        a, b = -tail + span * i / steps, -tail + span * (i + 1) / steps
        items.append(line(C, C - a, C, C - b, width((a + b) / 2), "#FFFFFFFF", "BUTT", grad=g))
    pts = [(-3, -tail), (-wmax / 2, shoulder), (0, length), (wmax / 2, shoulder), (3, -tail)]
    for (xa, da), (xb, db) in zip(pts, pts[1:] + pts[:1]):
        items.append(line(C + xa, C - da, C + xb, C - db, 1.6, "#FFFFFFFF", grad=g))
    core_end = length - 10
    for i in range(steps):
        a, b = neck + (core_end - neck) * i / steps, neck + (core_end - neck) * (i + 1) / steps
        w = width((a + b) / 2) - 5.2
        if w > 0.4:
            items.append(line(C, C - a, C, C - b, w, color_core, "BUTT"))
    return items


def logo_mark(logo, cx, cy, color, h=20):
    k = h / 13
    if logo == "anthropic":
        segs = [((-2.5, -6.5), (-8, 6.5)), ((-2.5, -6.5), (3, 6.5)), ((-6.1, 2), (1.1, 2)), ((2.5, -6.5), (8, 6.5))]
        return [line(cx + a[0] * k, cy + a[1] * k, cx + b[0] * k, cy + b[1] * k, 3, color) for a, b in segs]
    if logo == "claude":
        angles = [0, 28, 62, 88, 121, 148, 181, 209, 238, 272, 300, 331]
        lengths = [7.4, 5.6, 7.0, 5.3, 7.3, 5.9, 6.8, 5.2, 7.2, 5.7, 7.0, 5.4]
        out = []
        for a, ln in zip(angles, lengths):
            x1, y1 = polar(1.3 * k, a, cx, cy)
            x2, y2 = polar(ln * k, a, cx, cy)
            out.append(line(x1, y1, x2, y2, 2.4, color))
        return out
    return []


# Day-date window at 3
WIN = dict(x=C + 38, y=C - 17, w=90, h=34, split=C + 98)


def dial_print():
    return [("text", dict(cx=C, cy=C + 72, size=27, text="100m", color=PRINT, weight="NORMAL")),
            ("text", dict(cx=C, cy=C + 96, size=12, text="WATER RESISTANT", color=PRINT)),
            ("text", dict(cx=C, cy=C + 112, size=14, text="PROFESSIONAL", color=PRINT))]


def date_window():
    x, y, w, h, s = WIN["x"], WIN["y"], WIN["w"], WIN["h"], WIN["split"]
    return [("box", dict(x=x, y=y, w=w, h=h, rad=3, fill="#FFECEDED", stroke="#FF8E9399", sw=2.2)),
            line(s, y + 3, s, y + h - 3, 1.4, "#FF8E9399"),
            ("text", dict(cx=(x + s) / 2, cy=C, size=18, source="day", text="MON", color="#FF1B1C1D")),
            ("text", dict(cx=(s + x + w) / 2, cy=C, size=18, source="date", text="1", color="#FF1B1C1D"))]


# ---------------------------------------------------------------------------
# Watch Face Format renderer
# ---------------------------------------------------------------------------
def wff_shape(kind, p, ind):
    if kind == "line":
        g = p.get("grad")
        inner = (f'<LinearGradient startX="{f(g[0])}" startY="{f(g[1])}" endX="{f(g[2])}" endY="{f(g[3])}" '
                 f'colors="{" ".join(g[4])}" positions="{" ".join(f(v) for v in g[5])}"/>') if g else ""
        stroke = (f'<Stroke color="{wcol(p["color"])}" thickness="{f(p["w"])}" cap="{p["cap"]}">{inner}</Stroke>' if g
                  else f'<Stroke color="{wcol(p["color"])}" thickness="{f(p["w"])}" cap="{p["cap"]}"/>')
        return (f'{ind}<Line startX="{f(p["x1"])}" startY="{f(p["y1"])}" endX="{f(p["x2"])}" endY="{f(p["y2"])}">'
                f'{stroke}</Line>')
    if kind == "dot":
        d = 2 * p["r"]
        return (f'{ind}<Ellipse x="{f(p["cx"] - p["r"])}" y="{f(p["cy"] - p["r"])}" width="{f(d)}" height="{f(d)}">'
                f'<Fill color="{wcol(p["color"])}"/></Ellipse>')
    if kind in ("rrect", "box"):
        if kind == "rrect":
            x, y = C - p["w"] / 2, C - p["r"] - p["h"] / 2
        else:
            x, y = p["x"], p["y"]
        stroke = f'<Stroke color="{p["stroke"]}" thickness="{f(p["sw"])}"/>' if p["stroke"] else ""
        return (f'{ind}<RoundRectangle x="{f(x)}" y="{f(y)}" width="{f(p["w"])}" height="{f(p["h"])}" '
                f'cornerRadiusX="{f(p["rad"])}" cornerRadiusY="{f(p["rad"])}"><Fill color="{p["fill"]}"/>{stroke}</RoundRectangle>')
    raise ValueError(kind)


def wff_draw(items, ind, name, extra=""):
    out = [f'{ind}<PartDraw name="{name}" x="0" y="0" width="{W}" height="{W}"{extra}>']
    out += [wff_shape(k, p, ind + "  ") for k, p in items]
    out.append(f"{ind}</PartDraw>")
    return out


def wff_text(p, ind, name):
    size = p["size"]
    bw, bh = size * 4.5, size * 1.4
    if p.get("source") == "day":
        body = '<Upper><Template>%s<Parameter expression="[DAY_OF_WEEK_S]"/></Template></Upper>'
    elif p.get("source") == "date":
        body = '<Template>%d<Parameter expression="[DAY]"/></Template>'
    else:
        body = p["text"]
    bw, bh = round(bw / 2) * 2, round(bh / 2) * 2   # PartText takes whole pixels
    rot = f' angle="{p["angle"]}"' if p.get("angle") else ""
    return [f'{ind}<PartText name="{name}" x="{round(p["cx"]) - bw // 2}" y="{round(p["cy"]) - bh // 2}" width="{bw}" height="{bh}"{rot}>',
            f'{ind}  <Text align="CENTER"><Font family="SYNC_TO_DEVICE" size="{f(size)}" weight="{p.get("weight", "BOLD")}" '
            f'color="{wcol(p["color"])}">{body}</Font></Text>',
            f"{ind}</PartText>"]


def sweep(stops):
    cols, pos = stops
    return (f'<SweepGradient centerX="{f(C)}" centerY="{f(C)}" startAngle="0" endAngle="360" '
            f'colors="{" ".join(cols)}" positions="{" ".join(f(v) for v in pos)}"/>')


def wff_sheens(ind, tilt):
    """Dial and ring sheens. With tilt on they turn a little, in opposite directions, as the wrist tilts."""
    d, rm, rw = R_DIAL, (R_DIAL + R_EDGE) / 2, R_EDGE - R_DIAL
    out = []
    for name, shape, k in (
            ("dialSheen", f'<Ellipse x="{f(C - d)}" y="{f(C - d)}" width="{2 * d}" height="{2 * d}">'
                          f'<Fill color="#FFFFFFFF">{sweep(DIAL_SHEEN)}</Fill></Ellipse>', (1.4, 1.0)),
            ("ringSheen", f'<Ellipse x="{f(C - rm)}" y="{f(C - rm)}" width="{f(2 * rm)}" height="{f(2 * rm)}">'
                          f'<Stroke color="#FFFFFFFF" thickness="{f(rw)}">{sweep(RING_SHEEN)}</Stroke></Ellipse>', (-0.9, -0.7))):
        out.append(f'{ind}<PartDraw name="{name}" x="0" y="0" width="{W}" height="{W}" pivotX="0.5" pivotY="0.5">')
        if tilt:
            out.append(f'{ind}  <Gyro angle="{TILT.format(a=k[0], b=k[1])}"/>')
        out.append(f"{ind}  {shape}")
        out.append(f"{ind}</PartDraw>")
    return out


def build_wff():
    L = ['<?xml version="1.0" encoding="utf-8"?>',
         "<!-- Generated by tools/generate.py - edit the generator, not this file. -->",
         f'<WatchFace width="{W}" height="{W}" clipShape="CIRCLE">',
         '  <Metadata key="CLOCK_TYPE" value="ANALOG"/>',
         '  <Metadata key="PREVIEW_TIME" value="10:10:32"/>',
         "  <UserConfigurations>",
         '    <ColorConfiguration id="dial" displayName="@string/dial_color" defaultValue="slate">']
    L += [f'      <ColorOption id="{i}" displayName="@string/dial_{i}" colors="{c}"/>' for i, _, c in DIALS]
    L += ["    </ColorConfiguration>",
          '    <ColorConfiguration id="accent" displayName="@string/accent_color" defaultValue="yellow">']
    L += [f'      <ColorOption id="{i}" displayName="@string/accent_{i}" colors="{c}"/>' for i, _, c in ACCENTS]
    L += ["    </ColorConfiguration>",
          '    <ListConfiguration id="logo" displayName="@string/logo" defaultValue="none">']
    L += [f'      <ListOption id="{i}" displayName="@string/logo_{i}"/>' for i, _ in LOGOS]
    L += ["    </ListConfiguration>",
          '    <BooleanConfiguration id="tilt" displayName="@string/tilt" defaultValue="TRUE"/>',
          "  </UserConfigurations>", f'  <Scene backgroundColor="{CASE}">']
    ind = "    "

    # Dial: theme colour, literal light-to-shadow glow on top (hidden in ambient)
    L.append(f'{ind}<PartDraw name="dial" x="0" y="0" width="{W}" height="{W}">')
    L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="0"/>')
    d = R_DIAL
    L.append(f'{ind}  <Ellipse x="{f(C - d)}" y="{f(C - d)}" width="{2 * d}" height="{2 * d}"><Fill color="{wcol(DIAL)}"/></Ellipse>')
    L.append(f'{ind}  <Ellipse x="{f(C - d)}" y="{f(C - d)}" width="{2 * d}" height="{2 * d}"><Fill color="#FFFFFFFF">'
             f'<RadialGradient centerX="{f(C - 45)}" centerY="{f(C - 70)}" radius="{2 * d}" colors="{" ".join(DIAL_GLOW[0])}" '
             f'positions="{" ".join(f(v) for v in DIAL_GLOW[1])}"/></Fill></Ellipse>')
    L.append(f'{ind}  <Ellipse x="{f(C - d)}" y="{f(C - d)}" width="{2 * d}" height="{2 * d}"><Stroke color="#FF000000" thickness="3"/></Ellipse>')
    L.append(f"{ind}</PartDraw>")

    L.append(f'{ind}<PartImage name="metal" x="0" y="0" width="{W}" height="{W}">')
    L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="0"/>')
    L.append(f'{ind}  <Image resource="metal_texture"/>')
    L.append(f"{ind}</PartImage>")
    L.append(f'{ind}<BooleanConfiguration id="tilt">')
    for opt in ("TRUE", "FALSE"):
        L.append(f'{ind}  <BooleanOption id="{opt}">')
        L.append(f'{ind}    <Group name="sheen{opt.title()}" x="0" y="0" width="{W}" height="{W}">')
        L.append(f'{ind}      <Variant mode="AMBIENT" target="alpha" value="0"/>')
        L += wff_sheens(ind + "      ", opt == "TRUE")
        L.append(f"{ind}    </Group>")
        L.append(f"{ind}  </BooleanOption>")
    L.append(f"{ind}</BooleanConfiguration>")

    L.append(f'{ind}<Group name="print" x="0" y="0" width="{W}" height="{W}">')
    L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="0"/>')
    for n, p in enumerate(dial_print()):
        L += wff_text(p[1], ind + "  ", f"print{n}")
    L.append(f'{ind}  <ListConfiguration id="logo">')
    for lid, _ in LOGOS:
        L.append(f'{ind}    <ListOption id="{lid}">')
        items = logo_mark(lid, C, C - 84, SILVER) or [("dot", dict(cx=C, cy=C - 84, r=0.1, color="#00000000"))]
        L += wff_draw(items, ind + "      ", f"logo_{lid}")
        L.append(f"{ind}    </ListOption>")
    L.append(f"{ind}  </ListConfiguration>")
    L.append(f"{ind}</Group>")

    # Teeth with lume bars, each drawn at 12 and rotated about the centre
    L.append(f'{ind}<Group name="teeth" x="0" y="0" width="{W}" height="{W}">')
    for h, items in enumerate(teeth()):
        L += wff_draw(items, ind + "  ", f"tooth{h}", f' pivotX="0.5" pivotY="0.5" angle="{h * 30}"')
    L.append(f"{ind}</Group>")

    L.append(f'{ind}<Group name="ticks" x="0" y="0" width="{W}" height="{W}">')
    L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="90"/>')
    L += wff_draw(minute_ticks(), ind + "  ", "minuteTicks")
    L.append(f"{ind}</Group>")

    L.append(f'{ind}<Group name="numerals" x="0" y="0" width="{W}" height="{W}">')
    L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="150"/>')
    for n, p in enumerate(numerals()):
        L += wff_text(p[1], ind + "  ", f"numeral{n + 1}")
    L.append(f"{ind}</Group>")

    L.append(f'{ind}<Group name="dayDate" x="0" y="0" width="{W}" height="{W}">')
    L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="130"/>')
    win = date_window()
    L += wff_draw([it for it in win if it[0] != "text"], ind + "  ", "window")
    L += wff_text(win[2][1], ind + "  ", "day")
    L += wff_text(win[3][1], ind + "  ", "date")
    L.append(f"{ind}</Group>")

    # Hands
    for name, (length, wmax), expr in (("hourHand", HOUR_HAND, "[HOUR_0_11_MINUTE] * 30"),
                                       ("minuteHand", MIN_HAND, "[MINUTE_SECOND] * 6")):
        L.append(f'{ind}<Group name="{name}" x="0" y="0" width="{W}" height="{W}" pivotX="0.5" pivotY="0.5">')
        L.append(f'{ind}  <Transform target="angle" value="{expr}"/>')
        L += wff_draw(sword(length, wmax), ind + "  ", name + "Shape")
        L.append(f"{ind}</Group>")
    L += wff_draw([("dot", dict(cx=C, cy=C, r=7.5, color=SILVER))], ind, "hub")
    L.append(f'{ind}<Group name="secondHand" x="0" y="0" width="{W}" height="{W}" pivotX="0.5" pivotY="0.5">')
    L.append(f'{ind}  <Variant mode="AMBIENT" target="alpha" value="0"/>')
    L.append(f'{ind}  <Transform target="angle" value="[SECOND] * 6"/>')
    L += wff_draw(seconds_items(), ind + "  ", "secondShape")
    L.append(f"{ind}</Group>")
    L += ["  </Scene>", "</WatchFace>"]
    return "\n".join(L) + "\n"


def seconds_items():
    return [line(C, C + SEC_HAND[0], C, C - SEC_HAND[1], 3.4, ACCENT, "BUTT"),
            ("dot", dict(cx=C, cy=C, r=4.5, color=ACCENT)),
            ("dot", dict(cx=C, cy=C, r=1.6, color=HAND_CORE))]


# ---------------------------------------------------------------------------
# SVG preview renderer (same geometry)
# ---------------------------------------------------------------------------
_gid = [0]


def svg_lingrad(g):
    _gid[0] += 1
    gid = f"lg{_gid[0]}"
    stops = "".join(f'<stop offset="{f(pos)}" stop-color="#{c[3:]}" stop-opacity="{int(c[1:3], 16) / 255:.3f}"/>'
                    for c, pos in zip(g[4], g[5]))
    return gid, (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{f(g[0])}" y1="{f(g[1])}" '
                 f'x2="{f(g[2])}" y2="{f(g[3])}">{stops}</linearGradient>')


def svg_items(items, pick, extra=""):
    o = []
    for kind, p in items:
        if kind == "line":
            col, op = scol(p["color"], pick)
            if p.get("grad"):
                gid, defs = svg_lingrad(p["grad"])
                o.append(f"<defs>{defs}</defs>")
                col, op = f"url(#{gid})", "1"
            o.append(f'<line x1="{f(p["x1"])}" y1="{f(p["y1"])}" x2="{f(p["x2"])}" y2="{f(p["y2"])}" stroke="{col}" '
                     f'stroke-opacity="{op}" stroke-width="{f(p["w"])}" stroke-linecap="{p["cap"].lower()}"/>')
        elif kind == "dot":
            col, op = scol(p["color"], pick)
            o.append(f'<circle cx="{f(p["cx"])}" cy="{f(p["cy"])}" r="{f(p["r"])}" fill="{col}" fill-opacity="{op}"/>')
        elif kind in ("rrect", "box"):
            if kind == "rrect":
                x, y, rot = C - p["w"] / 2, C - p["r"] - p["h"] / 2, f' transform="rotate({p["deg"]} {C} {C})"'
            else:
                x, y, rot = p["x"], p["y"], ""
            fc, fop = scol(p["fill"], pick)
            st = f' stroke="{scol(p["stroke"], pick)[0]}" stroke-width="{f(p["sw"])}"' if p["stroke"] else ""
            o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(p["w"])}" height="{f(p["h"])}" rx="{f(p["rad"])}" fill="{fc}" fill-opacity="{fop}"{st}{rot}/>')
        elif kind == "text":
            col, op = scol(p["color"], pick)
            wt = "normal" if p.get("weight") == "NORMAL" else "bold"
            rot = f' transform="rotate({p["angle"]} {f(p["cx"])} {f(p["cy"])})"' if p.get("angle") else ""
            o.append(f'<text x="{f(p["cx"])}" y="{f(p["cy"])}" font-family="Roboto, Segoe UI, sans-serif" font-size="{f(p["size"])}" '
                     f'font-weight="{wt}" fill="{col}" text-anchor="middle" dominant-baseline="central"'
                     f'{rot}>{p["text"]}</text>')
    return o


def css_conic(stops):
    parts = []
    for c, pos in zip(*stops):
        a = int(c[1:3], 16) / 255
        rgb = "255,255,255" if c[3:] == "FFFFFF" else "0,0,0"
        parts.append(f"rgba({rgb},{a:.3f}) {pos * 360:.1f}deg")
    return f"conic-gradient(from 0deg, {', '.join(parts)})"


def svg_sheens():
    """The sweep gradients, drawn with CSS conic gradients (SVG has none). Shown untilted."""
    d, rw = R_DIAL, R_EDGE - R_DIAL
    return [f'<foreignObject x="0" y="0" width="{W}" height="{W}"><div xmlns="http://www.w3.org/1999/xhtml" '
            f'style="position:absolute;left:{C - R_EDGE}px;top:{C - R_EDGE}px;width:{2 * R_EDGE}px;height:{2 * R_EDGE}px;'
            f'border-radius:50%;background:{css_conic(RING_SHEEN)};'
            f'-webkit-mask:radial-gradient(circle, transparent {d}px, #000 {d}px)"></div>'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="position:absolute;left:{C - d}px;top:{C - d}px;'
            f'width:{2 * d}px;height:{2 * d}px;border-radius:50%;background:{css_conic(DIAL_SHEEN)}"></div></foreignObject>']


def build_svg(pick, logo, hh=10, mm=10, ss=32):
    minute = mm + ss / 60
    m_ang, h_ang, s_ang = minute * 6, ((hh % 12) + minute / 60) * 30, ss * 6
    dc, _ = scol(DIAL, pick)
    stops = "".join(f'<stop offset="{f(p)}" stop-color="{scol(c, pick)[0]}" stop-opacity="{scol(c, pick)[1]}"/>'
                    for c, p in zip(*DIAL_GLOW))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">',
         f'<defs><radialGradient id="g" gradientUnits="userSpaceOnUse" cx="{C - 45}" cy="{C - 70}" r="{2 * R_DIAL}">{stops}</radialGradient>'
         f'<clipPath id="c"><circle cx="{C}" cy="{C}" r="{C}"/></clipPath></defs>',
         f'<g clip-path="url(#c)"><rect width="{W}" height="{W}" fill="#{CASE[3:]}"/>',
         f'<circle cx="{C}" cy="{C}" r="{R_DIAL}" fill="{dc}"/>',
         f'<circle cx="{C}" cy="{C}" r="{R_DIAL}" fill="url(#g)" stroke="#000" stroke-width="3"/>',
         f'<image href="../app/src/main/res/drawable-nodpi/metal_texture.png" x="0" y="0" width="{W}" height="{W}"/>']
    o += svg_sheens()
    o += svg_items(dial_print(), pick)
    o += svg_items(logo_mark(logo, C, C - 84, SILVER), pick)
    for h, items in enumerate(teeth()):
        # Draw each tooth upright and rotate the group, as the watch does (bevel lines are in local coords).
        o.append(f'<g transform="rotate({h * 30} {C} {C})">')
        o += svg_items([(k, dict(p, deg=0)) if k == "rrect" else (k, p) for k, p in items], pick)
        o.append("</g>")
    o += svg_items(minute_ticks(), pick)
    o += svg_items(numerals(), pick)
    o += svg_items(date_window(), pick)
    o.append(f'<g transform="rotate({f(h_ang)} {C} {C})">')
    o += svg_items(sword(*HOUR_HAND), pick)
    o.append(f'</g><g transform="rotate({f(m_ang)} {C} {C})">')
    o += svg_items(sword(*MIN_HAND), pick)
    o.append("</g>")
    o += svg_items([("dot", dict(cx=C, cy=C, r=7.5, color=SILVER))], pick)
    o.append(f'<g transform="rotate({f(s_ang)} {C} {C})">')
    o += svg_items(seconds_items(), pick)
    o.append("</g></g></svg>")
    return "\n".join(o)


def build_strings():
    s = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>",
         '    <string name="app_name">Rampart</string>',
         '    <string name="dial_color">Dial</string>',
         '    <string name="accent_color">Seconds</string>',
         '    <string name="logo">Logo</string>',
         '    <string name="tilt">Tilt shine</string>']
    s += [f'    <string name="dial_{i}">{n}</string>' for i, n, _ in DIALS]
    s += [f'    <string name="accent_{i}">{n}</string>' for i, n, _ in ACCENTS]
    s += [f'    <string name="logo_{i}">{n}</string>' for i, n in LOGOS]
    s.append("</resources>")
    return "\n".join(s) + "\n"


if __name__ == "__main__":
    res = ROOT / "app/src/main/res"
    (res / "raw").mkdir(parents=True, exist_ok=True)
    (res / "raw/watchface.xml").write_text(build_wff())
    (res / "values/strings.xml").write_text(build_strings())
    prev = ROOT / "preview"
    prev.mkdir(exist_ok=True)
    for old in prev.glob("*.svg"):
        old.unlink()
    for (did, _, dcol), (aid, _, acol) in zip(DIALS, ACCENTS):
        (prev / f"{did}-{aid}.svg").write_text(build_svg({"dial": dcol, "accent": acol}, "none"))
    for lid, _ in LOGOS[1:]:
        (prev / f"logo-{lid}.svg").write_text(build_svg({"dial": DIALS[0][2], "accent": ACCENTS[0][2]}, lid))
    print("wrote watchface.xml, strings.xml and preview SVGs")
