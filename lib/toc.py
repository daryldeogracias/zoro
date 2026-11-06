"""Replace a generated table of contents inside a README without leaving markers in the file.

The old format wrapped the table in HTML comments, which Obsidian shows as raw text in edit mode.
The table is found by its header row instead ("| File |" or "| Domain |"), with an optional
"Progress:" line above it. Old comment markers are removed when met. Stdlib only.
"""
import re

OLD_BLOCK = re.compile(r"<!-- toc:start -->.*?<!-- toc:end -->\n?", re.S)
OLD_LINE = re.compile(r"^[ \t]*<!-- toc:(?:start|end) -->[ \t]*\n?", re.M)
TABLE = re.compile(r"^(?:Progress: [^\n]*\n\n)?\| (?:File|Domain) \|[^\n]*\n(?:\|[^\n]*(?:\n|$))+", re.M)


def replace_table(text, block):
    """Return text with its generated table swapped for block (appended when there is none)."""
    block = block.rstrip("\n") + "\n"
    if OLD_BLOCK.search(text):
        return OLD_BLOCK.sub(lambda _: block, text, count=1)
    if TABLE.search(text):
        return TABLE.sub(lambda _: block, text, count=1)
    return text.rstrip("\n") + "\n\n" + block


def strip_markers(text):
    return OLD_LINE.sub("", text)
