import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "subhashishbudati9976-creator"

OUTPUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"

URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_page():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers, timeout=20)
    response.raise_for_status()

    return response.text


def parse_contributions(html):
    soup = BeautifulSoup(html, "html.parser")

    days = []

    for cell in soup.select("[data-date]"):
        date = cell.get("data-date")

        if not date:
            continue

        level = cell.get("data-level", "0")

        # GitHub normally exposes contribution count
        # through the aria-label.
        label = cell.get("aria-label", "")

        count_match = re.search(
            r"(\d+)\s+contribution",
            label,
            re.IGNORECASE
        )

        count = int(count_match.group(1)) if count_match else 0

        days.append({
            "date": date,
            "count": count,
            "level": int(level) if level.isdigit() else 0
        })

    # Remove duplicates
    unique = {}

    for day in days:
        unique[day["date"]] = day

    return sorted(unique.values(), key=lambda x: x["date"])


def calculate_stats(days):
    counts = [day["count"] for day in days]

    total = sum(counts)
    best_day = max(counts, default=0)

    longest_streak = 0
    current_streak = 0

    for day in days:
        if day["count"] > 0:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 0

    current = 0

    for day in reversed(days):
        if day["count"] > 0:
            current += 1
        else:
            break

    return {
        "total": total,
        "current_streak": current,
        "longest_streak": longest_streak,
        "best_day": best_day
    }


def main():
    print(f"Fetching contributions for {USERNAME}...")

    html = fetch_page()
    days = parse_contributions(html)

    if not days:
        raise RuntimeError(
            "No contribution data found. GitHub may have changed the page structure."
        )

    stats = calculate_stats(days)

    output = {
        "username": USERNAME,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "stats": stats,
        "days": days
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print(f"Saved {len(days)} contribution days.")
    print(f"Total contributions: {stats['total']}")
    print(f"Current streak: {stats['current_streak']}")
    print(f"Longest streak: {stats['longest_streak']}")
    print(f"Best day: {stats['best_day']}")


if __name__ == "__main__":
    main()