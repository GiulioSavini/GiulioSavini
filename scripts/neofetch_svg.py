#!/usr/bin/env python3
"""Render the neofetch block as a font-independent SVG (braille art -> dot matrix)."""
import pathlib
from xml.sax.saxutils import escape

ART = """\
⠄⠄⠄⠄⢠⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⣿⣿⣆
⠄⠄⣼⢀⣿⣿⣿⣿⣏⡏⠄⠹⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⡆
⠄⠄⡟⣼⣿⣿⣿⣿⣿⠄⠄⠄⠈⠻⣿⣿⣿⣿⣿⣿⣿⣇⢻⣿⣿⣿⣿
⠄⢰⠃⣿⣿⠿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠙⠿⣿⣿⣿⣿⣿⠄⢿⣿⣿⣿⡄
⠄⢸⢠⣿⣿⣧⡙⣿⣿⡆⠄⠄⠄⠄⠄⠄⠄⠈⠛⢿⣿⣿⡇⠸⣿⡿⣸⡇
⠄⠈⡆⣿⣿⣿⣿⣦⡙⠳⠄⠄⠄⠄⠄⠄⢀⣠⣤⣀⣈⠙⠃⠄⠿⢇⣿⡇
⠄⠄⡇⢿⣿⣿⣿⣿⡇⠄⠄⠄⠄⠄⣠⣶⣿⣿⣿⣿⣿⣿⣷⣆⡀⣼⣿⡇
⠄⠄⢹⡘⣿⣿⣿⢿⣷⡀⠄⢀⣴⣾⣟⠉⠉⠉⠉⣽⣿⣿⣿⣿⠇⢹⣿⠃
⠄⠄⠄⢷⡘⢿⣿⣎⢻⣷⠰⣿⣿⣿⣿⣦⣀⣀⣴⣿⣿⣿⠟⢫⡾⢸⡟
⠄⠄⠄⠄⠻⣦⡙⠿⣧⠙⢷⠙⠻⠿⢿⡿⠿⠿⠛⠋⠉⠄⠂⠘⠁⠞
⠄⠄⠄⠄⠄⠈⠙⠑⣠⣤⣴⡖⠄⠿⣋⣉⣉⡁⠄⢾⣦"""

INFO = [
    ("User", "Giulio Savini"),
    ("Role", "Infrastructure & Platform Engineer"),
    ("Location", "Italy"),
    ("OS", "Linux x86_64 (Hardened Kernel)"),
    ("Uptime", "24/7 Automated Operations"),
    ("Core Focus", "DevSecOps | SIEM | Multi-Cloud"),
    ("IaC", "Terraform · Ansible · Docker · K8s"),
    ("Security", "Wazuh · HashiCorp Vault · Trivy"),
    ("Cloud", "AWS · Azure · GCP · Oracle OCI"),
    ("Observability", "Icinga · Prometheus · Grafana"),
    ("Languages", "Go · Python · Bash · Rust"),
]

BG, PANEL, BORDER = "#0D1117", "#161B22", "#30363D"
RED, TEXT, MUTED = "#E0202C", "#C9D1D9", "#8B949E"
DOT = 4.0          # dot spacing in px
R = 1.7           # dot radius
BITS = [(0, 0, 1), (0, 1, 2), (0, 2, 4), (1, 0, 8), (1, 1, 16), (1, 2, 32), (0, 3, 64), (1, 3, 128)]

lines = ART.split("\n")
cols = max(len(l) for l in lines)
art_w, art_h = cols * 2 * DOT, len(lines) * 4 * DOT
pad, line_h, info_x = 28, 22, 40 + art_w + 36
width, height = int(info_x + 420), int(max(art_h, len(INFO) * line_h) + 110)

circles = []
for cy, line in enumerate(lines):
    for cx, ch in enumerate(line):
        v = ord(ch) - 0x2800
        if ch == "⠄":  # background filler in the original art
            continue
        for dx, dy, b in BITS:
            if v & b:
                x = 40 + (cx * 2 + dx) * DOT + DOT / 2
                y = 68 + (cy * 4 + dy) * DOT + DOT / 2
                circles.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R}"/>')

info = []
for i, (k, v) in enumerate(INFO):
    y = 86 + i * line_h
    info.append(
        f'<text x="{info_x}" y="{y}" class="mono"><tspan fill="{RED}" font-weight="700">{k}</tspan>'
        f'<tspan fill="{MUTED}">: </tspan><tspan fill="{TEXT}">{escape(v)}</tspan></text>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
  .mono {{ font: 13px "JetBrains Mono", "Fira Code", "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; }}
  .cursor {{ animation: blink 1.1s steps(2, start) infinite; }}
  @keyframes blink {{ to {{ visibility: hidden; }} }}
  .dot {{ animation: fade 2.4s ease-in-out infinite alternate; }}
  @keyframes fade {{ from {{ opacity: .55; }} to {{ opacity: 1; }} }}
</style>
<rect width="100%" height="100%" rx="12" fill="{BG}" stroke="{BORDER}"/>
<rect x="0.5" y="0.5" width="{width-1}" height="34" rx="12" fill="{PANEL}"/>
<rect x="0.5" y="22" width="{width-1}" height="13" fill="{PANEL}"/>
<circle cx="20" cy="18" r="5" fill="{RED}"/><circle cx="38" cy="18" r="5" fill="{BORDER}"/><circle cx="56" cy="18" r="5" fill="{BORDER}"/>
<text x="{width/2}" y="22" text-anchor="middle" class="mono" fill="{MUTED}">giulio@workstation — neofetch</text>
<text x="40" y="56" class="mono"><tspan fill="{RED}">giulio@workstation</tspan><tspan fill="{MUTED}">:~$ </tspan><tspan fill="{TEXT}">neofetch</tspan></text>
<g class="dot" fill="{TEXT}">{''.join(circles)}</g>
{''.join(info)}
<text x="40" y="{height-22}" class="mono"><tspan fill="{RED}">giulio@workstation</tspan><tspan fill="{MUTED}">:~$ </tspan><tspan fill="{TEXT}" class="cursor">▌</tspan></text>
</svg>
'''
out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "neofetch.svg"
out.write_text(svg, encoding="utf-8")
print(f"wrote {out} ({width}x{height}, {len(circles)} dots)")
