#!/bin/bash
# credential-scan-on-push.sh
#
# PreToolUse hook fired by .claude/settings.json on every Bash invocation.
# No-op for any command other than `git push`. For `git push`, scans the
# diff between origin/main and HEAD for likely credential patterns; if
# any are found, exits 2 (blocking the push) with a clear message.
#
# Mirrors the credential regex in sync/sync-from-vault.sh — kept in sync
# manually for now. If you change one, change the other.
#
# Hook env: $CLAUDE_TOOL_INPUT_COMMAND is the Bash command Claude is about
# to run.

set -uo pipefail

cmd="${CLAUDE_TOOL_INPUT_COMMAND:-}"

# Quick filter: only inspect git push commands. Allow plain `git push --help` etc.
if ! echo "$cmd" | grep -qE '(^|[[:space:]])git[[:space:]]+push([[:space:]]|$)'; then
  exit 0
fi

# We're inside a git push. Find what's being pushed (commits since origin/main).
# If origin/main isn't fetched (cold checkout) the diff falls back to nothing
# and we let the push proceed — the manual check via sync-from-vault.sh stays
# the safety net for that case.
diff=$(git diff origin/main..HEAD 2>/dev/null || true)
if [[ -z "$diff" ]]; then
  exit 0
fi

CREDENTIAL_REGEX='(ghp_|gho_|ghs_|sk-ant-api03-|sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{35}|ya29\.[A-Za-z0-9_-]{20,}|xox[bopa]-[0-9A-Za-z-]{10,})'

found=$(echo "$diff" | grep -E "$CREDENTIAL_REGEX" || true)
if [[ -z "$found" ]]; then
  exit 0
fi

echo "BLOCKED: likely credential pattern in commits about to be pushed:" >&2
echo "$found" | head -5 >&2
echo "" >&2
echo "Inspect with: git log origin/main..HEAD -p | grep -E '$CREDENTIAL_REGEX'" >&2
echo "Resolve before re-running git push." >&2
exit 2
