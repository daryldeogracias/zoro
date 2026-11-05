#!/usr/bin/env python3
"""Rebuild the dojo's tables of contents and enforce the 120-line cap.

Usage: reindex.py
Layout:
  dojo/README.md                 table of domains
  dojo/<domain>/README.md        description + table of files
  dojo/<domain>/<topic>.md       frontmatter `summary:` + content

Prints OVER / MISSING lines for anything the agent must fix, and exits 1 if any.
Stdlib only.
"""
import os
import re
import sys

WS = os.environ.get("CLAUDE_WORKSPACE", os.path.expanduser("~/Desktop/Zoro-Files"))
DOJO = os.path.join(WS, "dojo")
LIMIT = 120
START, END = "<!-- toc:start -->", "<!-- toc:end -->"
problems = []


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def frontmatter(text, key):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    k = re.search(rf"^{key}:\s*(.+)$", m.group(1), re.M)
    return k.group(1).strip() if k else ""


def nlines(text):
    return len(text.splitlines())


def check_limit(path, text):
    n = nlines(text)
    if n > LIMIT:
        problems.append(f"OVER {n}/{LIMIT}: {path}")
    return n


def write_toc(readme, title, header, rows, default_desc):
    """Replace the block between markers, creating the README if absent."""
    block = f"{START}\n{header}\n" + "\n".join(rows) + f"\n{END}"
    if os.path.exists(readme):
        text = read(readme)
        if START in text and END in text:
            text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
    else:
        text = f"---\ndescription: {default_desc}\n---\n\n# {title}\n\n{block}\n"
    with open(readme, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def main():
    if not os.path.isdir(DOJO):
        os.makedirs(DOJO)
    domains = sorted(
        d for d in os.listdir(DOJO)
        if os.path.isdir(os.path.join(DOJO, d)) and not d.startswith(".")
    )
    domain_rows = []
    for d in domains:
        ddir = os.path.join(DOJO, d)
        topics = sorted(
            f for f in os.listdir(ddir)
            if f.endswith(".md") and f != "README.md" and not f.startswith(".")
        )
        rows = []
        for t in topics:
            path = os.path.join(ddir, t)
            text = read(path)
            n = check_limit(path, text)
            summary = frontmatter(text, "summary")
            if not summary:
                problems.append(f"MISSING summary: {path}")
            rows.append(f"| [{t[:-3]}]({t}) | {summary} | {n} |")
        readme = os.path.join(ddir, "README.md")
        text = write_toc(
            readme, d.replace("-", " ").title(), "| File | What's in it | Lines |\n|---|---|---|",
            rows, "TODO: describe this domain in one line",
        )
        desc = frontmatter(text, "description")
        if not desc or desc.startswith("TODO"):
            problems.append(f"MISSING description: {readme}")
        check_limit(readme, read(readme))
        domain_rows.append(f"| [{d}]({d}/README.md) | {desc} | {len(topics)} |")

    root = os.path.join(DOJO, "README.md")
    write_toc(
        root, "Dojo", "| Domain | What it covers | Files |\n|---|---|---|",
        domain_rows, "Index of everything the crew has trained into the dojo",
    )
    check_limit(root, read(root))

    print(f"Reindexed {len(domains)} domain(s) in {DOJO}")
    for p in problems:
        print(p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
