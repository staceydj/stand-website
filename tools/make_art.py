"""Generate STAND's original line icons and decorative line art as SVG files.

Run: python3 tools/make_art.py
Writes into assets/art/. Every drawing here is new; nothing is traced from the original site.
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'art')
os.makedirs(OUT, exist_ok=True)

DEEP = '#0A4B57'
TEAL = '#0F6A78'
TURQ = '#00CFEA'
GREY = '#C7D0D6'
CHAR = '#2F4A52'

# ---------------------------------------------------------------- icons (64x64, stroke drawings)
ICONS = {
    # navigation: Your concerns
    'strategy': '<circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="13"/><circle cx="32" cy="32" r="4"/><path d="M32 4v10M32 50v10M4 32h10M50 32h10"/>',
    'culture': '<circle cx="20" cy="22" r="7"/><circle cx="44" cy="22" r="7"/><path d="M8 50c0-9 5-15 12-15s12 6 12 15"/><path d="M32 50c0-9 5-15 12-15s12 6 12 15"/><path d="M26 56h12"/>',
    'guidance': '<path d="M32 6v52"/><path d="M14 14h28l8 7-8 7H14z"/><path d="M50 34H24l-8 7 8 7h26z"/><path d="M24 58h16"/>',
    'sustainability': '<path d="M12 52C12 26 30 12 54 10c0 26-14 42-38 42"/><path d="M12 52l26-26"/><path d="M24 40h12M30 34v-8"/>',
    # navigation: Accompaniment
    'transformation': '<path d="M50 24A20 20 0 0 0 14 22"/><path d="M14 10v12h12"/><path d="M14 40a20 20 0 0 0 36 2"/><path d="M50 54V42H38"/><circle cx="32" cy="32" r="5"/>',
    'workshop': '<rect x="12" y="8" width="40" height="30" rx="2"/><path d="M32 38v8M22 58l10-12 10 12"/><path d="M19 30l9-9 6 6 11-11"/>',
    'groups': '<circle cx="32" cy="18" r="7"/><circle cx="14" cy="28" r="6"/><circle cx="50" cy="28" r="6"/><path d="M20 54c0-10 5-17 12-17s12 7 12 17"/><path d="M4 52c0-8 4-13 10-13 3 0 5 1 7 3"/><path d="M60 52c0-8-4-13-10-13-3 0-5 1-7 3"/>',
    'conflict': '<path d="M6 12h30v20H18l-8 7v-7H6z"/><path d="M28 30v8h18l8 7v-7h4V22h-12"/><path d="M14 22h14"/>',
    'coaching': '<circle cx="20" cy="18" r="7"/><circle cx="46" cy="24" r="6"/><path d="M8 54c0-11 5-19 12-19 4 0 7 2 9 5"/><path d="M36 54c0-9 4-15 10-15s10 6 10 15"/><path d="M30 10h14v8h-4l-4 4v-4h-6z"/>',
    # navigation: Resources
    'book': '<path d="M32 16c-6-5-15-6-24-4v38c9-2 18-1 24 4 6-5 15-6 24-4V12c-9-2-18-1-24 4z"/><path d="M32 16v38"/><path d="M14 22c4-1 8-1 12 1M14 30c4-1 8-1 12 1M38 23c4-2 8-2 12-1M38 31c4-2 8-2 12-1"/>',
    'media': '<rect x="6" y="12" width="52" height="34" rx="4"/><path d="M27 21l12 8-12 8z"/><path d="M22 54h20M32 46v8"/>',
    'digital': '<rect x="18" y="4" width="28" height="56" rx="5"/><path d="M28 10h8M30 52h4"/><path d="M24 22h16M24 30h16M24 38h10"/>',
    'newsletter': '<rect x="6" y="14" width="52" height="36" rx="3"/><path d="M6 17l26 19 26-19"/><path d="M6 47l19-15M58 47L39 32"/>',
    # card icons
    'puzzle': '<path d="M10 22h12a5 5 0 1 1 10 0h12v12a5 5 0 1 0 0 10v12H32a5 5 0 1 0-10 0H10V44a5 5 0 1 1 0-10z"/>',
    'rocket': '<path d="M32 4c10 8 14 20 12 34H20C18 24 22 12 32 4z"/><circle cx="32" cy="22" r="5"/><path d="M20 38l-8 10 10-2M44 38l8 10-10-2"/><path d="M26 44l2 12 4-6 4 6 2-12"/>',
    'map': '<path d="M6 14l16-6 20 6 16-6v42l-16 6-20-6-16 6z"/><path d="M22 8v42M42 14v42"/><path d="M12 36c6-6 12 2 18-6s12 0 18-8" stroke-dasharray="3 4"/><path d="M45 18l6 6M51 18l-6 6"/>',
    'bulb': '<path d="M22 40c-6-4-10-10-10-17a20 20 0 0 1 40 0c0 7-4 13-10 17v6H22z"/><path d="M24 52h16M27 58h10"/><path d="M28 40V30l4 4 4-4v10"/>',
    'tent': '<path d="M4 54h56"/><path d="M8 54L32 12l24 42"/><path d="M32 12v42M24 54l8-16 8 16"/><path d="M32 12l-4-6M32 12l4-6"/>',
    'fire': '<path d="M32 46c-8 0-12-5-12-11 0-8 8-12 8-20 6 4 6 10 6 10s2-3 2-7c6 5 8 11 8 17 0 6-4 11-12 11z"/><path d="M10 56l44-8M10 48l44 8"/>',
    'notes': '<rect x="10" y="6" width="34" height="48" rx="3"/><path d="M18 18h18M18 26h18M18 34h12"/><path d="M50 22l6 6-18 18-8 2 2-8z"/>',
    'backpack': '<path d="M16 22c0-8 7-12 16-12s16 4 16 12v32a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4z"/><path d="M26 10V6h12v4"/><rect x="22" y="34" width="20" height="14" rx="2"/><path d="M22 40h20M16 28h32"/>',
    'news': '<path d="M8 10h40v42a4 4 0 0 1-4 4H12a4 4 0 0 1-4-4z"/><path d="M48 20h8v32a4 4 0 0 1-8 0"/><rect x="14" y="16" width="28" height="10"/><path d="M14 32h28M14 38h28M14 44h18"/>',
}


def icon(name, color, width=2.4):
    body = ICONS[name]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


for n in ICONS:
    with open(os.path.join(OUT, f'icon-{n}.svg'), 'w') as f:
        f.write(icon(n, DEEP))
    with open(os.path.join(OUT, f'icon-{n}-light.svg'), 'w') as f:
        f.write(icon(n, '#ffffff'))

# ---------------------------------------------------------------- dashed journey paths


def dashed(path, w, h, name, color=TURQ):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none">'
           f'<path d="{path}" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-dasharray="12 10"/></svg>')
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(svg)


# services: swoops down from the top-left with one loop
dashed('M60 0C40 120 120 220 230 250C330 278 360 200 300 180C220 150 120 260 70 360C40 420 30 480 40 560', 400, 560, 'path-services.svg')
# offers: winding line down the right side
dashed('M30 0C140 40 230 120 200 220C170 320 60 330 90 430C110 500 180 520 160 600', 260, 600, 'path-offers.svg')

# ---------------------------------------------------------------- line-art backdrops
random.seed(7)


def ridge_lines(w, h, n, base, amp, color, opacity, name, stroke=1.2):
    paths = []
    for i in range(n):
        y0 = base + i * (h - base) / n
        pts = []
        x = 0
        peaks = [(random.uniform(0, w), random.uniform(0.4, 1.0)) for _ in range(4)]
        while x <= w:
            y = y0
            for px, s in peaks:
                y -= amp * s * math.exp(-((x - px) / (w * 0.12)) ** 2) * (1 - i / (n + 2))
            y += math.sin(x / 37 + i) * 3
            pts.append(f'{x:.0f},{y:.0f}')
            x += 12
        paths.append(f'<polyline points="{" ".join(pts)}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none" stroke="{color}" '
           f'stroke-width="{stroke}" opacity="{opacity}" stroke-linejoin="round">{"".join(paths)}</svg>')
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(svg)


# behind the signpost: contour ridges
ridge_lines(1600, 820, 9, 330, 300, TEAL, 0.35, 'contours-signs.svg')
# footer backdrop
ridge_lines(1200, 500, 7, 220, 200, TEAL, 0.4, 'contours-footer.svg', stroke=1.4)


# CTA backdrop: a hand-drawn style route map with markers
def route_map(name):
    w, h = 1600, 1200
    parts = []
    # contour blobs
    for cx, cy, r in [(260, 260, 120), (1250, 300, 150), (900, 820, 130), (380, 860, 110), (1400, 900, 90)]:
        for k in range(3):
            rr = r - k * 28
            pts = []
            for a in range(0, 361, 15):
                t = math.radians(a)
                j = 1 + 0.12 * math.sin(3 * t + k) + 0.06 * math.cos(5 * t)
                pts.append(f'{cx + rr * j * math.cos(t):.0f},{cy + rr * 0.75 * j * math.sin(t):.0f}')
            parts.append(f'<polyline points="{" ".join(pts)}"/>')
    # dotted trail
    parts.append('<path d="M80 1100C300 900 200 700 500 640S900 700 1000 520 1300 260 1520 120" stroke-dasharray="4 10"/>')
    # markers: crosses, little peaks and a star
    for x, y in [(520, 640), (1010, 520), (1500, 130)]:
        parts.append(f'<path d="M{x-14} {y-14}l28 28M{x+14} {y-14}l-28 28"/>')
    for x, y in [(700, 260), (760, 300), (1150, 1000), (200, 560)]:
        parts.append(f'<path d="M{x-30} {y+20}l20-34 12 18 10-12 18 28z"/>')
    parts.append('<path d="M120 120v60M90 150h60M100 130l20-10 20 10M100 170l20 10 20-10"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none" stroke="{TEAL}" '
           f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{"".join(parts)}</svg>')
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(svg)


route_map('route-map.svg')
print('wrote', len(os.listdir(OUT)), 'files to', os.path.abspath(OUT))
