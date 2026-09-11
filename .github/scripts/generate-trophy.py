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

    progress_percent = max(0, min(100, progress_percent))


progress_width = 280 * progress_percent / 100


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
            dy="12"
            stdDeviation="14"
            flood-opacity="0.45"/>

    </filter>

</defs>


<!-- Background -->

<rect
    width="1100"
    height="460"
    rx="30"
    fill="url(#background)"/>


<!-- ================= TROPHY AREA ================= -->

<g filter="url(#shadow)">

    <!-- Left handle -->

    <path
        d="M190 105
           C105 85, 75 130, 105 180
           C125 215, 160 215, 195 185"
        fill="none"
        stroke="url(#trophy)"
        stroke-width="22"
        stroke-linecap="round"/>


    <!-- Right handle -->

    <path
        d="M410 105
           C495 85, 525 130, 495 180
           C475 215, 440 215, 405 185"
        fill="none"
        stroke="url(#trophy)"
        stroke-width="22"
        stroke-linecap="round"/>


    <!-- Cup -->

    <path
        d="M175 75
           L425 75
           L395 190
           C385 235, 350 260, 300 260
           C250 260, 215 235, 205 190
           Z"
        fill="url(#trophy)"/>


    <!-- Star -->

    <path
        d="M300 105
           L318 145
           L360 148
           L327 173
           L338 215
           L300 190
           L262 215
           L273 173
           L240 148
           L282 145
           Z"
        fill="#fff7ed"/>


    <!-- Stem -->

    <rect
        x="280"
        y="255"
        width="40"
        height="55"
        rx="8"
        fill="url(#trophy)"/>


    <!-- Base -->

    <rect
        x="220"
        y="305"
        width="160"
        height="28"
        rx="9"
        fill="url(#trophy)"/>

</g>


<!-- Trophy label -->

<text
    x="300"
    y="370"
    text-anchor="middle"
    fill="#cbd5e1"
    font-family="Arial, Helvetica, sans-serif"
    font-size="18"
    font-weight="600">

    YOUR GITHUB TROPHY

</text>


<!-- ================= DIVIDER ================= -->

<line
    x1="535"
    y1="50"
    x2="535"
    y2="410"
    stroke="#334155"
    stroke-width="2"/>


<!-- ================= INFORMATION AREA ================= -->

<text
    x="810"
    y="75"
    text-anchor="middle"
    fill="#f8fafc"
    font-family="Arial, Helvetica, sans-serif"
    font-size="36"
    font-weight="700">

    GITHUB TROPHY

</text>


<text
    x="810"
    y="108"
    text-anchor="middle"
    fill="#94a3b8"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    @{USERNAME}

</text>


<text
    x="810"
    y="155"
    text-anchor="middle"
    fill="{color_mid}"
    font-family="Arial, Helvetica, sans-serif"
    font-size="30"
    font-weight="700">

    {level}

</text>


<text
    x="810"
    y="190"
    text-anchor="middle"
    fill="#f8fafc"
    font-family="Arial, Helvetica, sans-serif"
    font-size="20">

    Activity Score: {activity_score}

</text>


<!-- Progress bar -->

<rect
    x="660"
    y="210"
    width="280"
    height="15"
    rx="8"
    fill="#334155"/>


<rect
    x="660"
    y="210"
    width="{progress_width}"
    height="15"
    rx="8"
    fill="url(#trophy)"/>


<text
    x="955"
    y="223"
    fill="#cbd5e1"
    font-family="Arial, Helvetica, sans-serif"
    font-size="14">

    {progress_percent}%

</text>


<text
    x="810"
    y="255"
    text-anchor="middle"
    fill="#94a3b8"
    font-family="Arial, Helvetica, sans-serif"
    font-size="15">

    Next Rank: {next_level}

</text>


<!-- Stats -->

<text
    x="810"
    y="295"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    Repositories: {public_repos}

</text>


<text
    x="810"
    y="325"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    Followers: {followers}

</text>


<text
    x="810"
    y="355"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    Stars: {total_stars}

</text>


<text
    x="810"
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
    y="435"
    text-anchor="middle"
    fill="#64748b"
    font-family="Arial, Helvetica, sans-serif"
    font-size="14">

    Automatically updated • {updated}

</text>


</svg>
'''


OUTPUT.write_text(svg, encoding="utf-8")


print("🏆 Trophy generated successfully!")
print(f"Repositories: {public_repos}")
print(f"Followers: {followers}")
print(f"Following: {following}")
print(f"Stars: {total_stars}")
print(f"Forks: {total_forks}")
print(f"Activity Score: {activity_score}")
print(f"Level: {level}")
print(f"Progress: {progress_percent}%")
print(f"Next Level: {next_level}")
print("SVG trophy saved successfully!")
