#!/usr/bin/env python3
"""Give every README.md entry that links to a GitHub repository a live star badge.

The badge sits right after the name, in GitHub's own star-button style:

    - [name](https://github.com/owner/repo) ![Stars](https://img.shields.io/github/stars/owner/repo?style=social) - What it does.

awesome-lint only accepts that position when the description starts with a capital letter
or code, so an entry whose description starts otherwise (say, "macOS ...") keeps its badge
at the end of the line instead, and the result always passes lint.

shields.io fetches the count each time the page loads, so counts never go stale.
This script only adds missing badges, fixes ones whose URL no longer matches the
entry's link, and removes old plain-text `(★ N)` counts. Links into subdirectories
(/tree/, /blob/) are skipped, since the parent repository's stars don't describe
the linked project. The Stars workflow runs it whenever README.md changes on main,
and scheduled showcase updates run it before publishing; contributors can leave
badges off.

    scripts/update-stars.py            # rewrite README.md
    scripts/update-stars.py --check    # exit 1 when a badge is missing, without writing

`fetch_stars()` reads current counts through `gh api graphql` for tools that need
the numbers, such as scripts/render-images.py.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"
ENTRY = re.compile(r"^(- \[[^\]]+\]\(https://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?/?\))"
                   r"(?: !\[Stars\]\([^)\s]+\))? - (.*)$")
OLD_TEXT = re.compile(r" \(★ [\d.]+k?\)$")
END_BADGE = re.compile(r" !\[Stars\]\(https://img\.shields\.io/github/stars/[^)\s]+\)$")
BATCH = 50


def badge(owner, repo):
    return f"![Stars](https://img.shields.io/github/stars/{owner}/{repo}?style=social)"


def apply_badges(lines):
    updated = []
    for line in lines:
        match = ENTRY.match(line)
        if match:
            link, owner, repo, description = match.groups()
            description = OLD_TEXT.sub("", END_BADGE.sub("", description))
            if re.match(r"[A-Z`]", description):
                line = f"{link} {badge(owner, repo)} - {description}"
            else:
                line = f"{link} - {description} {badge(owner, repo)}"
        updated.append(line)
    return updated


def repositories(lines):
    """owner/name keys for entries that link directly to a repository."""
    found = []
    for line in lines:
        match = ENTRY.match(line)
        if match:
            found.append(f"{match.group(2)}/{match.group(3)}".lower())
    return sorted(set(found))


def format_stars(count):
    if count < 1000:
        return str(count)
    value = f"{count / 1000:.1f}".removesuffix(".0") if count < 10000 else str(round(count / 1000))
    return value + "k"


def fetch_stars(repos):
    """Map owner/name keys to star counts; repositories that can't be read are left out."""
    counts = {}
    for start in range(0, len(repos), BATCH):
        chunk = repos[start:start + BATCH]
        fields = " ".join(
            f'r{i}: repository(owner: {json.dumps(r.split("/")[0])}, name: {json.dumps(r.split("/")[1])}) {{ stargazerCount }}'
            for i, r in enumerate(chunk))
        # Missing repositories come back as null fields with errors, and gh then exits non-zero.
        result = subprocess.run(["gh", "api", "graphql", "-f", f"query={{ {fields} }}"],
                                capture_output=True, text=True, timeout=120)
        try:
            data = json.loads(result.stdout).get("data") or {}
        except ValueError:
            raise RuntimeError(f"GitHub GraphQL request failed: {result.stderr.strip()[:200]}")
        for i, repo in enumerate(chunk):
            node = data.get(f"r{i}")
            if node:
                counts[repo] = node["stargazerCount"]
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="Report missing or stale badges without writing README.md")
    parser.add_argument("--readme", type=Path, default=README, help=argparse.SUPPRESS)
    args = parser.parse_args()
    text = args.readme.read_text(encoding="utf-8")
    lines = text.splitlines()
    updated = "\n".join(apply_badges(lines)) + ("\n" if text.endswith("\n") else "")
    changed = updated != text
    print(f"{len(repositories(lines))} repository entries; README.md {'needs badge updates' if changed else 'is current'}")
    if changed and not args.check:
        args.readme.write_text(updated, encoding="utf-8")
    return 1 if changed and args.check else 0


if __name__ == "__main__":
    sys.exit(main())
