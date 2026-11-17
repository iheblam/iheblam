"""Generates the animated arcade-style SVGs used by the profile README.

Run:  python scripts/generate_assets.py   (writes into ./assets)
Everything is pure SVG + CSS/SMIL animation, so it renders inside GitHub's <img> sandbox.
"""
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

FONT = "'Press Start 2P','Courier New',Courier,monospace"
BG, PANEL = "#0b0420", "#130829"
CYAN, PINK, YELLOW, GREEN, PURPLE, WHITE = "#00f0ff", "#ff2bd6", "#ffe600", "#39ff14", "#7b2cff", "#ffffff"


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name)


def sprite(grid, colors, x, y, s, extra=""):
    """Pixel sprite from a list of strings. Merges horizontal runs into single rects."""
    out = []
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == "." or ch not in colors:
                c += 1
                continue
            start = c
            while c < len(row) and row[c] == ch:
                c += 1
            out.append(f'<rect x="{x + start * s}" y="{y + r * s}" width="{(c - start) * s}" height="{s}" fill="{colors[ch]}"/>')
    return f'<g {extra}>' + "".join(out) + "</g>"


COMMON_DEFS = f"""
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".35"/></pattern>
<linearGradient id="neon" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PINK}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/></linearGradient>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="roll" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
"""


def crt_overlay(w, h):
    return f"""<rect width="{w}" height="{h}" fill="url(#scan)"/>
<rect class="roll" x="0" y="-60" width="{w}" height="60" fill="url(#roll)"/>
<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="14" fill="none" stroke="url(#neon)" stroke-width="3"/>"""


CRT_CSS = "@keyframes roll{from{transform:translateY(0)}to{transform:translateY(%dpx)}} .roll{animation:roll 6s linear infinite}"
BLINK_CSS = "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}} .blink{animation:blink 1s steps(1) infinite}"

# ---------------------------------------------------------------- sprites (original designs)
SHIP = ["XX.......", ".XXX.....", ".XoXXXX..", "XXXXXXXXc", ".XoXXXX..", ".XXX.....", "XX......."]
BUG_A = ["..X...X..", "...X.X...", ".XXXXXXX.", "XX.XXX.XX", "XXXXXXXXX", ".X.X.X.X.", "X.......X"]
BUG_B = ["..X...X..", "...X.X...", ".XXXXXXX.", "XX.XXX.XX", "XXXXXXXXX", ".X.X.X.X.", ".X.....X."]

AVATAR = [
    "....HHHHHHHH....",
    "...HHHHHHHHHH...",
    "..HHHHHHHHHHHH..",
    ".PHHSSSSSSSSHHP.",
    ".PHSSSSSSSSSSHP.",
    ".PSGGGGSSGGGGSP.",
    ".PSGEEGGGGEEGSP.",
    ".PSGGGGSSGGGGSP.",
    "..SSSSSSSSSSSS..",
    "..SSSSSMMSSSSSm.",
    "...SSSSSSSSSSm..",
    "....SSSSSSSSm...",
    "...KKKKSSKKKK...",
    "..KKKKKKKKKKKK..",
    ".KKKKKKKKKKKKKK.",
    ".KKKWKKKKKKWKKK.",
    ".KKKWKKKKKKWKKK.",
    ".KKKKKKKKKKKKKK.",
]
for row in AVATAR:
    assert len(row) == 16, row

ICONS = {
    "eye": ["..XXXX..", ".X....X.", "X..oo..X", "X.oooo.X", "X..oo..X", ".X....X.", "..XXXX..", "........"],
    "heart": [".XX..XX.", "XXXXXXXX", "XoXXXXXX", "XXXXXXXX", ".XXXXXX.", "..XXXX..", "...XX...", "........"],
    "monitor": ["XXXXXXXX", "XooooooX", "XoXoooXX", "XooooooX", "XXXXXXXX", "...XX...", "..XXXX..", "........"],
    "bolt": ["....XX..", "...XX...", "..XX....", ".XXXXXX.", "....XX..", "...XX...", "..XX....", "........"],
    "bubble": ["XXXXXXXX", "X......X", "X.o.o.oX", "X......X", "XXXXXXXX", ".XX.....", "X.......", "........"],
    "pad": ["........", ".XXXXXX.", "XXoXXXXX", "XoooXXoX", "XXoXXoXX", "XXXXXXXX", "XX....XX", "........"],
    "trophy": ["XXXXXXXX", "X.XXXX.X", ".XXXXXX.", "..XXXX..", "...XX...", "...XX...", "..XXXX..", ".XXXXXX."],
    "coin": ["..XXXX..", ".XooooX.", "XooXXooX", "XooXooX.", "XooXXooX", "XooooooX", ".XooooX.", "..XXXX.."],
}


# ---------------------------------------------------------------- HERO
def hero():
    W, H, HZ = 840, 320, 212
    rnd = random.Random(7)

    def stars(n, size):
        pts = [(rnd.randint(0, W), rnd.randint(46, HZ - 8)) for _ in range(n)]
        return "".join(f'<rect x="{x + dx}" y="{y}" width="{size}" height="{size}"/>' for x, y in pts for dx in (0, W))

    twinkles = "".join(
        f'<rect x="{rnd.randint(20, W - 20)}" y="{rnd.randint(50, 190)}" width="3" height="3" class="tw" style="animation-delay:-{rnd.random() * 3:.2f}s"/>'
        for _ in range(14))

    # perspective grid
    vlines = "".join(f'<line x1="{420 + i * 14}" y1="{HZ}" x2="{420 + i * 115}" y2="{H}"/>' for i in range(-11, 12))
    hlines = "".join(
        f'<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}"><animate attributeName="y1" values="{HZ};{H}" dur="3.5s" begin="-{k * 0.5}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".55 0 1 1"/>'
        f'<animate attributeName="y2" values="{HZ};{H}" dur="3.5s" begin="-{k * 0.5}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".55 0 1 1"/></line>'
        for k in range(7))

    # sun with stripes
    stripes = "".join(f'<rect x="300" y="{y}" width="240" height="{hgt}" fill="#000"/>'
                      for y, hgt in [(168, 2), (178, 3), (188, 4), (198, 5), (207, 6)])

    # typing roles
    roles = ["> AI ENGINEER", "> DATA SCIENTIST", "> RAG / LLM BUILDER", "> FULL-STACK DEVELOPER", "> BUG HUNTER (LVL MAX)"]
    cw, ty, dur = 13, 132, 3.6
    typing = []
    for i, r in enumerate(roles):
        n = len(r)
        x0 = 420 - n * cw / 2
        widths, xs = [], []
        type_n = n + 1
        for k in range(type_n):
            widths.append(k * cw); xs.append(x0 + k * cw)
        hold = 6
        widths += [n * cw] * hold; xs += [x0 + n * cw] * hold
        for k in range(n - 1, -1, -2):
            widths.append(k * cw); xs.append(x0 + k * cw)
        widths.append(0); xs.append(x0)
        m = len(widths)
        kt = ";".join(f"{j / m:.4f}" for j in range(m))
        begin = "0s;t%d.end" % (len(roles) - 1) if i == 0 else "t%d.end" % (i - 1)
        wv = ";".join(str(v) for v in widths)
        xv = ";".join(f"{v:.1f}" for v in xs)
        typing.append(f"""<clipPath id="c{i}"><rect x="{x0 - 2}" y="{ty - 20}" width="0" height="28">
<animate id="t{i}" attributeName="width" values="{wv}" keyTimes="{kt}" calcMode="discrete" dur="{dur}s" begin="{begin}"/></rect></clipPath>
<text x="{x0}" y="{ty}" textLength="{n * cw}" lengthAdjust="spacing" clip-path="url(#c{i})" fill="{CYAN}" font-size="21" font-weight="700" filter="url(#glow)">{r.replace(">", "&gt;")}</text>
<rect y="{ty - 18}" width="11" height="22" fill="{PINK}" opacity="0" x="{x0}">
<animate attributeName="x" values="{xv}" keyTimes="{kt}" calcMode="discrete" dur="{dur}s" begin="t{i}.begin"/>
<animate attributeName="opacity" values="1;0;1" dur=".5s" begin="t{i}.begin" end="t{i}.end" repeatCount="indefinite" calcMode="discrete"/></rect>""")

    # combat lane
    lane = 266
    ship = sprite(SHIP, {"X": CYAN, "o": PINK, "c": WHITE}, 60, lane - 14, 4)
    flame = f'<g class="flame"><rect x="44" y="{lane - 4}" width="12" height="4" fill="{YELLOW}"/><rect x="38" y="{lane - 3}" width="6" height="2" fill="#ff7a00"/></g>'
    bug_c = {"X": GREEN}
    bug = (f'<g class="bug"><g class="fa">{sprite(BUG_A, bug_c, 752, lane - 14, 4)}</g>'
           f'<g class="fb">{sprite(BUG_B, bug_c, 752, lane - 14, 4)}</g></g>')
    parts, pcss = [], []
    for j in range(10):
        ang = j * 36
        import math
        dx, dy = 34 * math.cos(math.radians(ang)), 34 * math.sin(math.radians(ang))
        col = [YELLOW, PINK, GREEN, WHITE][j % 4]
        parts.append(f'<rect class="p{j}" x="768" y="{lane - 2}" width="5" height="5" fill="{col}"/>')
        pcss.append(f"@keyframes p{j}{{0%,44%{{transform:translate(0,0);opacity:0}}46%{{opacity:1}}70%,100%{{transform:translate({dx:.0f}px,{dy:.0f}px);opacity:0}}}} .p{j}{{animation:p{j} 2.4s linear infinite}}")

    # odometer (bugs squashed counter) synced with hits
    odo = []
    for col, (cls, x) in enumerate([("h", 768), ("t", 782), ("u", 796)]):
        digits = "".join(f'<text x="{x}" y="{40 + d * 16}" text-anchor="middle">{d}</text>' for d in range(10))
        odo.append(f'<g clip-path="url(#odoc)"><g class="{cls}">{digits}</g></g>')

    css = f"""
text{{font-family:{FONT}}}
@keyframes drift{{to{{transform:translateX(-{W}px)}}}}
.s1{{animation:drift 60s linear infinite}} .s2{{animation:drift 25s linear infinite}}
@keyframes tw{{0%,100%{{opacity:.2}}50%{{opacity:1}}}} .tw{{animation:tw 3s ease-in-out infinite;fill:{CYAN}}}
@keyframes g1{{0%,88%,100%{{transform:translate(0,0)}}89%{{transform:translate(-5px,2px)}}91%{{transform:translate(4px,-2px)}}93%{{transform:translate(-2px,0)}}}}
@keyframes g2{{0%,88%,100%{{transform:translate(0,0)}}89%{{transform:translate(5px,-2px)}}91%{{transform:translate(-4px,2px)}}93%{{transform:translate(3px,1px)}}}}
.g1{{animation:g1 3.2s steps(1) infinite}} .g2{{animation:g2 3.2s steps(1) infinite}}
@keyframes sun{{0%,100%{{opacity:.95}}50%{{opacity:.75}}}} .sun{{animation:sun 4s ease-in-out infinite}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}} .shipg{{animation:bob 1.2s steps(2) infinite}}
@keyframes fl{{0%,100%{{opacity:1}}50%{{opacity:.3}}}} .flame{{animation:fl .15s steps(1) infinite}}
@keyframes laser{{0%{{transform:translateX(0);opacity:1}}45%{{transform:translateX(650px);opacity:1}}46%,100%{{transform:translateX(650px);opacity:0}}}}
.laser{{animation:laser 2.4s linear infinite}}
@keyframes bug{{0%,44%{{opacity:1;transform:translateX(0)}}45%,82%{{opacity:0;transform:translateX(30px)}}90%,100%{{opacity:1;transform:translateX(0)}}}}
.bug{{animation:bug 2.4s steps(1) infinite}}
@keyframes fa{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}} @keyframes fb{{0%,49%{{opacity:0}}50%,100%{{opacity:1}}}}
.fa{{animation:fa .4s steps(1) infinite}} .fb{{animation:fb .4s steps(1) infinite}}
@keyframes odo{{to{{transform:translateY(-160px)}}}}
.u{{animation:odo 24s steps(10) -1.32s infinite}} .t{{animation:odo 240s steps(10) -1.32s infinite}} .h{{animation:odo 2400s steps(10) -1.32s infinite}}
{BLINK_CSS} {CRT_CSS % (H + 60)}
{' '.join(pcss)}
"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>{css}</style>
<defs>{COMMON_DEFS}
<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".7" stop-color="#2a0b4a"/><stop offset="1" stop-color="#5a0f62"/></linearGradient>
<linearGradient id="sung" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{YELLOW}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="gnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a0533"/><stop offset="1" stop-color="{BG}"/></linearGradient>
<mask id="sunm"><rect width="{W}" height="{HZ}" fill="#fff"/>{stripes}</mask>
<clipPath id="odoc"><rect x="755" y="27" width="55" height="17"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<g fill="#fff" opacity=".5" class="s1">{stars(45, 1)}</g>
<g fill="#fff" opacity=".9" class="s2">{stars(18, 2)}</g>
{twinkles}
<circle class="sun" cx="420" cy="{HZ}" r="70" fill="url(#sung)" mask="url(#sunm)" filter="url(#glow)"/>
<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#gnd)"/>
<g stroke="{PINK}" stroke-width="1.2" opacity=".55">{vlines}{hlines}</g>
<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}" stroke="{PINK}" stroke-width="2" filter="url(#glow)"/>

<g font-size="12" letter-spacing="2">
<text x="30" y="24" fill="{PINK}">1UP</text><text x="30" y="40" fill="#fff">IHEB</text>
<text x="420" y="24" fill="{PINK}" text-anchor="middle">HI-SCORE</text><text x="420" y="40" fill="#fff" text-anchor="middle">INFINITY</text>
<text x="810" y="24" fill="{PINK}" text-anchor="end">BUGS SQUASHED</text>
<g fill="{GREEN}" font-size="14">{''.join(odo)}</g>
</g>

<g font-size="52" font-weight="700" text-anchor="middle" letter-spacing="6">
<text class="g1" x="420" y="94" fill="{CYAN}" opacity=".85">IHEB LAMOUCHI</text>
<text class="g2" x="420" y="94" fill="{PINK}" opacity=".85">IHEB LAMOUCHI</text>
<text x="420" y="94" fill="#fff" stroke="{BG}" stroke-width="1">IHEB LAMOUCHI</text>
</g>
{''.join(typing)}

<g class="shipg">{flame}{ship}</g>
<rect class="laser" x="98" y="{lane - 2}" width="22" height="4" fill="{YELLOW}" filter="url(#glow)"/>
{bug}
{''.join(parts)}

<text class="blink" x="420" y="306" text-anchor="middle" font-size="13" letter-spacing="3" fill="{YELLOW}">- PRESS START -</text>
{crt_overlay(W, H)}
</g></svg>"""


# ---------------------------------------------------------------- PLAYER CARD
def player_card():
    W, H = 840, 300
    av_colors = {"H": "#2b1055", "S": "#f2c29b", "G": CYAN, "E": "#0b0420", "M": "#b5536b", "P": PINK, "m": PINK, "K": PURPLE, "W": WHITE}
    avatar = sprite(AVATAR, av_colors, 52, 52, 10)
    eyelids = (f'<g class="lid"><rect x="{52 + 4 * 10}" y="{52 + 6 * 10}" width="20" height="10" fill="{CYAN}"/>'
               f'<rect x="{52 + 10 * 10}" y="{52 + 6 * 10}" width="20" height="10" fill="{CYAN}"/></g>')
    rnd = random.Random(3)
    bits = "".join(
        f'<text class="bit" x="{rnd.randint(40, 210)}" y="250" style="animation-delay:-{rnd.random() * 4:.2f}s" fill="{rnd.choice([CYAN, PINK, GREEN])}">{rnd.choice(["0", "1", "&lt;/&gt;", "{}", "AI", "λ"])}</text>'
        for _ in range(9))

    stats = [("AI / LLM", 95, CYAN), ("DATA / ML", 90, PINK), ("BACKEND", 88, YELLOW), ("FRONTEND", 80, GREEN), ("DEVOPS", 78, PURPLE)]
    rows = []
    seg_w, gap, nseg, bx = 14, 3, 20, 400
    for i, (name, val, col) in enumerate(stats):
        y = 150 + i * 26
        lit = round(val / 100 * nseg)
        segs = []
        for s in range(nseg):
            x = bx + s * (seg_w + gap)
            if s < lit:
                segs.append(f'<rect x="{x}" y="{y - 12}" width="{seg_w}" height="14" fill="{col}" opacity="0">'
                            f'<animate attributeName="opacity" to="1" begin="{0.4 + i * 0.25 + s * 0.04:.2f}s" dur=".01s" fill="freeze"/></rect>')
            else:
                segs.append(f'<rect x="{x}" y="{y - 12}" width="{seg_w}" height="14" fill="#2a1a4a"/>')
        rows.append(f'<text x="268" y="{y}" font-size="13" fill="#cbb8ff" letter-spacing="1">{name}</text>' + "".join(segs)
                    + f'<text x="{bx + nseg * (seg_w + gap) + 8}" y="{y}" font-size="13" fill="{col}" opacity="0">{val}'
                    f'<animate attributeName="opacity" to="1" begin="{0.4 + i * 0.25 + lit * 0.04:.2f}s" dur=".01s" fill="freeze"/></text>')

    css = f"""
text{{font-family:{FONT}}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}} .av{{animation:bob 1.4s steps(2) infinite}}
@keyframes lid{{0%,92%,100%{{opacity:0}}93%,97%{{opacity:1}}}} .lid{{animation:lid 4s steps(1) infinite}}
@keyframes bit{{0%{{transform:translateY(0);opacity:0}}15%{{opacity:1}}100%{{transform:translateY(-220px);opacity:0}}}} .bit{{animation:bit 4s linear infinite;font-size:12px}}
@keyframes sh{{from{{transform:translateX(-300px)}}to{{transform:translateX(900px)}}}} .shine{{animation:sh 3.5s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}} .dot{{animation:pulse 1.2s ease-in-out infinite}}
{BLINK_CSS} {CRT_CSS % (H + 60)}
"""
    corner = lambda x, y, sx, sy: f'<path d="M{x} {y + sy * 18}V{y}H{x + sx * 18}" fill="none" stroke="{YELLOW}" stroke-width="4"/>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>{css}</style>
<defs>{COMMON_DEFS}<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="plat"><stop offset="0" stop-color="{CYAN}" stop-opacity=".7"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient></defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{PANEL}"/>
<rect x="24" y="24" width="214" height="252" rx="6" fill="{BG}" stroke="#3a2370" stroke-width="2"/>
{corner(24, 24, 1, 1)}{corner(238, 24, -1, 1)}{corner(24, 276, 1, -1)}{corner(238, 276, -1, -1)}
<ellipse cx="131" cy="248" rx="80" ry="12" fill="url(#plat)"/>
{bits}
<g class="av">{avatar}{eyelids}</g>
<text x="131" y="44" text-anchor="middle" font-size="11" fill="{YELLOW}" letter-spacing="2">PLAYER 1</text>

<text x="268" y="50" font-size="12" fill="{PINK}" letter-spacing="3">// CHARACTER SELECTED</text>
<text x="268" y="84" font-size="30" font-weight="700" fill="#fff" letter-spacing="2">IHEB LAMOUCHI</text>
<text x="268" y="108" font-size="13" fill="{CYAN}" letter-spacing="1">CLASS: AI ENGINEER    GUILD: DATA SCIENCE &amp; AI</text>
<circle class="dot" cx="273" cy="124" r="5" fill="{GREEN}"/>
<text x="286" y="128" font-size="12" fill="#cbb8ff">ONLINE - training models &amp; squashing bugs<tspan class="blink" fill="{GREEN}">_</tspan></text>
{''.join(rows)}
<rect class="shine" x="0" y="0" width="160" height="{H}" fill="url(#sg)" transform="skewX(-20)"/>
{crt_overlay(W, H)}
</g></svg>"""


# ---------------------------------------------------------------- SECTION HEADERS
def header(title, sub, col):
    W, H = 840, 68
    tw = len(title) * 17
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>
text{{font-family:{FONT}}}
@keyframes ar{{0%,100%{{transform:translateX(0);opacity:1}}50%{{transform:translateX(8px);opacity:.4}}}}
@keyframes al{{0%,100%{{transform:translateX(0);opacity:1}}50%{{transform:translateX(-8px);opacity:.4}}}}
.ar{{animation:ar .9s steps(3) infinite}} .al{{animation:al .9s steps(3) infinite}}
@keyframes run{{from{{transform:translateX(0)}}to{{transform:translateX({W}px)}}}} .run{{animation:run 2.8s linear infinite}}
</style>
<defs><filter id="glow" x="-20%" y="-80%" width="140%" height="260%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset=".5" stop-color="{col}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>
<line x1="0" x2="{W}" y1="45" y2="45" stroke="url(#ln)" stroke-width="2" opacity=".6"/>
<rect class="run" x="-60" y="43" width="60" height="4" fill="{col}" filter="url(#glow)"/>
<g fill="{col}" font-size="22" font-weight="700">
<text class="ar" x="{420 - tw / 2 - 52}" y="33">&gt;&gt;</text>
<text class="al" x="{420 + tw / 2 + 22}" y="33">&lt;&lt;</text>
</g>
<text x="420" y="33" text-anchor="middle" font-size="26" font-weight="700" fill="#fff" letter-spacing="5" filter="url(#glow)">{title}</text>
<text x="420" y="61" text-anchor="middle" font-size="11" fill="{col}" letter-spacing="2" opacity=".9">{sub}</text>
</svg>"""


# ---------------------------------------------------------------- QUEST CARDS
RARITY = {"LEGENDARY": YELLOW, "EPIC": PINK, "RARE": CYAN}


def quest(title, rarity, icon, lines, loot, lvl):
    W, H = 410, 180
    col = RARITY[rarity]
    ic = sprite(ICONS[icon], {"X": col, "o": WHITE}, 330, 26, 7)
    desc = "".join(f'<text x="22" y="{86 + i * 18}" font-size="12" fill="#cbb8ff">{l}</text>' for i, l in enumerate(lines))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>
text{{font-family:{FONT}}}
@keyframes dash{{to{{stroke-dashoffset:-48}}}} .border{{animation:dash 1.6s linear infinite}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}} .ic{{animation:bob 1.2s steps(2) infinite}}
{BLINK_CSS}
@keyframes sh{{0%,60%{{transform:translateX(-200px)}}100%{{transform:translateX(600px)}}}} .shine{{animation:sh 4s ease-in-out infinite}}
</style>
<defs><clipPath id="cc"><rect width="{W}" height="{H}" rx="10"/></clipPath>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1a0b38"/><stop offset="1" stop-color="{BG}"/></linearGradient>
<linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".3"/></pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g clip-path="url(#cc)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect x="14" y="14" width="{len(rarity) * 8 + 84}" height="20" rx="3" fill="{col}"/>
<text x="22" y="28" font-size="11" font-weight="700" fill="{BG}" letter-spacing="1">* {rarity} QUEST</text>
<text x="22" y="62" font-size="21" font-weight="700" fill="#fff" letter-spacing="1">{title}</text>
{desc}
<text x="22" y="160" font-size="11" fill="{col}">LOOT: <tspan fill="#fff">{loot}</tspan></text>
<text x="388" y="160" font-size="11" fill="{YELLOW}" text-anchor="end" class="blink">START &gt;</text>
<text x="388" y="102" font-size="10" fill="{col}" text-anchor="end">LV.{lvl}</text>
<g class="ic" filter="url(#glow)">{ic}</g>
<rect class="shine" x="0" y="0" width="100" height="{H}" fill="url(#sg)" transform="skewX(-20)"/>
<rect width="{W}" height="{H}" fill="url(#scan)"/>
<rect class="border" x="2" y="2" width="{W - 4}" height="{H - 4}" rx="10" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="36 12"/>
</g></svg>"""


QUESTS = [
    ("crisisvision", "CRISISVISION", "LEGENDARY", "eye", ["Multimodal crisis analysis from", "text + images, CLIP consistency", "checks, MLflow experiment tracking."], "Python  CLIP  MLflow", 60),
    ("homedoc", "HOMEDOC", "EPIC", "heart", ["Intelligent medical diagnosis", "system: symptom analysis through", "a REST API + web frontend."], "TypeScript  REST API", 45),
    ("techcare", "TECHCARE PRO", "EPIC", "monitor", ["PC repair management system", "with built-in AI support for", "diagnosing customer issues."], "JavaScript  AI", 40),
    ("sportwear", "SPORTWEAR", "RARE", "bolt", ["Full e-commerce platform for", "athletic gear: React frontend", "powered by a Django REST API."], "React  Django", 35),
    ("socialfeed", "SOCIAL FEED", "RARE", "bubble", ["Social platform: Django GraphQL", "API with JWT auth + push notifs,", "and a cross-platform Flutter app."], "Django  GraphQL  Flutter", 35),
    ("esport", "ESPORT ARENA", "RARE", "pad", ["Esport tournament arena website,", "split into a frontend and a", "JavaScript backend."], "HTML  JavaScript", 20),
]


# ---------------------------------------------------------------- ACHIEVEMENTS
def achievements():
    W, H = 840, 190
    items = [("PCAP", "Python Institute", "Certified Associate", YELLOW),
             ("DATA SCIENCE", "Cisco", "Essentials", CYAN),
             ("VERSION CTRL", "Meta", "Git mastery", PINK),
             ("IELTS", "English", "Proficiency", GREEN)]
    cards, css = [], []
    for i, (t, a, b, col) in enumerate(items):
        x = 18 + i * 204
        tro = sprite(ICONS["trophy"], {"X": col}, x + 72, 40, 7)
        cards.append(f"""<g class="a{i}"><rect x="{x}" y="24" width="192" height="148" rx="8" fill="{BG}" stroke="{col}" stroke-width="2"/>
<g filter="url(#glow)">{tro}</g>
<text x="{x + 96}" y="122" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">{t}</text>
<text x="{x + 96}" y="142" text-anchor="middle" font-size="11" fill="{col}">{a}</text>
<text x="{x + 96}" y="158" text-anchor="middle" font-size="11" fill="#cbb8ff">{b}</text></g>""")
        css.append(f"@keyframes a{i}{{0%{{opacity:0;transform:translateY(30px) scale(.6)}}70%{{opacity:1;transform:translateY(-6px) scale(1.06)}}100%{{opacity:1;transform:none}}}}"
                   f".a{i}{{transform-box:fill-box;transform-origin:center;animation:a{i} .6s ease-out {0.3 + i * 0.5:.1f}s both}}")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{FONT}}} {' '.join(css)}
@keyframes sh{{0%,50%{{transform:translateX(-200px)}}100%{{transform:translateX(1000px)}}}} .shine{{animation:sh 5s ease-in-out 2.5s infinite}}
{BLINK_CSS} {CRT_CSS % (H + 60)}</style>
<defs>{COMMON_DEFS}<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="{PANEL}"/>
<text class="blink" x="420" y="16" text-anchor="middle" font-size="10" fill="{YELLOW}" letter-spacing="3">4 / 4 ACHIEVEMENTS UNLOCKED</text>
{''.join(cards)}
<rect class="shine" x="0" y="0" width="140" height="{H}" fill="url(#sg)" transform="skewX(-20)"/>
{crt_overlay(W, H)}</g></svg>"""


# ---------------------------------------------------------------- GAME OVER / FOOTER
def footer():
    W, H = 840, 200
    digits = "".join(
        f'<text x="560" y="118" font-size="40" font-weight="700" fill="{PINK}" opacity="0" filter="url(#glow)">{d}'
        f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;.0001;.1" calcMode="discrete" dur="10s" begin="{9 - d}s" repeatCount="indefinite"/></text>'
        for d in range(9, -1, -1))
    coin = sprite(ICONS["coin"], {"X": "#c79a00", "o": YELLOW}, -16, -16, 4)
    rnd = random.Random(11)
    sparks = "".join(f'<rect x="{rnd.randint(10, W - 10)}" y="{rnd.randint(10, H - 10)}" width="3" height="3" fill="{rnd.choice([CYAN, PINK, YELLOW])}" class="tw" style="animation-delay:-{rnd.random() * 3:.2f}s"/>' for _ in range(26))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{FONT}}}
@keyframes spin{{0%,100%{{transform:scaleX(1)}}50%{{transform:scaleX(.1)}}}} .coin{{animation:spin 1s steps(4) infinite}}
@keyframes drop{{0%{{transform:translate(700px,40px)}}60%{{transform:translate(700px,120px)}}61%,100%{{transform:translate(700px,120px);opacity:0}}}}
.drop{{animation:drop 2s ease-in infinite}}
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:1}}}} .tw{{animation:tw 2.6s ease-in-out infinite}}
@keyframes g1{{0%,90%,100%{{transform:translate(0,0)}}92%{{transform:translate(-4px,1px)}}94%{{transform:translate(3px,-1px)}}}} .g1{{animation:g1 2.5s steps(1) infinite}}
{BLINK_CSS} {CRT_CSS % (H + 60)}</style>
<defs>{COMMON_DEFS}<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>
<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="{BG}"/>
{sparks}
<text class="g1" x="420" y="64" text-anchor="middle" font-size="34" font-weight="700" fill="{CYAN}" opacity=".8" letter-spacing="4">THANKS FOR PLAYING</text>
<text x="420" y="64" text-anchor="middle" font-size="34" font-weight="700" fill="#fff" letter-spacing="4" filter="url(#glow)">THANKS FOR PLAYING</text>
<text x="300" y="118" font-size="28" font-weight="700" fill="{YELLOW}" letter-spacing="3">CONTINUE?</text>
{digits}
<text class="blink" x="420" y="168" text-anchor="middle" font-size="13" fill="#cbb8ff" letter-spacing="2">INSERT COIN: CONNECT WITH ME BELOW</text>
<g class="drop"><g class="coin">{coin}</g></g>
<g transform="translate(140,110)"><g class="coin">{coin}</g></g>
{crt_overlay(W, H)}</g></svg>"""


if __name__ == "__main__":
    save("hero.svg", hero())
    save("player.svg", player_card())
    save("achievements.svg", achievements())
    save("gameover.svg", footer())
    for key, title, rarity, icon, lines, loot, lvl in QUESTS:
        save(f"quest-{key}.svg", quest(title, rarity, icon, lines, loot, lvl))
    for key, title, sub, col in [
        ("player", "SELECT PLAYER", "// who is behind the keyboard", CYAN),
        ("inventory", "INVENTORY", "// weapons &amp; spells currently equipped", PINK),
        ("quests", "QUEST LOG", "// click a quest to enter the dungeon", YELLOW),
        ("achievements", "ACHIEVEMENTS", "// certified loot", GREEN),
        ("stats", "BATTLE STATS", "// live from the arena", PURPLE),
        ("connect", "MULTIPLAYER", "// press a button to join the party", CYAN),
    ]:
        save(f"h-{key}.svg", header(title, sub, col))
