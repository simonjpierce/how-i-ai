#!/bin/bash
# Auto-commit hook — debounced background commit of vault edits to git.
#
# Fires on PostToolUse:Edit|Write. Looks up the vault root from your
# per-project config (~/.claude/projects/<key>/config.json: vault.path),
# checks the edited file is inside that vault, and commits it on a
# 120-second debounce so rapid edits don't produce a flood of WIP commits.
#
# Designed to be silent on the happy path (exit 0). Skips entirely if:
#   - No config.json maps any vault containing the edited file
#   - The vault has no .git (not a git repo — opt-out by design)
#   - A commit ran in the last 120 seconds
#   - A fresh git index.lock exists (another git process is mid-operation)

input=$(cat)

# Extract the edited file path from the hook payload.
FILE_PATH=$(echo "$input" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0

# Find the vault config whose vault.path is a prefix of FILE_PATH.
# This works for users with multiple vaults — the right one is selected
# automatically based on where the edit landed.
VAULT=$(python3 - "$FILE_PATH" <<'EOF' 2>/dev/null
import json, glob, os, sys
fp = sys.argv[1] if len(sys.argv) > 1 else ""
best = ""
for p in sorted(glob.glob(os.path.expanduser("~/.claude/projects/*/config.json"))):
    try:
        cfg = json.load(open(p))
        vp = cfg.get("vault", {}).get("path", "")
        if vp and fp.startswith(vp.rstrip("/") + "/") and len(vp) > len(best):
            best = vp
    except Exception:
        pass
print(best)
EOF
)

[ -z "$VAULT" ] && exit 0
[ ! -d "$VAULT/.git" ] && exit 0

# Debounce: skip if last auto-commit was <120s ago. The lock file is keyed
# on the vault path so multi-vault users get per-vault debouncing.
LOCK_KEY=$(echo -n "$VAULT" | shasum | awk '{print $1}')
LOCK="/tmp/claude-autocommit-${LOCK_KEY}"
NOW=$(date +%s)
LAST=$(cat "$LOCK" 2>/dev/null || echo 0)
if [ $((NOW - LAST)) -lt 120 ]; then
    exit 0
fi

cd "$VAULT" || exit 0

# Remove stale git index.lock (>30s old) — async hooks can leave these behind
# when iCloud sync, Obsidian indexing, or another commit was interrupted.
LOCK_FILE="$VAULT/.git/index.lock"
if [ -f "$LOCK_FILE" ]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCK_FILE") ))
    if [ "$LOCK_AGE" -gt 30 ]; then
        rm -f "$LOCK_FILE"
    else
        # Lock is fresh — another git process is running, skip this commit
        exit 0
    fi
fi

# Stage only the edited file. `git add -A` would sweep up unrelated changes
# (including iCloud-sync-corrupted files as collateral damage).
git add "$FILE_PATH" 2>/dev/null
if ! git diff-index --quiet HEAD 2>/dev/null; then
    BASENAME=$(basename "$FILE_PATH")
    git commit -m "wip: auto-commit (edited $BASENAME)" 2>/dev/null
    echo "$NOW" > "$LOCK"
fi
exit 0
