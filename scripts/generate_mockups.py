from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'images'
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 1000
FONT_DIR = '/usr/share/fonts/truetype/dejavu'
REG = f'{FONT_DIR}/DejaVuSans.ttf'
BOLD = f'{FONT_DIR}/DejaVuSans-Bold.ttf'
MONO = f'{FONT_DIR}/DejaVuSansMono.ttf'

VARIANTS = [
    ('neon-gold', 'Neon Gold', '#f2c94c', '#fff4c7', '#2e2510'),
    ('cyber-pink', 'Cyber Pink', '#ff4da6', '#ffd6e9', '#351326'),
    ('electric-blue', 'Electric Blue', '#24b8ff', '#ccefff', '#102a38'),
    ('vibrant-emerald', 'Vibrant Emerald', '#20c997', '#c9f7e9', '#0d3027'),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size=22, fill='#e8edf3', bold=False, anchor=None):
    draw.text(xy, value, font=font(BOLD if bold else REG, size), fill=fill, anchor=anchor)


def wrapped(draw, xy, value, width, size, fill, line_gap=10):
    f = font(REG, size)
    words, lines, line = value.split(), [], ''
    for word in words:
        candidate = f'{line} {word}'.strip()
        if draw.textlength(candidate, font=f) <= width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    x, y = xy
    for item in lines:
        draw.text((x, y), item, font=f, fill=fill)
        y += size + line_gap
    return y


def make_image(slug, label, accent, bubble, bubble_text):
    bg = '#111418'
    panel = '#181d23'
    panel2 = '#20262e'
    border = '#303844'
    muted = '#8893a1'
    bright = '#f2f5f8'
    assistant = '#20262e'
    img = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(img)

    # Window chrome and subtle depth.
    rounded(d, (38, 30, W - 38, H - 30), 18, fill='#0d1013', outline='#38414d', width=2)
    d.rectangle((40, 86, W - 40, H - 32), fill=bg)
    d.line((40, 86, W - 40, 86), fill=border, width=2)
    d.line((330, 88, 330, H - 32), fill=border, width=2)
    for i, c in enumerate(['#ff6b6b', '#f7c948', '#20c997']):
        d.ellipse((64 + i * 24, 55, 76 + i * 24, 67), fill=c)
    text(d, (140, 51), 'Hermes', 20, bright, True)
    rounded(d, (W - 410, 46, W - 226, 72), 13, fill=panel2, outline=border)
    text(d, (W - 318, 59), 'Demo Profile', 14, bright, True, 'mm')
    d.ellipse((W - 249, 53, W - 237, 65), fill=accent)
    text(d, (W - 200, 59), '⌄', 20, muted, anchor='mm')

    # Sidebar.
    text(d, (72, 126), 'WORKSPACE', 12, muted, True)
    nav = [('✦', 'New session'), ('◫', 'Sessions'), ('⌁', 'Skills'), ('⚙', 'Settings')]
    for i, (icon, name) in enumerate(nav):
        y = 172 + i * 53
        active = i == 0
        if active:
            rounded(d, (58, y - 18, 306, y + 22), 10, fill='#252c35')
        text(d, (78, y), icon, 19, accent if active else muted, anchor='lm')
        text(d, (112, y), name, 16, bright if active else muted, active, 'lm')
    text(d, (72, 424), 'RECENT', 12, muted, True)
    for i, name in enumerate(['Color study', 'Quiet planning', 'Tiny experiments']):
        text(d, (78, 462 + i * 40), name, 15, '#b4bdc8')
    rounded(d, (58, H - 104, 306, H - 58), 10, fill=panel, outline=border)
    d.ellipse((78, H - 91, 94, H - 75), fill=accent)
    text(d, (110, H - 83), f'{label} accent', 13, bright, True, 'lm')

    # Conversation header.
    text(d, (382, 130), 'A small creative session', 26, bright, True)
    text(d, (382, 166), 'Fictional preview · no live data', 14, muted)
    d.line((382, 198, W - 88, 198), fill=border, width=2)

    # Assistant intro.
    rounded(d, (382, 238, W - 88, 344), 13, fill=assistant, outline=border, width=1)
    d.ellipse((410, 263, 448, 301), fill='#5f6b78')
    text(d, (429, 282), 'H', 18, '#ffffff', True, 'mm')
    text(d, (472, 258), 'Hermes', 15, bright, True)
    wrapped(d, (472, 286), 'Ready when you are. This preview keeps the assistant surface calm so the message accent can take the stage.', 930, 16, '#b9c3ce', 6)

    # User message: accent is deliberately high-contrast but restrained.
    ux1, uy1, ux2, uy2 = 690, 392, W - 88, 520
    rounded(d, (ux1 + 4, uy1 + 7, ux2 + 4, uy2 + 7), 14, fill='#0b0d10')
    rounded(d, (ux1, uy1, ux2, uy2), 14, fill=bubble, outline=accent, width=3)
    d.ellipse((ux1 + 24, uy1 + 22, ux1 + 56, uy1 + 54), fill=accent)
    text(d, (ux1 + 40, uy1 + 38), 'Y', 14, bubble_text, True, 'mm')
    text(d, (ux1 + 76, uy1 + 22), 'You', 14, bubble_text, True)
    text(d, (ux2 - 24, uy1 + 23), 'just now', 12, bubble_text, anchor='ra')
    wrapped(d, (ux1 + 76, uy1 + 51), 'Show me three ways to make this tiny idea feel memorable.', ux2 - ux1 - 112, 18, '#2a2930', 7)

    # Assistant reply.
    rounded(d, (382, 572, W - 88, 722), 13, fill=assistant, outline=border, width=1)
    d.ellipse((410, 598, 448, 636), fill='#5f6b78')
    text(d, (429, 617), 'H', 18, '#ffffff', True, 'mm')
    text(d, (472, 592), 'Hermes', 15, bright, True)
    wrapped(d, (472, 621), '1. Give the opening a sharp little surprise.\n2. Repeat one visual motif until it becomes a signature.\n3. End with a line that leaves the door slightly open.', 930, 17, '#c5cdd6', 10)

    # Composer.
    rounded(d, (382, 784, W - 88, 894), 14, fill=panel, outline=border, width=2)
    text(d, (410, 818), 'Write a fictional message…', 17, '#697584')
    rounded(d, (W - 202, 817, W - 120, 861), 10, fill=accent)
    text(d, (W - 161, 839), 'Send  ›', 15, bubble_text, True, 'mm')
    text(d, (382, 936), 'Hermes Message Accents', 13, muted)
    text(d, (W - 88, 936), label, 13, accent, True, 'ra')
    img.save(OUT / f'{slug}.png', optimize=True)


for variant in VARIANTS:
    make_image(*variant)
print(f'created {len(VARIANTS)} images in {OUT}')
