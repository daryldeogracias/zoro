---
name: tick
description: Tick off checklist items as work completes. Use when a ticket item is finished, or the user says "done with X" or "mark it off".
model: sonnet
---

Tick what is verified done, so the checklist always matches reality and a fresh chat knows where the work stands.

Workspace: the path in the session start notice (default `~/Desktop/roronoa/`)

1. Find the spec and ticket: read `specs/<slug>/README.md`, then the ticket. When the spec, ticket or item is ambiguous, ask which one and wait.
2. Confirm the item is done: the file exists, the test passed, or the user said so. Tick only confirmed items.
3. Run `python3 ../kata/scripts/specs.py tick <slug> <ticket> <n> [<n> ...]` from this skill's base directory (`n` counts the ticket's checklist items from 1). It flips the boxes and rebuilds the README.
4. Finish when the script prints the new count and the next open item. Tell the user both and show the ticket link the script prints.

Close with one line: "✅ Ticked. <done>/<total> on <ticket>."
