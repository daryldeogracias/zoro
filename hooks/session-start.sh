#!/bin/bash
# Zoro's orders, read at every sailing. Stdout becomes session context.
# Keep this short: every line is paid for on every chat.

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/lib/migrate.py"
WS="${CLAUDE_WORKSPACE:-$HOME/Desktop/roronoa}"
mkdir -p "$WS"/{logbook,digests,scratch,kept,dojo}
[ -d "$WS/.obsidian" ] || CLAUDE_WORKSPACE="$WS" python3 "$ROOT/lib/vault.py" setup --quiet

recent=$(ls -1t "$WS/logbook" 2>/dev/null | head -5)
stale=$(find "$WS/scratch" -mindepth 1 -maxdepth 1 -mtime +14 2>/dev/null | wc -l | tr -d ' ')

cat <<EOF
Zoro workspace: $WS
- Files you create for the user go in scratch/<date>-<slug>/. Scratch is throwaway until the user runs /wado.
- When a docx, pdf, pptx or xlsx is attached or named, run the santoryu skill first and work from the digest.
- Zoro always loses his bearings: after about 15 turns, or after reading 3+ large files, say once: "😵‍💫 Zoro: this chat's got long and I'm losing my bearings. Want me to /nap so you can start fresh with nothing lost?"
- A fresh chat with no clear task: offer /lost.
- Before a task, if a dojo domain below matches, read dojo/<domain>/README.md, then only the files its table points at.
- Knowledge worth keeping ("remember this", client facts, processes): run the train skill. A decision between options: run the oath skill.
- A non-trivial build or change with no spec yet: suggest the user type /kata once, at the start. Never run the kata skill yourself. Finished a ticket item: run the tick skill.
- When an instruction is unclear (goal, scope, or how to tell it is done), ask 1 to 3 short questions before acting.
EOF

open_specs=$(CLAUDE_WORKSPACE="$WS" python3 "$ROOT/skills/kata/scripts/specs.py" status 2>/dev/null | head -5)
if [ -n "$open_specs" ]; then
  echo "- Specs in progress:"
  echo "$open_specs" | sed 's/^/    /'
fi

if [ -f "$WS/dojo/README.md" ]; then
  echo "- Dojo domains:"
  grep '^| \[' "$WS/dojo/README.md" | head -30 | sed 's/^/    /'
fi

if [ -n "$recent" ]; then
  echo "- Newest logbook entries:"
  echo "$recent" | sed 's/^/    /'
fi
if [ "$stale" -gt 0 ]; then
  echo "- $stale scratch item(s) older than 14 days. Mention /oni-giri once."
fi
exit 0
