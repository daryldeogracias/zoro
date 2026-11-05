---
name: wado
description: Keep scratch files for good. Use when the user wants to keep, save or preserve something, or answers yes to "worth keeping?".
model: sonnet
---

Wado Ichimonji is the sword Zoro never gives up. Whatever the user keeps stays in `kept/`; everything else stays scratch.

Workspace: `~/Claude-Workspace/`

1. Identify the items: the ones the user named, otherwise the newest `scratch/` folder.
2. Move them to `kept/<topic>/`, choosing a topic folder name from the content (e.g. `gmv-campaign`).
3. In the newest logbook entry, change each moved file's path and mark it `kept`.
4. Finish when every item sits under `kept/` and `grep -r "<old path>" logbook/` returns nothing. Print the new paths.

Flourish: "Wado stays with me. Kept."
