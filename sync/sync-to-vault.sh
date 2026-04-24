#!/bin/bash
# sync-to-vault.sh — pull skills from the repo back into ~/.claude/skills/
#
# Run this after a PR has merged (or as part of /update) so your local
# canonical skills directory matches what's on main. Dry-run by default;
# re-run with --apply to copy changes across.
#
# The repo's skills/ is path-sanitised (placeholders $VAULT_PATH and
# $CLAUDE_CONFIG stand in for your actual paths, for portability across
# contributor machines). This script reverses the sanitisation before
# comparing or applying, so your ~/.claude/skills/ ends up with the
# paths resolved for your machine.
#
# Usage:
#   ./sync/sync-to-vault.sh            # dry run — show diffs
#   ./sync/sync-to-vault.sh --apply    # copy desanitised content into ~/.claude/skills/

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "${VAULT_PATH:-}" ]]; then
  VAULT_PATH="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Simon's Vault"
fi
CLAUDE_CONFIG="${CLAUDE_CONFIG:-$HOME/.claude}"
MODE="${1:-dry-run}"

STAGE_DIR="$(mktemp -d "/tmp/mmf-claude-code-revstage.XXXXXX")"
trap 'rm -rf "$STAGE_DIR"' EXIT

cd "$REPO_ROOT"

echo "Pulling latest from origin/main..."
git pull origin main --quiet

echo "Staging repo skills with placeholders resolved..."
cp -R "$REPO_ROOT/skills" "$STAGE_DIR/skills"

# Reverse the sanitisation applied by sync-from-vault.sh.
desanitise() {
  local file="$1"
  sed -i.bak \
    -e "s|\$VAULT_PATH|${VAULT_PATH}|g" \
    -e "s|\$CLAUDE_CONFIG|${CLAUDE_CONFIG}|g" \
    "$file"
  rm -f "$file.bak"
}

while IFS= read -r -d '' file; do
  desanitise "$file"
done < <(find "$STAGE_DIR/skills" -type f -name '*.md' -print0)

echo ""
echo "--- Comparing desanitised repo content against ~/.claude/skills/ ---"

changed_skills=()
new_skills=()
for skill_dir in "$STAGE_DIR/skills"/*/; do
  [[ -d "$skill_dir" ]] || continue
  skill_name=$(basename "$skill_dir")
  stage_path="$STAGE_DIR/skills/$skill_name"
  local_path="$CLAUDE_CONFIG/skills/$skill_name"

  if [[ ! -d "$local_path" ]]; then
    echo ""
    echo "NEW: $skill_name — present in repo, absent from ~/.claude/skills/"
    new_skills+=("$skill_name")
    continue
  fi

  if diff -rq "$stage_path" "$local_path" > /dev/null 2>&1; then
    continue
  fi

  echo ""
  echo "=== $skill_name has changes ==="
  diff -ur "$local_path" "$stage_path" | head -80
  changed_skills+=("$skill_name")
done

total=$((${#changed_skills[@]} + ${#new_skills[@]}))

if [[ $total -eq 0 ]]; then
  echo ""
  echo "No changes to pull. ~/.claude/skills/ is in sync with the repo."
  exit 0
fi

echo ""
echo "Summary: $total skill(s) out of sync."
if [[ ${#changed_skills[@]} -gt 0 ]]; then
  echo "  Changed: ${changed_skills[*]}"
fi
if [[ ${#new_skills[@]} -gt 0 ]]; then
  echo "  New:     ${new_skills[*]}"
fi

if [[ "$MODE" != "--apply" ]]; then
  echo ""
  echo "Dry run. Re-run with --apply to copy these into ~/.claude/skills/."
  echo ""
  echo "WARNING: --apply is destructive against ~/.claude/skills/. If you have"
  echo "uncommitted local edits to a skill that's also changed in the repo,"
  echo "--apply will overwrite your local edits. Merge manually before re-running."
  exit 0
fi

echo ""
echo "--- Applying changes to ~/.claude/skills/ ---"
for skill_name in "${changed_skills[@]}" "${new_skills[@]}"; do
  stage_path="$STAGE_DIR/skills/$skill_name"
  local_path="$CLAUDE_CONFIG/skills/$skill_name"
  rm -rf "$local_path"
  cp -R "$stage_path" "$local_path"
  echo "  Applied: $skill_name"
done

echo ""
echo "Done. ~/.claude/skills/ now matches the repo (with paths resolved)."
echo "Note: your ~/.claude/ repo may have uncommitted changes in skills/ —"
echo "the auto-commit hook (or next commit) will capture them to"
echo "simonjpierce/claude-code-config."
