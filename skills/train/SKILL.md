---
name: train
description: Save important knowledge so every future chat can find it. Use for "remember this", "this is important", "add this to our docs", or when a decision, client fact or process should outlive the chat.
model: sonnet
---

Zoro trains in the dojo every day. Knowledge worth keeping goes there, small and indexed, so any chat can find it without reading everything.

Workspace: `~/Claude-Workspace/dojo/`

```
dojo/README.md                 table of domains
dojo/<domain>/README.md        one-line description + table of files
dojo/<domain>/<topic>.md       frontmatter `summary: <one line>`, then content
```

Every file stays at or under 120 lines. Domain and topic names are kebab-case (`gmv-campaigns`, `brand-voice`).

1. Pick the domain from `dojo/README.md`. When none fits, create `dojo/<domain>/`; ask the user only if two domains are plausible.
2. Read the domain's README table. Extend the matching topic file, or create a new `<topic>.md` that starts with `summary: <one line>` in frontmatter.
3. Write short facts: who, what, when, why. Link to `digests/` files instead of copying them.
4. Run `python3 scripts/reindex.py` from this skill's base directory. It rebuilds every table and prints `OVER` and `MISSING` lines for anything to fix.
5. Split each `OVER` file at a heading boundary into two files, each with its own `summary:`. Fill each `MISSING` item. Rerun step 4.
6. Finish when reindex prints no `OVER` or `MISSING` lines. Print the paths you wrote.

Flourish: "Trained. The dojo remembers."
