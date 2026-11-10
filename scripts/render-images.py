#!/usr/bin/env python3
"""Render the README preview image, and optionally an update announcement, from README.md.

    scripts/render-images.py                                   # writes assets/preview.png
    scripts/render-images.py --since b6287c4 --announcement .local/update.png

The preview shows each section with its project count and most-starred entries. The
announcement lists the projects added since a Git revision, grouped by section, for
posting to the showcase channel. Rendering uses headless Google Chrome (macOS path by
default, or $CHROME) and looks best with JetBrains Mono installed.
"""
import argparse
import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SKIP = {"Contents", "Contributing", "Official resources"}
ENTRY = re.compile(r"^- \[([^\]]+)\]\((\S+?)\)")
STARS = re.compile(r"\(★ ([\d.]+)(k?)\)$")

STYLE = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { width: %(w)spx; height: %(h)spx; overflow: hidden; color: #e6e9f0;
  font-family: -apple-system, "SF Pro Display", "Inter", "Helvetica Neue", sans-serif;
  background: radial-gradient(circle at 92%% -10%%, #222a35 0 26%%, transparent 26.2%%),
              radial-gradient(circle at 78%% 18%%, #18202b 0 34%%, transparent 34.2%%), #0d131b; }
.mono { font-family: "JetBrains Mono", "SF Mono", Menlo, monospace; }
.accent { color: #f0895a; }
.dim { color: #8a94a6; }
.card { background: #1a2330; border-radius: 16px; padding: 18px 22px; }
.label { color: #f0895a; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; font-size: 15px; }
.row { display: flex; justify-content: space-between; gap: 10px; font-size: 16px; line-height: 27px; }
.row .name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.row .star { color: #8a94a6; font-size: 13px; flex: none; }
"""


def parse(text):
    sections, current = [], None
    for line in text.splitlines():
        if line.startswith("## "):
            current = None if line[3:] in SKIP else {"name": line[3:], "entries": []}
            if current:
                sections.append(current)
        elif current is not None and (match := ENTRY.match(line)):
            stars = STARS.search(line)
            value = float(stars.group(1)) * (1000 if stars.group(2) else 1) if stars else 0
            current["entries"].append({"name": match.group(1), "url": match.group(2).rstrip("/").lower(),
                                       "stars": stars.group(1) + stars.group(2) if stars else "", "value": value})
    return sections


def rows(entries):
    return "".join(f'<div class="row mono"><span class="name">{html.escape(e["name"])}</span>'
                   f'<span class="star">{"★ " + e["stars"] if e["stars"] else ""}</span></div>' for e in entries)


def preview(sections):
    total = sum(len(s["entries"]) for s in sections)
    cards = "".join(
        f'<div class="card"><div class="label">{html.escape(s["name"])}</div>'
        f'<div class="dim" style="font-size:14px;margin:4px 0 10px">{len(s["entries"])} project{"s" if len(s["entries"]) != 1 else ""}</div>'
        f'{rows(sorted(s["entries"], key=lambda e: -e["value"])[:3])}</div>' for s in sections)
    return f"""<style>{STYLE % {"w": 1600, "h": 750}}
.grid {{ position: absolute; inset: 56px 60px; display: grid; gap: 18px;
  grid-template-columns: repeat(5, 1fr); grid-template-rows: repeat(3, 1fr); }}
.head {{ grid-column: span 2; display: flex; flex-direction: column; justify-content: center; padding-left: 4px; }}
</style><div class="grid"><div class="head">
<div style="font-size:72px;font-weight:800;letter-spacing:-.02em;line-height:1">awesome-rex</div>
<div class="dim" style="font-size:19px;margin-top:14px">Tools, plugins and integrations for Rex, collected from #showcase</div>
<div class="mono accent" style="font-size:19px;margin-top:8px">github.com/beejmaxx/awesome-rex</div>
<div class="dim" style="font-size:16px;margin-top:16px">{total} projects · {len(sections)} sections · ★ refreshed weekly · PRs welcome</div>
</div>{cards}</div>"""


def announcement(sections, before, merged_prs):
    new = [{"name": s["name"], "entries": [e for e in s["entries"] if e["url"] not in before]} for s in sections]
    new = [s for s in new if s["entries"]]
    added = sum(len(s["entries"]) for s in new)
    total = sum(len(s["entries"]) for s in sections)
    groups = "".join(f'<div class="group"><div class="label" style="margin-bottom:6px">{html.escape(s["name"])}</div>'
                     f'{rows(s["entries"])}</div>' for s in new)
    prs = f" · {merged_prs} community PRs merged" if merged_prs else ""
    return f"""<style>{STYLE % {"w": 1600, "h": 1000}}
.wrap {{ position: absolute; inset: 56px 64px 48px; display: flex; flex-direction: column; }}
.cols {{ column-count: 5; column-gap: 18px; margin-top: 30px; flex: 1; }}
.group {{ break-inside: avoid; background: #1a2330; border-radius: 14px; padding: 14px 18px 12px; margin-bottom: 16px; }}
</style><div class="wrap">
<div style="display:flex;align-items:baseline;gap:22px">
<div style="font-size:30px;font-weight:700">awesome-rex</div>
<div class="mono accent" style="font-size:20px">github.com/beejmaxx/awesome-rex</div></div>
<div style="font-size:84px;font-weight:800;letter-spacing:-.02em;line-height:1.05;margin-top:12px">+{added} new projects</div>
<div class="dim" style="font-size:22px;margin-top:10px">{total - added} → {total} projects{prs} · reorganized into {len(sections)} sections · ★ star counts, refreshed weekly</div>
<div class="cols">{groups}</div>
<div class="dim" style="font-size:17px">Built something for Rex? Post it in #showcase or open a PR.</div>
</div>"""


def render(page, out, width, height):
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp, "page.html")
        source.write_text(f'<!doctype html><meta charset="utf-8">{page}', encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        f"--window-size={width},{height}", f"--screenshot={out}", source.as_uri()],
                       check=True, capture_output=True, timeout=120)
    print(f"Wrote {out}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--preview", type=Path, default=ROOT / "assets/preview.png")
    parser.add_argument("--since", help="Git revision to compare against for the announcement")
    parser.add_argument("--announcement", type=Path, help="Where to write the announcement image")
    parser.add_argument("--merged-prs", type=int, default=0, help="Community PRs merged since --since")
    parser.add_argument("--renamed", action="append", default=[], metavar="OLD=NEW",
                        help="Treat a renamed entry's new URL as already listed")
    args = parser.parse_args()
    sections = parse((ROOT / "README.md").read_text(encoding="utf-8"))
    render(preview(sections), args.preview.resolve(), 1600, 750)
    if args.announcement:
        if not args.since:
            parser.error("--announcement needs --since")
        old = subprocess.run(["git", "show", f"{args.since}:README.md"], cwd=ROOT, check=True,
                             capture_output=True, text=True).stdout
        before = {e["url"] for s in parse(old) for e in s["entries"]}
        for pair in args.renamed:
            old_url, new_url = pair.split("=", 1)
            if old_url.rstrip("/").lower() in before:
                before.add(new_url.rstrip("/").lower())
        render(announcement(sections, before, args.merged_prs), args.announcement.resolve(), 1600, 1000)


if __name__ == "__main__":
    sys.exit(main())
