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
    W, H = 1100, 400
    s = Svg(W, H, t)
    CY = 196
    X_DS, W_DS = 16, 150
    s.box(X_DS, CY - 40, W_DS, 80)
    s.text(X_DS + W_DS / 2, CY - 2, "2,843 videos", 19, 700)
    s.text(X_DS + W_DS / 2, CY + 20, "8 countries", 14.5, 400, t["gray"])
    X_IN, W_IN, H_IN, GAP_Y = 236, 214, 60, 96
    ys = [CY - GAP_Y, CY, CY + GAP_Y]
    s.text(X_IN, ys[0] - H_IN / 2 - 14, "THREE SIGNALS PER VIDEO", 12.5, 700, t["gray"], "start", 1.1)
    for yc, n, kind in zip(ys, ["Thumbnail", "Subtitles", "Video description"], ["thumbnail", "subtitles", "description"]):
        s.box(X_IN, yc - H_IN / 2, W_IN, H_IN)
        icon(s, kind, X_IN + 14, yc - 11)
        s.text(X_IN + 54, yc + 5.5, n, 16, 700, anchor="start")
    bus1 = X_DS + W_DS + 30
    s.line([(X_DS + W_DS, CY), (bus1, CY)], head=False)
    s.line([(bus1, ys[0]), (bus1, ys[2])], head=False)
    for yc in ys:
        s.line([(bus1, yc), (X_IN - 2, yc)])
    X_PR, W_PR = 512, 214
    bus2 = X_IN + W_IN + 26
    for yc in ys:
        s.line([(X_IN + W_IN, yc), (bus2, yc)], head=False)
    s.line([(bus2, ys[0]), (bus2, ys[2])], head=False)
    s.line([(bus2, CY), (X_PR - 2, CY)])
    PT, PH = CY - 104, 208
    s.box(X_PR, PT, W_PR, PH)
    s.text(X_PR + 18, PT + 34, "Prompt", 20, 700, anchor="start")
    for i, (n, hot) in enumerate([("Zero-shot", False), ("Fixed few-shot", False), ("Dynamic few-shot", True)]):
        y0 = PT + 56 + i * 48
        if hot:
            s.box(X_PR + 16, y0, W_PR - 32, 40, t["accent"], t["tint"], 1.8, 20)
            s.text(X_PR + W_PR / 2, y0 + 25.5, n, 16, 700, t["accent"])
        else:
            s.box(X_PR + 16, y0, W_PR - 32, 40, t["soft"], None, 1.4, 20)
            s.text(X_PR + W_PR / 2, y0 + 25.5, n, 16, 700)
    BY = PT + PH + 48
    s.box(X_PR, BY, W_PR, 46, t["soft"], None, 1.4)
    s.text(X_PR + W_PR / 2, BY + 29, "Example bank", 16, 700)
    s.line([(X_PR + 40, BY - 2), (X_PR + 40, PT + PH + 4)], accent=True)
    s.text(X_PR + 54, PT + PH + 31, "2 similar examples", 14.5, 400, t["accent"], "start")
    X_LLM, W_LLM = 766, 124
    s.box(X_LLM, CY - 62, W_LLM, 124)
    s.text(X_LLM + W_LLM / 2, CY - 8, "LLM", 22, 700)
    s.text(X_LLM + W_LLM / 2, CY + 17, "4 proprietary", 14.5, 400, t["gray"])
    s.text(X_LLM + W_LLM / 2, CY + 36, "2 open-weight", 14.5, 400, t["gray"])
    s.line([(X_PR + W_PR, CY), (X_LLM - 2, CY)])
    X_OUT, W_OUT, OB = 942, 142, 34
    bus3 = X_LLM + W_LLM + 24
    s.line([(X_LLM + W_LLM, CY), (bus3, CY)], head=False)
    s.line([(bus3, CY - OB), (bus3, CY + OB)], head=False)
    s.line([(bus3, CY - OB), (X_OUT - 2, CY - OB)])
    s.line([(bus3, CY + OB), (X_OUT - 2, CY + OB)])
    s.box(X_OUT, CY - OB - 22, W_OUT, 44, t["accent"], t["tint"], 1.8, 22)
    s.text(X_OUT + W_OUT / 2, CY - OB + 5.5, "Misleading", 16, 700, t["accent"])
    s.box(X_OUT, CY + OB - 22, W_OUT, 44, t["line"], None, 1.6, 22)
    s.text(X_OUT + W_OUT / 2, CY + OB + 5.5, "Not misleading", 16, 700)
    s.save(f"public/{name}-{'dark' if t is THEMES['dark'] else 'light'}.svg")


# ----------------------------------------------------------------------------
# Web Conference paper: the whole study as one picture (numbers are the paper's own)
# ----------------------------------------------------------------------------
def www(name, theme, t):
    """The Web Conference study as a picture: who and what was studied, what was built, how it
    was tested, what it found. Drawn at display size (520 wide)."""
    W, H = 520, 1044
    s = Svg(W, H, t)
    ink, gray, acc, soft, line, bg, tint = t["ink"], t["gray"], t["accent"], t["soft"], t["line"], t["bg"], t["tint"]

    def rule(y):
        s.p.append(f'<path d="M6,{y} H{W - 6}" stroke="{soft}" stroke-width="1.2"/>')

    def g(x, y, inner, k=1.0, stroke=None, sw=1.8, fill="none"):
        s.p.append(f'<g transform="translate({x},{y}) scale({k})" fill="{fill}" stroke="{stroke or line}" '
                   f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{inner}</g>')

    def solid(x, y, inner, color):
        s.p.append(f'<g transform="translate({x},{y})" fill="{color}">{inner}</g>')

    # ---- icons (local coordinates, about 40 by 40 unless noted)
    WORKER = ('<circle cx="10" cy="12" r="5"/><path d="M4.2,10 Q4.2,3 10,3 Q15.8,3 15.8,10"/><path d="M2.5,10 H17.5"/>'
              '<path d="M1.5,34 Q1.5,20 10,20 Q18.5,20 18.5,34"/>')                                   # 20 x 34
    FACTORY = ('<path d="M1,50 V24 L16,13 V24 L31,13 V24 L46,13 V24 H59 V50 Z"/><path d="M47,24 V4 H56 V24"/>'
               '<path d="M9,38 H15 M24,38 H30 M39,38 H45"/>')                                        # 60 x 50
    PHONE = ('<rect x="1" y="1" width="58" height="100" rx="10"/><path d="M22,9 H38"/>'
             '<rect x="9" y="32" width="42" height="46" rx="6"/><path d="M15,68 H26 M34,68 H45"/>')   # 60 x 102
    PIN = '<path d="M30,62 C25,55 24,52 24,49 A6,6 0 0 1 36,49 C36,52 35,55 30,62 Z"/><circle cx="30" cy="49" r="2"/>'
    CAMERA = '<rect x="1" y="7" width="26" height="18" rx="4"/><circle cx="14" cy="16" r="5"/><path d="M8,7 L10,3 H18 L20,7"/>'
    MIC = '<rect x="9" y="1" width="9" height="16" rx="4.5"/><path d="M4,13 Q4,23 13.5,23 Q23,23 23,13"/><path d="M13.5,23 V28"/>'
    BUBBLE = '<path d="M3,3 H25 Q27,3 27,5 V17 Q27,19 25,19 H12 L6,25 V19 H3 Q1,19 1,17 V5 Q1,3 3,3 Z"/>'
    DOC = '<path d="M6,1 H26 L34,9 V39 H6 Z"/><path d="M26,1 V9 H34"/><path d="M12,19 H28 M12,26 H28 M12,33 H21"/>'
    CHIP = ('<rect x="4" y="4" width="32" height="32" rx="8"/><path d="M13,-1 V4 M20,-1 V4 M27,-1 V4 M13,36 V41 M20,36 V41 M27,36 V41"/>')
    SPEAKER = '<path d="M2,15 H9 L19,7 V33 L9,25 H2 Z"/><path d="M25,14 Q30,20 25,26"/><path d="M30,9 Q38,20 30,31"/>'
    FRAME = '<rect x="1" y="3" width="46" height="34" rx="5"/><path d="M8,29 V20 L16,13 L24,20 V29 Z"/>'
    FRAME_PIN = '<path d="M36,28 C32,23 31,21 31,19 A5,5 0 0 1 41,19 C41,21 40,23 36,28 Z"/><circle cx="36" cy="19" r="1.7"/>'

    def face(cx, cy, mood, color):
        k = 1.15
        eyes = '<circle cx="-8" cy="-5" r="1.9" fill="%s" stroke="none"/><circle cx="8" cy="-5" r="1.9" fill="%s" stroke="none"/>' % (color, color)
        mouth = {"smile": '<path d="M-9,6 Q0,15 9,6"/>',
                 "frown": '<path d="M-8,11 Q0,6 8,11"/>',
                 "worried": '<path d="M-9,13 Q0,5 9,13"/><path d="M-12,-9 L-5,-12 M12,-9 L5,-12"/>'}[mood]
        g(cx, cy, '<circle r="22"/>' + eyes + mouth, k, color, 1.7)

    # ================= 1. who and what was studied
    s.text(6, 26, "Who and what we studied", 19, 700, anchor="start")
    for x0 in (6, 266):
        s.p.append(f'<rect x="{x0}" y="40" width="248" height="104" rx="10" fill="none" stroke="{soft}" stroke-width="1.4"/>')
    g(41, 63, FACTORY, 1.15)
    for x in (129, 163, 197):
        g(x, 81, WORKER, 1.15)
    g(326, 47, PHONE, 0.9)
    g(326, 47, PIN, 0.9, acc, 1.9)
    g(404, 56, CAMERA, 1.0)
    g(406, 90, MIC, 1.0)
    g(404, 118, BUBBLE, 0.8)
    s.text(130, 172, "34 factory workers", 17, 700)
    s.text(130, 192, "interviewed in Lahore", 15, 400, gray)
    s.text(390, 172, "50 apps", 17, 700)
    s.text(390, 192, "loan, gambling, and trading", 15, 400, gray)
    s.text(6, 224, "30 of the 34 had never been told how their data is protected.", 16, 400, gray, "start")
    rule(248)

    # ================= 2. what was built
    s.text(6, 282, "What we built from each privacy policy", 19, 700, anchor="start")
    for cx, icon, label in [(70, DOC, "Privacy policy"), (260, None, "LLM summary"), (450, SPEAKER, "Urdu audio")]:
        s.box(cx - 48, 300, 96, 76, soft, None, 1.4, 10)
        if icon:
            g(cx - 20, 318, icon, 1.0)
        s.text(cx, 402, label, 16, 700)
    g(260 - 20, 318, CHIP, 1.0)
    s.text(260, 342, "AI", 15, 700)
    s.line([(122, 338), (208, 338)])
    s.line([(312, 338), (398, 338)])
    s.line([(450, 412), (450, 458)])
    s.line([(450, 430), (130, 430), (130, 458)])
    for x0, title, sub in [(6, "Intervention 1", "audio summary"), (266, "Intervention 2", "audio plus risk visuals")]:
        s.box(x0, 460, 248, 118, acc, tint, 1.8, 10)
        s.text(x0 + 124, 546, title, 17, 700, acc)
        s.text(x0 + 124, 567, sub, 15, 400, gray)
    g(110, 474, SPEAKER, 1.0, acc, 1.9)
    g(330, 474, SPEAKER, 1.0, acc, 1.9)
    s.text(384, 500, "+", 24, 400, acc)
    g(402, 478, FRAME, 0.95, acc, 1.9)
    g(402, 478, FRAME_PIN, 0.95, acc, 1.9)
    rule(604)

    # ================= 3. how it was tested
    s.text(6, 638, "How it was tested", 19, 700, anchor="start")
    for x0, cx, mood, color, a, b in [
        (6, 82, "smile", ink, "Baseline", "most were confident"),
        (184, 260, "frown", ink, "Intervention 1", "more cautious"),
        (362, 438, "worried", acc, "Intervention 2", "92 to 94% cautious"),
    ]:
        s.box(x0, 656, 152, 92, soft, None, 1.4, 10)
        face(cx, 702, mood, color)
        s.text(cx, 774, a, 16, 700)
        s.text(cx, 794, b, 15, 400, gray)
    s.line([(160, 702), (182, 702)])
    s.line([(338, 702), (360, 702)])
    s.text(6, 828, "Each person rated their confidence in installing a finance app.", 16, 400, gray, "start")
    rule(854)

    # ================= 4. what it finds
    s.text(6, 888, "What it finds", 19, 700, anchor="start")
    person = '<circle cx="8" cy="5" r="4.2"/><path d="M1,22 Q1,12 8,12 Q15,12 15,22 Z"/>'
    phone = (f'<rect width="15" height="23" rx="3.4"/><rect x="2" y="3.6" width="11" height="14" rx="1.4" fill="{bg}"/>'
             f'<circle cx="7.5" cy="20.4" r="1.2" fill="{bg}"/>')
    for i in range(20):
        solid(6 + 21 * i, 906, person, acc if i < 17 else soft)
    s.p.append(f'<text x="6" y="958" font-size="16"><tspan font-weight="700" fill="{acc}">85%</tspan>'
               f'<tspan fill="{gray}"> of participants did not understand basic app permissions</tspan></text>')
    for i in range(10):
        solid(6 + 26 * i, 981, phone, acc if i < 8 else soft)
    s.p.append(f'<text x="6" y="1032" font-size="16"><tspan font-weight="700" fill="{ink}">80%</tspan>'
               f'<tspan fill="{gray}"> of apps (40 of 50) ask for more permissions than they need</tspan></text>')
    s.save(f"public/{name}-{theme}.svg")


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
    """The whole safeMAS paper as one picture. Drawn at the size it is shown (520 wide),
    so the text here is the text on the page. Terms and numbers are the paper's own."""
    W, H = 520, 840
    s = Svg(W, H, t)
    ink, gray, acc, soft = t["ink"], t["gray"], t["accent"], t["soft"]

    def rule(y):
        s.p.append(f'<path d="M6,{y} H{W - 6}" stroke="{soft}" stroke-width="1.2"/>')

    # 1. the setup: same tasks, five team structures
    s.text(6, 28, "The same tasks, five team structures", 19, 700, anchor="start")
    for i, (kind, label) in enumerate([("single", "Single agent"), ("centralized", "Centralized"),
                                       ("decentralized", "Decentralized"), ("hybrid", "Hybrid"),
                                       ("independent", "Independent")]):
        xc = 52 + 104 * i
        glyph(s, kind, xc - 25, 78, 1.25)
        s.text(xc, 122, label, 15, 400)
    s.text(6, 154, "In a team the tools are split, so no agent can finish alone.", 16, 400, gray, "start")
    rule(180)

    # 2. the attack: one payload, three ways in, and what it does next
    s.text(6, 214, "One payload, three ways to plant it", 19, 700, anchor="start")
    for xc, kind, label in [(90, "instruction", "Instruction injection"), (260, "tool", "Tool poisoning"),
                            (430, "message", "Message tampering")]:
        glyph(s, kind, xc - 25, 262, 1.25)
        s.text(xc, 304, label, 15, 400)
    for xc in (90, 260, 430):
        s.p.append(f'<path d="M{xc},316 V336" stroke="{acc}" stroke-width="1.8"/>')
    s.p.append(f'<path d="M73,336 H430" stroke="{acc}" stroke-width="1.8"/>')
    s.line([(73, 336), (73, 362)], accent=True)
    BY, BH = 364, 50
    for x0, w, label, hot in [(6, 134, "Relay agent", False), (193, 134, "Record", False), (386, 128, "Target agent", True)]:
        if hot:
            s.box(x0, BY, w, BH, acc, t["tint"], 1.8)
            s.text(x0 + w / 2, BY + 31, label, 17, 700, acc)
        else:
            s.box(x0, BY, w, BH)
            s.text(x0 + w / 2, BY + 31, label, 17, 700)
    s.line([(140, BY + BH / 2), (191, BY + BH / 2)], accent=True)
    s.line([(327, BY + BH / 2), (384, BY + BH / 2)], accent=True)
    s.text(6, 446, "The relay agent writes the payload into a record.", 16, 400, gray, "start")
    s.text(6, 470, "The target agent reads it and makes the harmful write.", 16, 400, gray, "start")
    rule(496)

    # 3. the measurement
    s.text(6, 530, "What is measured", 19, 700, anchor="start")
    for x0, label in [(6, "Attack success"), (178, "Task completion"), (350, "Model calls")]:
        s.box(x0, 548, 164, 46, soft, None, 1.6)
        s.text(x0 + 82, 578, label, 16.5, 700)
    s.text(6, 624, "Attack success and task completion come from the final state,", 16, 400, gray, "start")
    s.text(6, 646, "with no language model as judge.", 16, 400, gray, "start")
    rule(672)

    # 4. what it finds
    s.text(6, 706, "What it finds", 19, 700, anchor="start")
    for x0, big, color, lines in [
        (6, "76%", acc, ["of runs: a tampered", "message succeeds"]),
        (178, "39 to 40%", ink, ["on orchestrated teams,", "vs 41% for one agent,", "same attacks"]),
        (350, "42 to 49%", ink, ["of the task done by", "orchestrated teams, vs", "90% for one agent"]),
    ]:
        s.text(x0, 756, big, 30, 700, color, "start")
        for i, line in enumerate(lines):
            s.text(x0, 784 + 20 * i, line, 15, 400, gray, "start")
    s.save(f"public/{name}-{theme}.svg")


if __name__ == "__main__":
    for theme, t in THEMES.items():
        clickbait("icwsm-pipeline", t)
        www("www-overview", theme, t)
        safemas("safemas-overview", theme, t)
