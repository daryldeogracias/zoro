# Zoro

Never lose the thread, never re-read the same brief. A Claude Code plugin for people who hit usage limits because their chats grow huge and they re-attach the same documents.

Everything lives in `~/Desktop/Zoro-Files/`.

| Command | Zoro | What it does |
|---|---|---|
| `/nap` | Sleeps anywhere | Saves a short logbook entry. Safe to start a fresh chat afterwards. |
| `/lost` | Always lost | Resumes from the logbook in a fresh chat. |
| `/santoryu` | Three Sword Style | Digests a docx/pdf/pptx/xlsx once. Later chats read a ~150-word summary instead of the file. Runs automatically when a document is attached. |
| `/wado` | Wado Ichimonji, never given up | Moves scratch files to `kept/` for good. |
| `/train` | Trains in the dojo | Saves important knowledge into `dojo/<domain>/`, with a table of contents per domain and a 120-line cap per file. Future chats see the domain list at start, and every prompt is matched against the domains so Claude is told which README to read. |
| `/oni-giri` | Cuts it down | Moves scratch older than 14 days to the Trash. Asks first. |
| Zoro (automatic) | Losing his bearings | Warns once when a chat is getting heavy and offers `/nap`. |

## Folders

- `logbook/` session notes
- `digests/` document digests
- `scratch/` everything Claude creates, throwaway by default
- `kept/` what you chose to keep
- `dojo/` durable knowledge: `dojo/<domain>/README.md` (table of contents) plus topic files, each at most 120 lines. A script rebuilds the tables and flags files to split.

## Install (local test)

    claude --plugin-dir ~/Desktop/zoro

Team rollout: push this folder to a git repo with a `marketplace.json`, then everyone runs `/plugin install zoro`.
