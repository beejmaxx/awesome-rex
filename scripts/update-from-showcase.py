#!/usr/bin/env python3
"""Export Rex's showcase and threads, then write candidates for an awesome-rex update.

Requires the installed DiscordChatExporter CLI. Reads DISCORD_TOKEN from the
environment, then macOS Keychain. In an interactive terminal, a missing token
is requested with echo disabled.
Use --from-export PATH to scan an existing export without Discord access.
"""
import argparse
import getpass
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOWCASE = "1562386678499250246"
KEYCHAIN_SERVICE = "awesome-rex.discord-token"


def saved_token():
    """Read only this project's Keychain item, keeping its value out of output."""
    if sys.platform != "darwin" or not shutil.which("security"):
        return ""
    result = subprocess.run([
        "security", "find-generic-password", "-a", getpass.getuser(),
        "-s", KEYCHAIN_SERVICE, "-w",
    ], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def scanner():
    spec = importlib.util.spec_from_file_location("export_scanner", ROOT / "scripts/new-from-export.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-export", type=Path, help="Skip downloading; read this export file or directory")
    parser.add_argument("--output-dir", type=Path, help="New directory for exports and reports; defaults to .local/showcase/<UTC timestamp>")
    parser.add_argument("--channel", default=SHOWCASE, help="Channel ID to export (default: Rex showcase)")
    args = parser.parse_args()
    started = datetime.now(timezone.utc)
    run_dir = (args.output_dir or ROOT / ".local/showcase" / started.strftime("%Y%m%dT%H%M%S.%fZ")).expanduser().resolve()
    # Each run is separate, so a failed export cannot be mistaken for an older one.
    if run_dir.exists():
        parser.exit(1, f"Error: output directory already exists: {run_dir}\n")
    export_path = args.from_export.expanduser().resolve() if args.from_export else run_dir / "json"
    if args.from_export and not export_path.exists():
        parser.exit(1, f"Error: export path does not exist: {export_path}\n")
    if not args.from_export:
        exporter = shutil.which("discord-chat-exporter") or shutil.which("DiscordChatExporter.Cli")
        if not exporter:
            parser.exit(1, "Error: install DiscordChatExporter.Cli or put discord-chat-exporter on PATH.\n")
        token = os.environ.get("DISCORD_TOKEN", "").strip() or saved_token()
        if not token:
            if not sys.stdin.isatty():
                parser.exit(1, "Error: no DISCORD_TOKEN or readable macOS Keychain token. Set the environment variable, unlock/save the Keychain item, or run interactively for a hidden prompt.\n")
            token = getpass.getpass("Discord token (hidden; not saved): ").strip()
        if not token:
            parser.exit(1, "Error: empty Discord token.\n")
        run_dir.mkdir(parents=True, mode=0o700)
        command = [
            exporter, "export", "--channel", args.channel,
            "--format", "Json", "--include-threads", "All",
            "--before", started.isoformat(), "--utc", "true",
            "--markdown", "false", "--media", "false",
            "--output", str(export_path) + os.sep,
        ]
        env = dict(os.environ, DISCORD_TOKEN=token)
        print("Exporting showcase and all accessible threads (text only)...", flush=True)
        result = subprocess.run(command, env=env)
        del token, env
        if result.returncode:
            parser.exit(1, f"Error: exporter exited with {result.returncode}; no candidate report was generated. Partial files: {run_dir}\n")
    try:
        scan = scanner()
        candidates = scan.find_candidates(export_path, (ROOT / "README.md").read_text(encoding="utf-8"))
        report = scan.format_candidates(candidates)
        run_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        (run_dir / "candidates.json").write_text(json.dumps(candidates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (run_dir / "candidates.txt").write_text(report, encoding="utf-8")
        (run_dir / "run.json").write_text(json.dumps({
            "startedAt": started.isoformat(),
            "channelId": args.channel,
            "exportPath": str(export_path),
            "downloaded": not bool(args.from_export),
            "candidateCount": len(candidates),
        }, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"\nFound {len(candidates)} candidate(s). Review report: {run_dir / 'candidates.txt'}\n")
    sys.stdout.write(report)
    print("Review each public project before editing README.md. Reports and exports stay local.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nUpdate interrupted; no README changes were made.")
