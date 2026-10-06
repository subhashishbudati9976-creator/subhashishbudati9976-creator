import json
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "contributions.json"
OUTPUT_FILE = ROOT / "profile" / "contribution-heatmap.svg"


WIDTH = 1000
HEIGHT = 300

CELL_SIZE = 12
GAP = 4

LEFT = 30
TOP = 75


COLORS = {
    0: "#161B22",
    1: "#202B3D",
    2: "#354A70",
    3: "#586FA8",
    4: "#7AA2F7",
}


def load_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_cells(days):
    cells = []

    # GitHub calendar = 7 rows
    for index, day in enumerate(days):
        date = datetime.strptime(day["date"], "%Y-%m-%d")

        weekday = date.weekday()

        # Monday = 0 → GitHub layout wants Sunday at bottom.
        row = (weekday + 1) % 7

        column = index // 7

        x = LEFT + column * (CELL_SIZE + GAP)
        y = TOP + row * (CELL_SIZE + GAP)

        level = min(int(day["level"]), 4)

        delay = column * 0.018 + row * 0.025

        cells.append(
            f"""
            <rect
                x="{x}"
                y="{y}"
                width="{CELL_SIZE}"
                height="{CELL_SIZE}"
                rx="3"
                fill="{COLORS[level]}"
                opacity="0"
            >
                <animate
                    attributeName="opacity"
                    from="0"
                    to="1"
                    dur="0.35s"
                    begin="{delay:.3f}s"
                    fill="freeze"
                />
            </rect>
            """
        )

    return "\n".join(cells)


def generate_svg(data):
    stats = data["stats"]
    username = data["username"]

    cells = build_cells(data["days"])

    generated = data.get("generated_at", "")

    return f"""<svg
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
    stroke="#30363D"
/>

<style>
    .title {{
        font-family: monospace;
        font-size: 18px;
        font-weight: bold;
        fill: #E6EDF3;
    }}

    .subtitle {{
        font-family: monospace;
        font-size: 12px;
        fill: #8B949E;
    }}

    .stat {{
        font-family: monospace;
        font-size: 13px;
        fill: #C9D1D9;
    }}

    .accent {{
        fill: #7AA2F7;
    }}
</style>

<text
    x="30"
    y="35"
    class="title"
>
    {username}@github ~ $ contributions
</text>

<text
    x="30"
    y="55"
    class="subtitle"
>
    live activity • automatically refreshed
</text>

{cells}

<text
    x="30"
    y="245"
    class="stat"
>
    CONTRIBUTIONS
    <tspan class="accent">{stats["total"]}</tspan>
</text>

<text
    x="250"
    y="245"
    class="stat"
>
    CURRENT STREAK
    <tspan class="accent">{stats["current_streak"]}</tspan>
</text>

<text
    x="480"
    y="245"
    class="stat"
>
    LONGEST STREAK
    <tspan class="accent">{stats["longest_streak"]}</tspan>
</text>

<text
    x="720"
    y="245"
    class="stat"
>
    BEST DAY
    <tspan class="accent">{stats["best_day"]}</tspan>
</text>

<text
    x="30"
    y="275"
    class="subtitle"
>
    generated: {generated}
</text>

</svg>
"""


def main():
    data = load_data()

    svg = generate_svg(data)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(svg, encoding="utf-8")

    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()