#!/usr/bin/env python3
import sys
import os
import re
import urllib.request
import datetime
import xml.etree.ElementTree as ET

def fetch_base_svg():
    timestamp = int(datetime.datetime.now().timestamp())
    url = f"https://github-readme-activity-graph.ashutosh-dwivedi0710.workers.dev/graph?username=Mukilan-s18&theme=tokyo-night&bg_color=0d1117&color=ded39e&line=ded39e&point=9b8042&area=true&hide_border=true&custom_title=Mukilan%20S%27s%20Activity%20Graph&_={timestamp}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        print(f"Primary worker failed: {e}, trying vercel fallback...")
        url_fallback = f"https://github-readme-activity-graph.vercel.app/graph?username=Mukilan-s18&theme=tokyo-night&bg_color=0d1117&color=ded39e&line=ded39e&point=9b8042&area=true&hide_border=true&custom_title=Mukilan%20S%27s%20Activity%20Graph&_={timestamp}"
        req_fallback = urllib.request.Request(url_fallback, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_fallback, timeout=15) as resp:
            return resp.read().decode('utf-8')

def sanitize_svg_header(svg):
    """Replace foreignObject with standard SVG text to avoid WebKit/Camo issues."""
    title_text = '<text x="600" y="38" text-anchor="middle" fill="#ded39e" font-size="20" font-weight="700" font-family="Segoe UI, Ubuntu, sans-serif">\\1</text>'
    svg = re.sub(
        r'<foreignObject[^>]*>.*?<h1[^>]*>(.*?)</h1>.*?</foreignObject>',
        title_text,
        svg,
        flags=re.DOTALL
    )
    return svg

def generate_animated_svg(raw_base_svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    svg = sanitize_svg_header(raw_base_svg)

    defs = """<defs>
  <!-- Champagne Gold & Obsidian Gradient with breathing opacity -->
  <linearGradient id="animatedAreaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#ded39e" stop-opacity="0.5">
      <animate attributeName="stop-opacity" values="0.25;0.6;0.25" dur="3s" repeatCount="indefinite" />
    </stop>
    <stop offset="50%" stop-color="#9b8042" stop-opacity="0.25">
      <animate attributeName="stop-opacity" values="0.1;0.35;0.1" dur="3s" repeatCount="indefinite" />
    </stop>
    <stop offset="85%" stop-color="#544320" stop-opacity="0.1" />
    <stop offset="100%" stop-color="#0d1117" stop-opacity="0.0" />
  </linearGradient>

  <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3.5" result="blur" />
    <feMerge>
      <feMergeNode in="blur" />
      <feMergeNode in="SourceGraphic" />
    </feMerge>
  </filter>
</defs>"""

    # Inject Defs
    svg = re.sub(r'(<svg[^>]*>)', r'\1\n' + defs, svg, count=1)

    # Base CSS with Champagne Gold & Obsidian Styling
    css = """
    .ct-series-a .ct-area {
      fill: url(#animatedAreaGrad) !important;
    }
    .ct-series-a .ct-line {
      stroke: #ded39e !important;
      stroke-width: 3.5px !important;
      filter: drop-shadow(0 0 6px rgba(222, 211, 158, 0.8)) !important;
      stroke-linecap: round !important;
      stroke-linejoin: round !important;
    }
    .ct-series-a .ct-point {
      stroke: #9b8042 !important;
      fill: #ffffff !important;
      filter: drop-shadow(0 0 4px #ded39e) !important;
    }
    .ct-label {
      fill: #ded39e !important;
      color: #ded39e !important;
      font-weight: 500 !important;
    }
    .ct-grid {
      stroke: #262014 !important;
      stroke-dasharray: 2, 4 !important;
      opacity: 0.65 !important;
    }
    """
    svg = svg.replace('</style>', css + '\n</style>')

    # Inject continuous traveling laser pulse animation into .ct-line (Effect #4)
    line_anim = (
        ' stroke-dasharray="24, 12, 6, 12"'
        '>'
        '<animate attributeName="stroke-dashoffset" from="0" to="-108" dur="2s" repeatCount="indefinite" />'
        '<animate attributeName="stroke-width" values="3.2;4.2;3.2" dur="2s" repeatCount="indefinite" />'
    )
    svg = re.sub(r'(<path[^>]*?class="ct-line"[^>]*?)>', r'\g<1>' + line_anim, svg)

    # Inject pulsing radius/stroke-width on every data point (.ct-point)
    point_anim = (
        '<animate attributeName="stroke-width" values="6;13;6" dur="1.8s" repeatCount="indefinite" />'
        '<animate attributeName="stroke-opacity" values="0.6;1;0.6" dur="1.8s" repeatCount="indefinite" />'
    )
    svg = re.sub(r'(<line[^>]*?class="ct-point"[^>]*?>)(</line>)', r'\g<1>' + point_anim + r'\g<2>', svg)

    # Validate XML
    ET.fromstring(svg)

    out_file = os.path.join(out_dir, "activity-graph.svg")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Mukilan's Animated Activity Graph generated successfully at {out_file}!")

if __name__ == '__main__':
    base = fetch_base_svg()
    out = sys.argv[1] if len(sys.argv) > 1 else "github-metrics"
    generate_animated_svg(base, out)
