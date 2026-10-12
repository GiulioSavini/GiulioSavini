#!/usr/bin/env python3
"""Self-contained typewriter SVG (no external services or fonts)."""
import pathlib
from xml.sax.saxutils import escape

LINES = [
    "Infrastructure & Platform Engineering",
    "DevSecOps, SIEM & Security Automation",
    "Multi-Cloud Architecture — AWS · Azure · GCP · OCI",
    "Ansible Galaxy Author & OSS Maintainer",
    "Container Orchestration & Observability",
]
RED, MUTED = "#E0202C", "#8B949E"
W, H, FS = 720, 44, 18
TYPE, HOLD, CHAR = 1.6, 1.6, 0.6  # seconds typing, seconds hold, approx char width in em
per = TYPE + HOLD
total = per * len(LINES)

parts = []
for i, line in enumerate(LINES):
    text_w = len(line) * FS * CHAR
    x0 = (W - text_w) / 2
    parts.append(f'''
  <g style="animation: show{i} {total:.1f}s steps(1,end) infinite">
    <clipPath id="c{i}"><rect x="{x0:.0f}" y="0" height="{H}" width="0" style="animation: type{i} {total:.1f}s steps({len(line)},end) infinite"/></clipPath>
    <text x="{W/2}" y="29" text-anchor="middle" class="t" clip-path="url(#c{i})">{escape(line)}</text>
  </g>''')

keyframes = []
for i, line in enumerate(LINES):
    s, e_type, e = i * per / total * 100, (i * per + TYPE) / total * 100, (i + 1) * per / total * 100
    text_w = len(line) * FS * CHAR
    keyframes.append(f'''
  @keyframes show{i} {{ 0%,{s:.2f}% {{ visibility: hidden; }} {s:.2f}%,{e:.2f}% {{ visibility: visible; }} {e:.2f}%,100% {{ visibility: hidden; }} }}
  @keyframes type{i} {{ 0%,{s:.2f}% {{ width: 0; }} {e_type:.2f}%,100% {{ width: {text_w:.0f}px; }} }}''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .t {{ font: 600 {FS}px "JetBrains Mono", "Fira Code", "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; fill: {RED}; }}
  .p {{ font: 600 {FS}px "JetBrains Mono", "Fira Code", "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; fill: {MUTED}; }}
  .cur {{ animation: blink 1s steps(2,start) infinite; fill: {RED}; }}
  @keyframes blink {{ to {{ visibility: hidden; }} }}{''.join(keyframes)}
</style>
<rect width="100%" height="100%" fill="none"/>{''.join(parts)}
<text x="{W-40}" y="29" class="cur">▌</text>
</svg>
'''
out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "typing.svg"
out.write_text(svg, encoding="utf-8")
print(f"wrote {out} ({len(svg)} bytes)")
