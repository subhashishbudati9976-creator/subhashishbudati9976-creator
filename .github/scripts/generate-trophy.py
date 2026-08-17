import json
from pathlib import Path
from datetime import datetime
from urllib.request import Request, urlopen


USERNAME = "subhashishbudati9976-creator"
OUTPUT = Path("trophy.svg")


def get_github_stats():
    url = f"https://api.github.com/users/{USERNAME}"

    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "GitHub-Trophy-Generator"
        }
    )

    with urlopen(request) as response:
        data = response.read().decode("utf-8")

    return json.loads(data)


def get_repositories():
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"

    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "GitHub-Trophy-Generator"
        }
    )

    with urlopen(request) as response:
        data = response.read().decode("utf-8")

    return json.loads(data)


# Get GitHub profile data
stats = get_github_stats()

# Get repository data
repositories = get_repositories()


# Profile statistics
public_repos = stats.get("public_repos", 0)
followers = stats.get("followers", 0)
following = stats.get("following", 0)


# Repository statistics
total_stars = sum(
    repo.get("stargazers_count", 0)
    for repo in repositories
)

total_forks = sum(
    repo.get("forks_count", 0)
    for repo in repositories
)


# Calculate custom activity score
activity_score = (
    public_repos * 2
    + followers * 3
    + total_stars * 5
    + total_forks * 4
)


# Determine trophy level
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

progress_width = 260 * progress_percent / 100

updated = datetime.utcnow().strftime("%Y-%m-%d")


# Debug information
print("🏆 Trophy generated successfully!")
print(f"Username: {USERNAME}")
print(f"Repositories: {public_repos}")
print(f"Followers: {followers}")
print(f"Following: {following}")
print(f"Stars: {total_stars}")
print(f"Forks: {total_forks}")
print(f"Activity Score: {activity_score}")
print(f"Level: {level}")


# Generate SVG
svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="1000"
height="460"
viewBox="0 0 1000 460">

<defs>

    <linearGradient id="background"
        x1="0%" y1="0%"
        x2="100%" y2="100%">

        <stop offset="0%" stop-color="#020617"/>
        <stop offset="100%" stop-color="#172554"/>

    </linearGradient>

    <linearGradient id="gold"
        x1="0%" y1="0%"
        x2="100%" y2="100%">

        <stop offset="0%" stop-color="#fef08a"/>
        <stop offset="50%" stop-color="#facc15"/>
        <stop offset="100%" stop-color="#a16207"/>

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
    width="1000"
    height="420"
    rx="30"
    fill="url(#background)"/>


<!-- Trophy -->

<g filter="url(#shadow)">

    <!-- Left handle -->

    <path
        d="M280 85
           C200 70, 165 110, 190 165
           C210 205, 250 205, 280 175"
        fill="none"
        stroke="url(#gold)"
        stroke-width="18"
        stroke-linecap="round"/>


    <!-- Right handle -->

    <path
        d="M520 85
           C600 70, 635 110, 610 165
           C590 205, 550 205, 520 175"
        fill="none"
        stroke="url(#gold)"
        stroke-width="18"
        stroke-linecap="round"/>


    <!-- Cup -->

    <path
        d="M270 70
           L530 70
           L500 180
           C490 220, 455 245, 400 245
           C345 245, 310 220, 300 180
           Z"
        fill="url(#gold)"/>


    <!-- Star -->

    <path
        d="M400 95
           L415 130
           L452 132
           L423 154
           L433 190
           L400 168
           L367 190
           L377 154
           L348 132
           L385 130
           Z"
        fill="#fff7ed"/>


    <!-- Stem -->

    <rect
        x="380"
        y="240"
        width="40"
        height="50"
        rx="7"
        fill="url(#gold)"/>


    <!-- Base -->

    <rect
        x="330"
        y="285"
        width="140"
        height="25"
        rx="8"
        fill="url(#gold)"/>

</g>


<!-- Title -->

<text
    x="700"
    y="90"
    text-anchor="middle"
    fill="#f8fafc"
    font-family="Arial, Helvetica, sans-serif"
    font-size="34"
    font-weight="700">

    GITHUB TROPHY

</text>


<!-- Username -->

<text
    x="700"
    y="125"
    text-anchor="middle"
    fill="#cbd5e1"
    font-family="Arial, Helvetica, sans-serif"
    font-size="18">

    @{USERNAME}

</text>


<!-- Level -->

<text
    x="700"
    y="170"
    text-anchor="middle"
    fill="#facc15"
    font-family="Arial, Helvetica, sans-serif"
    font-size="28"
    font-weight="700">

    {level}

</text>


<!-- Activity Score -->

<text
    x="700"
    y="205"
    text-anchor="middle"
    fill="#f8fafc"
    font-family="Arial, Helvetica, sans-serif"
    font-size="20">

    Activity Score: {activity_score}

</text>


<!-- Progress bar background -->

<rect
    x="570"
    y="220"
    width="260"
    height="14"
    rx="7"
    fill="#334155"/>


<!-- Progress bar -->

<rect
    x="570"
    y="220"
    width="{progress_width}"
    height="14"
    rx="7"
    fill="url(#gold)"/>


<!-- Progress percentage -->

<text
    x="850"
    y="233"
    text-anchor="start"
    fill="#cbd5e1"
    font-family="Arial, Helvetica, sans-serif"
    font-size="14">

    {progress_percent}%

</text>


<!-- Next rank -->

<text
    x="700"
    y="260"
    text-anchor="middle"
    fill="#94a3b8"
    font-family="Arial, Helvetica, sans-serif"
    font-size="15">

    Next: {next_level}

</text>


<!-- Stats -->

<text
    x="700"
    y="285"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    Repositories: {public_repos}

</text>


<text
    x="700"
    y="315"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    Followers: {followers}

</text>


<text
    x="700"
    y="345"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    ⭐ Stars: {total_stars}

</text>


<text
    x="700"
    y="375"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="17">

    🍴 Forks: {total_forks}

</text>


<!-- Updated -->

<text
    x="500"
    y="430"
    text-anchor="middle"
    fill="#64748b"
    font-family="Arial, Helvetica, sans-serif"
    font-size="14">

    Automatically updated • {updated}

</text>


</svg>
'''


# Write SVG file
OUTPUT.write_text(svg, encoding="utf-8")

print("SVG trophy saved successfully!")
