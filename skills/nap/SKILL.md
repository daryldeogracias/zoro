---
name: nap
description: Save a logbook entry so a fresh chat loses nothing. Use when wrapping up, when the chat feels heavy, or when Zoro says he is losing his bearings.
model: sonnet
---

Zoro naps anywhere. Log the voyage first, then the user can leave this chat safely.

Workspace: `~/Claude-Workspace/`

1. Get the timestamp with `date +%Y-%m-%d-%H%M`. Write `logbook/<timestamp>-<slug>.md` using the template below, under 40 lines.
2. List the files you created this chat. Move any that sit outside `scratch/` into `scratch/<date>-<slug>/`.
3. Ask: "Any of these worth keeping?" Hand the answer to the `wado` skill.
4. Finish when the entry exists and you have printed its full path, then say: "Napping. Start a fresh chat any time and run /lost."

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
- <decision, and why in a few words>

## Open questions
- <question>

## Files
- <full path> : <what it is> (scratch | kept | digest)

## Next step
<one line>
```

Write for a reader who has never seen this chat. Name people, files and numbers explicitly.
