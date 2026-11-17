"""Generates the animated data / ML themed SVGs used by the profile README.

Run:  python scripts/generate_assets.py   (rewrites ./assets)
Everything is pure SVG + CSS/SMIL animation, so it renders inside GitHub's <img> sandbox.
"""
import glob
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)
for old in glob.glob(os.path.join(OUT, "*.svg")):
    os.remove(old)

FONT = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
BG, PANEL, DIM, MUTED = "#060a18", "#0b1226", "#1b2a4a", "#7f8db3"
CYAN, TEAL, VIOLET, PINK, AMBER, WHITE = "#00e5ff", "#00ffa3", "#8b5cf6", "#ff3ea5", "#ffb800", "#ffffff"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name)


DEFS = f"""
<radialGradient id="bgr" cx=".5" cy=".35" r=".8"><stop offset="0" stop-color="#0e1838"/><stop offset="1" stop-color="{BG}"/></radialGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{DIM}"/></pattern>
<linearGradient id="neon" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="9s" repeatCount="indefinite"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
"""
BLINK = "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}} .blink{animation:blink 1s steps(1) infinite}"
PULSE = "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}} .pulse{animation:pulse 1.4s ease-in-out infinite}"


def frame(w, h, body, css, extra_defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<style>text{{font-family:{FONT}}} {BLINK} {PULSE} {css}</style>
<defs>{DEFS}{extra_defs}<clipPath id="card"><rect width="{w}" height="{h}" rx="14"/></clipPath></defs>
<g clip-path="url(#card)"><rect width="{w}" height="{h}" fill="url(#bgr)"/><rect width="{w}" height="{h}" fill="url(#dots)" opacity=".7"/>
{body}
<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="14" fill="none" stroke="url(#neon)" stroke-width="2.5"/></g></svg>"""


def window_bar(w, title, right=""):
    return (f'<rect width="{w}" height="34" fill="#080e20"/><line x1="0" x2="{w}" y1="34" y2="34" stroke="{DIM}"/>'
            f'<circle cx="20" cy="17" r="5" fill="#ff5f57"/><circle cx="36" cy="17" r="5" fill="#febc2e"/><circle cx="52" cy="17" r="5" fill="#28c840"/>'
            f'<text x="70" y="21" font-size="12" fill="{MUTED}">{esc(title)}</text>{right}')


def typing_clip(cid, x, y, n, cw, begin, dur, h=20, freeze=True):
    """clipPath revealing n chars one by one."""
    vals = ";".join(str(round(k * cw, 1)) for k in range(n + 1))
    kt = ";".join(f"{k / (n + 1):.4f}" for k in range(n + 1))
    fz = ' fill="freeze"' if freeze else ""
    return (f'<clipPath id="{cid}"><rect x="{x - 2}" y="{y - h + 5}" width="0" height="{h}">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{dur}s" begin="{begin}"{fz}/></rect></clipPath>')


# ================================================================= HERO: live data pipeline
def hero():
    W, H = 840, 370
    rnd = random.Random(42)
    body = []

    # binary rain (data streams)
    for c in range(16):
        x = rnd.randint(10, W - 10)
        lines = "".join(f'<text x="{x}" y="{i * 14}">{rnd.choice("01")}</text>' for i in range(14))
        d = rnd.uniform(7, 14)
        body.append(f'<g class="rain" style="animation-duration:{d:.1f}s;animation-delay:-{rnd.uniform(0, d):.1f}s" '
                    f'fill="{rnd.choice([CYAN, VIOLET, TEAL])}" font-size="11">{lines}</g>')

    # window bar + live record counter (odometer, ~10 records/s)
    T0 = 128437.2
    odo_cols = []
    for i in range(7):
        period = 10 ** i  # full 0-9 cycle duration in seconds
        x = 806 - i * 8.6
        digits = "".join(f'<text x="{x:.1f}" y="{22 + d * 16}" text-anchor="middle">{d}</text>' for d in range(10))
        delay = (T0 % period)
        odo_cols.append(f'<g style="animation:odo {period}s steps(10) -{delay:.2f}s infinite">{digits}</g>')
    right = (f'<circle class="pulse" cx="560" cy="17" r="4" fill="{TEAL}"/><text x="570" y="21" font-size="11" fill="{TEAL}">STREAMING</text>'
             f'<text x="680" y="21" font-size="11" fill="{MUTED}">RECORDS</text>'
             f'<g clip-path="url(#odoc)" fill="{CYAN}" font-size="12">{"".join(odo_cols)}</g>')
    body.append(window_bar(W, "iheb@data-lab:~/pipeline$ ./run --stream --train", right))

    # name + typing roles
    body.append(f'<text x="420" y="96" text-anchor="middle" font-size="48" font-weight="800" letter-spacing="5" fill="{CYAN}" opacity=".35" filter="url(#glow)">IHEB LAMOUCHI</text>'
                f'<text x="420" y="96" text-anchor="middle" font-size="48" font-weight="800" letter-spacing="5" fill="url(#ng)">IHEB LAMOUCHI</text>'
                f'<rect class="sweep" x="0" y="50" width="70" height="56" fill="url(#sw)"/>')
    roles = ["$ AI SOFTWARE ENGINEER", "$ DATA SCIENCE & AI ENGINEERING", "$ RAG / LLM SYSTEMS BUILDER", "$ ML PIPELINES -> PRODUCTION"]
    cw, ty, dur = 12, 134, 3.8
    for i, r in enumerate(roles):
        n = len(r)
        x0 = 420 - n * cw / 2
        ws, xs = [], []
        for k in range(n + 1):
            ws.append(k * cw); xs.append(x0 + k * cw)
        ws += [n * cw] * 8; xs += [x0 + n * cw] * 8
        for k in range(n - 2, -1, -3):
            ws.append(k * cw); xs.append(x0 + k * cw)
        ws.append(0); xs.append(x0)
        m = len(ws)
        kt = ";".join(f"{j / m:.4f}" for j in range(m))
        begin = f"0s;t{len(roles) - 1}.end" if i == 0 else f"t{i - 1}.end"
        body.append(f"""<clipPath id="c{i}"><rect x="{x0 - 2}" y="{ty - 18}" width="0" height="26">
<animate id="t{i}" attributeName="width" values="{';'.join(map(str, ws))}" keyTimes="{kt}" calcMode="discrete" dur="{dur}s" begin="{begin}"/></rect></clipPath>
<text x="{x0}" y="{ty}" textLength="{n * cw}" lengthAdjust="spacing" clip-path="url(#c{i})" font-size="19" font-weight="700" fill="{TEAL}">{esc(r)}</text>
<rect y="{ty - 16}" width="10" height="20" fill="{PINK}" opacity="0" x="{x0}">
<animate attributeName="x" values="{';'.join(f'{v:.1f}' for v in xs)}" keyTimes="{kt}" calcMode="discrete" dur="{dur}s" begin="t{i}.begin"/>
<animate attributeName="opacity" values="1;0;1" dur=".6s" begin="t{i}.begin" end="t{i}.end" repeatCount="indefinite" calcMode="discrete"/></rect>""")

    # ---------- pipeline diagram
    cy = 262
    lab = lambda x, y, t, c=MUTED, a="middle": f'<text x="{x}" y="{y}" font-size="10" fill="{c}" text-anchor="{a}" letter-spacing="1">{t}</text>'
    srcs = [(200, CYAN, "POSTGRES"), (262, AMBER, "REST API"), (324, PINK, "DOCS / PDF")]
    # source icons
    body.append(f'<g stroke="{CYAN}" stroke-width="2" fill="{PANEL}"><path d="M48 190 v22 a22 6 0 0 0 44 0 v-22"/><ellipse cx="70" cy="190" rx="22" ry="6"/>'
                f'<path d="M48 201 a22 6 0 0 0 44 0" fill="none" opacity=".6"/></g>')
    body.append(f'<rect x="48" y="249" width="44" height="26" rx="5" fill="{PANEL}" stroke="{AMBER}" stroke-width="2"/>'
                f'<text x="70" y="267" text-anchor="middle" font-size="13" font-weight="700" fill="{AMBER}">{{ }}</text>')
    body.append(f'<g fill="{PANEL}" stroke="{PINK}" stroke-width="2"><rect x="56" y="308" width="30" height="34" rx="2"/><rect x="50" y="313" width="30" height="34" rx="2"/></g>'
                f'<g stroke="{PINK}" stroke-width="1.5" opacity=".8"><line x1="55" x2="74" y1="322" y2="322"/><line x1="55" x2="74" y1="328" y2="328"/><line x1="55" x2="68" y1="334" y2="334"/></g>')
    body.append(lab(70, 226, "POSTGRES") + lab(70, 290, "REST API") + lab(105, 360, "DOCS / PDF", a="start"))

    paths, packets = [], []

    def flow(pid, d, col, n, dur, size=5):
        paths.append(f'<path id="{pid}" d="{d}" fill="none" stroke="{col}" stroke-width="1.4" stroke-opacity=".35" stroke-dasharray="3 5" class="flow"/>')
        for k in range(n):
            packets.append(f'<rect x="{-size / 2}" y="{-size / 2}" width="{size}" height="{size}" fill="{col}" filter="url(#glow)">'
                           f'<animateMotion dur="{dur}s" begin="-{k * dur / n:.2f}s" repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></rect>')

    flow("f0", f"M94 200 C150 200 160 {cy} 205 {cy}", CYAN, 3, 2.4)
    flow("f1", f"M94 {cy} L205 {cy}", AMBER, 3, 2.1)
    flow("f2", f"M94 326 C150 326 160 {cy} 205 {cy}", PINK, 3, 2.6)
    flow("f3", f"M255 {cy} L318 {cy}", TEAL, 3, 1.3)

    # ETL gear
    teeth = "".join(f'<rect x="-4" y="-26" width="8" height="9" rx="1" transform="rotate({a})"/>' for a in range(0, 360, 45))
    body.append(f'<g transform="translate(230 {cy})"><g fill="{TEAL}">{teeth}<circle r="20"/>'
                f'<animateTransform attributeName="transform" type="rotate" values="0;360" dur="6s" repeatCount="indefinite"/></g>'
                f'<circle r="13" fill="{BG}"/><text y="4" text-anchor="middle" font-size="9" font-weight="700" fill="{TEAL}">ETL</text></g>')
    body.append(lab(230, 306, "TRANSFORM", TEAL))

    # vector DB
    body.append(f'<g stroke="{VIOLET}" stroke-width="2" fill="{PANEL}"><path d="M320 244 v36 a26 7 0 0 0 52 0 v-36"/><ellipse cx="346" cy="244" rx="26" ry="7"/></g>'
                f'<g stroke="{VIOLET}" stroke-width="1.4" fill="none" opacity=".6"><path d="M320 256 a26 7 0 0 0 52 0"/><path d="M320 268 a26 7 0 0 0 52 0"/></g>'
                f'<rect class="fillv" x="322" y="246" width="48" height="34" fill="{VIOLET}" opacity=".25"/>')
    body.append(lab(346, 306, "VECTOR DB", VIOLET))

    # neural network
    layers_x = [432, 502, 572, 640]
    counts = [4, 5, 5, 2]
    nodes = []
    for li, (lx, cnt) in enumerate(zip(layers_x, counts)):
        span = 30
        ys = [cy + (j - (cnt - 1) / 2) * span for j in range(cnt)]
        nodes.append([(lx, y) for y in ys])
    for j, (nx, ny) in enumerate(nodes[0]):
        flow(f"v{j}", f"M372 {cy} C400 {cy} 405 {ny} {nx - 8} {ny}", VIOLET, 1, 1.3, 4)
    edges = []
    for li in range(len(nodes) - 1):
        ln = "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for a in nodes[li] for b in nodes[li + 1])
        edges.append(f'<g stroke="{CYAN}" stroke-width="1" class="e" style="animation-delay:{0.15 + li * 0.45:.2f}s">{ln}</g>')
        edges.append(f'<g stroke="{DIM}" stroke-width="1" opacity=".9">{ln}</g>')
    body.append("".join(edges[1::2]) + "".join(edges[0::2]))
    for li, layer in enumerate(nodes):
        col = [CYAN, VIOLET, VIOLET, PINK][li]
        for (x, y) in layer:
            body.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{PANEL}" stroke="{col}" stroke-width="2"/>'
                        f'<circle cx="{x}" cy="{y}" r="5" fill="{col}" class="n" style="animation-delay:{li * 0.45:.2f}s"/>')
    body.append(lab(536, 360, "NEURAL NET  ::  FORWARD PASS", CYAN))

    # output
    for (x, y) in nodes[-1]:
        flow(f"o{y}", f"M{x + 8} {y} C680 {y} 680 {cy} 704 {cy}", PINK, 1, 1.0, 4)
    body.append(f'<rect x="704" y="{cy - 26}" width="112" height="52" rx="8" fill="{PANEL}" stroke="{PINK}" stroke-width="2"/>'
                f'<text x="760" y="{cy - 6}" text-anchor="middle" font-size="11" fill="{MUTED}" letter-spacing="1">INSIGHT</text>'
                f'<g class="out"><text x="760" y="{cy + 14}" text-anchor="middle" font-size="14" font-weight="700" fill="{TEAL}">✓ shipped</text></g>')

    body.insert(len(body), "".join(paths) + "".join(packets))

    css = f"""
@keyframes rain{{from{{transform:translateY(-200px)}}to{{transform:translateY({H}px)}}}} .rain{{animation:rain linear infinite;opacity:.13}}
@keyframes odo{{to{{transform:translateY(-160px)}}}}
@keyframes sweep{{0%,55%{{transform:translateX(-80px)}}100%{{transform:translateX({W + 80}px)}}}} .sweep{{animation:sweep 5s ease-in-out infinite}}
@keyframes flow{{to{{stroke-dashoffset:-16}}}} .flow{{animation:flow .8s linear infinite}}
@keyframes n{{0%{{opacity:.15}}10%{{opacity:1}}35%,100%{{opacity:.15}}}} .n{{animation:n 2.7s ease-out infinite}}
@keyframes e{{0%{{opacity:0}}10%{{opacity:.75}}30%,100%{{opacity:0}}}} .e{{animation:e 2.7s ease-out infinite}}
@keyframes out{{0%,55%{{opacity:.2}}65%,92%{{opacity:1}}100%{{opacity:.2}}}} .out{{animation:out 2.7s infinite}}
@keyframes fillv{{0%,100%{{transform:translateY(20px);opacity:.15}}50%{{transform:translateY(0);opacity:.4}}}} .fillv{{animation:fillv 3s ease-in-out infinite}}
"""
    extra = f"""<linearGradient id="ng" x1="0" x2="1"><stop offset="0" stop-color="{WHITE}"/><stop offset=".5" stop-color="#bfefff"/><stop offset="1" stop-color="{WHITE}"/></linearGradient>
<linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="odoc"><rect x="740" y="9" width="75" height="17"/></clipPath>"""
    return frame(W, H, "\n".join(body), css, extra)


# ================================================================= PROFILE: knowledge graph + model card
def profile():
    W, H = 840, 380
    cx, cy = 205, 208
    rnd = random.Random(5)
    clusters = [("RAG", CYAN, ["Embeddings", "Reranking"]),
                ("LLM", VIOLET, ["Ollama", "Qwen"]),
                ("ML", PINK, ["TensorFlow", "MLflow"]),
                ("DATA", AMBER, ["PostgreSQL", "MongoDB"]),
                ("BACKEND", TEAL, ["FastAPI", "Spring"]),
                ("DEVOPS", "#4da3ff", ["Docker", "Jenkins"])]

    def drift(x, y, amp):
        d = rnd.uniform(5, 9)
        a1, a2 = rnd.uniform(-amp, amp), rnd.uniform(-amp, amp)
        xs = f"{x:.1f};{x + a1:.1f};{x:.1f};{x - a1:.1f};{x:.1f}"
        ys = f"{y:.1f};{y + a2:.1f};{y:.1f};{y - a2:.1f};{y:.1f}"
        return xs, ys, d

    def anim(attr, vals, d):
        return f'<animate attributeName="{attr}" values="{vals}" dur="{d:.1f}s" repeatCount="indefinite"/>'

    def shift(vals, off):
        return ";".join(f"{float(v) + off:.1f}" for v in vals.split(";"))

    edges, nodes, labels, pulses = [], [], [], []
    for k, (name, col, leaves) in enumerate(clusters):
        ang = math.radians(-90 + k * 60)
        nx, ny = cx + 92 * math.cos(ang), cy + 92 * math.sin(ang)
        xs, ys, d = drift(nx, ny, 6)
        edges.append(f'<line x1="{cx}" y1="{cy}" stroke="{col}" stroke-opacity=".55" stroke-width="1.6">{anim("x2", xs, d)}{anim("y2", ys, d)}</line>')
        nodes.append(f'<circle r="21" fill="{PANEL}" stroke="{col}" stroke-width="2" filter="url(#glow)">{anim("cx", xs, d)}{anim("cy", ys, d)}</circle>')
        labels.append(f'<text text-anchor="middle" font-size="{9 if len(name) > 4 else 10}" font-weight="700" fill="{col}">{name}{anim("x", xs, d)}{anim("y", shift(ys, 3.5), d)}</text>')
        pulses.append(f'<circle r="3" fill="{col}" filter="url(#glow)"><animate attributeName="cx" values="{cx};{nx:.1f}" dur="1.8s" begin="{k * 0.3:.1f}s" repeatCount="indefinite"/>'
                      f'<animate attributeName="cy" values="{cy};{ny:.1f}" dur="1.8s" begin="{k * 0.3:.1f}s" repeatCount="indefinite"/>'
                      f'<animate attributeName="opacity" values="1;1;0" dur="1.8s" begin="{k * 0.3:.1f}s" repeatCount="indefinite"/></circle>')
        for s, leaf in zip((-17, 17), leaves):
            la = ang + math.radians(s)
            lx, ly = cx + 146 * math.cos(la), cy + 146 * math.sin(la)
            lxs, lys, ld = drift(lx, ly, 5)
            edges.append(f'<line stroke="{col}" stroke-opacity=".3" stroke-width="1" stroke-dasharray="3 3">{anim("x1", xs, d)}{anim("y1", ys, d)}{anim("x2", lxs, ld)}{anim("y2", lys, ld)}</line>')
            nodes.append(f'<circle r="5" fill="{col}" class="pulse" style="animation-delay:-{rnd.uniform(0, 1.4):.1f}s">{anim("cx", lxs, ld)}{anim("cy", lys, ld)}</circle>')
            below = ly > cy + 20
            above = ly < cy - 20
            off = 17 if below else (-10 if above else -10)
            labels.append(f'<text text-anchor="middle" font-size="9" fill="#c9d4f2">{leaf}{anim("x", lxs, ld)}{anim("y", shift(lys, off), ld)}</text>')

    center = (f'<circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="{CYAN}" stroke-width="2"><animate attributeName="r" values="30;62" dur="2.4s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>'
              f'<circle cx="{cx}" cy="{cy}" r="30" fill="url(#cg)" filter="url(#glow)"/>'
              f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="14" font-weight="800" fill="{BG}">IHEB</text>')
    graph = (f'<text x="24" y="28" font-size="11" fill="{MUTED}">knowledge_graph.render(node="iheb")</text>'
             + "".join(edges) + "".join(pulses) + "".join(nodes) + center + "".join(labels))

    # model card JSON
    X0 = 440
    card = [f'<rect x="{X0 - 14}" y="44" width="{W - X0 - 4}" height="{H - 62}" rx="10" fill="#070d1f" stroke="{DIM}"/>',
            f'<text x="{X0}" y="66" font-size="11" fill="{MUTED}">model_card.json</text>',
            f'<line x1="{X0 - 14}" x2="{W - 18}" y1="76" y2="76" stroke="{DIM}"/>']
    K, S, P = CYAN, AMBER, "#5b6b95"
    lines = [
        [("{", P)],
        [('  "name": ', K), ('"Iheb Lamouchi"', S), (",", P)],
        [('  "role": ', K), ('"AI Software Engineer"', S), (",", P)],
        [('  "track": ', K), ('"Data Science & AI Eng."', S), (",", P)],
        [('  "focus": ', K), ('["RAG","LLM","ML","APIs"]', S), (",", P)],
        [('  "status": ', K), ('"training models..."', TEAL)],
        [("}", P)],
    ]
    cw = 7.8
    t = 0.3
    for i, parts in enumerate(lines):
        y = 100 + i * 19
        txt = "".join(p for p, _ in parts)
        n = len(txt)
        d = max(0.15, n * 0.035)
        card.append(typing_clip(f"j{i}", X0, y, n, cw, f"{t:.2f}s", d))
        spans = "".join(f'<tspan fill="{c}">{esc(p)}</tspan>' for p, c in parts)
        card.append(f'<text x="{X0}" y="{y}" font-size="13" textLength="{n * cw:.1f}" lengthAdjust="spacing" xml:space="preserve" clip-path="url(#j{i})">{spans}</text>')
        t += d + 0.1

    # skill weights bar chart
    weights = [("ai_llm", .95, CYAN), ("data_ml", .90, PINK), ("backend", .88, TEAL), ("frontend", .80, AMBER), ("devops", .78, VIOLET)]
    card.append(f'<text x="{X0}" y="250" font-size="11" fill="{MUTED}">// skill_weights (normalized)</text>')
    bx, bw = X0 + 80, 220
    for i, (n, v, c) in enumerate(weights):
        y = 270 + i * 19
        b = t + 0.2 + i * 0.15
        card.append(f'<text x="{X0}" y="{y + 9}" font-size="11" fill="#c9d4f2">{n}</text>'
                    f'<rect x="{bx}" y="{y}" width="{bw}" height="11" rx="2" fill="{DIM}" opacity=".6"/>'
                    f'<rect x="{bx}" y="{y}" width="0" height="11" rx="2" fill="{c}"><animate attributeName="width" from="0" to="{bw * v:.0f}" begin="{b:.2f}s" dur=".9s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect>'
                    f'<text x="{bx + bw + 8}" y="{y + 9}" font-size="11" fill="{c}" opacity="0">{v:.2f}<animate attributeName="opacity" to="1" begin="{b + 0.8:.2f}s" dur=".2s" fill="freeze"/></text>')
    card.append(f'<rect x="{X0 + 14}" y="202" width="8" height="15" fill="{TEAL}" class="blink"/>')

    extra = f'<radialGradient id="cg"><stop offset="0" stop-color="{WHITE}"/><stop offset="1" stop-color="{CYAN}"/></radialGradient>'
    return frame(W, H, graph + "".join(card), "", extra)


# ================================================================= SECTION HEADERS
def header(idx, title, sub, col):
    W, H = 840, 74
    tw = (len(title) + 2) * 15.6
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{FONT}}} {BLINK}
@keyframes flow{{to{{stroke-dashoffset:-32}}}} .flow{{animation:flow 1s linear infinite}}
@keyframes run{{from{{transform:translateX(-80px)}}to{{transform:translateX({W + 80}px)}}}} .run{{animation:run 3s cubic-bezier(.6,0,.4,1) infinite}}
</style>
<defs><filter id="glow" x="-50%" y="-100%" width="200%" height="300%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset=".5" stop-color="{col}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>
<text x="420" y="32" text-anchor="middle" font-size="26" font-weight="800" letter-spacing="2" fill="#fff" filter="url(#glow)"><tspan fill="{col}">❯ </tspan>{title}</text>
<rect class="blink" x="{420 + tw / 2 + 4}" y="12" width="13" height="24" fill="{col}"/>
<text x="{420 - tw / 2 - 16}" y="31" text-anchor="end" font-size="12" fill="{col}" opacity=".7">[{idx:02d}]</text>
<text x="420" y="54" text-anchor="middle" font-size="12" fill="#7f8db3">{esc(sub)}</text>
<line x1="40" x2="{W - 40}" y1="68" y2="68" stroke="url(#ln)" stroke-width="2" stroke-dasharray="10 6" class="flow"/>
<rect class="run" x="0" y="65" width="60" height="6" rx="3" fill="{col}" filter="url(#glow)"/>
</svg>"""


# ================================================================= PROJECT CARDS
def viz(kind, col):
    """Mini live visual drawn in the top-right box of a project card (x 296..392, y 16..92)."""
    if kind == "fusion":
        return (f'<rect x="300" y="22" width="34" height="20" rx="3" fill="none" stroke="{CYAN}" stroke-width="1.5"/><text x="317" y="36" text-anchor="middle" font-size="9" fill="{CYAN}">IMG</text>'
                f'<rect x="300" y="64" width="34" height="20" rx="3" fill="none" stroke="{AMBER}" stroke-width="1.5"/><text x="317" y="78" text-anchor="middle" font-size="9" fill="{AMBER}">TXT</text>'
                f'<path id="pa" d="M334 32 C352 32 352 53 364 53" fill="none" stroke="{CYAN}" stroke-opacity=".4"/><path id="pb" d="M334 74 C352 74 352 53 364 53" fill="none" stroke="{AMBER}" stroke-opacity=".4"/>'
                + "".join(f'<circle r="2.5" fill="{c}"><animateMotion dur="1.2s" begin="-{k * 0.4:.1f}s" repeatCount="indefinite"><mpath href="#{p}"/></animateMotion></circle>'
                          for p, c in (("pa", CYAN), ("pb", AMBER)) for k in range(3))
                + f'<circle cx="376" cy="53" r="13" fill="{PANEL}" stroke="{col}" stroke-width="2" class="pulse"/><text x="376" y="56" text-anchor="middle" font-size="7" font-weight="700" fill="{col}">CLIP</text>')
    if kind == "ecg":
        seg = "l14 0 l4 -6 l4 6 l6 0 l3 6 l5 -30 l5 32 l4 -8 l5 0 l6 -5 l6 5 l14 0"
        return (f'<clipPath id="vb"><rect x="298" y="20" width="92" height="66"/></clipPath><g clip-path="url(#vb)">'
                f'<path class="ecg" d="M298 60 {seg} {seg} {seg}" fill="none" stroke="{col}" stroke-width="2" filter="url(#glow)"/></g>'
                f'<text x="388" y="86" text-anchor="end" font-size="9" fill="{col}">72 bpm</text>')
    if kind == "radar":
        rings = "".join(f'<circle cx="345" cy="54" r="{r}" fill="none" stroke="{col}" stroke-opacity=".3"/>' for r in (12, 24, 34))
        blips = "".join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{TEAL}" class="pulse" style="animation-delay:-{d}s"/>' for x, y, d in ((356, 40, .2), (333, 66, .9), (362, 64, .5)))
        return (rings + f'<line x1="311" x2="379" y1="54" y2="54" stroke="{col}" stroke-opacity=".25"/><line x1="345" x2="345" y1="20" y2="88" stroke="{col}" stroke-opacity=".25"/>'
                f'<g><path d="M345 54 L345 20 A34 34 0 0 1 375 38 Z" fill="url(#rg)"/><animateTransform attributeName="transform" type="rotate" values="0 345 54;360 345 54" dur="2.5s" repeatCount="indefinite"/></g>' + blips)
    if kind == "bars":
        rnd = random.Random(9)
        out = []
        for i in range(6):
            hs = [rnd.randint(10, 60) for _ in range(4)]
            vals = ";".join(str(h) for h in hs + hs[:1])
            yv = ";".join(str(86 - h) for h in hs + hs[:1])
            out.append(f'<rect x="{302 + i * 15}" width="10" rx="1" fill="{col}" opacity="{0.5 + i * 0.09:.2f}" y="{86 - hs[0]}" height="{hs[0]}">'
                       f'<animate attributeName="height" values="{vals}" dur="4s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.25;.5;.75;1" keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1"/>'
                       f'<animate attributeName="y" values="{yv}" dur="4s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.25;.5;.75;1" keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1"/></rect>')
        return f'<line x1="298" x2="392" y1="87" y2="87" stroke="{MUTED}"/>' + "".join(out)
    if kind == "graph":
        pts = [(345, 54), (312, 30), (378, 28), (306, 76), (382, 78), (345, 22), (345, 88)]
        ed = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5), (2, 5), (3, 6), (4, 6), (1, 3), (2, 4)]
        lines = "".join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" stroke="{col}" stroke-opacity=".35"/>' for a, b in ed)
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="{6 if i == 0 else 4}" fill="{col}" class="pulse" style="animation-delay:{i * 0.2:.1f}s"/>' for i, (x, y) in enumerate(pts))
        return lines + dots
    if kind == "rank":
        out = []
        for i, base in enumerate((80, 64, 50, 36)):
            out.append(f'<text x="300" y="{32 + i * 17}" font-size="9" fill="{MUTED}">#{i + 1}</text>'
                       f'<rect x="316" y="{24 + i * 17}" height="10" rx="2" fill="{col}" opacity="{1 - i * 0.18:.2f}" width="{base - 10}">'
                       f'<animate attributeName="width" values="{base - 10};{base - 30};{base - 4};{base - 10}" dur="{3 + i * 0.4:.1f}s" repeatCount="indefinite"/></rect>')
        return "".join(out)
    return ""


PROJECTS = [
    ("crisisvision", "CRISISVISION", "MULTIMODAL AI", CYAN, "fusion",
     ["Multimodal crisis analysis from", "text + images, CLIP consistency", "checks, MLflow experiment tracking."], "Python · CLIP · MLflow"),
    ("homedoc", "HOMEDOC", "HEALTH AI", PINK, "ecg",
     ["Intelligent medical diagnosis", "system: symptom analysis through", "a REST API + web frontend."], "TypeScript · REST API"),
    ("techcare", "TECHCARE PRO", "AI SUPPORT", TEAL, "radar",
     ["PC repair management system", "with built-in AI support for", "diagnosing customer issues."], "JavaScript · AI"),
    ("sportwear", "SPORTWEAR", "E-COMMERCE", AMBER, "bars",
     ["Full e-commerce platform for", "athletic gear: React frontend", "powered by a Django REST API."], "React · Django"),
    ("socialfeed", "SOCIAL FEED", "SOCIAL GRAPH", VIOLET, "graph",
     ["Social platform: Django GraphQL", "API with JWT auth + push notifs,", "and a cross-platform Flutter app."], "Django · GraphQL · Flutter"),
    ("esport", "ESPORT ARENA", "WEB PLATFORM", "#4da3ff", "rank",
     ["Esport tournament arena website,", "split into a frontend and a", "JavaScript backend."], "HTML · JavaScript"),
]


def project(title, tag, col, kind, lines, stack):
    W, H = 410, 180
    desc = "".join(f'<text x="22" y="{92 + i * 18}" font-size="12" fill="#c9d4f2">{esc(l)}</text>' for i, l in enumerate(lines))
    css = (f"@keyframes ecg{{to{{transform:translateX(-71px)}}}} .ecg{{animation:ecg 1.6s linear infinite}}"
           f"@keyframes lap{{to{{stroke-dashoffset:-100}}}} .lap{{animation:lap 3.5s linear infinite}}")
    body = f"""
<rect x="16" y="16" width="{len(tag) * 7.3 + 28:.0f}" height="20" rx="10" fill="{col}" fill-opacity=".15" stroke="{col}"/>
<circle cx="27" cy="26" r="3.5" fill="{col}" class="pulse"/>
<text x="36" y="30" font-size="10" font-weight="700" fill="{col}" letter-spacing="1">{tag}</text>
<text x="22" y="66" font-size="21" font-weight="800" fill="#fff" letter-spacing="1">{title}</text>
{desc}
<line x1="22" x2="388" y1="146" y2="146" stroke="{DIM}"/>
<text x="22" y="166" font-size="11" fill="{col}">stack: <tspan fill="#fff">{esc(stack)}</tspan></text>
<text x="388" y="166" font-size="11" fill="{col}" text-anchor="end">inspect <tspan class="blink">→</tspan></text>
<rect x="294" y="14" width="100" height="80" rx="6" fill="#070d1f" stroke="{DIM}"/>
{viz(kind, col)}
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="12" fill="none" stroke="{col}" stroke-opacity=".35" stroke-width="1.5"/>
<rect class="lap" x="2" y="2" width="{W - 4}" height="{H - 4}" rx="12" fill="none" stroke="{col}" stroke-width="3" pathLength="100" stroke-dasharray="7 93" filter="url(#glow)"/>"""
    extra = f'<radialGradient id="rg" cx="0" cy="1" r="1"><stop offset="0" stop-color="{col}" stop-opacity=".7"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{FONT}}} {BLINK} {PULSE} {css}</style>
<defs>{DEFS}{extra}<clipPath id="cc"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>
<g clip-path="url(#cc)"><rect width="{W}" height="{H}" fill="url(#bgr)"/><rect width="{W}" height="{H}" fill="url(#dots)" opacity=".6"/>{body}</g></svg>"""


# ================================================================= TRAINING LOG (certifications as checkpoints)
def training():
    W, H = 840, 270
    x0, x1, y0, y1 = 70, 800, 50, 190
    rnd = random.Random(4)
    N = 80
    loss, acc = [], []
    for i in range(N + 1):
        f = i / N
        x = x0 + f * (x1 - x0)
        l = y0 + 10 + (y1 - y0 - 25) * (1 - math.exp(-4 * f)) + rnd.uniform(-4, 4) * (1 - f)
        a = y1 - 10 - (y1 - y0 - 30) * (1 - math.exp(-3.2 * f)) + rnd.uniform(-3, 3) * (1 - f)
        loss.append((x, l)); acc.append((x, a))
    pl = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in loss)
    pa = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in acc)
    grid = "".join(f'<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" stroke="{DIM}" stroke-dasharray="2 4"/>' for y in range(y0, y1 + 1, 35))
    certs = [(.18, "PCAP", "Python Institute", AMBER), (.42, "DATA SCIENCE", "Cisco Essentials", CYAN),
             (.66, "VERSION CONTROL", "Meta", PINK), (.9, "IELTS", "English", TEAL)]
    cps, css = [], []
    cycle = 9
    plen = lambda pts: sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    Ll, La = plen(loss), plen(acc)
    def appear(f):
        t = 0.5 * f
        return (f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t:.3f};{t + 0.03:.3f};.92;1" dur="{cycle}s" repeatCount="indefinite"/>')
    for i, (f, name, org, col) in enumerate(certs):
        idx = round(f * N)
        x, y = acc[idx]
        cps.append(f'<g opacity="0">{appear(f)}<line x1="{x:.1f}" x2="{x:.1f}" y1="{y:.1f}" y2="208" stroke="{col}" stroke-dasharray="2 3" opacity=".7"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="none" stroke="{col}"><animate attributeName="r" values="6;16" dur="1.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="1.4s" repeatCount="indefinite"/></circle>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{col}" filter="url(#glow)"/>'
                   f'<text x="{x:.1f}" y="226" text-anchor="middle" font-size="12" font-weight="800" fill="{col}">✓ {name}</text>'
                   f'<text x="{x:.1f}" y="243" text-anchor="middle" font-size="10" fill="#c9d4f2">{org}</text></g>')
    def draw(L):
        return (f'stroke-dasharray="{L:.0f} {L:.0f}" stroke-dashoffset="{L:.0f}"><animate attributeName="stroke-dashoffset" values="{L:.0f};0;0;0" keyTimes="0;.5;.92;1" dur="{cycle}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="1;1;1;0" keyTimes="0;.5;.92;1" dur="{cycle}s" repeatCount="indefinite"/>')
    ep = (f'<animate attributeName="x1" values="{x0};{x1};{x1}" keyTimes="0;.5;1" dur="{cycle}s" repeatCount="indefinite"/>'
          f'<animate attributeName="x2" values="{x0};{x1};{x1}" keyTimes="0;.5;1" dur="{cycle}s" repeatCount="indefinite"/>')
    body = f"""
<text x="24" y="30" font-size="12" fill="{MUTED}">training_log :: certifications saved as checkpoints</text>
<g font-size="11"><line x1="560" x2="582" y1="26" y2="26" stroke="{PINK}" stroke-width="2"/><text x="588" y="30" fill="{PINK}">train_loss</text>
<line x1="680" x2="702" y1="26" y2="26" stroke="{TEAL}" stroke-width="2"/><text x="708" y="30" fill="{TEAL}">skill_acc</text></g>
{grid}
<line x1="{x0}" x2="{x0}" y1="{y0 - 6}" y2="{y1}" stroke="{MUTED}"/><line x1="{x0}" x2="{x1}" y1="{y1}" y2="{y1}" stroke="{MUTED}"/>
<text x="{x1}" y="{y1 + 14}" text-anchor="end" font-size="10" fill="{MUTED}">epoch →</text>
<text x="{x0 - 8}" y="{y0 + 4}" text-anchor="end" font-size="10" fill="{MUTED}">1.0</text><text x="{x0 - 8}" y="{y1}" text-anchor="end" font-size="10" fill="{MUTED}">0.0</text>
<path d="{pl}" fill="none" stroke="{PINK}" stroke-width="2" stroke-opacity=".8" {draw(Ll)}</path>
<path d="{pa}" fill="none" stroke="{TEAL}" stroke-width="2.5" filter="url(#glow)" {draw(La)}</path>
<line x1="{x0}" x2="{x0}" y1="{y0 - 6}" y2="{y1}" stroke="{CYAN}" stroke-opacity=".5">{ep}</line>
{''.join(cps)}"""
    return frame(W, H, body, "")


# ================================================================= FOOTER: terminal
def footer():
    W, H = 840, 250
    rows = [
        (0.4, [("$ ", TEAL), ("python connect.py --target iheb_lamouchi", WHITE)]),
        (1.4, [("[INFO] ", CYAN), ("loading shared interests: AI · RAG · data ...... ", "#c9d4f2"), ("done", TEAL)]),
        (2.3, [("[INFO] ", CYAN), ("opening socket to a new collaborator .......... ", "#c9d4f2"), ("done", TEAL)]),
        (3.2, [("[ OK ] ", TEAL), ("pipeline finished · 0 errors · thanks for scrolling!", WHITE)]),
    ]
    out = [window_bar(W, "iheb@data-lab:~ — zsh")]
    for i, (t, parts) in enumerate(rows):
        y = 70 + i * 26
        spans = "".join(f'<tspan fill="{c}">{esc(p)}</tspan>' for p, c in parts)
        out.append(f'<text x="28" y="{y}" font-size="14" opacity="0" xml:space="preserve">{spans}<set attributeName="opacity" to="1" begin="{t}s" fill="freeze"/></text>')
    out.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="2.5s" fill="freeze"/>'
               f'<rect x="28" y="168" width="560" height="12" rx="3" fill="{DIM}"/>'
               f'<rect x="28" y="168" width="0" height="12" rx="3" fill="url(#neon)"><animate attributeName="width" to="560" begin="2.5s" dur="1.2s" fill="freeze"/></rect>'
               f'<text x="600" y="179" font-size="13" fill="{TEAL}" opacity="0">100%<set attributeName="opacity" to="1" begin="3.7s" fill="freeze"/></text></g>')
    out.append(f'<text x="28" y="218" font-size="15" font-weight="700" fill="{AMBER}" opacity="0">&gt;&gt;&gt; pick a channel below to connect<set attributeName="opacity" to="1" begin="4.2s" fill="freeze"/></text>'
               f'<rect x="372" y="204" width="10" height="18" fill="{AMBER}" opacity="0"><set attributeName="opacity" to="1" begin="4.2s" fill="freeze"/>'
               f'<animate attributeName="fill-opacity" values="1;0;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    return frame(W, H, "".join(out), "")


# ================================================================= SQL QUERY ENGINE (real data from the GitHub API)
FALLBACK_LANGS = [("Python", 6), ("JavaScript", 3), ("HTML", 2), ("C++", 1), ("CSS", 1), ("Dart", 1), ("Jupyter Notebook", 1), ("TypeScript", 1)]


def fetch_languages(user="iheblam"):
    import json
    import urllib.request
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{user}/repos?per_page=100",
                                     headers={"User-Agent": "profile-asset-generator"})
        tok = os.environ.get("GITHUB_TOKEN")
        if tok:
            req.add_header("Authorization", f"Bearer {tok}")
        repos = json.load(urllib.request.urlopen(req, timeout=20))
        counts = {}
        for r in repos:
            if r.get("language") and not r.get("fork"):
                counts[r["language"]] = counts.get(r["language"], 0) + 1
        langs = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
        return langs or FALLBACK_LANGS, sum(1 for r in repos if not r.get("fork"))
    except Exception as e:  # offline: keep the last known numbers
        print("GitHub API unavailable, using fallback:", e)
        return FALLBACK_LANGS, 20


def query_engine():
    W, H = 840, 345
    langs, total = fetch_languages()
    KW, ID, CM = VIOLET, WHITE, MUTED
    sql = [
        [("SELECT ", KW), ("language,", ID)],
        [("       COUNT", KW), ("(*) ", ID), ("AS ", KW), ("repos", ID)],
        [("FROM   ", KW), ("iheb.public_repos", AMBER)],
        [("WHERE  ", KW), ("language ", ID), ("IS NOT NULL", KW)],
        [("GROUP  BY ", KW), ("language", ID)],
        [("ORDER  BY ", KW), ("repos ", ID), ("DESC", KW), (";", ID)],
    ]
    out = [window_bar(W, "psql :: iheb@github_warehouse — live query")]
    out.append(f'<rect x="20" y="50" width="370" height="{H - 70}" rx="8" fill="#070d1f" stroke="{DIM}"/>'
               f'<text x="34" y="72" font-size="11" fill="{CM}">-- what do I build with? (refreshed daily)</text>')
    cw, t = 7.8, 0.4
    for i, parts in enumerate(sql):
        y = 100 + i * 22
        txt = "".join(p for p, _ in parts)
        n = len(txt)
        d = n * 0.03
        out.append(f'<text x="34" y="{y}" font-size="12" fill="{DIM}">{i + 1}</text>')
        out.append(typing_clip(f"q{i}", 56, y, n, cw, f"{t:.2f}s", d))
        spans = "".join(f'<tspan fill="{c}">{esc(p)}</tspan>' for p, c in parts)
        out.append(f'<text x="56" y="{y}" font-size="13" textLength="{n * cw:.1f}" lengthAdjust="spacing" xml:space="preserve" clip-path="url(#q{i})">{spans}</text>')
        t += d + 0.08
    # execute: spinner then status
    run_at, done_at = t + 0.2, t + 1.4
    sy = 100 + len(sql) * 22 + 22
    out.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{run_at:.2f}s"/><set attributeName="opacity" to="0" begin="{done_at:.2f}s"/>'
               f'<g transform="translate(42 {sy - 4})"><circle r="7" fill="none" stroke="{DIM}" stroke-width="2.5"/>'
               f'<path d="M0 -7 A7 7 0 0 1 7 0" fill="none" stroke="{CYAN}" stroke-width="2.5"><animateTransform attributeName="transform" type="rotate" values="0;360" dur=".7s" repeatCount="indefinite"/></path></g>'
               f'<text x="56" y="{sy}" font-size="12" fill="{CYAN}">executing on {total} repositories...</text></g>')
    out.append(f'<text x="34" y="{sy}" font-size="12" fill="{TEAL}" opacity="0">✓ {len(langs)} rows returned · query OK'
               f'<set attributeName="opacity" to="1" begin="{done_at:.2f}s" fill="freeze"/></text>')
    out.append(f'<rect x="34" y="{sy + 14}" width="8" height="15" fill="{TEAL}" opacity="0"><set attributeName="opacity" to="1" begin="{done_at:.2f}s" fill="freeze"/>'
               f'<animate attributeName="fill-opacity" values="1;0;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>')

    # result grid
    X = 410
    out.append(f'<rect x="{X}" y="50" width="{W - X - 20}" height="{H - 70}" rx="8" fill="#070d1f" stroke="{DIM}"/>'
               f'<text x="{X + 16}" y="76" font-size="11" fill="{CM}" letter-spacing="1">LANGUAGE</text>'
               f'<text x="{X + 178}" y="76" font-size="11" fill="{CM}" letter-spacing="1">REPOS</text>'
               f'<line x1="{X}" x2="{W - 20}" y1="86" y2="86" stroke="{DIM}"/>')
    cols = [CYAN, AMBER, PINK, TEAL, VIOLET, "#4da3ff", "#ff7a59", "#c6ff3d"]
    mx = max(c for _, c in langs)
    barmax = W - 20 - (X + 215) - 20
    for i, (lang, cnt) in enumerate(langs):
        y = 108 + i * 28
        b = done_at + 0.15 + i * 0.18
        col = cols[i % len(cols)]
        bw = barmax * cnt / mx
        out.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{b:.2f}s" fill="freeze"/>'
                   f'<rect x="{X + 6}" y="{y - 16}" width="{W - X - 32}" height="24" rx="4" fill="{col}" opacity=".06"/>'
                   f'<text x="{X + 16}" y="{y}" font-size="13" fill="#fff">{esc(lang)}</text>'
                   f'<text x="{X + 178}" y="{y}" font-size="13" font-weight="700" fill="{col}">{cnt}</text>'
                   f'<rect x="{X + 215}" y="{y - 11}" height="12" rx="2" fill="{col}" width="0" filter="url(#glow)">'
                   f'<animate attributeName="width" from="0" to="{bw:.0f}" begin="{b:.2f}s" dur=".8s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect></g>')
    # looping scan highlight over the result rows
    out.append(f'<rect x="{X + 2}" y="92" width="{W - X - 24}" height="26" fill="{CYAN}" opacity="0">'
               f'<animate attributeName="opacity" to=".08" begin="{done_at + 2:.2f}s" dur=".01s" fill="freeze"/>'
               f'<animate attributeName="y" values="{";".join(str(92 + k * 28) for k in range(len(langs)))}" dur="{len(langs) * 0.6:.1f}s" calcMode="discrete" begin="{done_at + 2:.2f}s" repeatCount="indefinite"/></rect>')
    return frame(W, H, "".join(out), "")


if __name__ == "__main__":
    save("pipeline-hero.svg", hero())
    save("query.svg", query_engine())
    save("profile.svg", profile())
    save("training.svg", training())
    save("footer.svg", footer())
    for key, *rest in PROJECTS:
        save(f"p-{key}.svg", project(*rest))
    for i, (key, title, sub, col) in enumerate([
        ("whoami", "WHOAMI", "-- SELECT * FROM engineers WHERE name = 'iheb';", CYAN),
        ("stack", "TECH_STACK", "-- feature store: tools running in production", TEAL),
        ("pipelines", "PIPELINES", "-- deployed projects · click a card to inspect", PINK),
        ("training", "TRAINING_LOG", "-- certifications, saved as model checkpoints", AMBER),
        ("metrics", "METRICS", "-- live telemetry streamed from github", VIOLET),
        ("socket", "CONNECT", "-- open a socket, let's build something data-driven", CYAN),
    ], 1):
        save(f"h-{key}.svg", header(i, title, sub, col))
