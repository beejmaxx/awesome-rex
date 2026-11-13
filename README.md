# Awesome Rex [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

![awesome-rex: tools, plugins and integrations for Rex](assets/banner.jpg)

A curated list of public tools, plugins, and integrations for Rex, the terminal workspace by Superlogical, built on its documented Lua config, CLI, and server API. Rex is in closed beta, so most of these are early and move fast. *demo* links go to a GIF, video, or screenshot.

## Contents

- [Sessions and workspaces](#sessions-and-workspaces)
- [Recovery](#recovery)
- [Mobile clients](#mobile-clients)
- [Coding agents](#coding-agents)
- [Agent dashboards](#agent-dashboards)
- [Editors](#editors)
- [Code review](#code-review)
- [Pickers and navigation](#pickers-and-navigation)
- [Previews and media](#previews-and-media)
- [Themes and appearance](#themes-and-appearance)
- [Workflow utilities](#workflow-utilities)
- [Frameworks](#frameworks)
- [Fun](#fun)
- [Official resources](#official-resources)

## Sessions and workspaces

- [rexkit](https://github.com/snipeship/rexkit) ![Stars](https://img.shields.io/github/stars/snipeship/rexkit?style=social) - Session manager with a file picker and tmux-style keybindings. ([demo](https://github.com/user-attachments/assets/d1d325c4-4cff-4e40-b755-0541d977c1b7))
- [raycast-rex-sessions](https://github.com/esttorhe/raycast-rex-sessions) ![Stars](https://img.shields.io/github/stars/esttorhe/raycast-rex-sessions?style=social) - Raycast extension for switching sessions, sesh entries, and zoxide directories.
- [rex-sessionizer](https://github.com/haxybaxy/rex-sessionizer) ![Stars](https://img.shields.io/github/stars/haxybaxy/rex-sessionizer?style=social) - Floating fzf project picker that opens or creates a directory's session.
- [herdr2rex](https://github.com/tornikegomareli/herdr2rex) ![Stars](https://img.shields.io/github/stars/tornikegomareli/herdr2rex?style=social) - Imports herdr workspaces into Rex, including resumable agent conversations.
- [rex-sessions by arnold-c](https://github.com/arnold-c/rex-sessions) ![Stars](https://img.shields.io/github/stars/arnold-c/rex-sessions?style=social) - Fuzzy session and project picker with pinned sessions and remote servers.
- [resh](https://github.com/CruelAddict/resh) ![Stars](https://img.shields.io/github/stars/CruelAddict/resh?style=social) - Native macOS session manager with project discovery and an agent view.
- [rex-sessions-alfred](https://github.com/LouLouLibs/rex-sessions-alfred) ![Stars](https://img.shields.io/github/stars/LouLouLibs/rex-sessions-alfred?style=social) - Alfred workflow for finding and switching to local and remote Rex tabs.
- [rexp](https://github.com/itsjustaplant/rexp) ![Stars](https://img.shields.io/github/stars/itsjustaplant/rexp?style=social) - Saves and launches project workspaces defined in YAML.
- [sex](https://github.com/rtuszik/sex) ![Stars](https://img.shields.io/github/stars/rtuszik/sex?style=social) - Session picker combining Rex sessions, sesh config, and zoxide directories.
- [rex-sessionizer by 0xViva](https://github.com/0xViva/rex-sessionizer) ![Stars](https://img.shields.io/github/stars/0xViva/rex-sessionizer?style=social) - Fzf project switcher that opens sessions and runs configured commands.
- [hatch](https://github.com/gcacoutinho/rex-hatch) ![Stars](https://img.shields.io/github/stars/gcacoutinho/rex-hatch?style=social) - Creates sessions from per-project Lua layout files, with an fzf picker.
- [ghostmux](https://github.com/jackkeller/ghostmux) ![Stars](https://img.shields.io/github/stars/jackkeller/ghostmux?style=social) - Launches YAML-defined sessions, tabs, and pane layouts on macOS.
- [lazyrex](https://github.com/rbobillot/lazyrex) ![Stars](https://img.shields.io/github/stars/rbobillot/lazyrex?style=social) - Terminal UI for managing sessions, windows, and panes across Rex servers.

## Recovery

- [rexume](https://github.com/Entwining/rexume) ![Stars](https://img.shields.io/github/stars/Entwining/rexume?style=social) - Restores sessions and agent conversations after the Rex server stops.
- [rexurrect](https://github.com/cemcatik/rexurrect) ![Stars](https://img.shields.io/github/stars/cemcatik/rexurrect?style=social) - Saves and recreates sessions after a crash or reboot, like tmux-resurrect.
- [rex-sessions](https://github.com/AlbertoBarrago/rex-sessions) ![Stars](https://img.shields.io/github/stars/AlbertoBarrago/rex-sessions?style=social) - Saves and restores layouts and working directories, with macOS autosave.
- [rex-agent-archive](https://github.com/unknowntheory/rex-agent-archive) ![Stars](https://img.shields.io/github/stars/unknowntheory/rex-agent-archive?style=social) - Archives Claude Code and Codex conversations when tabs close, to resume later.
- [rex-agent-resume](https://github.com/YangJonghun/rex-agent-resume) ![Stars](https://img.shields.io/github/stars/YangJonghun/rex-agent-resume?style=social) - Resumes coding agents in their original panes after a server restart on macOS.
- [rex-restore-claude](https://github.com/marfillaster/rex-restore-claude) ![Stars](https://img.shields.io/github/stars/marfillaster/rex-restore-claude?style=social) - Puts a Claude Code resume command in each pane's prompt after a restart.

## Mobile clients

- [RexPocket](https://github.com/leizhiyuan/rexpocket) ![Stars](https://img.shields.io/github/stars/leizhiyuan/rexpocket?style=social) - Android client for browsing sessions and sending input (build from source).
- [Rexling](https://github.com/shulhi/rexling) ![Stars](https://img.shields.io/github/stars/shulhi/rexling?style=social) - Unofficial Android client for Rex terminals across servers over Tailscale.
- [rexc](https://github.com/Nam0101/rexc) ![Stars](https://img.shields.io/github/stars/Nam0101/rexc?style=social) - Android client with sessions, terminals, and an inbox for blocked agents.
- [Rhubarb](https://github.com/Joshua-Wise/rhubarb) ![Stars](https://img.shields.io/github/stars/Joshua-Wise/rhubarb?style=social) - Unofficial Android client with live terminals and agent alerts over Tailscale.

## Coding agents

- [rex-agent-kit](https://github.com/theJiawen/rex-agent-kit) ![Stars](https://img.shields.io/github/stars/theJiawen/rex-agent-kit?style=social) - Tiles every tab into one grid and back, plus a key for a Claude Code tab. ([demo](https://github.com/theJiawen/rex-agent-kit/blob/main/docs/agent-wall.gif))
- [ah](https://github.com/david-crespo/ah) ![Stars](https://img.shields.io/github/stars/david-crespo/ah?style=social) - HTML tools such as dashboards and diff viewers that talk back to your agent. ([demo](https://github.com/david-crespo/ah#readme))
- [Amber](https://amber.benhid.dev/) - Suggests `CLAUDE.md` changes when a Claude Code session goes idle.
- [Pi runbook](https://github.com/polo871209/dotfiles/tree/main/.pi/agent/extensions/runbook) - Turns commands from Pi agents into steps you run, paste, or copy.
- [rexgram](https://github.com/beejmaxx/rexgram) ![Stars](https://img.shields.io/github/stars/beejmaxx/rexgram?style=social) - Talk to the Claude Code and Codex agents in your panes from Telegram.
- [rex-launch](https://github.com/nicosuave/rex-launch) ![Stars](https://img.shields.io/github/stars/nicosuave/rex-launch?style=social) - Popup that launches Claude Code or Codex with a prompt in a new Git worktree.
- [rex-mcp-bridge](https://github.com/fatwang2/rex-mcp-bridge) ![Stars](https://img.shields.io/github/stars/fatwang2/rex-mcp-bridge?style=social) - MCP server that lets agents read and run commands in visible Rex windows.
- [rex-agent-relay](https://github.com/civitaspo/rex-agent-relay) ![Stars](https://img.shields.io/github/stars/civitaspo/rex-agent-relay?style=social) - Relays turns and changed files between paired Claude Code and Codex agents.
- [Rex extensions for Claude Code](https://github.com/evgeny-golubev/rex-extensions) ![Stars](https://img.shields.io/github/stars/evgeny-golubev/rex-extensions?style=social) - Adds an activity sidecar, conversation recovery, and file previews on macOS.
- [clnkr](https://github.com/clnkr-ai/clnkr) ![Stars](https://img.shields.io/github/stars/clnkr-ai/clnkr?style=social) - Coding agent CLI that reports its state to Rex's status indicators.
- [hermes-rex](https://github.com/vanhoof/hermes-rex) ![Stars](https://img.shields.io/github/stars/vanhoof/hermes-rex?style=social) - Hermes Agent plugin for Rex program status and pane context.
- [rex-grokbot-bridge](https://github.com/smarzban/rex-grokbot-bridge) ![Stars](https://img.shields.io/github/stars/smarzban/rex-grokbot-bridge?style=social) - MCP and webhook bridge that lets Grok Bot inspect and control Rex panes.
- [tr3x](https://github.com/macnason/tr3x) ![Stars](https://img.shields.io/github/stars/macnason/tr3x?style=social) - Shows T3 Code conversations as Rex tabs, with replies sent back to T3.
- [barbasol-can](https://github.com/pthm/barbasol-can) ![Stars](https://img.shields.io/github/stars/pthm/barbasol-can?style=social) - Moves Claude Code, Codex, and OpenCode conversations to another Rex host.
- [rex-claude](https://www.aitmpl.com/component/skill/productivity/rex-claude) - Claude Code skill that opens and drives other Claude Code sessions in panes.
- [pi-rex-agents](https://github.com/JohnWJ-co/pi-rex-agents) ![Stars](https://img.shields.io/github/stars/JohnWJ-co/pi-rex-agents?style=social) - Runs Pi subagents in Rex panes, tabs, or minimized layers and returns results automatically.

## Agent dashboards

- [rex-radar](https://github.com/hecspc/rex-radar) ![Stars](https://img.shields.io/github/stars/hecspc/rex-radar?style=social) - Menu bar, widget, iPhone, and Watch apps for Claude agents (build from source). ([demo](https://github.com/hecspc/rex-radar/blob/main/docs/screenshots/mac-panel.png))
- [rexboard](https://github.com/vanducng/rexboard) ![Stars](https://img.shields.io/github/stars/vanducng/rexboard?style=social) - Attention board showing which agent panes are waiting, and for how long. ([demo](https://github.com/vanducng/rexboard/blob/main/docs/assets/demo.gif))
- [cheap-rex-display](https://github.com/yethranayeh/cheap-rex-display) ![Stars](https://img.shields.io/github/stars/yethranayeh/cheap-rex-display?style=social) - ESP32 desk display that shows agent status and blinks when one needs you. ([demo](https://res.cloudinary.com/drwbqceye/image/upload/v1792852978/opencode-status-cycle_r6f1ad.webp))
- [ai-usage](https://github.com/trishtzy/ai-usage) ![Stars](https://img.shields.io/github/stars/trishtzy/ai-usage?style=social) - Tracks Claude Code, Codex, and other AI usage limits inside Rex. ([demo](https://github.com/trishtzy/ai-usage/blob/main/ai-usage-demo.gif))
- [rex-usage](https://github.com/AlbertoBarrago/rex-usage) ![Stars](https://img.shields.io/github/stars/AlbertoBarrago/rex-usage?style=social) - Claude Code and Codex usage dashboard with token charts and cost estimates.
- [Shepherd](https://github.com/getshepherd/shepherd) ![Stars](https://img.shields.io/github/stars/getshepherd/shepherd?style=social) - Desktop agent dashboard with an experimental Rex backend on macOS.
- [Opscope mux-activity](https://github.com/stealth-factory/opscope/tree/main/widgets/src/widgets/mux-activity) - Lists Rex agents and processes by how much attention they need.
- [rexpad](https://github.com/almonk/rexpad) ![Stars](https://img.shields.io/github/stars/almonk/rexpad?style=social) - Live agent todo lists rendered beside the agent.
- [rex-micro](https://github.com/JiehoonKwak/rex-micro) ![Stars](https://img.shields.io/github/stars/JiehoonKwak/rex-micro?style=social) - Turns a Work Louder Codex Micro into an agent status display and controller.
- [rexq](https://github.com/tfcace/rexq) ![Stars](https://img.shields.io/github/stars/tfcace/rexq?style=social) - Floating inbox for questions and decisions from Claude Code and Pi.
- [Tea](https://github.com/ianiv/tea) ![Stars](https://img.shields.io/github/stars/ianiv/tea?style=social) - Menu bar monitor for macOS that jumps to Claude Code panes (build from source).
- [agentmeter](https://github.com/SaeedNoshadi89/agentmeter) ![Stars](https://img.shields.io/github/stars/SaeedNoshadi89/agentmeter?style=social) - Shows remaining Claude Code and Codex usage limits in a popup or pane.
- [Rex's Tail](https://github.com/travelingflwr/rex-tail) ![Stars](https://img.shields.io/github/stars/travelingflwr/rex-tail?style=social) - Panel beside Rex on macOS showing agent activity and weather (build from source).
- [rex-agents](https://github.com/irfn/rex-agents) ![Stars](https://img.shields.io/github/stars/irfn/rex-agents?style=social) - Agent sidebar across hosts that jumps to agents waiting for input.

## Editors

- [rex-navigator.nvim](https://github.com/baggiponte/rex-navigator.nvim) ![Stars](https://img.shields.io/github/stars/baggiponte/rex-navigator.nvim?style=social) - `Ctrl-h/j/k/l` across Neovim windows and Rex panes, like vim-tmux-navigator. ([demo](https://github.com/baggiponte/rex-navigator.nvim/blob/main/docs/assets/navigation.gif))
- [smart-splits-backend-rex](https://github.com/rawnly/smart-splits-backend-rex) ![Stars](https://img.shields.io/github/stars/rawnly/smart-splits-backend-rex?style=social) - Rex backend for smart-splits.nvim: navigate and resize across Neovim and Rex.
- [nvim-rex](https://github.com/theboxer/nvim-rex) ![Stars](https://img.shields.io/github/stars/theboxer/nvim-rex?style=social) - Seamless navigation between Neovim and Rex.
- [neorex](https://github.com/alexrlocke/neorex) ![Stars](https://img.shields.io/github/stars/alexrlocke/neorex?style=social) - Neovim frontend for macOS that maps editor splits to Rex panes.
- [colorrex.nvim](https://github.com/reklai/colorrex.nvim) ![Stars](https://img.shields.io/github/stars/reklai/colorrex.nvim?style=social) - Neovim colorscheme built from Rex's terminal palette, updated live.
- [navigator.nvim](https://github.com/omenlog/neovim-navigator) ![Stars](https://img.shields.io/github/stars/omenlog/neovim-navigator?style=social) - Moves focus between Neovim splits and Rex panes with the same keys.
- [lazyrex.nvim](https://github.com/omenlog/lazyrex) ![Stars](https://img.shields.io/github/stars/omenlog/lazyrex?style=social) - Persistent LazyGit float that opens files in the originating Neovim.
- [vim-rex-navigator](https://github.com/pankrashin/vim-rex-navigator) ![Stars](https://img.shields.io/github/stars/pankrashin/vim-rex-navigator?style=social) - Focus, move, resize, and close Vim windows and Rex panes with the same keys.
- [rex-runner.nvim](https://github.com/oligot/rex-runner.nvim) ![Stars](https://img.shields.io/github/stars/oligot/rex-runner.nvim?style=social) - Port of vim-tmux-runner: sends lines and commands to a scratch pane.
- [Rexel](https://github.com/dakra/rexel) ![Stars](https://img.shields.io/github/stars/dakra/rexel?style=social) - Emacs client for attaching to Rex sessions and managing terminals through Ghostel.

## Code review

- [rexdiff](https://github.com/rednafi/rexdiff) ![Stars](https://img.shields.io/github/stars/rednafi/rexdiff?style=social) - Review what a coding agent changed without leaving Rex, like herdr-reviewr. ([demo](https://github.com/user-attachments/assets/d56af0f9-e1ff-422d-b0e7-0e5afe3320ae))
- [reviewr.nvim](https://github.com/paul-enz/reviewr.nvim) ![Stars](https://img.shields.io/github/stars/paul-enz/reviewr.nvim?style=social) - Review Git diffs in Neovim and send line comments to an agent in Rex. ([demo](https://github.com/paul-enz/reviewr.nvim/blob/main/assets/demo.gif))
- [tuicr](https://github.com/agavra/tuicr) ![Stars](https://img.shields.io/github/stars/agavra/tuicr?style=social) - Terminal diff reviewer with line comments, plus a skill to open it in Rex.
- [rexdiff by victorvf](https://github.com/victorvf/rexdiff) ![Stars](https://img.shields.io/github/stars/victorvf/rexdiff?style=social) - Live file tree and Git diffs in a pane, with staging and commits.
- [rexamine](https://github.com/segersniels/rexamine) ![Stars](https://img.shields.io/github/stars/segersniels/rexamine?style=social) - Review local changes or a GitHub PR and send line comments to your agent. ([demo](https://github.com/segersniels/rexamine/blob/main/assets/demo.gif))
- [rex.nvim](https://github.com/rawnly/rex.nvim) ![Stars](https://img.shields.io/github/stars/rawnly/rex.nvim?style=social) - Annotate code in Neovim and send comments to a coding agent in Rex. ([demo](https://github.com/user-attachments/assets/47bc945d-6377-4df5-80a6-93bd219fd1b6))
- [rex-relay.nvim](https://github.com/crierr/rex-relay.nvim) ![Stars](https://img.shields.io/github/stars/crierr/rex-relay.nvim?style=social) - Sends file:line references and review comments from Neovim to agents in Rex.

## Pickers and navigation

- [Pane Switcher for Rex](https://github.com/Kristijan/pane-switcher-for-rex) ![Stars](https://img.shields.io/github/stars/Kristijan/pane-switcher-for-rex?style=social) - Native macOS picker that searches panes across local and remote hosts.
- [rex-opener](https://github.com/shaheislam/rex-opener) ![Stars](https://img.shields.io/github/stars/shaheislam/rex-opener?style=social) - Open URLs and file paths from terminal output with configurable keybindings. ([demo](https://github.com/shaheislam/rex-opener/blob/main/assets/demo.gif))
- [Tab Numbers for Rex](https://github.com/manishprivet/.dotfiles/tree/main/.config/rex/extensions/tab-numbers) - Numbers tab titles to match indexed keyboard shortcuts on macOS.
- [rex-worktrunk](https://github.com/haxybaxy/rex-worktrunk) ![Stars](https://img.shields.io/github/stars/haxybaxy/rex-worktrunk?style=social) - Fzf pickers for Git worktrees through worktrunk, with a session per worktree.
- [sshpick](https://github.com/calvindotnow/sshpick) ![Stars](https://img.shields.io/github/stars/calvindotnow/sshpick?style=social) - Floating SSH host picker that opens connections in named tabs.
- [Rex Worktrees](https://github.com/samuelho-dev/rex-worktrees) ![Stars](https://img.shields.io/github/stars/samuelho-dev/rex-worktrees?style=social) - Picker for Git worktrees and Jujutsu workspaces in Rex sessions.
- [Rex copy-mode](https://github.com/CJNE/rex-copy-mode) ![Stars](https://img.shields.io/github/stars/CJNE/rex-copy-mode?style=social) - Opens scrollback in a Neovim overlay for keyboard search and copying.
- [rex-open](https://github.com/HaydenMeloche/rex-open) ![Stars](https://img.shields.io/github/stars/HaydenMeloche/rex-open?style=social) - Picks files, links, commands, and SQL from pane output to open or copy.
- [rex-fzf-url](https://github.com/devert/rex-fzf-url) ![Stars](https://img.shields.io/github/stars/devert/rex-fzf-url?style=social) - Floating fzf picker for opening or copying URLs from pane scrollback.
- [rex-fingers](https://github.com/xeind/rex-fingers) ![Stars](https://img.shields.io/github/stars/xeind/rex-fingers?style=social) - Letter hints to copy paths, URLs, and hashes from a pane, like tmux-fingers.

## Previews and media

- [Rex Markdown for Pi](https://github.com/jal-co/jalco-dotfiles/tree/main/tools/rex-markdown) - Previews Markdown links from Pi beside the originating pane on macOS.
- [krd](https://github.com/zzjcool/krd) ![Stars](https://img.shields.io/github/stars/zzjcool/krd?style=social) - Shows and controls a macOS desktop in a Rex pane over SSH with Kitty graphics.
- [tkmp](https://github.com/tfcace/tkmp) ![Stars](https://img.shields.io/github/stars/tfcace/tkmp?style=social) - Live Markdown and Mermaid previews in a pane through Kitty graphics.
- [md-viewer](https://github.com/good-banana/rexworks/tree/main/md-viewer) - Renders Markdown in a Rex pane with links, search, and live updates.
- [rexshow](https://github.com/wcwung/rexshow) ![Stars](https://img.shields.io/github/stars/wcwung/rexshow?style=social) - Shows screenshots and screen recordings beside your coding agents.
- [rex-canvas](https://github.com/AlbertoBarrago/rex-canvas) ![Stars](https://img.shields.io/github/stars/AlbertoBarrago/rex-canvas?style=social) - Watches a PNG and shows updates in a pane beside the agent.
- [rex-typst](https://github.com/CiaranMcDonnell/rex-typst) ![Stars](https://img.shields.io/github/stars/CiaranMcDonnell/rex-typst?style=social) - Live Typst preview in a Rex pane, including unsaved Neovim buffers.
- [scrcpyt](https://github.com/leset0ng/scrcpyt) ![Stars](https://img.shields.io/github/stars/leset0ng/scrcpyt?style=social) - Mirrors and controls Android devices in Rex through scrcpy and Kitty graphics.
- [rex-sim](https://github.com/wobsoriano/rex-sim) ![Stars](https://img.shields.io/github/stars/wobsoriano/rex-sim?style=social) - Shows and controls iOS simulators and Android emulators in panes on macOS.
- [rex-md-viewer](https://github.com/zztkm/rex-md-viewer) ![Stars](https://img.shields.io/github/stars/zztkm/rex-md-viewer?style=social) - Previews Markdown in a reusable Rex split pane with live updates.
- [Leaf](https://github.com/DeepanshuMishraa/leaf) ![Stars](https://img.shields.io/github/stars/DeepanshuMishraa/leaf?style=social) - Reads documents and reviews diffs in Rex, with selections sent to coding agents.
- [mddog](https://github.com/qu8n/mddog) ![Stars](https://img.shields.io/github/stars/qu8n/mddog?style=social) - Renders Markdown with images, diagrams, and live reload in Rex on macOS.

## Themes and appearance

- [rex-nobeta-icon](https://github.com/Stanzilla/rex-nobeta-icon) ![Stars](https://img.shields.io/github/stars/Stanzilla/rex-nobeta-icon?style=social) - Replaces the beta app icon with the plain one; re-run after each update.
- [rex-themes](https://github.com/AlbertoBarrago/rex-themes) ![Stars](https://img.shields.io/github/stars/AlbertoBarrago/rex-themes?style=social) - Theme library and CLI for previewing and importing Rex themes.
- [rex-theme-importer](https://github.com/alexrlocke/rex-theme-importer) ![Stars](https://img.shields.io/github/stars/alexrlocke/rex-theme-importer?style=social) - Fzf picker for previewing Ghostty themes and importing them into Rex.
- [rexeme](https://github.com/DeepanshuMishraa/rexeme) ![Stars](https://img.shields.io/github/stars/DeepanshuMishraa/rexeme?style=social) - Applies Rex's theme to 52 editors, terminals, and CLI tools on macOS.

## Workflow utilities

- [rex-image-paste](https://github.com/pablasso/rex-image-paste) ![Stars](https://img.shields.io/github/stars/pablasso/rex-image-paste?style=social) - Paste images into remote hosts with `Cmd+Shift+V`.
- [logi-rex](https://github.com/aruniverse/logi-rex) ![Stars](https://img.shields.io/github/stars/aruniverse/logi-rex?style=social) - Maps Logitech controls to Rex tabs, panes, and sessions.
- [RAFT](https://github.com/theboxer/raft) ![Stars](https://img.shields.io/github/stars/theboxer/raft?style=social) - Nine floating terminal slots per session, tab, or pane.
- [Courier](https://github.com/abhi-reducto/courier) ![Stars](https://img.shields.io/github/stars/abhi-reducto/courier?style=social) - Menu bar app for macOS that sends files over SSH and pastes their remote paths.
- [Rex Floaters](https://github.com/enkelm/rex-floaters) ![Stars](https://img.shields.io/github/stars/enkelm/rex-floaters?style=social) - Reusable floating terminals for tools such as LazyGit and btop.
- [rex8s](https://github.com/vitalbh/rex8s) ![Stars](https://img.shields.io/github/stars/vitalbh/rex8s?style=social) - Kubernetes toolkit with cluster panes, log splits, and rollout status.
- [heypad](https://github.com/travelingflwr/heypad) ![Stars](https://img.shields.io/github/stars/travelingflwr/heypad?style=social) - HEY email client rendered in Rex panes.
- [RexDeck](https://github.com/Mathews-Tom/RexDeck) ![Stars](https://img.shields.io/github/stars/Mathews-Tom/RexDeck?style=social) - Opt-in integrations for terminal tools and API views in native panes.
- [Herdrex](https://github.com/elonnzhang/Herdrex) ![Stars](https://img.shields.io/github/stars/elonnzhang/Herdrex?style=social) - Serves a Herdr server as a Rex host, so Rex.app can drive Herdr's panes. ([demo](https://github.com/elonnzhang/Herdrex/blob/main/imgs/herdrex-in-rex.png))
- [Pulse for Rex](https://github.com/fatwang2/Pulse/tree/main/rex) - Shows stock and crypto watchlists with price charts in a Rex pane.
- [smart-title-rex](https://github.com/TaterDoge/smart-title-rex) - Renames each tab automatically from the focused terminal's recent output, using an OpenAI-compatible model. ([demo](https://github.com/TaterDoge/smart-title-rex/blob/main/docs/demo.gif))

## Frameworks

- [LazyRex](https://github.com/lazy-rex/LazyRex) ![Stars](https://img.shields.io/github/stars/lazy-rex/LazyRex?style=social) - Plugin hub with versioned plugins, dependencies, and cross-server messaging.
- [Amber](https://github.com/rawnly/amber) ![Stars](https://img.shields.io/github/stars/rawnly/amber?style=social) - Lua plugin manager with versions and a lockfile, formerly Rex Plugin Manager.
- [rexuikit](https://github.com/dphaener/rexuikit) ![Stars](https://img.shields.io/github/stars/dphaener/rexuikit?style=social) - Go toolkit for building Rex UIs: floating layers, splits, forms, and dialogs.

## Fun

- [rex-orbit](https://github.com/benhid/rex-orbit) ![Stars](https://img.shields.io/github/stars/benhid/rex-orbit?style=social) - Your Claude Code agents as pixel bots orbiting a dinosaur. ([demo](https://github.com/benhid/rex-orbit/blob/main/assets/demo-light.png))

## Official resources

- [Rex](https://www.superlogical.com/rex) - Product page.
- [Documentation](https://www.superlogical.com/rex/docs) - Lua config, keybindings, CLI, and the server API.

## Contributing

Additions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
