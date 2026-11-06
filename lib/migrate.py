#!/usr/bin/env python3
"""One-time move of the old Zoro-Files workspace to roronoa. Safe to run at every session start.

Does nothing when CLAUDE_WORKSPACE is set, when there is no old folder, or when both folders exist
(then it warns once per session and leaves both alone). After a move it repoints any symlink under
~/.claude/projects/*/memory that pointed into the old folder, so per-project memory keeps working.
Prints one line per action. Stdlib only; never raises.
"""
import os
import sys

HOME = os.path.expanduser("~")
OLD = os.path.join(HOME, "Desktop", "Zoro-Files")
NEW = os.path.join(HOME, "Desktop", "roronoa")


def repoint():
    projects = os.path.join(HOME, ".claude", "projects")
    count = 0
    try:
        names = os.listdir(projects)
    except OSError:
        return 0
    for name in names:
        link = os.path.join(projects, name, "memory")
        if not os.path.islink(link):
            continue
        target = os.readlink(link)
        if target == OLD or target.startswith(OLD + os.sep):
            fresh = NEW + target[len(OLD):]
            os.unlink(link)
            os.symlink(fresh, link)
            count += 1
    return count


def main():
    if os.environ.get("CLAUDE_WORKSPACE") or not os.path.isdir(OLD) or os.path.islink(OLD):
        return
    if os.path.exists(NEW):
        print("Zoro: both ~/Desktop/Zoro-Files and ~/Desktop/roronoa exist. Left both alone. "
              "Tell the user to merge or remove the old one by hand.")
        return
    os.rename(OLD, NEW)
    n = repoint()
    msg = "Zoro: moved ~/Desktop/Zoro-Files to ~/Desktop/roronoa (the workspace is now called roronoa)."
    if n:
        msg += " Repointed %d project memory link(s)." % n
    print(msg)


try:
    main()
except Exception as e:
    print("Zoro: could not migrate the workspace (%s). Nothing was changed." % e, file=sys.stderr)
