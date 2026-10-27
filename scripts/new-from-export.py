#!/usr/bin/env python3
"""List GitHub repositories mentioned in a Discord channel export that aren't in README.md yet.

Point it at a DiscordChatExporter JSON file, or a directory of them (threads included):

    scripts/new-from-export.py path/to/export/

Each candidate prints with its first mention: date, author, and the message text.
Exporting the channel is up to you; this script only reads the files.
"""
import json
import re
import sys
from pathlib import Path

REPO = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)")
# GitHub paths that aren't repositories.
SKIP_OWNERS = {"user-attachments", "orgs", "settings", "features", "sponsors"}


def messages(path):
    files = sorted(path.rglob("*.json")) if path.is_dir() else [path]
    for f in files:
        data = json.loads(f.read_text())
        yield from data.get("messages", [])


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    readme = (Path(__file__).resolve().parent.parent / "README.md").read_text().lower()
    seen = {}
    for m in messages(Path(sys.argv[1])):
        text = m.get("content", "") + " " + " ".join(e.get("url") or "" for e in m.get("embeds", []))
        for repo in REPO.findall(text):
            repo = repo.removesuffix(".git").rstrip(".")
            owner = repo.split("/")[0].lower()
            if owner in SKIP_OWNERS or f"github.com/{repo.lower()}" in readme:
                continue
            seen.setdefault(repo.lower(), (repo, m))
    if not seen:
        print("Nothing new.")
    for repo, m in sorted(seen.values(), key=lambda x: x[1].get("timestamp", "")):
        author = m.get("author", {})
        print(f"https://github.com/{repo}")
        print(f"  {m.get('timestamp', '')[:10]}  {author.get('nickname') or author.get('name', '?')}")
        print("  " + " ".join(m.get("content", "").split())[:200])
        print()


if __name__ == "__main__":
    main()
