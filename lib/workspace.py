"""Shared workspace location for every Zoro script and hook.

The default is ~/Desktop/roronoa. CLAUDE_WORKSPACE overrides it. Stdlib only.
"""
import os
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
