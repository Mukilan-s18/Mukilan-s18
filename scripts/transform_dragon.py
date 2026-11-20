#!/usr/bin/env python3
import sys
import re

def transform_to_dragon(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg = f.read()

    # Celestial Azure & Golden Dragon Head
    dragon_element = """<g class="s s0">
  <g transform="translate(-3, -3) scale(1.35)">
    <!-- Dragon Horns (Imperial Gold #ded39e) -->
    <path d="M 3,4 Q 1,0 0,-3 Q 3,-1 4,3" fill="#ded39e" stroke="#b45309" stroke-width="0.4" />
    <path d="M 13,4 Q 15,0 16,-3 Q 13,-1 12,3" fill="#ded39e" stroke="#b45309" stroke-width="0.4" />
    
    <!-- Dragon Head Crown (Deep Azure & Sapphire #0284c7) -->
    <polygon points="4,3 8,1 12,3 15,7 13,13 8,15 3,13 1,7" fill="#0284c7" stroke="#38bdf8" stroke-width="0.6"/>
    
    <!-- Dragon Brow / Crest (#38bdf8) -->
    <path d="M 4,4 Q 8,2 12,4 Q 8,6 4,4" fill="#38bdf8"/>
    
    <!-- Glowing Golden-Amber Dragon Eyes (#ded39e) -->
    <ellipse cx="4.5" cy="7.5" rx="1.8" ry="1.2" fill="#ded39e" />
    <ellipse cx="11.5" cy="7.5" rx="1.8" ry="1.2" fill="#ded39e" />
    
    <!-- Slit Pupils -->
    <line x1="4.5" y1="6.8" x2="4.5" y2="8.2" stroke="#0f172a" stroke-width="0.8" stroke-linecap="round"/>
    <line x1="11.5" y1="6.8" x2="11.5" y2="8.2" stroke="#0f172a" stroke-width="0.8" stroke-linecap="round"/>
    
    <!-- Eye Sparkles -->
    <circle cx="4.2" cy="7.2" r="0.4" fill="#ffffff"/>
    <circle cx="11.2" cy="7.2" r="0.4" fill="#ffffff"/>
    
    <!-- Snout & Nostrils -->
    <rect x="5.5" y="10" width="5" height="4" rx="1.5" fill="#0369a1"/>
    <circle cx="6.8" cy="11.5" r="0.5" fill="#0284c7"/>
    <circle cx="9.2" cy="11.5" r="0.5" fill="#0284c7"/>
    
    <!-- Flowing Celestial Whiskers (Imperial Gold #ded39e) -->
    <path d="M 3,10 Q -2,12 -3,16" fill="none" stroke="#ded39e" stroke-width="0.6" stroke-linecap="round"/>
    <path d="M 13,10 Q 18,12 19,16" fill="none" stroke="#ded39e" stroke-width="0.6" stroke-linecap="round"/>
    
    <!-- Dragon Fangs -->
    <polygon points="5.5,13.5 6.5,13.5 6,15" fill="#ffffff"/>
    <polygon points="9.5,13.5 10.5,13.5 10,15" fill="#ffffff"/>
    
    <!-- Celestial Cyan Breath Sparkle -->
    <circle cx="8" cy="16" r="1.5" fill="#38bdf8" opacity="0.8">
      <animate attributeName="r" values="1;2.2;1" dur="0.8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.9;0.3;0.9" dur="0.8s" repeatCount="indefinite"/>
    </circle>
  </g>
</g>"""

    # Replace s0 with the standalone Celestial Dragon
    svg = re.sub(r'<rect class="s s0"[^>]*/>', dragon_element, svg)
    # Remove body segments to keep a clean, elegant dragon runner
    svg = re.sub(r'<rect class="s s1"[^>]*/>', '', svg)
    svg = re.sub(r'<rect class="s s2"[^>]*/>', '', svg)
    svg = re.sub(r'<rect class="s s3"[^>]*/>', '', svg)

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Transformed {svg_path} into Celestial Dragon Runner!")

if __name__ == '__main__':
    for path in sys.argv[1:]:
        transform_to_dragon(path)
