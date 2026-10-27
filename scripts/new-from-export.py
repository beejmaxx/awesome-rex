#!/usr/bin/env python3
"""List GitHub repositories mentioned in a Discord channel export that aren't in README.md yet.

Point it at a DiscordChatExporter JSON file, or a directory of them (threads included):

    scripts/new-from-export.py path/to/export/

Each candidate prints with its earliest mention: date, author, message link, and text.
Use --json for machine-readable results. To fetch a fresh export first, run
scripts/update-from-showcase.py instead.
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)")
# GitHub paths that aren't repositories.
SKIP_OWNERS = {"user-attachments", "orgs", "settings", "features", "sponsors"}
SKIP_REPOS = {"beejmaxx/awesome-rex"}  # Announcements of this list aren't additions.


def repositories(text):
    for repo in REPO.findall(text):
        repo = repo.rstrip(".").removesuffix(".git")
        if repo.split("/")[0].lower() not in SKIP_OWNERS:
            yield repo


def messages(path):
    if not path.exists():
        raise ValueError(f"Export path does not exist: {path}")
    files = sorted(path.rglob("*.json")) if path.is_dir() else [path]
    exports = 0
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise ValueError(f"Cannot read {f}: {error}") from error
        # Ignore manifests and other JSON stored alongside channel exports.
        if not isinstance(data, dict) or not isinstance(data.get("channel"), dict):
            continue
        if not isinstance(data.get("messages"), list):
            raise ValueError(f"Missing message array in export: {f}")
        exports += 1
        for message in data["messages"]:
            if not isinstance(message, dict):
                raise ValueError(f"Invalid message in export: {f}")
            yield message, data, f
    if not exports:
        raise ValueError(f"No DiscordChatExporter channel JSON files found in {path}")


def mention_order(candidate):
    stamp = candidate["timestamp"]
    try:
        date = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
    except ValueError:
        date = datetime.max.replace(tzinfo=timezone.utc)
    return date, candidate["url"]


def find_candidates(path, readme):
    existing = {repo.lower() for repo in repositories(readme)}
    seen = {}
    for message, export, source in messages(path):
        content = message.get("content") or ""
        text = content + " " + " ".join(
            embed.get("url") or "" for embed in message.get("embeds", [])
        )
        for repo in repositories(text):
            key = repo.lower()
            if key in existing or key in SKIP_REPOS:
                continue
            author = message.get("author") or {}
            guild = export.get("guild", {}).get("id")
            channel = export["channel"].get("id")
            mid = message.get("id")
            message_url = (
                f"https://discord.com/channels/{guild}/{channel}/{mid}"
                if guild and channel and mid else None
            )
            candidate = {
                "repository": repo,
                "url": f"https://github.com/{repo}",
                "timestamp": message.get("timestamp") or "",
                "author": author.get("nickname") or author.get("name") or author.get("username") or "?",
                "content": content,
                "messageUrl": message_url,
                "sourceFile": str(source),
            }
            if key not in seen or mention_order(candidate) < mention_order(seen[key]):
                seen[key] = candidate
    return sorted(seen.values(), key=mention_order)


def format_candidates(candidates):
    if not candidates:
        return "Nothing new.\n"
    blocks = []
    for candidate in candidates:
        lines = [
            candidate["url"],
            f"  {candidate['timestamp'][:10]}  {candidate['author']}",
        ]
        if candidate["messageUrl"]:
            lines.append("  " + candidate["messageUrl"])
        lines.append("  " + " ".join(candidate["content"].split())[:200])
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    parser.add_argument("--readme", type=Path, default=Path(__file__).resolve().parent.parent / "README.md")
    parser.add_argument("--json", action="store_true", help="Print candidates as JSON")
    args = parser.parse_args()
    try:
        candidates = find_candidates(args.export, args.readme.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    if args.json:
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(format_candidates(candidates))


if __name__ == "__main__":
    main()
