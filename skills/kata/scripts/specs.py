#!/usr/bin/env python3
"""Zoro's kata ledger: rebuild spec tables of contents, tick checklist items, enforce the 120-line cap.

Usage:
  specs.py index                                  rebuild every specs/<slug>/README.md
  specs.py tick   <slug> <ticket> <n> [<n> ...]   tick checklist items (1-based), then index
  specs.py untick <slug> <ticket> <n> [<n> ...]   untick items, then index
  specs.py status                                 one line per spec that still has open items

Layout:
  specs/<slug>/README.md          progress + table of files (rebuilt here)
  specs/<slug>/spec*.md           the approved plan (frontmatter `summary:`)
  specs/<slug>/t01-<name>.md      a ticket: frontmatter `summary:`, a checklist of `- [ ]` items

`index` prints OVER / MISSING lines for anything the agent must fix and exits 1 if any.
Stdlib only.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from workspace import WS, link_line  # noqa: E402
from toc import replace_table  # noqa: E402

SPECS = os.path.join(WS, "specs")
LIMIT = 120
BOX = re.compile(r"^(\s*- \[)([ xX])(\] .*)$")
TICKET = re.compile(r"^t\d+.*\.md$")
problems = []


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def frontmatter(text, key):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    k = re.search(rf"^{key}:\s*(.+)$", m.group(1), re.M) if m else None
    return k.group(1).strip() if k else ""


def check_limit(path, text):
    n = len(text.splitlines())
    if n > LIMIT:
        problems.append(f"OVER {n}/{LIMIT}: {path}")
    return n


def boxes(text):
    """(line index, checked, label) for every checklist item."""
    out = []
    for i, line in enumerate(text.splitlines()):
        m = BOX.match(line)
        if m:
            out.append((i, m.group(2).lower() == "x", m.group(3)[2:].strip()))
    return out


def spec_dirs():
    if not os.path.isdir(SPECS):
        return []
    return sorted(
        d for d in os.listdir(SPECS)
        if os.path.isdir(os.path.join(SPECS, d)) and not d.startswith(".")
    )


def files_of(slug):
    d = os.path.join(SPECS, slug)
    names = sorted(f for f in os.listdir(d) if f.endswith(".md") and f != "README.md")
    return [f for f in names if not TICKET.match(f)], [f for f in names if TICKET.match(f)]


def totals(slug):
    done = total = tickets_done = 0
    docs, tickets = files_of(slug)
    for t in tickets:
        b = boxes(read(os.path.join(SPECS, slug, t)))
        d = sum(1 for _, c, _ in b if c)
        done += d
        total += len(b)
        if b and d == len(b):
            tickets_done += 1
    return done, total, tickets_done, len(tickets)


def index():
    for slug in spec_dirs():
        d = os.path.join(SPECS, slug)
        docs, tickets = files_of(slug)
        rows = []
        for f in docs + tickets:
            path = os.path.join(d, f)
            text = read(path)
            check_limit(path, text)
            summary = frontmatter(text, "summary")
            if not summary:
                problems.append(f"MISSING summary: {path}")
            mark = ""
            if f in tickets:
                b = boxes(text)
                done = sum(1 for _, c, _ in b if c)
                if not b:
                    problems.append(f"MISSING checklist: {path}")
                mark = f"{done}/{len(b)}" + (" ✓" if b and done == len(b) else "")
            rows.append(f"| [{f[:-3]}]({f}) | {summary} | {mark} |")
        done, total, tdone, tcount = totals(slug)
        block = (
            f"Progress: {done}/{total} items · {tdone}/{tcount} tickets done\n\n"
            "| File | What's in it | Done |\n|---|---|---|\n" + "\n".join(rows)
        )
        readme = os.path.join(d, "README.md")
        if os.path.exists(readme):
            text = read(readme)
            text = replace_table(text, block)
        else:
            title = slug.replace("-", " ").title()
            text = f"---\nsummary: Spec and tickets for {title}\n---\n\n# {title}\n\n{block}\n"
        with open(readme, "w", encoding="utf-8") as f:
            f.write(text)
        check_limit(readme, text)
    try:
        import vault
        vault.backfill()
    except Exception:
        pass
    print(f"Reindexed {len(spec_dirs())} spec(s) in {SPECS}")
    for p in problems:
        print(p)
    return 1 if problems else 0


def set_boxes(slug, ticket, numbers, value):
    d = os.path.join(SPECS, slug)
    if not os.path.isdir(d):
        sys.exit(f"No such spec: {slug}")
    matches = [t for t in files_of(slug)[1] if t == ticket or t.startswith(ticket)]
    if len(matches) != 1:
        sys.exit(f"Ticket '{ticket}' matched {len(matches)} files in {slug}: {matches}")
    path = os.path.join(d, matches[0])
    lines = read(path).splitlines()
    found = boxes("\n".join(lines))
    for n in numbers:
        if not 1 <= n <= len(found):
            sys.exit(f"{matches[0]} has {len(found)} checklist items; no item {n}")
        i = found[n - 1][0]
        m = BOX.match(lines[i])
        lines[i] = f"{m.group(1)}{'x' if value else ' '}{m.group(3)}"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    after = boxes("\n".join(lines))
    done = sum(1 for _, c, _ in after if c)
    print(f"{matches[0]}: {done}/{len(after)} done")
    print(link_line(path))
    for _, c, label in after:
        if not c:
            print(f"next: {label}")
            break
    return index()


def status():
    for slug in spec_dirs():
        done, total, tdone, tcount = totals(slug)
        if total and done < total:
            docs, tickets = files_of(slug)
            nxt = ""
            for t in tickets:
                for _, c, label in boxes(read(os.path.join(SPECS, slug, t))):
                    if not c:
                        nxt = f'{t[:-3]}: "{label}"'
                        break
                if nxt:
                    break
            print(f"{slug}: {done}/{total} items done, next {nxt}")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd = args[0]
    if cmd == "index":
        sys.exit(index())
    if cmd in ("tick", "untick") and len(args) >= 4:
        try:
            numbers = [int(a) for a in args[3:]]
        except ValueError:
            sys.exit("Item numbers must be integers (1-based)")
        sys.exit(set_boxes(args[1], args[2], numbers, cmd == "tick"))
    if cmd == "status":
        return status()
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
