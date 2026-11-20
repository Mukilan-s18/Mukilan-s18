#!/usr/bin/env python3
import sys
import os
import re
import urllib.request
import datetime

def fetch_base_svg():
    timestamp = int(datetime.datetime.now().timestamp())
    url = f"https://github-readme-activity-graph.ashutosh-dwivedi0710.workers.dev/graph?username=Mukilan-s18&theme=tokyo-night&bg_color=0d1117&color=ded39e&line=ded39e&point=9b8042&area=true&hide_border=true&_={timestamp}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        print(f"Primary worker failed: {e}, trying vercel fallback...")
        url_fallback = f"https://github-readme-activity-graph.vercel.app/graph?username=Mukilan-s18&theme=tokyo-night&bg_color=0d1117&color=ded39e&line=ded39e&point=9b8042&area=true&hide_border=true&_={timestamp}"
        req_fallback = urllib.request.Request(url_fallback, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_fallback, timeout=15) as resp:
            return resp.read().decode('utf-8')

def sanitize_svg_header(svg):
    """Replace foreignObject with standard SVG text to avoid WebKit/Camo issues."""
    svg = re.sub(
        r'<foreignObject[^>]*>.*?<h1[^>]*>(.*?)</h1>.*?</foreignObject>',
        r'<text x="600" y="38" text-anchor="middle" fill="#ded39e" font-size="20" font-weight="600" font-family="\'Segoe UI\', Ubuntu, -apple-system, BlinkMacSystemFont, sans-serif">\1</text>',
        svg,
        flags=re.DOTALL
    )
    return svg

def clarify_timeline_labels(svg):
    """
    Clarifies the x-axis timeline with explicit month milestone labels
    (Oct 21 -> Nov 1 -> Nov 20) in Champagne Gold (#ded39e).
    """
    def replace_label(match):
        attrs = match.group(1)
        day_str = match.group(2).strip()
        
        label_map = {
            "21": "Oct 21",
            "25": "Oct 25",
            "1": "Nov 1",
            "5": "Nov 5",
            "10": "Nov 10",
            "15": "Nov 15",
            "20": "Nov 20",
        }
        
        new_text = label_map.get(day_str, day_str)
        if " " in new_text:
            return f'<text {attrs} font-weight="700" fill="#ded39e">{new_text}</text>'
        return f'<text {attrs} fill="#9b8042">{new_text}</text>'

    svg = re.sub(
        r'<text ([^>]*?class="ct-label ct-horizontal ct-end"[^>]*)>([^<]+)</text>',
        replace_label,
        svg
    )
    svg = re.sub(r'(class="ct-axis-title ct-label"[^>]*)>', r'\g<1> fill="#ded39e">', svg)
    return svg

def get_line_path(svg):
    m = re.search(r'<path[^>]*class="ct-line"[^>]*d="([^"]+)"', svg)
    if not m:
        m = re.search(r'<path[^>]*d="([^"]+)"[^>]*class="ct-line"', svg)
    return m.group(1) if m else ""

def generate_animated_svg(raw_base_svg, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    svg = sanitize_svg_header(raw_base_svg)
    svg = clarify_timeline_labels(svg)
    line_path = get_line_path(svg)

    defs = """<defs>
  <!-- Champagne Gold & Obsidian Gradient (#0d1117 -> #544320 -> #9b8042 -> #ded39e) -->
  <linearGradient id="champagneGoldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#ded39e" stop-opacity="0.55">
      <animate attributeName="stop-color" values="#ded39e;#9b8042;#544320;#ded39e" dur="7s" repeatCount="indefinite" />
      <animate attributeName="stop-opacity" values="0.35;0.65;0.35" dur="3s" repeatCount="indefinite" />
    </stop>
    <stop offset="45%" stop-color="#9b8042" stop-opacity="0.35">
      <animate attributeName="stop-color" values="#9b8042;#544320;#9b8042" dur="7s" repeatCount="indefinite" />
    </stop>
    <stop offset="85%" stop-color="#544320" stop-opacity="0.15" />
    <stop offset="100%" stop-color="#0d1117" stop-opacity="0.0" />
  </linearGradient>

  <!-- Champagne Gold Neon Glow Filter -->
  <filter id="goldNeonGlow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3.5" result="blur" />
    <feMerge>
      <feMergeNode in="blur" />
      <feMergeNode in="SourceGraphic" />
    </feMerge>
  </filter>

  <!-- Sparkle Filter -->
  <filter id="sparkleGlow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="2.5" result="blur" />
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
      fill: url(#champagneGoldGrad) !important;
    }
    .ct-series-a .ct-line {
      stroke: #ded39e !important;
      stroke-width: 3.5px !important;
      filter: url(#goldNeonGlow) !important;
    }
    .ct-series-a .ct-point {
      stroke: #9b8042 !important;
      stroke-linecap: round !important;
    }
    .ct-label.ct-vertical {
      fill: #9b8042 !important;
    }
    .ct-grid.ct-horizontal, .ct-grid.ct-vertical {
      stroke: #262014 !important;
      stroke-dasharray: 2, 4 !important;
      opacity: 0.65 !important;
    }
    """
    svg = svg.replace('</style>', css + '\n</style>')

    # Animate point nodes with breathing glow
    point_anim = (
        '<animate attributeName="stroke-width" values="6;13;6" dur="1.8s" repeatCount="indefinite" />'
        '<animate attributeName="stroke-opacity" values="0.6;1;0.6" dur="1.8s" repeatCount="indefinite" />'
        '<animate attributeName="stroke" values="#9b8042;#ded39e;#9b8042" dur="3s" repeatCount="indefinite" />'
    )
    svg = re.sub(r'(<line[^>]*?class="ct-point"[^>]*?>)(</line>)', r'\g<1>' + point_anim + r'\g<2>', svg)

    # Dynamic elements: Summit Sparkles & Golden Dragon Comet Particle
    dynamic_elements = f"""<g>
  <!-- Peak Milestone 1: Day 21 (x=90, y=80) Champagne Gold Sparkle Star -->
  <g transform="translate(90, 68)">
    <g filter="url(#goldNeonGlow)">
      <path d="M 0,-14 Q 0,0 14,0 Q 0,0 0,14 Q 0,0 -14,0 Q 0,0 0,-14 Z" fill="#ded39e" opacity="0.95">
        <animateTransform attributeName="transform" type="rotate" values="0;360" dur="8s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.6;1;0.6" dur="1.8s" repeatCount="indefinite" />
      </path>
      <circle r="4" fill="#ffffff" />
      <circle r="8" fill="#ded39e" opacity="0.35">
        <animate attributeName="r" values="6;12;6" dur="1.8s" repeatCount="indefinite" />
      </circle>
    </g>
  </g>

  <!-- Peak Milestone 2: Today Nov 20 (x=1150, y=140) Summit Sparkle Star -->
  <g transform="translate(1150, 126)">
    <g filter="url(#sparkleGlow)">
      <path d="M 0,-12 Q 0,0 12,0 Q 0,0 0,12 Q 0,0 -12,0 Q 0,0 0,-12 Z" fill="#ded39e" opacity="0.95">
        <animateTransform attributeName="transform" type="rotate" values="360;0" dur="6s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.7;1;0.7" dur="1.5s" repeatCount="indefinite" />
      </path>
      <circle r="3.5" fill="#ffffff" />
      <circle r="7" fill="#9b8042" opacity="0.4">
        <animate attributeName="r" values="5;10;5" dur="1.5s" repeatCount="indefinite" />
      </circle>
    </g>
  </g>

  <!-- Champagne Gold Dragon Comet Particle Riding along the timeline -->
  <g filter="url(#goldNeonGlow)">
    <circle r="12" fill="#ded39e" opacity="0.25">
      <animate attributeName="r" values="8;14;8" dur="1.2s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.15;0.4;0.15" dur="1.2s" repeatCount="indefinite" />
    </circle>
    <!-- Champagne Gold Core #ded39e -->
    <circle r="5.5" fill="#ded39e" />
    <circle r="3" fill="#ffffff" />
    <!-- Dragon Whiskers Trail in #9b8042 -->
    <line x1="-8" y1="-3" x2="-2" y2="0" stroke="#9b8042" stroke-width="1.2" stroke-linecap="round"/>
    <line x1="-8" y1="3" x2="-2" y2="0" stroke="#9b8042" stroke-width="1.2" stroke-linecap="round"/>
    <animateMotion path="{line_path}" dur="4.5s" repeatCount="indefinite" rotate="auto" />
  </g>
</g>"""

    svg = svg.replace('</svg>', dynamic_elements + '\n</svg>')

    out_file = os.path.join(out_dir, "activity-graph.svg")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Mukilan's Animated Activity Graph generated successfully at {out_file}!")

if __name__ == '__main__':
    base = fetch_base_svg()
    out = sys.argv[1] if len(sys.argv) > 1 else "github-metrics"
    generate_animated_svg(base, out)
