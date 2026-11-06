---
name: oath
description: Record a decision as an ADR in the dojo. Use when two or more options were weighed and one was chosen, or the user says "record this decision" or "write an ADR".
model: sonnet
---

An oath is a decision sworn once, with its reason, so nobody re-argues it in a new chat.

Workspace: the path in the session start notice (default `~/Desktop/roronoa/`)

ADRs live in the dojo: `dojo/<domain>/adr-NNN-<slug>.md`, at most 40 lines each, so the same tables of contents and per-prompt matching find them.

1. Check that the chat holds the options considered, the choice and the reason. When any is missing, ask for it and wait.
2. Pick the domain from `dojo/README.md`, or create `dojo/<domain>/`. Ask only if two domains are plausible.
3. Number it: count the existing `adr-*.md` files in the domain and add 1, as three digits.
4. Write the file from the template below. When it replaces an earlier ADR, change that ADR's `Status:` line to `superseded by ADR-NNN`.
5. Run `python3 ../train/scripts/reindex.py` from this skill's base directory. Fix each `OVER` or `MISSING` line and rerun.
6. Finish when reindex prints no problems and you have printed the ADR path.

## Template

```markdown
---
summary: ADR-NNN <the decision in one line> (accepted)
---

# ADR-NNN: <title>

Status: accepted
Date: <YYYY-MM-DD>

## Context
<why a decision was needed, 2-4 lines>

## Options considered
- <option>: <one line>

## Decision
<what was chosen and why>

## Consequences
- <what gets easier or harder>
```

Close with one line: "📜 Oath sworn. ADR-NNN is in the dojo."
