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
import json
import os
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


# Get GitHub profile data
stats = get_github_stats()

public_repos = stats["public_repos"]
followers = stats["followers"]
following = stats["following"]


# Determine trophy level
if public_repos >= 30:
    level = "LEGENDARY"
elif public_repos >= 20:
    level = "MASTER"
elif public_repos >= 10:
    level = "RISING STAR"
elif public_repos >= 5:
    level = "BUILDER"
else:
    level = "ROOKIE"


updated = datetime.utcnow().strftime("%Y-%m-%d")


svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="1000"
height="420"
viewBox="0 0 1000 420">

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

    <path
        d="M280 85
           C200 70, 165 110, 190 165
           C210 205, 250 205, 280 175"
        fill="none"
        stroke="url(#gold)"
        stroke-width="18"
        stroke-linecap="round"/>

    <path
        d="M520 85
           C600 70, 635 110, 610 165
           C590 205, 550 205, 520 175"
        fill="none"
        stroke="url(#gold)"
        stroke-width="18"
        stroke-linecap="round"/>

    <path
        d="M270 70
           L530 70
           L500 180
           C490 220, 455 245, 400 245
           C345 245, 310 220, 300 180
           Z"
        fill="url(#gold)"/>

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

    <rect
        x="380"
        y="240"
        width="40"
        height="50"
        rx="7"
        fill="url(#gold)"/>

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
    y="105"
    text-anchor="middle"
    fill="#f8fafc"
    font-family="Arial, Helvetica, sans-serif"
    font-size="38"
    font-weight="700">

    GITHUB TROPHY

</text>


<!-- Username -->

<text
    x="700"
    y="145"
    text-anchor="middle"
    fill="#cbd5e1"
    font-family="Arial, Helvetica, sans-serif"
    font-size="20">

    @{USERNAME}

</text>


<!-- Level -->

<text
    x="700"
    y="190"
    text-anchor="middle"
    fill="#facc15"
    font-family="Arial, Helvetica, sans-serif"
    font-size="28"
    font-weight="700">

    {level}

</text>


<!-- Stats -->

<text
    x="700"
    y="240"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="18">

    Repositories: {public_repos}

</text>


<text
    x="700"
    y="275"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="18">

    Followers: {followers}

</text>


<text
    x="700"
    y="310"
    text-anchor="middle"
    fill="#e2e8f0"
    font-family="Arial, Helvetica, sans-serif"
    font-size="18">

    Following: {following}

</text>


<text
    x="500"
    y="375"
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
print(f"Username: {USERNAME}")
print(f"Repositories: {public_repos}")
print(f"Followers: {followers}")
print(f"Following: {following}")
print(f"Level: {level}")
