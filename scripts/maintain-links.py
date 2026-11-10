#!/usr/bin/env python3
"""Repair README.md links on a schedule, so dead links get fixed instead of failing CI.

For every entry that links into GitHub, one batched GraphQL query asks where the
repository lives now:

- renamed or transferred: the entry's GitHub URLs (link, demo, badge) move to the new name;
- deleted, or made private: the entry is removed (git history keeps it).

If more than a few entries look deleted at once, nothing is removed, since that points
to an API problem rather than many projects vanishing. Links outside GitHub can't be
repaired automatically; they're checked and listed in the report, and never fail the run.
The Maintain workflow commits the result, so nobody needs to step in.

    scripts/maintain-links.py              # repair README.md and print a report
    scripts/maintain-links.py --dry-run    # report only

Needs `gh` signed in, or GH_TOKEN set (in Actions).
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = re.compile(r"^- \[([^\]]+)\]\((https?://[^)\s]+)\) - ")
GITHUB = re.compile(r"^https://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?(?=/|$)")
BATCH = 50
spec = importlib.util.spec_from_file_location("stars", ROOT / "scripts/update-stars.py")
stars = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stars)


def github_repo(url):
    match = GITHUB.match(url)
    return f"{match.group(1)}/{match.group(2)}" if match else None


def lookup(repos):
    """Map each owner/name to its current owner/name, or None when GitHub can't find it."""
    found = {}
    for start in range(0, len(repos), BATCH):
        chunk = repos[start:start + BATCH]
        fields = " ".join(
            f'r{i}: repository(owner: {json.dumps(r.split("/")[0])}, name: {json.dumps(r.split("/")[1])}) {{ nameWithOwner }}'
            for i, r in enumerate(chunk))
        result = subprocess.run(["gh", "api", "graphql", "-f", f"query={{ {fields} }}"],
                                capture_output=True, text=True, timeout=120)
        try:
            payload = json.loads(result.stdout)
        except ValueError:
            raise RuntimeError(f"GitHub GraphQL request failed: {result.stderr.strip()[:200]}")
        missing = {e["path"][0] for e in payload.get("errors", []) if e.get("type") == "NOT_FOUND" and e.get("path")}
        data = payload.get("data") or {}
        for i, repo in enumerate(chunk):
            node = data.get(f"r{i}")
            if node:
                found[repo] = node["nameWithOwner"]
            elif f"r{i}" in missing:
                found[repo] = None
            # Anything else (rate limit, outage) is left out, so the entry is left alone.
    return found


def site_ok(url):
    request = urllib.request.Request(url, headers={"User-Agent": "awesome-rex-link-check"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return response.status < 400
        except urllib.error.HTTPError as error:
            if error.code in (403, 429) or error.code >= 500:
                continue  # bot blocking, rate limits, and outages aren't dead links
            return False
        except (urllib.error.URLError, TimeoutError, OSError):
            continue
    return True  # never call a link dead on transient failures alone


def repair(lines, current, max_removals):
    """Return (lines, renamed, removed, held): held lists deletions skipped by the safety limit."""
    renamed, gone = [], []
    for index, line in enumerate(lines):
        match = ENTRY.match(line)
        repo = github_repo(match.group(2)) if match else None
        if repo is None or repo not in current:
            continue
        if current[repo] is None:
            gone.append(index)
        elif current[repo].lower() != repo.lower():
            old = re.escape(repo)
            lines[index] = re.sub(rf"(github\.com/){old}(?=[/)?#]|$)", lambda m: m.group(1) + current[repo],
                                  line, flags=re.I)
            renamed.append(f"{match.group(1)}: {repo} -> {current[repo]}")
    held = []
    if len(gone) > max_removals:
        held, gone = [ENTRY.match(lines[i]).group(1) for i in gone], []
    removed = [ENTRY.match(lines[i]).group(1) for i in gone]
    lines = [line for i, line in enumerate(lines) if i not in set(gone)]
    return stars.apply_badges(lines), renamed, removed, held


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Report without writing README.md")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md", help=argparse.SUPPRESS)
    args = parser.parse_args()
    text = args.readme.read_text(encoding="utf-8")
    lines = text.splitlines()
    urls = [m.group(2) for m in map(ENTRY.match, lines) if m]
    repos = sorted({r for r in map(github_repo, urls) if r})
    current = lookup(repos)
    lines, renamed, removed, held = repair(lines, current, max_removals=max(3, len(repos) // 20))
    broken_sites = [u for u in urls if not github_repo(u) and not site_ok(u)]

    report = [f"Checked {len(repos)} GitHub repositories and {len(urls) - sum(1 for u in urls if github_repo(u))} other links."]
    report += [f"- Renamed: {r}" for r in renamed]
    report += [f"- Removed (repository deleted or private): {r}" for r in removed]
    report += [f"- Not removed, too many at once (check by hand): {r}" for r in held]
    report += [f"- Not reachable (left in place): {u}" for u in broken_sites]
    if len(report) == 1:
        report.append("Everything resolves; nothing to repair.")
    print("\n".join(report))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
            summary.write("## Link maintenance\n\n" + "\n".join(report) + "\n")

    updated = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    if updated != text and not args.dry_run:
        args.readme.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
