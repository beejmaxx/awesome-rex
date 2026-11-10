# Contributing

Open a pull request that adds one line to the right section of `README.md`:

```
- [name](link) - What it does, in a sentence or two.
```

Please include only projects that:

- are public and work with Rex today;
- link to their own repository or site, not to Rex downloads, invites, or beta-only channels;
- have a README explaining what they do and how to install them.

Keep descriptions factual, and list new entries at the end of their section. Leave off the star badge: a workflow adds it after merging.

## Maintaining

`scripts/new-from-export.py` lists GitHub repositories mentioned in a Discord channel export (DiscordChatExporter JSON) that aren't in the list yet. CI runs `awesome-lint` on every change and checks all links every Monday. Entries that link to a GitHub repository end with a live shields.io star badge. Whenever `README.md` changes on `main`, the Stars workflow runs `scripts/update-stars.py` to add any missing badges and commits the result. Run it locally with `python3 scripts/update-stars.py`, or add `--check` to report missing badges without writing. After reorganizing sections or a large update, refresh the README preview image with `python3 scripts/render-images.py` (uses headless Google Chrome); add `--since REV --announcement PATH` to also render an image of the projects added since a revision. `assets/social-preview.png` is the card GitHub shows when the repository link is shared. It's drawn by hand, and GitHub has no API for it, so upload changes under Settings > General > Social preview.

To refresh from showcase, install [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) and run:

```sh
python3 scripts/update-from-showcase.py
```

The command reads `DISCORD_TOKEN` from the environment, then the macOS Keychain item `awesome-rex.discord-token` for your login account, or asks with a hidden prompt in an interactive terminal. It exports only the showcase channel, never its threads, then writes `candidates.txt`, `candidates.json`, and run metadata under `.local/showcase/`. Tokens are never placed in command arguments or saved in the repository. The local export directory is ignored by Git. Media is not downloaded, and each run uses a separate snapshot directory.

On macOS, save or replace your token in Keychain once with the following command. The final `-w` prompts for the value instead of putting it in shell history or process arguments:

```sh
security add-generic-password -U -a "$USER" -s awesome-rex.discord-token -w
```

Future refreshes can then use the saved token. If Keychain is locked, unlock it through macOS before running the updater. A revoked or expired token needs to be replaced.

For an incremental export, pass a previous successful snapshot's `startedAt` as `--after`, subtracting ten minutes for overlap:

```sh
python3 scripts/update-from-showcase.py --after 2026-11-01T11:50:00Z
```

This bounds downloads by message creation time, excluding threads entirely. Only advance the cutoff after the exported candidates have been reviewed and any additions published; failed exports or reviews must keep the old cutoff. Omit `--after` to rescan history, including edits to old messages that incremental exports cannot detect.

An agent can scan an existing export without credentials or another download:

```sh
python3 scripts/update-from-showcase.py --from-export /path/to/export/json/
```

The scanner compares exact repository names with the README (scheduled runs also resolve GitHub renames and skip repositories with open pull requests) and keeps each candidate's earliest mention, author, and source message link. It finds GitHub repository links in message text and embed URLs; it does not discover standalone websites or gists. Review candidates against the contribution criteria before adding them. Neither command edits the README, commits, pushes, or posts to Discord.

After reviewing the public projects, add qualifying entries to the appropriate README sections and validate the update:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
npx --yes awesome-lint
git diff --check
```

Then commit and push the requested repository update. Keep raw exports and candidate reports local.
