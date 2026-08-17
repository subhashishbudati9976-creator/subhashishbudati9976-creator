import json
from pathlib import Path
from datetime import datetime
from urllib.request import Request, urlopen


USERNAME = "subhashishbudati9976-creator"
OUTPUT = Path("trophy.svg")


def github_request(url):
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "GitHub-Trophy-Generator"
        }
    )

    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def get_github_stats():
    return github_request(
        f"https://api.github.com/users/{USERNAME}"
    )


def get_repositories():
    return github_request(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    )


stats = get_github_stats()
repositories = get_repositories()


public_repos = stats.get("public_repos", 0)
followers = stats.get("followers", 0)
following = stats.get("following", 0)


total_stars = sum(
    repo.get("stargazers_count", 0)
    for repo in repositories
)

total_forks = sum(
    repo.get("forks_count", 0)
    for repo in repositories
)


activity_score = (
    public_repos * 2
    + followers * 3
    + total_stars * 5
    + total_forks * 4
)


if activity_score >= 300:
    level = "LEGENDARY"
    next_level = "MAX LEVEL"
    current_threshold = 300
    next_threshold = 300

elif activity_score >= 150:
    level = "MASTER"
    next_level = "LEGENDARY"
    current_threshold = 150
    next_threshold = 300

elif activity_score >= 75:
    level = "RISING STAR"
    next_level = "MASTER"
    current_threshold = 75
    next_threshold = 150

elif activity_score >= 25:
    level = "BUILDER"
    next_level = "RISING STAR"
    current_threshold = 25
    next_threshold = 75

else:
    level = "ROOKIE"
    next_level = "BUILDER"
    current_threshold = 0
    next_threshold = 25


if level == "LEGENDARY":
    progress_percent = 100
else:
    progress = activity_score - current_threshold
    required = next_threshold - current_threshold

    progress_percent = int(
        (progress / required) * 100
    )

    progress_percent = max(
        0,
        min(100, progress_percent)
    )


progress_width = 250 * progress_percent / 100


if level == "LEGENDARY":
    color_start = "#e0f2fe"
    color_mid = "#67e8f9"
    color_end = "#0891b2"

elif level == "MASTER":
    color_start = "#f1f5f9"
    color_mid = "#cbd5e1"
    color_end = "#64748b"

elif level == "RISING STAR":
    color_start = "#fef08a"
    color_mid = "#facc15"
    color_end = "#a16207"

elif level == "BUILDER":
    color_start = "#e2e8f0"
    color_mid = "#94a3b8"
    color_end = "#475569"

else:
    color_start = "#fed7aa"
    color_mid = "#fb923c"
    color_end = "#9a3412"


updated = datetime.utcnow().strftime("%Y-%m-%d")


print("🏆 Trophy generated successfully!")
print(f"Repositories: {public_repos}")
print(f"Followers: {followers}")
print(f"Following: {following}")
print(f"Stars: {total_stars}")
print(f"Forks: {total_forks}")
print(f"Activity Score: {activity_score}")
print(f"Level: {level}")


svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="1100"
height="460"
viewBox="0 0 1100 460">

<defs>

    <linearGradient id="background"
        x1="0%" y1="0%"
        x2="100%" y2="100%">

        <stop offset="0%" stop-color="#020617"/>
        <stop offset="100%" stop-color="#172554"/>

    </linearGradient>

    <linearGradient id="trophy"
        x1="0%" y1="0%"
        x2="100%" y2="100%">

        <stop offset="0%" stop-color="{color_start}"/>
        <stop offset="50%" stop-color="{color_mid}"/>
        <stop offset="100%" stop-color="{color_end}"/>

    </linearGradient>

    <filter id="shadow">

        <feDropShadow
            dx="0"
            dy="10"
            stdDeviation="12"
            flood-opacity="0.4"/>

    </filter>

</defs>


<!-- Background -->

<rect
    width="1100"
    height="460"
    rx="30"
    fill="url(#background)"/>


<!-- LEFT SECTION : TROPHY -->

<g filter="url(#shadow)">

    <!-- Left handle -->

    <path
        d="M190 100
           C120 85, 90 120, 110 165
           C125 200, 155 205, 190 180"
        fill="none"
        stroke="url(#trophy)"
        stroke-width="18"
        stroke-linecap="round"/>


    <!-- Right handle -->

    <path
        d="M410 100
           C480 85, 510 120, 490 165
           C475 200, 445 205, 410 180"
        fill="none"
        stroke="url(#trophy)"
        stroke-width="18"
        stroke-linecap="round"/>


    <!-- Cup -->

    <path
        d="M180 80
           L420 80
           L395 180
           C385 220, 350 245, 300 245
           C250 245, 215 220, 205 180
           Z"
        fill="url(#trophy)"/>


    <!-- Star -->

    <path
        d="M300 105
           L315 140
           L352 142
           L323 164
           L333 200
           L300 178
           L267 200
           L277 164
           L248 142
           L285 140
           Z"
        fill="#fff7ed"/>


    <!-- Stem -->

    <rect
        x="280"
        y="240"
        width="40"
        height="50"
        rx="7"
        fill="url(#trophy)"/>


    <!-- Base -->

    <rect
        x="230"
        y="285"
        width="140"
        height="25"
        rx="8"
        fill="url(#trophy)"/>

</g>


<!-- Divider -->

<line
    x1="550"
    y1="55"
    x2="550"
    y2="405"
    stroke="#334155"
    stroke-width="2"/>


<!-- RIGHT SECTION -->

<text
    x="825"
    y="80"
    text-anchor="middle"
    fill="#f8fafc"
    font-family="Arial, Helvetica, sans-serif"
    font-size="34"
    font-weight="700">

    GITHUB TROPHY

</text>


<text
    x="825"
    y="115"
    text-anchor="middle"
    fill="#cbd5e1"
    font-family="Arial, Helvetica, sans-serif"
    font-size="18">

    @{USERNAME}

</text>


<text
    x="825"
    y="160"
    text-anchor="middle"
    fill="{color_mid}"
    font-family="Arial, Helvetica, sans-serif"
    font-size="28"
    font-weight="700">

    {level}

</text>


<text
    x="825"
    y="195"
    text-anchor="middle"
    fill="#f8fafc"
    font-family="Arial, Helvetica, sans-serif"
    font-size="20">

    Activity Score: {activity_score}

</text>


<!-- Progress background -->

<rect
    x="700"
    y="215"
    width="250"
    height="14"
    rx="7"
    fill="#334155"/>


<!-- Progress -->

<rect
    x="700"
    y="215"
    width="{progress_width}"
    height="14"
    rx="7"
    fill="url(#trophy)"/>


<text
    x="965"
    y="228"
    fill="#cbd5e1"
    font-family="Arial, Helvetica, sans-serif"
    font-size="14">

    {progress_percent}%

</text>


<text
    x="825"
    y="255"
    text-anchor="middle"
    fill="#94a3b8"
    font-family="Arial, Helvetica, sans-serif"
    font-size="15">

    Next: {next_level}

</text>


<!-- Stats -->

<text
    x="825"
    y="295"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    Repositories: {public_repos}

</text>


<text
    x="825"
    y="325"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    Followers: {followers}

</text>


<text
    x="825"
    y="355"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    Stars: {total_stars}

</text>


<text
    x="825"
    y="385"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    Forks: {total_forks}

</text>


<!-- Footer -->

<text
    x="550"
    y="430"
    text-anchor="middle"
    fill="#64748b"
    font-family="Arial, Helvetica, sans-serif"
    font-size="14">

    Automatically updated • {updated}

</text>


</svg>
'''


OUTPUT.write_text(svg, encoding="utf-8")

print("SVG trophy saved successfully!")
