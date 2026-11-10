#!/usr/bin/env python3
"""Refresh the GitHub star counts at the end of README.md entries.

Each entry that links straight to a GitHub repository gets a trailing count:

    - [name](https://github.com/owner/repo) - What it does. (★ 1.2k)

Links into subdirectories (/tree/, /blob/) are skipped, since the parent repository's
stars don't describe the linked project. Repositories with no stars get no count. If a
lookup fails, the entry keeps its previous count. A weekly workflow runs this script;
contributors don't need to add counts by hand.

    scripts/update-stars.py            # rewrite README.md
    scripts/update-stars.py --check    # exit 1 when counts are stale, without writing

Uses `gh api graphql`, so it needs `gh` signed in, or GH_TOKEN set (in Actions).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"
ENTRY = re.compile(r"^- \[[^\]]+\]\(https://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?/?\) - ")
STARS = re.compile(r" \(★ [\d.]+k?\)$")
BATCH = 50


def format_stars(count):
    if count < 1000:
        return str(count)
    value = f"{count / 1000:.1f}".removesuffix(".0") if count < 10000 else str(round(count / 1000))
    return value + "k"


def repositories(lines):
    """owner/name keys for entries that link directly to a repository."""
    found = []
    for line in lines:
        match = ENTRY.match(line)
        if match:
            found.append(f"{match.group(1)}/{match.group(2)}".lower())
    return sorted(set(found))


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


def apply_stars(lines, counts):
    updated = []
    for line in lines:
        match = ENTRY.match(line)
        if match:
            repo = f"{match.group(1)}/{match.group(2)}".lower()
            if repo in counts:
                line = STARS.sub("", line)
                if counts[repo]:
                    line += f" (★ {format_stars(counts[repo])})"
        updated.append(line)
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="Report stale counts without writing README.md")
    parser.add_argument("--readme", type=Path, default=README, help=argparse.SUPPRESS)
    args = parser.parse_args()
    text = args.readme.read_text(encoding="utf-8")
    lines = text.splitlines()
    repos = repositories(lines)
    counts = fetch_stars(repos)
    if len(counts) < len(repos) // 2:
        sys.exit(f"Only {len(counts)} of {len(repos)} repositories could be read; leaving README.md unchanged")
    updated = "\n".join(apply_stars(lines, counts)) + ("\n" if text.endswith("\n") else "")
    changed = updated != text
    print(f"{len(counts)} of {len(repos)} repositories read; README.md {'needs updating' if changed else 'is current'}")
    if changed and not args.check:
        args.readme.write_text(updated, encoding="utf-8")
    return 1 if changed and args.check else 0


if __name__ == "__main__":
    sys.exit(main())
