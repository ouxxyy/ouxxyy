"""Render the profile's star badges from GitHub repository data."""

import json
import subprocess
from pathlib import Path

BADGE_DIR = Path(__file__).resolve().parents[1] / "assets" / "stars"

# Preserve the label widths and two sizes of the original profile badges.
FEATURED = {
    "ouba-classmate": 135.5,
    "jd-resume-match": 141.75,
    "ai-interviewer": 128.5,
    "job-search": 101.5,
    "sherlock-company": 153,
    "codex-gif-video": 137.75,
    "storyboard-scavenger": 186,
    "mystery-skill": 120.25,
}
COMPACT = {
    "mbai": ("mbai", 37, "#2e1f5e"),
    "travel-art-album-skill": ("album", 45, "#9a3412"),
    "Attention": ("Attention", 61, "#172230"),
    "postapp": ("postapp", 53, "#0369a1"),
}


def render(repo, stars):
    if repo in FEATURED:
        label, left, color = repo.upper(), FEATURED[repo], "#d4b064"
        height, padding, digit, font, baseline = 28, 24, 8.25, 10, 17.5
        number_style = ' fill="#333" font-weight="bold"'
    else:
        label, left, color = COMPACT[repo]
        height, padding, digit, font, baseline = 20, 10, 7, 11, 14
        number_style = ""

    digits_width = len(str(stars)) * digit
    right = padding + digits_width
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{left + right:g}" height="{height}" role="img" aria-label="{repo}: {stars} GitHub stars">
  <title>{repo}: {stars} GitHub stars</title>
  <g shape-rendering="crispEdges">
    <rect width="{left:g}" height="{height}" fill="#555"/>
    <rect x="{left:g}" width="{right:g}" height="{height}" fill="{color}"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="{font}" text-rendering="geometricPrecision">
    <text x="{left / 2:g}" y="{baseline:g}" textLength="{left - padding:g}">{label}</text>
    <text x="{left + right / 2:g}" y="{baseline:g}" textLength="{digits_width:g}"{number_style}>{stars}</text>
  </g>
</svg>
'''


def main():
    badges = {}
    for repo in (*FEATURED, *COMPACT):
        response = subprocess.check_output(
            ["gh", "api", f"repos/ouxxyy/{repo}", "--jq", ".stargazers_count"],
            text=True, timeout=30,
        )
        stars = json.loads(response)
        if type(stars) is not int or stars < 0:
            raise ValueError(f"Invalid GitHub star count for {repo}: {stars!r}")
        badges[repo] = render(repo, stars)
        print(f"{repo}: {stars}", flush=True)

    # A failed API request leaves the entire previous snapshot in place.
    BADGE_DIR.mkdir(parents=True, exist_ok=True)
    for repo, svg in badges.items():
        (BADGE_DIR / f"{repo}.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
