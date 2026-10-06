from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

OUTPUT = ROOT / "profile" / "info-card.svg"


def main():

    svg = """<svg
    xmlns="http://www.w3.org/2000/svg"
    width="520"
    height="430"
    viewBox="0 0 520 430"
>

<rect
    width="100%"
    height="100%"
    rx="18"
    fill="#0D1117"
    stroke="#30363D"
/>

<style>

.title {
    font-family: monospace;
    font-size: 18px;
    font-weight: bold;
    fill: #E6EDF3;
}

.label {
    font-family: monospace;
    font-size: 13px;
    font-weight: bold;
    fill: #7AA2F7;
}

.value {
    font-family: monospace;
    font-size: 13px;
    fill: #C9D1D9;
}

.dim {
    font-family: monospace;
    font-size: 11px;
    fill: #8B949E;
}

.cursor {
    fill: #9B6CFF;
}

</style>

<text x="30" y="35" class="title">
subhashish@github
</text>

<text x="30" y="55" class="dim">
────────────────────────────────────────
</text>

<text x="30" y="90" class="label">
USER
</text>

<text x="150" y="90" class="value">
Subhashish Budati
</text>

<text x="30" y="125" class="label">
ROLE
</text>

<text x="150" y="125" class="value">
CSE Student
</text>

<text x="30" y="160" class="label">
PROGRAM
</text>

<text x="150" y="160" class="value">
B.Tech + M.Tech
</text>

<text x="30" y="195" class="label">
FOCUS
</text>

<text x="150" y="195" class="value">
AI • NLP • DevOps
</text>

<text x="30" y="230" class="label">
LANGUAGES
</text>

<text x="150" y="230" class="value">
C • Python • Java • SQL
</text>

<text x="30" y="265" class="label">
TOOLS
</text>

<text x="150" y="265" class="value">
Git • Docker • Jenkins
</text>

<text x="150" y="287" class="value">
GitHub Actions
</text>

<text x="30" y="322" class="label">
BUILDING
</text>

<text x="150" y="322" class="value">
AVENUE
</text>

<text x="30" y="357" class="label">
STATUS
</text>

<text x="150" y="357" class="value">
● BUILDING
</text>

<text x="30" y="395" class="dim">
$ ./keep_building.sh
</text>

<rect
    x="195"
    y="385"
    width="7"
    height="15"
    class="cursor"
>
    <animate
        attributeName="opacity"
        values="1;0;1"
        dur="1s"
        repeatCount="indefinite"
    />
</rect>

</svg>
"""

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(svg, encoding="utf-8")

    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()