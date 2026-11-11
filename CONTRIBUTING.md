# Contributing

Open a pull request that adds one line to the right section of `README.md`:

```
- [name](link) - What it does, in one short sentence.
```

Please include only projects that:

- are public and work with Rex today;
- link to their own repository or site, not to Rex downloads, invites, or beta-only channels;
- have a README explaining what they do and how to install them.

Keep descriptions factual and start them with a capital letter ("Menu bar app for macOS", not "macOS menu bar app"). List new entries at the end of their section. Leave off the star badge: a workflow adds it after merging.

## Maintaining

`scripts/new-from-export.py` lists GitHub repositories mentioned in a Discord channel export (DiscordChatExporter JSON) that aren't in the list yet. CI runs the unit tests and `awesome-lint` on every change, and pull requests also check the links they add. Every Monday, the Maintain workflow runs `scripts/maintain-links.py`: renamed repositories get their new URLs, deleted ones are removed, and links it can't repair are listed in the run summary. Only the scripts' own bugs can fail it. Entries that link to a GitHub repository show a live shields.io star badge right after the name. Whenever `README.md` changes on `main`, the Stars workflow runs `scripts/update-stars.py` to add any missing badges and commits the result. Run it locally with `python3 scripts/update-stars.py`, or add `--check` to report missing badges without writing. To announce an update in the showcase channel, `python3 scripts/render-images.py --since REV --announcement PATH` renders the projects added since a revision, grouped by section (uses headless Google Chrome). `--preview PATH` renders a card of every section and its most-starred projects. The README banner (`assets/banner.jpg`) and the card GitHub shows when the repository link is shared (`assets/social-preview.png`, the same art under GitHub's 1 MB limit) are hand-made. GitHub has no API for the social preview, so upload changes under Settings > General > Social preview.

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
