from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent.parent

SOURCE = ROOT / "profile" / "source-photo.jpg"
OUTPUT = ROOT / "profile" / "ascii-portrait.svg"


WIDTH = 370
HEIGHT = 430

COLS = 55
ROWS = 60

RAMP = " .:-=+*#%@"


def brightness_to_char(value):
    index = int((value / 255) * (len(RAMP) - 1))
    return RAMP[index]


def main():

    image = Image.open(SOURCE).convert("L")

    image = ImageOps.autocontrast(image)

    # Preserve aspect ratio while fitting the grid.
    image = image.resize((COLS, ROWS))

    cell_width = WIDTH / COLS
    cell_height = HEIGHT / ROWS

    text_elements = []

    for y in range(ROWS):

        row = []

        for x in range(COLS):

            pixel = image.getpixel((x, y))

            char = brightness_to_char(pixel)

            if char == " ":
                char = "."

            row.append(char)

        text = "".join(row)

        delay = y * 0.035

        text_elements.append(
            f"""
            <text
                x="0"
                y="{(y + 1) * cell_height:.2f}"
                class="ascii"
            >
                {text}
                <animate
                    attributeName="opacity"
                    from="0"
                    to="1"
                    dur="0.25s"
                    begin="{delay:.3f}s"
                    fill="freeze"
                />
            </text>
            """
        )

    svg = f"""<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>

<rect
    width="100%"
    height="100%"
    rx="18"
    fill="#0D1117"
/>

<style>

.ascii {{
    font-family: monospace;
    font-size: 6px;
    fill: #7AA2F7;
    white-space: pre;
}}

</style>

{"".join(text_elements)}

</svg>
"""

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(svg, encoding="utf-8")

    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
    