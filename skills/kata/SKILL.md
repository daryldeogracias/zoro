---
name: kata
description: Plan a build once, at the start: ask, plan, then write the spec and tickets.
model: claude-opus-5-5
disable-model-invocation: true
---

A kata is a practised sequence: ask, plan, approve, split into tickets. Each ticket is one fresh-chat-sized slice, so no chat has to carry the whole project.

This is the one planning pass, on Opus, at the start of the work. Only the user starts it by typing /kata. Once the spec and tickets exist, work continues with /lost and /tick, and replanning happens only when the user asks for it.

Workspace: the path in the session start notice (default `~/Desktop/Zoro-Files/`)

```
specs/<slug>/README.md       progress + table of files (rebuilt by script)
specs/<slug>/spec.md         the approved plan
specs/<slug>/t01-<name>.md   one ticket: summary, goal, checklist, done-when
```

Every file stays at or under 120 lines. Slugs are kebab-case.

1. List `specs/`. When a spec already covers this work, stop: point the user to /lost and /tick, and plan again only if they confirm they want a fresh plan. Otherwise check the request for a goal, a scope and a way to tell it is done. When any of the three is unclear, ask up to 3 short questions with AskUserQuestion, recommended answer first, then wait for the answers.
2. Enter plan mode with EnterPlanMode (if it is unavailable, ask the user to switch to plan mode). Explore read-only, write the plan, then request approval with ExitPlanMode.
3. After approval, write `spec.md` from the approved plan: `summary:` frontmatter, then Context, Approach, Files, Verification.
4. Split the work into tickets, one slice each, finishable in one chat. Each ticket has `summary:` frontmatter, then `## Goal`, `## Checklist` with 3 to 7 `- [ ]` items, and `## Done when` with a condition you can check.
5. Run `python3 scripts/specs.py index` from this skill's base directory. Split each file it flags `OVER` at a heading, and fill each `MISSING` item. Rerun.
6. Finish when index prints no `OVER` or `MISSING` lines and the README lists every ticket. Print the spec path and the first ticket, and tell the user to start it in a fresh chat with /lost.

Close with one line: "🥋 Kata drawn. Spec and tickets are ready."
