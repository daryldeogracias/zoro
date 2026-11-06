---
name: nap
description: Save a logbook entry so a fresh chat loses nothing. Use when wrapping up, when the chat feels heavy, or when Zoro says he is losing his bearings.
model: sonnet
---

Zoro naps anywhere. Log the voyage first, then the user can leave this chat safely.

Workspace: the path in the session start notice (default `~/Desktop/roronoa/`)

1. Scan the chat for decisions. Each one where two or more options were weighed, or the user chose, goes to the `oath` skill as an ADR. Smaller decisions stay as one-line bullets.
2. Get the timestamp with `date +%Y-%m-%d-%H%M`. Write `logbook/<timestamp>-<slug>.md` using the template below, under 40 lines. Link each ADR by its ID.
3. When this chat touched a spec, run `python3 ../kata/scripts/specs.py status` from this skill's base directory and put its line under `## Checklist`.
4. List the files you created this chat. Move any that sit outside `scratch/` into `scratch/<date>-<slug>/`.
5. Ask: "Any of these worth keeping?" Hand the answer to the `wado` skill.
6. Finish when the entry exists and you have printed its full path, then say: "😴 Napping. Start a fresh chat any time and run /lost."

## Template

```markdown
---
title: <what this session was about, 6 words max>
date: <YYYY-MM-DD>
status: open | done
---

## Where we got to
<2-4 lines>

## Decisions
- <decision, and why in a few words> (ADR-NNN when recorded)

## Checklist
- specs/<slug>: <done>/<total> items, next <ticket>

## Open questions
- <question>

## Files
- <full path> : <what it is> (scratch | kept | digest)

## Next step
<one line>
```

Write for a reader who has never seen this chat. Name people, files and numbers explicitly.
