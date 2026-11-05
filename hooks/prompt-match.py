#!/usr/bin/env python3
"""Zoro's nose for the dojo: on every prompt, point Claude at matching domains.

Reads the UserPromptSubmit JSON from stdin. Prints a hint only when a domain
matches, so unrelated prompts cost nothing. Stdlib only; never fails the prompt.
"""
import json
import os
import re
import sys

STOP = set("""about above after again also another because before being between could does doing from have
having here into just like make more most much need only other over please should some such than that their
them then there these they this those through under want what when where which while will with would your
yours help the and for you are can how why who not but use get let our any all was has had its out""".split())


BUILD = re.compile(
    r"\b(build|add|create|implement|refactor|migrate|redesign|develop|integrate|set up|make me)\b",
    re.I,
)


def words(text):
    out = set()
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        if len(w) >= 3 and w not in STOP:
            out.add(w[:-1] if w.endswith("s") and len(w) > 4 else w)
    return out


def frontmatter(text, key):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    k = re.search(rf"^{key}:\s*(.+)$", m.group(1), re.M) if m else None
    return k.group(1) if k else ""


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
    except Exception:
        return
    ws = os.environ.get("CLAUDE_WORKSPACE", os.path.expanduser("~/Desktop/Zoro-Files"))
    dojo = os.path.join(ws, "dojo")
    # A long prompt with a build verb is probably a real task: nudge towards planning first.
    if len(prompt) >= 80 and BUILD.search(prompt) and not prompt.lstrip().startswith("/"):
        print(
            "Zoro: this reads like a build or change request. If no spec exists yet, suggest the user "
            "type /kata once, at the start (never run it yourself). If the goal, scope or "
            "done-condition is unclear, ask first."
        )
    if not prompt or not os.path.isdir(dojo):
        return
    pw = words(prompt)
    scored = []
    for d in sorted(os.listdir(dojo)):
        ddir = os.path.join(dojo, d)
        if not os.path.isdir(ddir) or d.startswith("."):
            continue
        strong = words(d.replace("-", " "))
        weak = set()
        for f in os.listdir(ddir):
            if f.endswith(".md"):
                try:
                    with open(os.path.join(ddir, f), encoding="utf-8") as fh:
                        head = fh.read(2000)
                except OSError:
                    continue
                weak |= words(frontmatter(head, "summary") + " " + frontmatter(head, "description"))
        score = 3 * len(pw & strong) + len(pw & (weak - strong))
        if score >= 2:
            scored.append((score, d))
    scored.sort(reverse=True)
    for _, d in scored[:2]:
        print(f"Dojo match: read dojo/{d}/README.md (in {ws}), then only the files its table points at.")


try:
    main()
except Exception:
    pass
