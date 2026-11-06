"""Shared workspace location for every Zoro script and hook.

The default is ~/Desktop/roronoa. CLAUDE_WORKSPACE overrides it. Stdlib only.
"""
import os
import sys
import urllib.parse

DEFAULT = os.path.expanduser("~/Desktop/roronoa")
LEGACY = os.path.expanduser("~/Desktop/Zoro-Files")
WS = os.environ.get("CLAUDE_WORKSPACE") or DEFAULT


def vault_name():
    """The Obsidian vault name is the workspace folder's name."""
    return os.path.basename(WS.rstrip("/"))


def obsidian_link(path):
    """obsidian:// URL that opens a workspace file, or None when it is outside the workspace."""
    ws = os.path.realpath(WS)
    full = os.path.realpath(path)
    if full != ws and not full.startswith(ws + os.sep):
        return None
    rel = os.path.relpath(full, ws)
    if rel.endswith(".md"):
        rel = rel[:-3]
    return "obsidian://open?vault=%s&file=%s" % (
        urllib.parse.quote(vault_name(), safe=""),
        urllib.parse.quote(rel, safe="/"),
    )


LINK_TERMINALS = {"iTerm.app", "vscode", "WezTerm", "ghostty", "kitty", "Alacritty"}


def link_mode():
    """'link' when the terminal is known to open obsidian:// links on click, else 'command'.

    'command' prints the markdown link and also an `open "..."` line to paste. ZORO_LINKS=link|command overrides.
    """
    forced = os.environ.get("ZORO_LINKS", "")
    if forced in ("link", "command"):
        return forced
    return "link" if os.environ.get("TERM_PROGRAM") in LINK_TERMINALS else "command"


def link_line(path):
    """Text to show the user for a workspace file: a markdown link, plus an open command in 'command' mode."""
    url = obsidian_link(path)
    if not url:
        return path
    rel = os.path.relpath(os.path.realpath(path), os.path.realpath(WS))
    text = "[%s](%s)" % (rel, url)
    if link_mode() == "command":
        text += '\n  open "%s"' % url
    return text


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "mode":
        print(link_mode())
    elif len(sys.argv) >= 3 and sys.argv[1] == "link":
        for p in sys.argv[2:]:
            print(link_line(p))
    else:
        print("Usage: workspace.py mode | link <path> [<path> ...]")
        sys.exit(2)
