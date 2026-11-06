---
name: lost
description: Resume earlier work from the logbook. Use in a fresh chat for "continue where we left off", "pick up the GMV brief", "what were we doing".
model: sonnet
---

Zoro is always lost. Read the logbook and point him at the next job.

Workspace: the path in the session start notice (default `~/Desktop/roronoa/`)

1. List `logbook/` newest first. If the user named a topic, match it against entry titles. Otherwise show the 5 newest as `date, title, status` and ask which.
2. Open the chosen entry only. Open files from its `Files` section when the next ask needs them, preferring `digests/` over originals.
3. When the entry has a `## Checklist` line, open `specs/<slug>/README.md` and the next open ticket only.
4. Reply in three lines: where we got to, the next step (the ticket's next unchecked item when there is one), any open question. When the next step is unclear, ask. Finish when the user confirms or redirects.

Close with one line: "🧭 Found the way. Don't tell anyone I was lost."
