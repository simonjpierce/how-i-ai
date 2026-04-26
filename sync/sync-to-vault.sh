#!/bin/bash
# sync-to-vault.sh — pull skills, templates, and guides from the repo back into
# their canonical local locations on Simon's machine.
#
# Run this after a PR has merged (or as part of /update) so the local canonical
# directories match what's on main. Dry-run by default; re-run with --apply to
# copy changes across.
#
# The repo is path-sanitised ($VAULT_PATH and $CLAUDE_CONFIG stand in for
# actual paths so content is portable across contributor machines). This
# script reverses the sanitisation before comparing or applying.
#
# Usage:
#   ./sync/sync-to-vault.sh            # dry run — show diffs across all categories
#   ./sync/sync-to-vault.sh --apply    # copy desanitised content into local canonical paths

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

# --- Mappings ---
# Format: "repo_relative_path::target_absolute_path"
# Mirror of sync-from-vault.sh's source→target mappings, in reverse.

SKILLS=(
  "skills/transcribe::$CLAUDE_CONFIG/skills/transcribe"
  "skills/red-team::$CLAUDE_CONFIG/skills/red-team"
  "skills/pdf-to-markdown::$CLAUDE_CONFIG/skills/pdf-to-markdown"
  "skills/update::$CLAUDE_CONFIG/skills/update"
  "skills/document::$CLAUDE_CONFIG/skills/document"
  "skills/verify-citations::$CLAUDE_CONFIG/skills/verify-citations"
  "skills/mmf-brand::$CLAUDE_CONFIG/skills/mmf-brand"
  "skills/onboard::$CLAUDE_CONFIG/skills/onboard"
  "skills/review-friction::$CLAUDE_CONFIG/skills/review-friction"
  "skills/session-start::$CLAUDE_CONFIG/skills/session-start"
)

TEMPLATES=(
  "templates/starter-claude-config::$CLAUDE_CONFIG/templates/starter-claude-config"
  "templates/starter-vault::$CLAUDE_CONFIG/templates/starter-vault"
)

GUIDES=(
  "guides/ghostty-setup.md::$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Ghostty Setup Guide for Claude Code.md"
)

# --- Helpers ---

desanitise() {
  local file="$1"
  sed -i.bak \
    -e "s|\$VAULT_PATH|${VAULT_PATH}|g" \
    -e "s|\$CLAUDE_CONFIG|${CLAUDE_CONFIG}|g" \
    "$file"
  rm -f "$file.bak"
}

stage_and_desanitise() {
  # Copy a single repo path (file or directory) into the stage dir,
  # then run desanitise on every .md file underneath.
  local repo_rel="$1"
  local stage_path="$STAGE_DIR/$repo_rel"
  local source_path="$REPO_ROOT/$repo_rel"

  if [[ ! -e "$source_path" ]]; then
    return 1
  fi

  mkdir -p "$(dirname "$stage_path")"
  cp -R "$source_path" "$stage_path"

  if [[ -f "$stage_path" && "$stage_path" == *.md ]]; then
    desanitise "$stage_path"
  elif [[ -d "$stage_path" ]]; then
    while IFS= read -r -d '' file; do
      desanitise "$file"
    done < <(find "$stage_path" -type f -name '*.md' -print0)
  fi
}

# Per-category accumulators, keyed by mapping string. The function below
# compares one mapping at a time and prints the diff if there is one.
changed=()
new=()

compare_mapping() {
  local repo_rel="$1"
  local target="$2"
  local stage_path="$STAGE_DIR/$repo_rel"

  if [[ ! -e "$stage_path" ]]; then
    echo "  SKIP: $repo_rel — not present in repo" >&2
    return 0
  fi

  if [[ ! -e "$target" ]]; then
    echo ""
    echo "NEW: $repo_rel → $target (target absent locally)"
    new+=("$repo_rel::$target")
    return 0
  fi

  if diff -rq "$stage_path" "$target" > /dev/null 2>&1; then
    return 0
  fi

  echo ""
  echo "=== $repo_rel → $target has changes ==="
  diff -ur "$target" "$stage_path" | head -80
  changed+=("$repo_rel::$target")
}

apply_mapping() {
  local repo_rel="$1"
  local target="$2"
  local stage_path="$STAGE_DIR/$repo_rel"

  mkdir -p "$(dirname "$target")"
  if [[ -d "$target" ]]; then
    rm -rf "$target"
  elif [[ -f "$target" ]]; then
    rm -f "$target"
  fi
  cp -R "$stage_path" "$target"
  echo "  Applied: $repo_rel → $target"
}

# --- Stage every mapping ---

echo "Staging repo content with placeholders resolved..."
for mapping in "${SKILLS[@]}" "${TEMPLATES[@]}" "${GUIDES[@]}"; do
  repo_rel="${mapping%%::*}"
  stage_and_desanitise "$repo_rel" || echo "  SKIP: source missing — $repo_rel" >&2
done

echo ""
echo "--- Comparing desanitised repo content against local canonical paths ---"

echo ""
echo "[SKILLS]"
for mapping in "${SKILLS[@]}"; do
  repo_rel="${mapping%%::*}"
  target="${mapping##*::}"
  compare_mapping "$repo_rel" "$target"
done

echo ""
echo "[TEMPLATES]"
for mapping in "${TEMPLATES[@]}"; do
  repo_rel="${mapping%%::*}"
  target="${mapping##*::}"
  compare_mapping "$repo_rel" "$target"
done

echo ""
echo "[GUIDES]"
for mapping in "${GUIDES[@]}"; do
  repo_rel="${mapping%%::*}"
  target="${mapping##*::}"
  compare_mapping "$repo_rel" "$target"
done

total=$((${#changed[@]} + ${#new[@]}))

if [[ $total -eq 0 ]]; then
  echo ""
  echo "No changes to pull. Local paths are in sync with the repo."
  exit 0
fi

echo ""
echo "Summary: $total mapping(s) out of sync."
if [[ ${#changed[@]} -gt 0 ]]; then
  echo "  Changed:"
  printf '    %s\n' "${changed[@]}"
fi
if [[ ${#new[@]} -gt 0 ]]; then
  echo "  New:"
  printf '    %s\n' "${new[@]}"
fi

if [[ "$MODE" != "--apply" ]]; then
  echo ""
  echo "Dry run. Re-run with --apply to copy these into their local canonical paths."
  echo ""
  echo "WARNING: --apply is destructive. If you have uncommitted local edits to"
  echo "any path that's also changed in the repo, --apply will overwrite them."
  echo "Merge manually before re-running."
  exit 0
fi

echo ""
echo "--- Applying changes ---"
for mapping in "${changed[@]}" "${new[@]}"; do
  repo_rel="${mapping%%::*}"
  target="${mapping##*::}"
  apply_mapping "$repo_rel" "$target"
done

echo ""
echo "Done. Local canonical paths now match the repo (with paths resolved)."
echo "Note: ~/.claude/ may have uncommitted changes — the auto-commit hook"
echo "(or next commit) will capture them to simonjpierce/claude-code-config."
