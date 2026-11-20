#!/usr/bin/env python3
import sys
import re
import xml.etree.ElementTree as ET

def transform_to_dragon(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg = f.read()

    # Celestial Golden Dragon Head with swept-back horns, wings, ruby eyes, dorsal scales, and breathing golden fire trail
    dragon_head = """<g class="s s0">
  <g transform="translate(-5, -5) scale(1.45)">
    <!-- Swept-back Wings (Champagne Gold #ded39e with Deep Bronze #9b8042 struts) -->
    <path d="M 1,6 Q -6,1 -10,-4 Q -5,1 0,3" fill="#ded39e" stroke="#9b8042" stroke-width="0.6" opacity="0.95"/>
    <path d="M 15,6 Q 22,1 26,-4 Q 21,1 16,3" fill="#ded39e" stroke="#9b8042" stroke-width="0.6" opacity="0.95"/>
    
    <!-- Swept-back Champagne Horns (#ded39e) -->
    <path d="M 3,4 Q -1,-1 -3,-8 Q 1,-4 4,2" fill="#ded39e" stroke="#9b8042" stroke-width="0.6" />
    <path d="M 13,4 Q 17,-1 19,-8 Q 15,-4 12,2" fill="#ded39e" stroke="#9b8042" stroke-width="0.6" />
    
    <!-- Dragon Head Crown & Scales (Deep Gold #9b8042 & Obsidian Umber #544320) -->
    <polygon points="4,3 8,1 12,3 15,7 13,13 8,15 3,13 1,7" fill="#9b8042" stroke="#544320" stroke-width="0.6"/>
    
    <!-- Dorsal Scales along Central Crest Ridge -->
    <polygon points="8,-1 6.5,2 9.5,2" fill="#ded39e" stroke="#9b8042" stroke-width="0.4"/>
    <polygon points="8,2 6.5,5 9.5,5" fill="#ded39e" stroke="#9b8042" stroke-width="0.4"/>
    <polygon points="8,5 6.5,8 9.5,8" fill="#ded39e" stroke="#9b8042" stroke-width="0.4"/>
    
    <!-- Glowing Ruby Eyes (#ef4444) -->
    <ellipse cx="4.5" cy="7.5" rx="1.9" ry="1.3" fill="#ef4444">
      <animate attributeName="opacity" values="0.85;1;0.85" dur="1.2s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="11.5" cy="7.5" rx="1.9" ry="1.3" fill="#ef4444">
      <animate attributeName="opacity" values="0.85;1;0.85" dur="1.2s" repeatCount="indefinite"/>
    </ellipse>
    
    <!-- Slit Pupils (#0d1117) -->
    <line x1="4.5" y1="6.5" x2="4.5" y2="8.5" stroke="#0d1117" stroke-width="0.8" stroke-linecap="round"/>
    <line x1="11.5" y1="6.5" x2="11.5" y2="8.5" stroke="#0d1117" stroke-width="0.8" stroke-linecap="round"/>
    
    <!-- Ruby Eye Sparkles -->
    <circle cx="4.1" cy="7.0" r="0.45" fill="#ffffff"/>
    <circle cx="11.1" cy="7.0" r="0.45" fill="#ffffff"/>
    
    <!-- Snout & Nostrils (Obsidian Umber #544320) -->
    <rect x="5.5" y="10" width="5" height="4" rx="1.5" fill="#544320"/>
    <circle cx="6.8" cy="11.5" r="0.5" fill="#9b8042"/>
    <circle cx="9.2" cy="11.5" r="0.5" fill="#9b8042"/>
    
    <!-- Flowing Golden Whiskers (#ded39e) -->
    <path d="M 3,10 Q -2,12 -4,16" fill="none" stroke="#ded39e" stroke-width="0.6" stroke-linecap="round"/>
    <path d="M 13,10 Q 18,12 20,16" fill="none" stroke="#ded39e" stroke-width="0.6" stroke-linecap="round"/>
    
    <!-- Dragon Fangs -->
    <polygon points="5.5,13.5 6.5,13.5 6,15" fill="#ffffff"/>
    <polygon points="9.5,13.5 10.5,13.5 10,15" fill="#ffffff"/>
    
    <!-- Animated Breathing Golden Fire Trail (#ded39e) -->
    <g transform="translate(8, 15)">
      <path d="M 0,0 Q -2.5,3 0,6 Q 2.5,3 0,0" fill="#ded39e" opacity="0.95">
        <animate attributeName="d" values="M 0,0 Q -2,3 0,6 Q 2,3 0,0; M 0,0 Q -4,5 0,11 Q 4,5 0,0; M 0,0 Q -2,3 0,6 Q 2,3 0,0" dur="0.8s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.95;0.4;0.95" dur="0.8s" repeatCount="indefinite"/>
      </path>
      <circle cx="0" cy="4" r="1.5" fill="#ffffff">
        <animate attributeName="r" values="1;2.4;1" dur="0.8s" repeatCount="indefinite"/>
      </circle>
    </g>
  </g>
</g>"""

    # Ensure body segments s1, s2, s3 (the extending tail) exist
    tail_segments = """<rect class="s s1" width="12" height="12" rx="3.5" ry="3.5"/><rect class="s s2" width="12" height="12" rx="3.5" ry="3.5"/><rect class="s s3" width="12" height="12" rx="3.5" ry="3.5"/>"""

    # If s1 is not present, add tail segments before </svg>
    if '<rect class="s s1"' not in svg:
        svg = svg.replace('</svg>', f'{tail_segments}</svg>')

    # Replace s0 with dragon head
    if '<g class="s s0">' in svg:
        svg = re.sub(r'<g class="s s0">.*?(?=<rect class="s s1")', dragon_head, svg, count=1, flags=re.DOTALL)
    elif '<rect class="s s0"' in svg:
        svg = re.sub(r'<rect class="s s0"[^>]*/>', dragon_head, svg, count=1)

    # Clean existing custom CSS blocks
    svg = re.sub(r'/\* DRAGON_CSS_START \*/.*?/\* DRAGON_CSS_END \*/', '', svg, flags=re.DOTALL)
    svg = re.sub(r':root\s*\{\s*--cs:\s*#ded39e.*?\}\s*\}', '', svg, flags=re.DOTALL)

    # Style the dragon body and tail segments with the Champagne Gold & Obsidian theme
    dragon_css = """/* DRAGON_CSS_START */
    :root {
      --cs: #ded39e !important; /* Animated Breathing Golden Fire Trail */
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
    /* DRAGON_CSS_END */"""

    svg = svg.replace('</style>', dragon_css + '\n</style>')

    # Validate XML before saving!
    try:
        ET.fromstring(svg)
    except Exception as e:
        print(f"ERROR: XML validation failed for {svg_path}: {e}")
        raise e

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Transformed {svg_path} into Celestial Golden Dragon with swept-back horns, wings, ruby eyes, dorsal scales, and breathing fire trail!")

if __name__ == '__main__':
    for path in sys.argv[1:]:
        transform_to_dragon(path)
