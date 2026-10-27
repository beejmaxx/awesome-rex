# Awesome Rex [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of tools, plugins, and integrations for [Rex](https://www.superlogical.com/rex), the terminal workspace by Superlogical. Rex is in closed beta, so most of these are early and move fast.

Everything here is a public project built on Rex's documented Lua config, CLI, and server API. This list doesn't link to Rex downloads or to beta-only channels.

## Contents

- [Sessions and recovery](#sessions-and-recovery)
- [Coding agents](#coding-agents)
- [Agent dashboards](#agent-dashboards)
- [Editors](#editors)
- [Code review](#code-review)
- [Workflow utilities](#workflow-utilities)
- [Frameworks](#frameworks)
- [Fun](#fun)
- [Official resources](#official-resources)

## Sessions and recovery

- [rexume](https://github.com/Entwining/rexume) - Restores sessions, tabs, splits, working directories, and Claude Code, Codex, and Pi conversations after the Rex server stops. Re-prompts only agents whose turn was cut off.
- [rexurrect](https://github.com/cemcatik/rexurrect) - Saves sessions and recreates them after a crash, update, or reboot, like tmux-resurrect. Keeps scrollback.
- [rexkit](https://github.com/snipeship/rexkit) - Session manager that can create, rename, and close sessions, plus a file picker, tmux/zellij-style keybindings, and scrollback in Neovim.
- [raycast-rex-sessions](https://github.com/esttorhe/raycast-rex-sessions) - Raycast extension for switching Rex sessions, sesh entries, and zoxide directories.

## Coding agents

- [rex-agent-kit](https://github.com/theJiawen/rex-agent-kit) - Agent Wall tiles every tab into one grid and back again without restarting anything (it uses `session.move_block`). Also adds a key that opens a tab with Claude Code running.
- [ah](https://github.com/david-crespo/ah) - Local server and CLI for HTML tools that talk back to the agent running in a Rex tab: dashboards, task trackers, Markdown preview, diff and HTML viewers, all with highlight-and-comment.
- [Amber](https://amber.benhid.dev/) - When a Claude Code session goes idle, suggests changes to your `CLAUDE.md` for you to accept or reject.

## Agent dashboards

- [rex-radar](https://github.com/hecspc/rex-radar) - Menu bar app, widget, and iPhone, iPad, and Apple Watch apps showing every Claude agent across your Rex servers. Answer questions and jump to panes. Build it yourself in Xcode.
- [rexboard](https://github.com/vanducng/rexboard) - Attention board for agent panes on every host: which one is waiting, for how long, and a key to jump there.
- [cheap-rex-display](https://github.com/yethranayeh/cheap-rex-display) - ESP32 "Cheap Yellow Display" that shows agent status on your desk and blinks when one needs you.
- [ai-usage](https://github.com/trishtzy/ai-usage) - Tracks Claude Code, Codex, and other AI usage limits inside Rex.

## Editors

- [rex-navigator.nvim](https://github.com/baggiponte/rex-navigator.nvim) - `Ctrl-h/j/k/l` across Neovim windows and Rex panes, like vim-tmux-navigator.
- [smart-splits-backend-rex](https://github.com/rawnly/smart-splits-backend-rex) - Rex backend for smart-splits.nvim: navigate and resize across Neovim and Rex.
- [nvim-rex](https://github.com/theboxer/nvim-rex) - Seamless navigation between Neovim and Rex.

## Code review

- [rexdiff](https://github.com/rednafi/rexdiff) - Review what a coding agent changed without leaving Rex, in the style of herdr-reviewr.
- [reviewr.nvim](https://github.com/paul-enz/reviewr.nvim) - Review git diffs in Neovim and send line comments to an agent running in Rex, tmux, or WezTerm.

## Workflow utilities

- [rex-opener](https://github.com/shaheislam/rex-opener) - Open URLs and file paths from terminal output with configurable keybindings.
- [rex-image-paste](https://github.com/pablasso/rex-image-paste) - Paste images into remote hosts by copying them to a temporary file there (`Cmd+Shift+V`).
- [rex-nobeta-icon](https://github.com/Stanzilla/rex-nobeta-icon) - Replaces the beta app icon with the plain one. Re-run it after each update.

## Frameworks

- [LazyRex](https://github.com/lazy-rex/LazyRex) - Plugin hub for Rex with versioned plugins, dependencies, per-plugin databases, cross-server messaging, a TUI renderer, and plugin palette and CLI commands.

## Fun

- [rex-orbit](https://github.com/benhid/rex-orbit) - Your Claude Code agents as pixel bots orbiting a dinosaur, drawn with Kitty graphics.

## Official resources

- [Rex](https://www.superlogical.com/rex) - Product page.
- [Documentation](https://www.superlogical.com/rex/docs) - Lua config, keybindings, CLI, and the server API.

## Contributing

Additions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
