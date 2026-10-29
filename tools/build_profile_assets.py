"""Generates the light and dark SVGs for the RazinAI org profile.

Usage: python tools/build_profile_assets.py tools/icons profile/assets
"""

import base64
import pathlib
import sys
from html import escape

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
STILL = len(sys.argv) > 3
FREEZE = ("*{animation:none!important}.band{stroke-dashoffset:0!important}"
          ".bar{transform:none!important}.val,.rot.r0{opacity:1!important}")

THEMES = {
    "light": dict(ground="#F6F2E8", ground2="#EEE8D8", surface="#FBF9F3", ink="#2A1612",
                  muted="#6A5F55", line="#DCD4C0", mark="#4A1A14", accent="#9A3A1E",
                  signal="#D9A02B", other="#B9AE9C",
                  bands=["#F0CB7A", "#D9A02B", "#B8652A", "#7E2E1C", "#4A1A14"]),
    "dark": dict(ground="#1A0E0B", ground2="#23130F", surface="#2A1712", ink="#EEE9DC",
                 muted="#B0A699", line="#45302A", mark="#EEE9DC", accent="#E8956A",
                 signal="#E3AE45", other="#5E4A42",
                 bands=["#7E2E1C", "#B8652A", "#D9A02B", "#F0CB7A", "#EEE9DC"]),
}

SANS = "-apple-system, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
ARABIC = "'Noto Kufi Arabic', 'Geeza Pro', 'Segoe UI', 'Noto Sans Arabic', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

R_PATHS = ('<path d="M31.5 5H42.5V87H31.5Z" fill="currentColor"/>'
           '<path d="M53.30 54.35L62.70 48.65L82.94 82H70.07Z" fill="currentColor"/>'
           '<path d="M31.5 15.5H65A18 18 0 0 1 65 51.5C47.19 51.50 26.26 58.51 16.37 80.50" '
           'fill="none" stroke="currentColor" stroke-width="11"/>')


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def svg(w, h, body, style, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(label)}">'
            f'<title>{escape(label)}</title><style>{style}{FREEZE if STILL else ""}</style>{body}</svg>')


def write(name, theme, text):
    (OUT / f"{name}-{theme}.svg").write_text(text)


def hero(t, theme):
    w, h = 1280, 380
    bands = ""
    for i, color in enumerate(t["bands"]):
        y = 70 + i * 52
        d = f"M1010 {y + 190} C 1070 {y + 70}, 1160 {y - 10}, 1320 {y - 25}"
        bands += (f'<path class="band b{i}" d="{d}" stroke="{color}" stroke-width="26" '
                  f'fill="none" stroke-linecap="round" pathLength="1"/>')
    places = ["on your phone.", "in your browser.", "on your own machines."]
    rot = "".join(f'<text class="rot r{i}" x="330" y="265">{escape(p)}</text>' for i, p in enumerate(places))
    style = f"""
      text {{ font-family: {SANS}; }}
      .name {{ font-size: 84px; font-weight: 800; fill: {t['ink']}; letter-spacing: -2px; }}
      .ar {{ font-family: {ARABIC}; font-size: 58px; font-weight: 700; fill: {t['accent']}; }}
      .lead {{ font-size: 40px; font-weight: 600; fill: {t['ink']}; }}
      .rot {{ font-size: 40px; font-weight: 600; fill: {t['accent']}; opacity: 0;
              animation: rot 9s infinite both; }}
      .r1 {{ animation-delay: 3s; }} .r2 {{ animation-delay: 6s; }}
      @keyframes rot {{ 0% {{ opacity: 0; transform: translateY(14px); }}
                        5% {{ opacity: 1; transform: translateY(0); }}
                        30% {{ opacity: 1; transform: translateY(0); }}
                        35% {{ opacity: 0; transform: translateY(-14px); }}
                        100% {{ opacity: 0; }} }}
      .sub {{ font-size: 23px; fill: {t['muted']}; }}
      .mark {{ color: {t['mark']}; animation: rise 1s ease-out both; }}
      @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; }} }}
      .band {{ stroke-dasharray: 1; stroke-dashoffset: 1; opacity: .95;
               animation: draw 1.6s cubic-bezier(.2,.7,.2,1) forwards, drift 7s ease-in-out 1.6s infinite alternate; }}
      .b1 {{ animation-delay: .12s, 1.72s; }} .b2 {{ animation-delay: .24s, 1.84s; }}
      .b3 {{ animation-delay: .36s, 1.96s; }} .b4 {{ animation-delay: .48s, 2.08s; }}
      @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
      @keyframes drift {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-14px); }} }}
      .dot {{ fill: {t['signal']}; animation: blink 2.4s ease-in-out infinite; }}
      @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
    """
    body = f"""
      <defs><clipPath id="c"><rect width="{w}" height="{h}" rx="24"/></clipPath></defs>
      <g clip-path="url(#c)">
        <rect width="{w}" height="{h}" fill="{t['ground']}"/>
        {bands}
      </g>
      <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="24" fill="none" stroke="{t['line']}"/>
      <g class="mark" transform="translate(64 84) scale(2.5)">{R_PATHS}</g>
      <text class="name" x="330" y="150">Razin</text>
      <text class="ar" x="560" y="148">رزين</text>
      <text class="lead" x="330" y="215">AI that runs where you are,</text>
      {rot}
      <circle class="dot" cx="338" cy="318" r="6"/>
      <text class="sub" x="356" y="326">Arabic and English. Your data stays where it already is.</text>
    """
    write("hero", theme, svg(w, h, body, style, "Razin: AI that runs where you are"))


PRODUCTS = [
    dict(key="orb", name="Orb", kind="Android app", stage="Available now", live=True,
         icon=("orb-icon.webp", "image/webp"),
         desc=["Private, offline AI for Android. Chat, ask",
               "about photos and documents, and talk by",
               "voice, with no account and no cloud."],
         facts=[("Models", "Qwen3-VL, MiniCPM-V, Gemma 4"),
                ("Voice", "On-device Whisper"),
                ("Price", "One-time purchase, no ads")]),
    dict(key="deputy", name="Deputy", kind="Agent tool", stage="Developer preview", live=False,
         icon=("deputy-icon.svg", "image/svg+xml"),
         desc=["An agent in your browser that turns any page",
               "into a typed API for other agents. One call",
               "instead of screenshots and clicks."],
         facts=[("Runs in", "Your logged-in browser"),
                ("Talks to", "Any MCP client"),
                ("Install", "Chrome + npx deputy-mcp")]),
    dict(key="link", name="Link", kind="Android app", stage="In development", live=False,
         icon=("link-icon.svg", "image/svg+xml"),
         desc=["Run the coding agents on your own computer",
               "from your phone. Start a task, review the",
               "change and approve it."],
         facts=[("Connects", "SSH to Linux, macOS, WSL"),
                ("Agents", "Claude Code, Codex + 17 more"),
                ("Stage", "Android first")]),
    dict(key="ocr", name="Razin OCR", kind="Model", stage="In development", live=False, icon=None,
         desc=["OCR for images and scanned PDFs on your own",
               "hardware, made to be especially good at",
               "Arabic, dots and diacritics included."],
         facts=[("Input", "PNG, JPEG, scanned PDF"),
                ("Output", "Text + JSON with reading order"),
                ("Runs on", "Your CPU, no network")]),
]


def ocr_icon(t):
    return f"""
      <rect width="64" height="64" rx="15" fill="{t['ground2']}" stroke="{t['line']}"/>
      <text x="32" y="42" text-anchor="middle" style="font-family: {ARABIC}; font-size: 23px; font-weight: 700; fill: {t['ink']}">رزين</text>
      <rect class="scan" x="8" y="10" width="48" height="3" rx="1.5" fill="{t['signal']}"/>
    """


def card(t, theme, p):
    w, h = 500, 330
    if p["icon"]:
        icon = f'<image x="0" y="0" width="64" height="64" href="{data_uri(SRC / p["icon"][0], p["icon"][1])}"/>'
    else:
        icon = ocr_icon(t)
    pill_color = t["signal"] if p["live"] else (t["accent"] if p["stage"] == "Developer preview" else t["muted"])
    pill_w = 18 + len(p["stage"]) * 8.2 + 16
    desc = "".join(f'<text class="desc" x="36" y="{140 + i * 27}">{escape(l)}</text>' for i, l in enumerate(p["desc"]))
    facts = "".join(
        f'<text class="fk" x="36" y="{252 + i * 25}">{escape(k)}</text>'
        f'<text class="fv" x="118" y="{252 + i * 25}">{escape(v)}</text>' for i, (k, v) in enumerate(p["facts"]))
    style = f"""
      text {{ font-family: {SANS}; }}
      .name {{ font-size: 30px; font-weight: 750; fill: {t['ink']}; }}
      .kind {{ font-size: 17px; fill: {t['muted']}; }}
      .pill {{ font-size: 14px; font-weight: 600; fill: {pill_color}; }}
      .desc {{ font-size: 19px; fill: {t['ink']}; }}
      .fk {{ font-size: 15px; fill: {t['muted']}; }}
      .fv {{ font-size: 15px; fill: {t['ink']}; font-weight: 600; }}
      .card {{ animation: in .7s ease-out both; }}
      @keyframes in {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; }} }}
      .pulse {{ animation: pulse 1.8s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
      @keyframes pulse {{ from {{ opacity: .7; transform: scale(1); }} to {{ opacity: 0; transform: scale(2.6); }} }}
      .scan {{ animation: scan 2.6s ease-in-out infinite alternate; }}
      @keyframes scan {{ from {{ transform: translateY(0); }} to {{ transform: translateY(42px); }} }}
    """
    pulse = f'<circle class="pulse" cx="{w - 36 - pill_w + 16}" cy="47" r="4" fill="{pill_color}"/>' if p["live"] else ""
    body = f"""
      <g class="card">
        <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="{t['surface']}" stroke="{t['line']}"/>
        <g transform="translate(36 30)">{icon}</g>
        <text class="name" x="118" y="58">{escape(p['name'])}</text>
        <text class="kind" x="118" y="82">{escape(p['kind'])}</text>
        <rect x="{w - 36 - pill_w}" y="33" width="{pill_w}" height="28" rx="14" fill="none" stroke="{pill_color}" stroke-opacity=".55"/>
        {pulse}<circle cx="{w - 36 - pill_w + 16}" cy="47" r="4" fill="{pill_color}"/>
        <text class="pill" x="{w - 36 - pill_w + 28}" y="52">{escape(p['stage'])}</text>
        {desc}
        <line x1="36" x2="{w - 36}" y1="224" y2="224" stroke="{t['line']}"/>
        {facts}
      </g>
    """
    write(f"card-{p['key']}", theme, svg(w, h, body, style, f"{p['name']}: {' '.join(p['desc'])}"))


def bars(t, theme, name, title, note, rows, width=1000, shared=None):
    """rows: (label, [(value, text, is_ours)], right_text). Each row is scaled to its own max."""
    group_h = 30 * max(len(r[1]) for r in rows) + 34
    h = 96 + group_h * len(rows) + 40
    left, right = 230, 270
    span = width - left - right
    body = f'<rect x=".5" y=".5" width="{width - 1}" height="{h - 1}" rx="18" fill="{t["surface"]}" stroke="{t["line"]}"/>'
    body += f'<text class="title" x="36" y="52">{escape(title)}</text>'
    y = 96
    k = 0
    for label, series, right_text in rows:
        top = shared or max(v for v, _, _ in series)
        body += f'<text class="label" x="36" y="{y + 20}">{escape(label)}</text>'
        for i, (v, text, ours) in enumerate(series):
            bw = max(3, span * v / top)
            color = t["accent"] if ours else t["other"]
            by = y + i * 30
            body += (f'<rect class="bar" style="animation-delay:{k * .08:.2f}s" x="{left}" y="{by + 4}" '
                     f'width="{bw:.1f}" height="22" rx="4" fill="{color}"/>'
                     f'<text class="val" style="animation-delay:{k * .08 + .5:.2f}s" x="{left + bw + 10:.1f}" '
                     f'y="{by + 20}">{escape(text)}</text>')
            k += 1
        if right_text:
            body += f'<text class="big" x="36" y="{y + 50}">{escape(right_text)}</text>'
        y += group_h
    body += f'<text class="note" x="36" y="{h - 28}">{escape(note)}</text>'
    style = f"""
      text {{ font-family: {SANS}; }}
      .title {{ font-size: 21px; font-weight: 700; fill: {t['ink']}; }}
      .label {{ font-size: 15px; fill: {t['muted']}; }}
      .val {{ font-size: 14px; font-weight: 600; fill: {t['ink']}; font-family: {MONO};
              opacity: 0; animation: fade .4s ease-out forwards; }}
      .big {{ font-size: 20px; font-weight: 800; fill: {t['accent']}; }}
      .note {{ font-size: 13px; fill: {t['muted']}; }}
      .bar {{ transform-box: fill-box; transform-origin: left center; transform: scaleX(0);
              animation: grow 1s cubic-bezier(.2,.7,.2,1) forwards; }}
      @keyframes grow {{ to {{ transform: scaleX(1); }} }}
      @keyframes fade {{ to {{ opacity: 1; }} }}
    """
    write(name, theme, svg(width, h, body, style, title))


def legend_rows():
    return [
        ("Claude tokens", [(72632, "72,632  Deputy", True), (245250, "245,250  Playwright MCP", False)], "3.4× fewer"),
        ("Total cost", [(0.072, "$0.072  Deputy", True), (0.189, "$0.189  Playwright MCP", False)], "2.6× cheaper"),
        ("Page data sent", [(7269, "7,269 chars  Deputy", True), (46640, "46,640 chars  Playwright MCP", False)], "6.4× less"),
    ]


ARGUS = [("Starting point", 27.0), ("Shared NVENC context", 23.9), ("Pinned memory", 19.7),
         ("Two CUDA streams", 17.7), ("Rebalanced threads", 16.6), ("uint8 input", 16.4),
         ("fp16 model", 8.05), ("One CUDA context", 6.98)]


def argus_chart(t, theme):
    width, left, right = 1000, 250, 120
    span = width - left - right
    h = 100 + 34 * len(ARGUS) + 40
    body = f'<rect x=".5" y=".5" width="{width - 1}" height="{h - 1}" rx="18" fill="{t["surface"]}" stroke="{t["line"]}"/>'
    body += '<text class="title" x="36" y="52">argus: 16 streams × 300 frames, run time after each change</text>'
    for i, (label, s) in enumerate(ARGUS):
        y = 90 + i * 34
        bw = span * s / ARGUS[0][1]
        color = t["accent"] if i == len(ARGUS) - 1 else (t["other"] if i == 0 else t["signal"])
        body += (f'<text class="label" x="36" y="{y + 19}">{escape(label)}</text>'
                 f'<rect class="bar" style="animation-delay:{i * .18:.2f}s" x="{left}" y="{y + 3}" width="{bw:.1f}" '
                 f'height="22" rx="4" fill="{color}"/>'
                 f'<text class="val" style="animation-delay:{i * .18 + .6:.2f}s" x="{left + bw + 10:.1f}" y="{y + 19}">{s:g} s</text>')
    body += f'<text class="note" x="36" y="{h - 28}">RTX 3070 Laptop GPU. 3.9× faster end to end; inference went from about 180 to 770 frames per second.</text>'
    style = f"""
      text {{ font-family: {SANS}; }}
      .title {{ font-size: 21px; font-weight: 700; fill: {t['ink']}; }}
      .label {{ font-size: 15px; fill: {t['muted']}; }}
      .val {{ font-size: 14px; font-weight: 600; fill: {t['ink']}; font-family: {MONO};
              opacity: 0; animation: fade .4s ease-out forwards; }}
      .note {{ font-size: 13px; fill: {t['muted']}; }}
      .bar {{ transform-box: fill-box; transform-origin: left center; transform: scaleX(0);
              animation: grow .9s cubic-bezier(.2,.7,.2,1) forwards; }}
      @keyframes grow {{ to {{ transform: scaleX(1); }} }}
      @keyframes fade {{ to {{ opacity: 1; }} }}
    """
    write("argus-chart", theme, svg(width, h, body, style, "argus run time after each optimization"))


def ocr_chart(t, theme):
    rows = [("Tesseract fast", [(52.80, "52.80%  CER   0.199 s/image", False)], ""),
            ("Tesseract best", [(42.03, "42.03%  CER   0.288 s/image", False)], ""),
            ("PaddleOCR PP-OCRv5", [(15.23, "15.23%  CER   1.888 s/image", True)], "")]
    bars(t, theme, "ocr-chart", "Razin OCR: where pretrained models stand on Arabic (lower is better)",
         "14 synthetic Arabic pages, CPU, 6 September 2026. Diagnostics, not accuracy on your documents.", rows, shared=60)


for theme, t in THEMES.items():
    hero(t, theme)
    for p in PRODUCTS:
        card(t, theme, p)
    bars(t, theme, "deputy-chart", "Deputy vs Playwright MCP: one busy admin page with 400 orders",
         "Same task, same prompt, median of three runs, all succeeded. Both through claude -p.", legend_rows())
    argus_chart(t, theme)
    ocr_chart(t, theme)

print(sorted(p.name for p in OUT.iterdir()))
