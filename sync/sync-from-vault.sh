#!/bin/bash
# sync-from-vault.sh — mirror MMF Claude Code skills and guides from Simon's vault
# and ~/.claude/ into this repo.
#
# Runs from Simon's machine. Dry-run by default; --commit applies changes and pushes.
# After copying into the repo for the first time: chmod +x sync/sync-from-vault.sh
#
# Usage:
#   ./sync/sync-from-vault.sh              # dry run — stages, shows diff, no changes
#   ./sync/sync-from-vault.sh --commit     # applies changes, commits, pushes

set -euo pipefail

# --- Configuration ---

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Default vault path (override by setting VAULT_PATH before running). Using an if
# rather than ${VAR:-default} because the default contains an apostrophe that
# trips the bash 3.2 parser inside ${...:-...} expansions.
if [[ -z "${VAULT_PATH:-}" ]]; then
  VAULT_PATH="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Simon's Vault"
fi
CLAUDE_CONFIG="${CLAUDE_CONFIG:-$HOME/.claude}"
STAGE_DIR="$(mktemp -d "/tmp/mmf-claude-code-stage.XXXXXX")"
trap 'rm -rf "$STAGE_DIR"' EXIT

# Pull latest from the repo first so any merged PRs aren't overwritten by
# our push. If a PR has merged that introduced changes NOT yet present in
# ~/.claude/skills/, run sync-to-vault.sh --apply before this script so
# those changes flow back to the canonical source before we push.
cd "$REPO_ROOT"
git pull origin main --quiet

# Pre-flight: warn if there are open PRs touching the same paths we're about
# to overwrite. This catches the case where a contributor has work in flight
# that would be silently discarded by our push. Best-effort — only fires if
# `gh` is installed and authenticated; otherwise silent.
if command -v gh >/dev/null 2>&1; then
  open_prs=$(gh pr list --state open --json number,title,headRefName --limit 20 2>/dev/null || true)
  pr_count=$(echo "$open_prs" | python3 -c 'import json,sys; data=sys.stdin.read().strip(); print(len(json.loads(data)) if data else 0)' 2>/dev/null || echo 0)
  if [[ "$pr_count" -gt 0 ]]; then
    echo ""
    echo "NOTE: $pr_count open PR(s) on this repo. If any touch paths you're"
    echo "about to push, your push could silently discard their work."
    echo "$open_prs" | python3 -c 'import json,sys; [print(f"  #{p[\"number\"]} ({p[\"headRefName\"]}): {p[\"title\"]}") for p in json.loads(sys.stdin.read())]' 2>/dev/null || true
    echo ""
    echo "To check what each PR changes: gh pr diff <number>"
    echo "Continuing in 5 seconds — Ctrl-C to abort."
    sleep 5
  fi
fi

# Source → target mappings. Format: "source_absolute_path::target_path_in_repo"
# All skills canonically live in ~/.claude/skills/. The vault (05_AI WORKFLOW/
# CLAUDE/Skills/) has symlinks back there for Obsidian visibility — we sync from
# the canonical location to avoid cp -R only copying the symlinks themselves.

SKILLS=(
  "$CLAUDE_CONFIG/skills/transcribe::skills/transcribe"
  "$CLAUDE_CONFIG/skills/red-team::skills/red-team"
  "$CLAUDE_CONFIG/skills/pdf-to-markdown::skills/pdf-to-markdown"
  "$CLAUDE_CONFIG/skills/update::skills/update"
  "$CLAUDE_CONFIG/skills/document::skills/document"
  "$CLAUDE_CONFIG/skills/verify-citations::skills/verify-citations"
  "$CLAUDE_CONFIG/skills/mmf-brand::skills/mmf-brand"
  "$CLAUDE_CONFIG/skills/onboard::skills/onboard"
  "$CLAUDE_CONFIG/skills/review-friction::skills/review-friction"
  "$CLAUDE_CONFIG/skills/session-start::skills/session-start"
  "$CLAUDE_CONFIG/skills/refresh-skills::skills/refresh-skills"
)

GUIDES=(
  # WARNING: sync-from-vault is destructive on its target dirs (skills/, guides/,
  # templates/). On --commit it does `rm -rf <dir>` and re-copies from staged
  # mappings — so any file in those dirs WITHOUT a mapping here gets deleted.
  # Workflow: write the canonical doc in the vault first, add the mapping here,
  # THEN sync. Don't write directly to repo/guides/ — it'll be wiped on next sync.
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Ghostty Setup Guide for Claude Code.md::guides/ghostty-setup.md"
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Inviting Collaborators to mmf-claude-code.md::guides/inviting-collaborators.md"
)

TEMPLATES=(
  # Templates ship to the repo's templates/ dir. /onboard installs them into
  # users' machines on first run.
  "$CLAUDE_CONFIG/templates/starter-claude-config::templates/starter-claude-config"
  "$CLAUDE_CONFIG/templates/starter-vault::templates/starter-vault"
)

# --- Helpers ---

sanitise() {
  # Replace absolute local paths with placeholders so content is portable for other users.
  # Using | as sed delimiter because the vault path contains /.
  local file="$1"
  sed -i.bak \
    -e "s|${VAULT_PATH}|\$VAULT_PATH|g" \
    -e "s|${CLAUDE_CONFIG}|\$CLAUDE_CONFIG|g" \
    "$file"
  rm -f "$file.bak"
}

copy_and_sanitise() {
  local source="$1"
  local target="$2"
  local dest="$STAGE_DIR/$target"

  if [[ ! -e "$source" ]]; then
    echo "  SKIP: source missing — $source" >&2
    return 1
  fi

  mkdir -p "$(dirname "$dest")"
  cp -R "$source" "$dest"

  while IFS= read -r -d '' file; do
    sanitise "$file"
  done < <(find "$dest" -type f -name '*.md' -print0)
}

credential_scan() {
  # Cheap safety net — looks for common token shapes before committing.
  # Aborts the commit if it finds anything that looks like a real credential.
  local found
  found=$(grep -rE "(ghp_|gho_|ghs_|sk-ant-api03-|sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{35}|ya29\.[A-Za-z0-9_-]{20,}|xox[bopa]-[0-9A-Za-z-]{10,})" "$STAGE_DIR" 2>/dev/null || true)
  if [[ -n "$found" ]]; then
    echo "ERROR: Likely credential found in staged content:" >&2
    echo "$found" >&2
    echo "Resolve before re-running with --commit." >&2
    exit 1
  fi
}

# --- Main ---

echo "Staging into: $STAGE_DIR"
echo ""
echo "Skills:"
for mapping in "${SKILLS[@]}"; do
  source="${mapping%%::*}"
  target="${mapping##*::}"
  echo "  $target"
  copy_and_sanitise "$source" "$target" || true
done

if [[ ${#GUIDES[@]} -gt 0 ]]; then
  echo ""
  echo "Guides:"
  for mapping in "${GUIDES[@]}"; do
    source="${mapping%%::*}"
    target="${mapping##*::}"
    echo "  $target"
    copy_and_sanitise "$source" "$target" || true
  done
fi

if [[ ${#TEMPLATES[@]} -gt 0 ]]; then
  echo ""
  echo "Templates:"
  for mapping in "${TEMPLATES[@]}"; do
    source="${mapping%%::*}"
    target="${mapping##*::}"
    echo "  $target"
    copy_and_sanitise "$source" "$target" || true
  done
fi

credential_scan

echo ""
echo "--- Diff (repo → staged) ---"
for dir in skills guides templates; do
  if [[ -d "$REPO_ROOT/$dir" && -d "$STAGE_DIR/$dir" ]]; then
    diff -ur "$REPO_ROOT/$dir" "$STAGE_DIR/$dir" || true
  elif [[ -d "$STAGE_DIR/$dir" && ! -d "$REPO_ROOT/$dir" ]]; then
    echo "New directory: $dir/ (will be added):"
    find "$STAGE_DIR/$dir" -type f | head -40 | sed "s|$STAGE_DIR/|  + |"
  fi
done

# --- Commit ---

if [[ "${1:-}" == "--commit" ]]; then
  echo ""
  echo "--- Applying changes ---"
  for dir in skills guides templates; do
    if [[ -d "$STAGE_DIR/$dir" ]]; then
      rm -rf "$REPO_ROOT/$dir"
      cp -R "$STAGE_DIR/$dir" "$REPO_ROOT/$dir"
    fi
  done

  cd "$REPO_ROOT"
  # Stage each target dir separately — git add with multiple pathspecs aborts
  # on the first one that doesn't exist (e.g. guides/ before any guides are
  # added) and silently stages nothing even with || true.
  for dir in skills guides templates; do
    if [[ -d "$dir" ]]; then
      git add "$dir"
    fi
  done

  if git diff --cached --quiet; then
    echo "No changes to commit."
  else
    commit_msg="sync: mirror from vault ($(date -u +%Y-%m-%d))"
    git commit -m "$commit_msg"
    git push
    echo "Committed and pushed: $commit_msg"
  fi
else
  echo ""
  echo "Dry run. Re-run with --commit to apply and push."
fi
