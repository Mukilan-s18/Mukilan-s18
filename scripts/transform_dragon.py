#!/usr/bin/env python3
import sys
import re

def transform_to_dragon(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg = f.read()

    # Champagne Gold & Obsidian Dragon Head (#ded39e, #9b8042, #544320, #0d1117)
    dragon_head = """<g class="s s0">
  <g transform="translate(-3, -3) scale(1.35)">
    <!-- Dragon Horns (Champagne Gold #ded39e) -->
    <path d="M 3,4 Q 1,0 0,-3 Q 3,-1 4,3" fill="#ded39e" stroke="#9b8042" stroke-width="0.5" />
    <path d="M 13,4 Q 15,0 16,-3 Q 13,-1 12,3" fill="#ded39e" stroke="#9b8042" stroke-width="0.5" />
    
    <!-- Dragon Head Crown (Deep Gold #9b8042 & Obsidian Umber #544320) -->
    <polygon points="4,3 8,1 12,3 15,7 13,13 8,15 3,13 1,7" fill="#9b8042" stroke="#544320" stroke-width="0.6"/>
    
    <!-- Dragon Crest (#ded39e) -->
    <path d="M 4,4 Q 8,2 12,4 Q 8,6 4,4" fill="#ded39e"/>
    
    <!-- Glowing Champagne Gold Dragon Eyes (#ded39e) -->
    <ellipse cx="4.5" cy="7.5" rx="1.8" ry="1.2" fill="#ded39e" />
    <ellipse cx="11.5" cy="7.5" rx="1.8" ry="1.2" fill="#ded39e" />
    
    <!-- Slit Pupils -->
    <line x1="4.5" y1="6.8" x2="4.5" y2="8.2" stroke="#0d1117" stroke-width="0.8" stroke-linecap="round"/>
    <line x1="11.5" y1="6.8" x2="11.5" y2="8.2" stroke="#0d1117" stroke-width="0.8" stroke-linecap="round"/>
    
    <!-- Eye Sparkles -->
    <circle cx="4.2" cy="7.2" r="0.4" fill="#ffffff"/>
    <circle cx="11.2" cy="7.2" r="0.4" fill="#ffffff"/>
    
    <!-- Snout & Nostrils (Obsidian Umber #544320) -->
    <rect x="5.5" y="10" width="5" height="4" rx="1.5" fill="#544320"/>
    <circle cx="6.8" cy="11.5" r="0.5" fill="#9b8042"/>
    <circle cx="9.2" cy="11.5" r="0.5" fill="#9b8042"/>
    
    <!-- Flowing Golden Whiskers (#ded39e) -->
    <path d="M 3,10 Q -2,12 -3,16" fill="none" stroke="#ded39e" stroke-width="0.6" stroke-linecap="round"/>
    <path d="M 13,10 Q 18,12 19,16" fill="none" stroke="#ded39e" stroke-width="0.6" stroke-linecap="round"/>
    
    <!-- Dragon Fangs -->
    <polygon points="5.5,13.5 6.5,13.5 6,15" fill="#ffffff"/>
    <polygon points="9.5,13.5 10.5,13.5 10,15" fill="#ffffff"/>
    
    <!-- Celestial Golden Fire Breath Sparkle -->
    <circle cx="8" cy="16" r="1.5" fill="#ded39e" opacity="0.85">
      <animate attributeName="r" values="1;2.2;1" dur="0.8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.9;0.3;0.9" dur="0.8s" repeatCount="indefinite"/>
    </circle>
  </g>
</g>"""

    # Replace s0 with dragon head
    if '<g class="s s0">' in svg:
        svg = re.sub(r'<g class="s s0">.*?</g>\s*</g>', dragon_head, svg, count=1, flags=re.DOTALL)
    elif '<rect class="s s0"' in svg:
        svg = re.sub(r'<rect class="s s0"[^>]*/>', dragon_head, svg, count=1)

    # Ensure body segments s1, s2, s3 (the extending tail) exist!
    tail_segments = """<rect class="s s1" x="0" y="0" width="12" height="12" rx="3.5" ry="3.5"/>
<rect class="s s2" x="0" y="0" width="12" height="12" rx="3.5" ry="3.5"/>
<rect class="s s3" x="0" y="0" width="12" height="12" rx="3.5" ry="3.5"/>"""

    if 'class="s s1"' not in svg:
        svg = svg.replace('</svg>', tail_segments + '\n</svg>')

    # Style the dragon body and tail segments with the Champagne Gold & Obsidian theme
    dragon_css = """
    :root {
      --cs: #ded39e !important; /* Champagne Gold */
    }
    .s {
      shape-rendering: geometricPrecision;
      fill: #ded39e !important;
      stroke: #9b8042 !important;
      stroke-width: 0.8px;
    }
    .s.s1 {
      fill: #ded39e !important;
      stroke: #9b8042 !important;
    }
    .s.s2 {
      fill: #cbbd84 !important;
      stroke: #544320 !important;
    }
    .s.s3 {
      fill: #9b8042 !important;
      stroke: #0d1117 !important;
    }
    """
    svg = svg.replace('</style>', dragon_css + '\n</style>')

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Transformed {svg_path} into Champagne Gold Dragon with extending tail!")

if __name__ == '__main__':
    for path in sys.argv[1:]:
        transform_to_dragon(path)
