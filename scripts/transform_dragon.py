#!/usr/bin/env python3
import sys
import re
import xml.etree.ElementTree as ET

def transform_to_dragon(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg = f.read()

    # 1. Clean out existing head and custom CSS
    if '<g class="s s0">' in svg:
        svg = re.sub(r'<g class="s s0">.*?(?=<rect class="s s1")', '<rect class="s s0" width="12" height="12" rx="3" ry="3"/>', svg, count=1, flags=re.DOTALL)
    svg = re.sub(r'/\* DRAGON_CSS_START \*/.*?/\* DRAGON_CSS_END \*/', '', svg, flags=re.DOTALL)
    svg = re.sub(r':root\s*\{\s*--cs:\s*#ded39e.*?\}\s*\}', '', svg, flags=re.DOTALL)

    # Remove existing tail rects (s1..s30) to generate unified extending tail
    svg = re.sub(r'<rect class="s s\d+"[^>]*/>', '', svg)
    if '<rect class="s s0"' not in svg:
        svg = svg.replace('</svg>', '<rect class="s s0" width="12" height="12" rx="3" ry="3"/></svg>')

    # Helper to remove old keyframes
    def remove_keyframe(s, name):
        start = s.find(f"@keyframes {name}")
        if start == -1: return s
        brace_open = s.find("{", start)
        count = 1
        idx = brace_open + 1
        while count > 0 and idx < len(s):
            if s[idx] == "{": count += 1
            elif s[idx] == "}": count -= 1
            idx += 1
        return s[:start] + s[idx:]

    for k in range(1, 30):
        svg = remove_keyframe(svg, f"s{k}")

    # Helper to get keyframe block
    def get_block(s, name):
        start = s.find(f"@keyframes {name}")
        brace_open = s.find("{", start)
        count = 1
        idx = brace_open + 1
        while count > 0 and idx < len(s):
            if s[idx] == "{": count += 1
            elif s[idx] == "}": count -= 1
            idx += 1
        return s[brace_open+1:idx-1]

    kf0 = get_block(svg, "s0")
    raw_rules = re.findall(r"([^}]+)\{transform:translate\(([^)]+)\)\}", kf0)

    waypoints = []
    for pcts_str, trans in raw_rules[2:]:
        for p_str in pcts_str.split(","):
            p_val = float(p_str.replace("%", "").strip())
            waypoints.append((p_val, trans))

    waypoints.sort(key=lambda x: x[0])

    DT = 0.253165
    unlock_times = {
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 7.0,
        5: 10.0,
        6: 15.0,
        7: 20.0,
        8: 26.0,
        9: 35.0,
        10: 42.0,
        11: 50.0,
        12: 65.0,
        13: 78.0,
        14: 85.0,
        15: 89.0
    }

    new_css_rules = []
    new_keyframes = []
    new_rects = []

    # Option 2: Cyber-Mecha Wyrm (Aerodynamic Stealth Arrowhead Hull)
    cyber_head = """<g class="s s0">
  <g transform="translate(0, 0)">
    <!-- Aerodynamic Stealth Hull in Obsidian (#0d1117) with Champagne Gold Armor Trims (#ded39e) -->
    <polygon points="6,0 12,10 8,9 6,12 4,9 0,10" fill="#0d1117" stroke="#ded39e" stroke-width="1.2"/>
    <!-- High-Tech Armor Inlays (#544320 with #9b8042 edge) -->
    <polygon points="6,2 10,8 7,7.5 6,9.5 5,7.5 2,8" fill="#544320" stroke="#9b8042" stroke-width="0.6"/>
    <!-- Glowing Neon Visor Eye in Champagne Gold (#ded39e) -->
    <polygon points="3.5,6.5 5.5,5.5 5.5,7 3.5,7.5" fill="#ded39e"/>
    <polygon points="8.5,6.5 6.5,5.5 6.5,7 8.5,7.5" fill="#ded39e"/>
    <!-- Quantum Plasma Core (#ef4444) -->
    <circle cx="6" cy="8" r="1.2" fill="#ef4444">
      <animate attributeName="opacity" values="0.7;1;0.7" dur="1s" repeatCount="indefinite"/>
    </circle>
  </g>
</g>"""

    for k in range(1, 16):
        u_t = unlock_times[k]
        rules_dict = {}

        start_trans = f"{k * 16}px,-16px"
        rules_dict[0.0] = f"transform:translate({start_trans});opacity:{0 if u_t > 0 else 1};"

        if u_t > 0:
            rules_dict[round(u_t - 0.2, 2)] = f"transform:translate({start_trans});opacity:0;"
            rules_dict[round(u_t, 2)] = "opacity:1;"

        t_entry_pre = round((k - 1) * DT + 0.25, 2)
        t_entry = round(k * DT + 0.25, 2)
        rules_dict[t_entry_pre] = "transform:translate(0px,-16px);"
        rules_dict[t_entry] = "transform:translate(0px,0px);"

        for p_val, trans in waypoints:
            p_shifted = round(p_val + k * DT, 2)
            if p_shifted < 99.5:
                rules_dict[p_shifted] = f"transform:translate({trans});"

        t_exit = round(98.73 + k * DT, 2)
        if t_exit < 99.8:
            rules_dict[t_exit] = "transform:translate(64px,-16px);"

        rules_dict[99.75] = f"transform:translate({start_trans});opacity:{0 if u_t > 0 else 1};"
        rules_dict[100.0] = f"transform:translate({start_trans});opacity:{0 if u_t > 0 else 1};"

        sorted_p = sorted(rules_dict.keys())
        kf_inner = "".join([f"{p}%{{{rules_dict[p]}}}" for p in sorted_p])
        new_keyframes.append(f"@keyframes s{k}{{{kf_inner}}}")
        new_css_rules.append(f".s.s{k}{{transform:translate({start_trans});animation-name:s{k};}}")

        # Color gradient down the tail segments
        if k <= 3:
            fill_col = "#ded39e"
            stroke_col = "#9b8042"
            op = 0.95
        elif k <= 7:
            fill_col = "#d4af37"
            stroke_col = "#8c732b"
            op = 0.90
        elif k <= 11:
            fill_col = "#9b8042"
            stroke_col = "#544320"
            op = 0.85
        else:
            fill_col = "#544320"
            stroke_col = "#ded39e"
            op = 0.80

        new_rects.append(f"""<rect class="s s{k}" width="12" height="12" rx="3.5" ry="3.5" fill="{fill_col}" stroke="{stroke_col}" stroke-width="0.8" opacity="{op}"/>""")

    # Replace s0 rect with Cyber Head
    svg = svg.replace('<rect class="s s0" width="12" height="12" rx="3" ry="3"/>', cyber_head)
    # Add new extending tail rects before </svg>
    tail_block = "".join(new_rects)
    svg = svg.replace("</svg>", f"{tail_block}</svg>")

    custom_css = "/* DRAGON_CSS_START */\n"
    custom_css += ":root { --cs: #ded39e !important; }\n"
    custom_css += "".join(new_keyframes) + "\n"
    custom_css += "".join(new_css_rules) + "\n"
    custom_css += "/* DRAGON_CSS_END */\n"

    svg = svg.replace("</style>", custom_css + "</style>")

    # Validate XML before saving!
    try:
        ET.fromstring(svg)
    except Exception as e:
        print(f"ERROR: XML validation failed for {svg_path}: {e}")
        raise e

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Transformed {svg_path} into Cyber-Mecha Wyrm with dynamic extending tail (Snake Game mode)!")

if __name__ == '__main__':
    for path in sys.argv[1:]:
        transform_to_dragon(path)
