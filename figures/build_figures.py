"""Builds the theme-aware figures for the Publications section.

  python3 figures/build_figures.py

Every figure is written twice to public/, as NAME-light.svg and NAME-dark.svg, each
painted on the exact page background so it blends into the site. The page swaps the
two with the dark-mode toggle (see .figure in src/style.css).

  www-overview      the Web Conference study as one picture, at display size
  icwsm-pipeline    the ICWSM detection pipeline (a few words per box, one accent color)
  safemas-overview  the whole safeMAS paper as one picture, at display size

The palette below mirrors the CSS variables in src/style.css. If the site colors
change, change them here too and run this script again.
"""
from xml.sax.saxutils import escape

FONT = "Arial, Helvetica, Arimo, sans-serif"


def mix(a, b, t):
    """Blend hex color a toward b by fraction t."""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(pa, pb))


def make_theme(bg, ink, gray, line, soft, accent, tint_amount):
    return dict(bg=bg, ink=ink, gray=gray, line=line, soft=soft, accent=accent,
                tint=mix(bg, accent, tint_amount))


THEMES = {
    "light": make_theme("#f7f4ed", "#1c1b19", "#6a655b", "#3a3834", "#cdc6b4", "#9a3b26", 0.13),
    "dark": make_theme("#161513", "#e9e5db", "#a39d90", "#cfc9bb", "#4b473f", "#e39274", 0.20),
}


# ----------------------------------------------------------------------------
# small SVG drawing kit
# ----------------------------------------------------------------------------
class Svg:
    def __init__(self, w, h, t):
        self.w, self.h, self.t, self.p = w, h, t, []
        self.p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">')
        self.p.append('<defs>'
                      f'<marker id="a" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{t["line"]}"/></marker>'
                      f'<marker id="b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{t["accent"]}"/></marker>'
                      '</defs>')
        self.p.append(f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>')

    def box(self, x, y, w, h, stroke=None, fill=None, sw=1.6, r=6):
        stroke = stroke or self.t["line"]
        fill = fill or self.t["bg"]
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=17, weight=400, fill=None, anchor="middle", spacing=0, halo=False):
        fill = fill or self.t["ink"]
        sp = f' letter-spacing="{spacing}"' if spacing else ""
        hl = f' stroke="{self.t["bg"]}" stroke-width="7" stroke-linejoin="round" paint-order="stroke"' if halo else ""
        self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{sp}{hl}>{escape(s)}</text>')

    def line(self, pts, accent=False, head=True, sw=1.8):
        color = self.t["accent"] if accent else self.t["line"]
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        mk = f' marker-end="url(#{"b" if accent else "a"})"' if head else ""
        self.p.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"{mk}/>')

    def save(self, path):
        self.p.append('</svg>')
        open(path, "w").write("\n".join(self.p) + "\n")
        print("wrote", path)


def icon(s, kind, x, y):
    c = s.t["line"]
    g = f'<g transform="translate({x},{y})" fill="none" stroke="{c}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">'
    if kind == "thumbnail":
        g += '<rect width="30" height="22" rx="2.5"/><circle cx="9" cy="7.5" r="2.6"/><path d="M3,19 L11,11.5 L16,16 L20,12.5 L27,19"/>'
    elif kind == "subtitles":
        g += '<rect width="30" height="22" rx="2.5"/><path d="M6,12 H24 M6,17 H17"/>'
    else:
        g += '<path d="M4,0 H20 L26,6 V22 H4 Z"/><path d="M20,0 V6 H26"/><path d="M9,11 H21 M9,15.5 H21 M9,20 H16" stroke-width="1.4"/>'
    s.p.append(g + '</g>')


# ----------------------------------------------------------------------------
# ICWSM paper: misleading thumbnail detection pipeline (drawn here)
# ----------------------------------------------------------------------------
def clickbait(name, t):
    """The ICWSM detection pipeline, drawn at display size (720 wide), all text at least 14 px."""
    W, H = 720, 316
    s = Svg(W, H, t)
    ink, gray, acc, soft, line = t["ink"], t["gray"], t["accent"], t["soft"], t["line"]
    CY = 156

    # dataset
    s.box(6, CY - 34, 108, 68)
    s.text(60, CY - 3, "2,843 videos", 14.5, 700)
    s.text(60, CY + 18, "8 countries", 14, 400, gray)

    # three signals per video
    SX, SW, SH = 138, 136, 52
    ys = [CY - 72, CY, CY + 72]
    s.text(SX, 40, "Three signals per video", 14, 700, gray, "start")
    for yc, lines, kind in zip(ys, [["Thumbnail"], ["Subtitles"], ["Video", "description"]],
                               ["thumbnail", "subtitles", "description"]):
        s.box(SX, yc - SH / 2, SW, SH)
        icon(s, kind, SX + 9, yc - 11)
        if len(lines) == 1:
            s.text(SX + 46, yc + 5, lines[0], 14.5, 700, anchor="start")
        else:
            s.text(SX + 46, yc - 2, lines[0], 14.5, 700, anchor="start")
            s.text(SX + 46, yc + 15, lines[1], 14.5, 700, anchor="start")
    s.line([(114, CY), (126, CY)], head=False)
    s.line([(126, ys[0]), (126, ys[2])], head=False)
    for yc in ys:
        s.line([(126, yc), (SX - 2, yc)])

    # prompt
    PX, PW, PT, PH = 298, 150, 58, 186
    for yc in ys:
        s.line([(SX + SW, yc), (286, yc)], head=False)
    s.line([(286, ys[0]), (286, ys[2])], head=False)
    s.line([(286, CY), (PX - 2, CY)])
    s.box(PX, PT, PW, PH)
    s.text(PX + 14, PT + 28, "Prompt", 17, 700, anchor="start")
    for i, (n, hot) in enumerate([("Zero-shot", False), ("Fixed few-shot", False), ("Dynamic few-shot", True)]):
        y0 = PT + 44 + i * 44
        if hot:
            s.box(PX + 7, y0, PW - 14, 36, acc, t["tint"], 1.8, 18)
            s.text(PX + PW / 2, y0 + 23, n, 14, 700, acc)
        else:
            s.box(PX + 7, y0, PW - 14, 36, soft, None, 1.4, 18)
            s.text(PX + PW / 2, y0 + 23, n, 14, 700)
    s.box(PX, 276, PW, 34, soft, None, 1.4)
    s.text(PX + PW / 2, 298, "Example bank", 14.5, 700)
    s.line([(PX + 22, 274), (PX + 22, PT + PH + 3)], accent=True)
    s.text(PX + 34, 266, "2 similar examples", 14, 400, acc, "start")

    # LLM and the two outcomes
    s.line([(PX + PW, CY), (470, CY)])
    s.box(472, CY - 46, 100, 92)
    s.text(522, CY - 8, "LLM", 20, 700)
    s.text(522, CY + 14, "4 proprietary", 14, 400, gray)
    s.text(522, CY + 32, "2 open-weight", 14, 400, gray)
    s.line([(572, CY), (584, CY)], head=False)
    s.line([(584, CY - 30), (584, CY + 30)], head=False)
    s.line([(584, CY - 30), (594, CY - 30)])
    s.line([(584, CY + 30), (594, CY + 30)])
    s.box(596, CY - 50, 118, 40, acc, t["tint"], 1.8, 20)
    s.text(655, CY - 25, "Misleading", 14.5, 700, acc)
    s.box(596, CY + 10, 118, 40, line, None, 1.6, 20)
    s.text(655, CY + 35, "Not misleading", 14.5, 700)
    s.save(f"public/{name}-{'dark' if t is THEMES['dark'] else 'light'}.svg")


# ----------------------------------------------------------------------------
# safeMAS: attack success by team structure and by attack vector (numbers from the paper)
# ----------------------------------------------------------------------------
def glyph(s, kind, x, yc, k=1.0):
    """40 by 28 icons (scaled by k): team structures and attack vectors."""
    t = s.t
    ln, bg, ac = t["line"], t["bg"], t["accent"]
    P = lambda a, b: (a, b)
    out = []

    def head(a, b, direction):
        """Small filled arrowhead with its tip at (a, b); direction is 'down' or 'right'."""
        x, y = P(a, b)
        if direction == "down":
            pts = f"{x - 3.2},{y - 5} {x + 3.2},{y - 5} {x},{y}"
        else:
            pts = f"{x - 5},{y - 3.2} {x - 5},{y + 3.2} {x},{y}"
        out.append(f'<polygon points="{pts}" fill="{ac}"/>')

    def node(a, b, r=3.4, solid=False):
        cx, cy = P(a, b)
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{ln if solid else bg}" stroke="{ln}" stroke-width="1.5"/>')

    def seg(a, b, c, d, color=ln):
        x1, y1 = P(a, b); x2, y2 = P(c, d)
        out.append(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="1.5" stroke-linecap="round" fill="none"/>')

    if kind == "single":
        node(20, 14, 8)
    elif kind in ("centralized", "hybrid"):
        for xx in (6, 20, 34):
            seg(20, 5, xx, 24)
        if kind == "hybrid":
            seg(6, 24, 20, 24); seg(20, 24, 34, 24)
        node(20, 5, 3.8, True)
        for xx in (6, 20, 34):
            node(xx, 24)
    elif kind == "decentralized":
        seg(6, 14, 20, 14); seg(20, 14, 34, 14)
        for xx in (6, 20, 34):
            node(xx, 14)
    elif kind == "independent":
        for xx in (6, 20, 34):
            seg(xx, 5, 20, 24)
        for xx in (6, 20, 34):
            node(xx, 5)
        node(20, 24, 3.8, True)
    elif kind == "message":
        x1, y1 = P(9, 14); x2, y2 = P(31, 14)
        pts = [P(9, 14), P(15, 14), P(19, 6), P(22, 22), P(25, 14), P(31, 14)]
        d = "M" + " L".join(f"{a},{b}" for a, b in pts)
        out.append(f'<path d="{d}" stroke="{ac}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" fill="none"/>')
        node(5, 14); node(35, 14)
    elif kind == "instruction":
        bx, by = P(5, 1)
        out.append(f'<rect x="{bx}" y="{by}" width="30" height="12" rx="2.5" fill="none" stroke="{ln}" stroke-width="1.5"/>')
        seg(10, 5, 28, 5); seg(10, 9, 22, 9)
        a1, b1 = P(20, 13); a2, b2 = P(20, 17)
        out.append(f'<path d="M{a1},{b1} L{a2},{b2}" stroke="{ac}" stroke-width="1.8" stroke-linecap="round" fill="none"/>')
        head(20, 19.5, "down")
        node(20, 24.5, 3)
    else:  # tool return
        bx, by = P(2, 3)
        out.append(f'<rect x="{bx}" y="{by}" width="13" height="13" rx="2.5" fill="none" stroke="{ln}" stroke-width="1.5"/>')
        pts = [P(15, 9.5), P(33, 9.5), P(33, 14)]
        d = "M" + " L".join(f"{a},{b}" for a, b in pts)
        out.append(f'<path d="{d}" stroke="{ac}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" fill="none"/>')
        head(33, 17.5, "down")
        node(33, 23.5, 3)
    s.p.append(f'<g transform="translate({x},{round(yc - 14 * k, 2)}) scale({k})">' + "".join(out) + "</g>")


def safemas(name, theme, t):
    """The whole safeMAS paper in one wide picture: the team structures, how an attack travels,
    and the findings. Drawn at display size (720 wide), all text at least 14 px."""
    W, H = 720, 340
    s = Svg(W, H, t)
    ink, gray, acc, soft = t["ink"], t["gray"], t["accent"], t["soft"]

    # ---- left: the team structures
    s.text(6, 26, "Same tasks, five team structures", 18, 700, anchor="start")
    for xc, yc, kind, label in [(62, 66, "single", "Single agent"), (174, 66, "centralized", "Centralized"),
                                (286, 66, "decentralized", "Decentralized"), (118, 130, "hybrid", "Hybrid"),
                                (230, 130, "independent", "Independent")]:
        glyph(s, kind, xc - 24, yc, 1.2)
        s.text(xc, yc + 34, label, 15, 400)
    s.text(6, 192, "In a team the tools are split, so no", 14.5, 400, gray, "start")
    s.text(6, 211, "agent can finish alone.", 14.5, 400, gray, "start")
    s.p.append(f'<path d="M354,10 V214" stroke="{soft}" stroke-width="1.2"/>')

    # ---- right: one payload, how it travels
    X0 = 366
    s.text(X0, 26, "One payload, three ways in", 18, 700, anchor="start")
    for i, (a, b) in enumerate([("Instruction", "injection"), ("Tool", "poisoning"), ("Message", "tampering")]):
        x = X0 + i * 120
        s.box(x, 40, 108, 48, soft, None, 1.4, 8)
        s.text(x + 54, 60, a, 15, 700)
        s.text(x + 54, 78, b, 15, 700)
        s.p.append(f'<path d="M{x + 54},88 V100" stroke="{acc}" stroke-width="1.8"/>')
    s.p.append(f'<path d="M{X0 + 54},100 H{X0 + 240 + 54}" stroke="{acc}" stroke-width="1.8"/>')
    s.line([(X0 + 54, 100), (X0 + 54, 110)], accent=True)
    for x0, w, label, hot in [(X0, 100, "Relay agent", False), (X0 + 124, 100, "Record", False), (X0 + 248, 100, "Target agent", True)]:
        if hot:
            s.box(x0, 112, w, 44, acc, t["tint"], 1.8)
            s.text(x0 + w / 2, 140, label, 15, 700, acc)
        else:
            s.box(x0, 112, w, 44)
            s.text(x0 + w / 2, 140, label, 15, 700)
    s.line([(X0 + 102, 134), (X0 + 122, 134)], accent=True)
    s.line([(X0 + 226, 134), (X0 + 246, 134)], accent=True)
    s.text(X0, 180, "The relay agent writes the payload into", 14.5, 400, gray, "start")
    s.text(X0, 199, "a record. The target agent reads it and", 14.5, 400, gray, "start")
    s.text(X0, 218, "makes the harmful write.", 14.5, 400, gray, "start")

    # ---- bottom: what it finds
    s.p.append(f'<path d="M6,234 H{W - 6}" stroke="{soft}" stroke-width="1.2"/>')
    for x0, big, color, lines in [
        (6, "76%", acc, ["of runs: a tampered", "message succeeds"]),
        (176, "39 to 40%", ink, ["on orchestrated teams,", "vs 41% for one agent,", "same attacks"]),
        (346, "42 to 49%", ink, ["of the task done by", "orchestrated teams, vs", "90% for one agent"]),
    ]:
        s.text(x0, 270, big, 28, 700, color, "start")
        for i, line in enumerate(lines):
            s.text(x0, 292 + 19 * i, line, 14.5, 400, gray, "start")
    for i, line in enumerate(["Attack success and task", "completion come from the", "final state, with no", "language model as judge."]):
        s.text(526, 262 + 19 * i, line, 14.5, 400, gray, "start")
    s.save(f"public/{name}-{theme}.svg")


def www(name, theme, t):
    """The Web Conference study as a picture, in four columns: studied, built, tested, found.
    Drawn at display size (720 wide), all text at least 14 px. Numbers are the paper's own."""
    W, H = 720, 324
    s = Svg(W, H, t)
    ink, gray, acc, soft, line, bg, tint = t["ink"], t["gray"], t["accent"], t["soft"], t["line"], t["bg"], t["tint"]
    COLS = [6, 186, 366, 546]

    def g(x, y, inner, k=1.0, stroke=None, sw=1.8, fill="none"):
        s.p.append(f'<g transform="translate({x},{y}) scale({k})" fill="{fill}" stroke="{stroke or line}" '
                   f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{inner}</g>')

    def solid(x, y, inner, color):
        s.p.append(f'<g transform="translate({x},{y})" fill="{color}">{inner}</g>')

    WORKER = ('<circle cx="10" cy="12" r="5"/><path d="M4.2,10 Q4.2,3 10,3 Q15.8,3 15.8,10"/><path d="M2.5,10 H17.5"/>'
              '<path d="M1.5,34 Q1.5,20 10,20 Q18.5,20 18.5,34"/>')
    FACTORY = ('<path d="M1,50 V24 L16,13 V24 L31,13 V24 L46,13 V24 H59 V50 Z"/><path d="M47,24 V4 H56 V24"/>'
               '<path d="M9,38 H15 M24,38 H30 M39,38 H45"/>')
    PHONE = ('<rect x="1" y="1" width="58" height="100" rx="10"/><path d="M22,9 H38"/>'
             '<rect x="9" y="32" width="42" height="46" rx="6"/><path d="M15,68 H26 M34,68 H45"/>')
    PIN = '<path d="M30,62 C25,55 24,52 24,49 A6,6 0 0 1 36,49 C36,52 35,55 30,62 Z"/><circle cx="30" cy="49" r="2"/>'
    CAMERA = '<rect x="1" y="7" width="26" height="18" rx="4"/><circle cx="14" cy="16" r="5"/><path d="M8,7 L10,3 H18 L20,7"/>'
    MIC = '<rect x="9" y="1" width="9" height="16" rx="4.5"/><path d="M4,13 Q4,23 13.5,23 Q23,23 23,13"/><path d="M13.5,23 V28"/>'
    BUBBLE = '<path d="M3,3 H25 Q27,3 27,5 V17 Q27,19 25,19 H12 L6,25 V19 H3 Q1,19 1,17 V5 Q1,3 3,3 Z"/>'
    DOC = '<path d="M6,1 H26 L34,9 V39 H6 Z"/><path d="M26,1 V9 H34"/><path d="M12,19 H28 M12,26 H28 M12,33 H21"/>'
    CHIP = '<rect x="4" y="4" width="32" height="32" rx="8"/><path d="M13,-1 V4 M20,-1 V4 M27,-1 V4 M13,36 V41 M20,36 V41 M27,36 V41"/>'
    SPEAKER = '<path d="M2,15 H9 L19,7 V33 L9,25 H2 Z"/><path d="M25,14 Q30,20 25,26"/><path d="M30,9 Q38,20 30,31"/>'
    FRAME = '<rect x="1" y="3" width="46" height="34" rx="5"/><path d="M8,29 V20 L16,13 L24,20 V29 Z"/>'
    PERSON = '<circle cx="8" cy="5" r="4.2"/><path d="M1,22 Q1,12 8,12 Q15,12 15,22 Z"/>'
    PHONE_SM = (f'<rect width="15" height="23" rx="3.4"/><rect x="2" y="3.6" width="11" height="14" rx="1.4" fill="{bg}"/>'
                f'<circle cx="7.5" cy="20.4" r="1.2" fill="{bg}"/>')

    def face(cx, cy, mood, color, k):
        eyes = f'<circle cx="-8" cy="-5" r="1.9" fill="{color}" stroke="none"/><circle cx="8" cy="-5" r="1.9" fill="{color}" stroke="none"/>'
        mouth = {"smile": '<path d="M-9,6 Q0,15 9,6"/>',
                 "frown": '<path d="M-8,11 Q0,6 8,11"/>',
                 "worried": '<path d="M-9,13 Q0,5 9,13"/><path d="M-12,-9 L-5,-12 M12,-9 L5,-12"/>'}[mood]
        g(cx, cy, '<circle r="22"/>' + eyes + mouth, k, color, 1.7)

    for x in (180, 360, 540):
        s.p.append(f'<path d="M{x},10 V{H - 10}" stroke="{soft}" stroke-width="1.2"/>')

    # ---- 1. studied
    c = COLS[0]
    s.text(c, 26, "Studied", 17, 700, anchor="start")
    g(c + 18, 50, FACTORY, 0.8)
    for x in (c + 78, c + 100, c + 122):
        g(x, 63, WORKER, 0.8)
    s.text(c + 84, 112, "34 factory workers", 14.5, 700)
    s.text(c + 84, 131, "interviewed in Lahore", 14, 400, gray)
    g(c + 26, 154, PHONE, 0.72)
    g(c + 26, 154, PIN, 0.72, acc, 1.9)
    g(c + 86, 160, CAMERA, 0.85)
    g(c + 88, 188, MIC, 0.85)
    g(c + 86, 214, BUBBLE, 0.72)
    s.text(c + 84, 254, "50 apps", 14.5, 700)
    s.text(c + 84, 273, "loan, gambling, trading", 14, 400, gray)

    # ---- 2. built
    c = COLS[1]
    s.text(c, 26, "Built", 17, 700, anchor="start")
    for i, (icon, label) in enumerate([(DOC, "Privacy policy"), (None, "LLM summary"), (SPEAKER, "Urdu audio")]):
        y = 42 + i * 52
        s.box(c + 4, y, 44, 40, soft, None, 1.4, 8)
        if icon:
            g(c + 10, y + 4, icon, 0.8)
        else:
            g(c + 10, y + 4, CHIP, 0.8)
            s.text(c + 26, y + 25, "AI", 14, 700)
        s.text(c + 58, y + 25, label, 14.5, 700, anchor="start")
        if i < 2:
            s.line([(c + 26, y + 41), (c + 26, y + 51)])
    s.line([(c + 26, 187), (c + 26, 200), (c + 129, 200), (c + 129, 208)])
    s.line([(c + 43, 200), (c + 43, 208)])
    for x0, label_lines, icons in [(c + 4, ["Audio"], "one"), (c + 90, ["Audio and", "visuals"], "two")]:
        s.box(x0, 210, 76, 56, acc, tint, 1.8, 8)
        if icons == "one":
            g(x0 + 27, 223, SPEAKER, 0.85, acc, 1.9)
        else:
            g(x0 + 5, 233, SPEAKER, 0.55, acc, 1.9)
            g(x0 + 31, 235, FRAME, 0.9 * 0.7, acc, 1.9)
        for j, ln in enumerate(label_lines):
            s.text(x0 + 38, 288 + 18 * j, ln, 14.5, 700, acc)
    for x0, n in [(c + 4, "1"), (c + 90, "2")]:
        s.p.append(f'<circle cx="{x0 + 11}" cy="221" r="10" fill="{acc}"/>')
        s.text(x0 + 11, 226, n, 14, 700, bg)

    # ---- 3. tested
    c = COLS[2]
    s.text(c, 26, "Tested", 17, 700, anchor="start")
    for i, (mood, color, a, b) in enumerate([("smile", ink, "Baseline", "mostly confident"),
                                             ("frown", ink, "After 1", "more cautious"),
                                             ("worried", acc, "After 2", "92 to 94% cautious")]):
        yc = 68 + i * 64
        face(c + 18, yc, mood, color, 0.72)
        s.text(c + 42, yc - 1, a, 14.5, 700, anchor="start")
        s.text(c + 42, yc + 17, b, 14, 400, gray, "start")
        if i < 2:
            s.line([(c + 18, yc + 19), (c + 18, yc + 44)])
    for i, ln in enumerate(["Each person rated their", "confidence in installing", "a finance app."]):
        s.text(c, 252 + 19 * i, ln, 14, 400, gray, "start")

    # ---- 4. found
    c = COLS[3]
    s.text(c, 26, "Found", 17, 700, anchor="start")
    for i in range(20):
        solid(c + 2 + (i % 10) * 16.4, 42 + (i // 10) * 28, PERSON, acc if i < 17 else soft)
    s.p.append(f'<text x="{c}" y="118" font-size="14.5"><tspan font-weight="700" fill="{acc}">85%</tspan>'
               f'<tspan fill="{gray}"> did not understand</tspan></text>')
    s.text(c, 137, "basic app permissions", 14.5, 400, gray, "start")
    for i in range(10):
        solid(c + 2 + (i % 5) * 33, 160 + (i // 5) * 34, PHONE_SM, acc if i < 8 else soft)
    s.p.append(f'<text x="{c}" y="236" font-size="14.5"><tspan font-weight="700" fill="{ink}">80%</tspan>'
               f'<tspan fill="{gray}"> of apps (40 of 50)</tspan></text>')
    s.text(c, 255, "ask for more permissions", 14.5, 400, gray, "start")
    s.text(c, 274, "than needed", 14.5, 400, gray, "start")
    s.save(f"public/{name}-{theme}.svg")


if __name__ == "__main__":
    for theme, t in THEMES.items():
        clickbait("icwsm-pipeline", t)
        www("www-overview", theme, t)
        safemas("safemas-overview", theme, t)
