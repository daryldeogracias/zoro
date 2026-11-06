# Zoro

Never lose the thread, never re-read the same brief. A Claude Code plugin for people who hit usage limits because their chats grow huge and they re-attach the same documents.

Everything lives in `~/Desktop/roronoa/`.

| Command | Zoro | What it does |
|---|---|---|
| `/nap` | Sleeps anywhere | Saves a short logbook entry. Safe to start a fresh chat afterwards. |
| `/lost` | Always lost | Resumes from the logbook in a fresh chat. |
| `/santoryu` | Three Sword Style | Digests a docx/pdf/pptx/xlsx once. Later chats read a ~150-word summary instead of the file. Runs automatically when a document is attached. |
| `/wado` | Wado Ichimonji, never given up | Moves scratch files to `kept/` for good. |
| `/train` | Trains in the dojo | Saves important knowledge into `dojo/<domain>/`, with a table of contents per domain and a 120-line cap per file. Future chats see the domain list at start, and every prompt is matched against the domains so Claude is told which README to read. |
| `/kata` | A practised sequence | Runs once, at the start, on Opus 5.5, and only when you type it. Asks if the request is unclear, enters plan mode, and on approval writes `specs/<name>/spec.md` plus small ticket files. Each ticket has a checklist, so a fresh chat can take one ticket at a time. |
| `/tick` | Ticking things off | Marks verified checklist items done and rebuilds the spec's progress table. |
| `/oath` | A decision sworn once | Records a decision as an ADR in `dojo/<domain>/adr-NNN-<title>.md`. `/nap` offers it automatically for decisions that weighed options. |
| `/oni-giri` | Cuts it down | Moves scratch older than 14 days to the Trash. Asks first. |
| Zoro (automatic) | Losing his bearings | Warns once when a chat is getting heavy and offers `/nap`. |

## Folders

- `logbook/` session notes
- `digests/` document digests
- `scratch/` everything Claude creates, throwaway by default
- `kept/` what you chose to keep
- `specs/` plans and tickets from `/kata`: `specs/<name>/README.md` (progress) plus `spec.md` and `t01-...md` tickets
- `Home.md`, `.obsidian/` the Obsidian vault hub and settings
- `dojo/` durable knowledge (and ADRs from `/oath`): `dojo/<domain>/README.md` (table of contents) plus topic files, each at most 120 lines. A script rebuilds the tables and flags files to split.

## Obsidian: see the workspace as a map

The workspace is an [Obsidian](https://obsidian.md) vault. Open it to browse every logbook entry, spec, ADR and
dojo note, and use the graph view to see how they connect.

- On the first session after updating, Zoro writes the vault settings and a `Home.md` hub (start there).
  Obsidian must be installed (free). If it is open or not installed, Zoro prints the one step to take:
  *Open folder as vault* and pick `~/Desktop/roronoa`.
- Every file Zoro names comes with an `obsidian://` link. In terminals that open links on click (iTerm2,
  VS Code, WezTerm, Ghostty, kitty, Alacritty) just click it. In others (Hyper, Terminal.app) Zoro also prints
  an `open "obsidian://..."` line to paste. Force a mode with `ZORO_LINKS=link` or `ZORO_LINKS=command`.
- Files carry `tags:` (`logbook`, `dojo`, `<domain>`, `adr`, `spec`, `<slug>`, `digest`, `kept`) and `[[wikilinks]]`
  between logbook entries, specs, tickets, ADRs and dojo topics. `/train`, `/oath` and the spec scripts add missing
  tags automatically; `python3 lib/vault.py backfill` does it on demand.

## Upgrading from 0.4.x

`/plugin update zoro`, then start a new session. If `~/Desktop/Zoro-Files` exists and `~/Desktop/roronoa` does
not, Zoro moves it, repoints any `~/.claude/projects/*/memory` links that pointed into it and tells you. If both
exist, nothing is touched and Zoro warns you. Set `CLAUDE_WORKSPACE` to use another folder (no migration then).
Anything of yours that mentions `~/Desktop/Zoro-Files` (for example a line in `~/.claude/CLAUDE.md`) needs the
new path by hand.

## Install (local test)

    claude --plugin-dir ~/Desktop/zoro

Team rollout: push this folder to a git repo with a `marketplace.json`, then everyone runs `/plugin install zoro`.
