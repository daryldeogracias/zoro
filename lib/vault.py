#!/usr/bin/env python3
"""Make the Zoro workspace an Obsidian vault. Safe to run any number of times.

Usage: vault.py setup [--quiet]
Writes <workspace>/.obsidian/{app,graph}.json (only when absent, so the user's own tweaks stay) and
Home.md (rebuilt, rewritten only when it changed). Registers the vault with Obsidian only when Obsidian
is installed and not running (after a backup); otherwise prints the one manual step. Stdlib only.
"""
import json
import os
import re
import secrets
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from workspace import WS, vault_name  # noqa: E402

HOME = os.path.expanduser("~")
APP_JSON = {"promptDelete": False, "userIgnoreFilters": [".DS_Store"]}
GROUPS = [("dojo", 0x4C8BF5), ("logbook", 0xF5A623), ("specs", 0x7ED957), ("digests", 0xB57BEE),
          ("kept", 0xE5546B), ("scratch", 0x9AA0A6)]
GRAPH_JSON = {
    "search": "", "showTags": True, "showAttachments": False, "hideUnresolved": False, "showOrphans": True,
    "colorGroups": [{"query": "path:" + n, "color": {"a": 1, "rgb": c}} for n, c in GROUPS],
    "showArrow": False, "nodeSizeMultiplier": 1, "lineSizeMultiplier": 1,
}


def write_if_changed(path, text):
    try:
        with open(path, encoding="utf-8") as f:
            if f.read() == text:
                return False
    except OSError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def write_if_absent(path, data):
    if os.path.exists(path):
        return False
    return write_if_changed(path, json.dumps(data, indent=2) + "\n")


def home_md():
    lines = ["---", "tags: [home]", "---", "", "# roronoa", "",
             "Start here. Open the graph view (left ribbon) to see how everything connects.", "",
             "- [[dojo/README|Dojo]]: what the crew has trained, by domain"]
    specs = os.path.join(WS, "specs")
    slugs = sorted(d for d in os.listdir(specs) if os.path.isfile(os.path.join(specs, d, "README.md"))) \
        if os.path.isdir(specs) else []
    if slugs:
        lines += ["", "## Specs", ""] + ["- [[specs/%s/README|%s]]" % (s, s) for s in slugs]
    log = os.path.join(WS, "logbook")
    entries = sorted((f for f in os.listdir(log) if f.endswith(".md")), reverse=True)[:8] \
        if os.path.isdir(log) else []
    if entries:
        lines += ["", "## Newest logbook entries", ""] + ["- [[logbook/%s]]" % e[:-3] for e in entries]
    return "\n".join(lines) + "\n"


def obsidian_installed():
    return any(os.path.isdir(p) for p in ("/Applications/Obsidian.app", os.path.join(HOME, "Applications", "Obsidian.app")))


def obsidian_running():
    try:
        return subprocess.run(["pgrep", "-f", "Obsidian.app/Contents/MacOS"], capture_output=True).returncode == 0
    except OSError:
        return False


def config_path():
    mac = os.path.join(HOME, "Library", "Application Support", "obsidian", "obsidian.json")
    return mac if sys.platform == "darwin" else os.path.join(HOME, ".config", "obsidian", "obsidian.json")


def register():
    """Returns 'done', 'already' or 'manual:<reason>'."""
    cfg = config_path()
    real = os.path.realpath(WS)
    data = {"vaults": {}}
    if os.path.exists(cfg):
        try:
            with open(cfg, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            return "manual:could not read Obsidian's settings"
    vaults = data.setdefault("vaults", {})
    if any(os.path.realpath(v.get("path", "")) == real for v in vaults.values()):
        return "already"
    if obsidian_running():
        return "manual:Obsidian is open"
    if os.path.exists(cfg):
        bak = cfg + ".zoro-bak"
        if not os.path.exists(bak):
            with open(cfg, encoding="utf-8") as f, open(bak, "w", encoding="utf-8") as b:
                b.write(f.read())
    vaults[secrets.token_hex(8)] = {"path": real, "ts": int(time.time() * 1000)}
    os.makedirs(os.path.dirname(cfg), exist_ok=True)
    with open(cfg, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return "done"


def setup(quiet):
    obs = os.path.join(WS, ".obsidian")
    changed = [write_if_absent(os.path.join(obs, "app.json"), APP_JSON),
               write_if_absent(os.path.join(obs, "graph.json"), GRAPH_JSON),
               write_if_changed(os.path.join(WS, "Home.md"), home_md())]
    notes = []
    if not obsidian_installed():
        notes.append("Obsidian is not installed. Download it free from https://obsidian.md, then open the folder %s "
                     "as a vault (Open folder as vault)." % WS)
    else:
        state = register()
        if state == "done":
            changed.append(True)
            notes.append("Registered the vault '%s' in Obsidian. Open Obsidian and pick it." % vault_name())
        elif state.startswith("manual:"):
            notes.append("%s. In Obsidian choose Open folder as vault and pick %s." % (state[7:].capitalize(), WS))
    if any(changed) or notes:
        print("Zoro: Obsidian vault '%s' %s." % (vault_name(), "set up" if any(changed) else "checked"))
    for n in notes:
        print("Zoro: " + n)
    if not quiet and not any(changed) and not notes:
        print("Nothing to change.")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] != "setup":
        print(__doc__)
        sys.exit(2)
    try:
        setup("--quiet" in sys.argv)
    except Exception as e:
        print("Zoro: Obsidian setup skipped (%s)." % e, file=sys.stderr)
