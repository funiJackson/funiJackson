"""Generates the GitHub profile banner — two variants, light and dark.

Pure centred typography on a transparent background, three tiers.

Every letter is stamped out of a 5x7 bitmap font as SVG rects rather than set as
<text>. GitHub serves images through its camo proxy, which never loads an
@font-face, so real text would fall back to whatever font the viewer happens to
have. Blocks render identically everywhere — and they match the pixel icons on
the portfolio.
"""

FONT = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    '!': ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "'": ["00100", "00100", "00100", "00000", "00000", "00000", "00000"],
    ',': ["00000", "00000", "00000", "00000", "00100", "00100", "01000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "00000", "00100"],
    '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    ' ': ["00000"] * 7,
}

W, H = 720, 210

LINES = [
    ("HI! I'M JACKSON", 6, 34, "hero"),
    ("DESIGNER, ENGINEER AND DEVELOPER", 2, 118, "sub"),
    ("I MAKE THE AI BEHAVE", 2, 164, "muted"),
]

THEMES = {
    # on GitHub's dark canvas
    "dark": {"hero": "#9ece6a", "sub": "#dcd7ba", "muted": "#7f8b76"},
    # on GitHub's white canvas — the same hues, pushed down so they hold up
    "light": {"hero": "#4f7c42", "sub": "#3f4a37", "muted": "#7c8a73"},
}


def word_width(word, cell):
    """Width in px, with the trailing inter-letter gap trimmed."""
    return len(word) * 6 * cell - cell


def stamp(word, cell, y, fill, out):
    x = (W - word_width(word, cell)) / 2
    for char in word:
        glyph = FONT.get(char)
        if glyph is None:
            x += cell * 6
            continue
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == "1":
                    out.append(
                        f'<rect x="{x + col * cell:g}" y="{y + row * cell:g}" '
                        f'width="{cell}" height="{cell}" fill="{fill}"/>'
                    )
        x += cell * 6


def build(theme):
    colours = THEMES[theme]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="Hi! I\'m Jackson — designer, engineer and developer">'
    ]
    for word, cell, y, role in LINES:
        stamp(word, cell, y, colours[role], out)
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(build(sys.argv[1] if len(sys.argv) > 1 else "dark"))
