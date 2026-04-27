#!/bin/bash
# sync-from-vault.sh — mirror MMF Claude Code skills and guides from Simon's vault
# and ~/.claude/ into this repo.
#
# Runs from Simon's machine. Dry-run by default; --commit applies changes and pushes.
# After copying into the repo for the first time: chmod +x sync/sync-from-vault.sh
#
# Usage:
#   ./sync/sync-from-vault.sh                          # dry run — stages, shows diff, no changes
#   ./sync/sync-from-vault.sh --commit                 # applies changes, commits, pushes
#   ./sync/sync-from-vault.sh --commit --allow-missing # commit even if some mapped sources are missing
#                                                      # (use ONLY when intentionally pruning — otherwise
#                                                      # sync would silently delete repo content)

set -euo pipefail

# --- Flag parsing ---

COMMIT_MODE=false
ALLOW_MISSING=false
for arg in "$@"; do
  case "$arg" in
    --commit) COMMIT_MODE=true ;;
    --allow-missing) ALLOW_MISSING=true ;;
    *) echo "Unknown flag: $arg" >&2; exit 2 ;;
  esac
done

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
  "$CLAUDE_CONFIG/skills/polish::skills/polish"
  "$CLAUDE_CONFIG/skills/todo::skills/todo"
  "$CLAUDE_CONFIG/skills/science-paper::skills/science-paper"
  "$CLAUDE_CONFIG/skills/research::skills/research"
)

GUIDES=(
  # WARNING: sync-from-vault is destructive on its target dirs (skills/, guides/,
  # templates/). On --commit it does `rm -rf <dir>` and re-copies from staged
  # mappings — so any file in those dirs WITHOUT a mapping here gets deleted.
  # Workflow: write the canonical doc in the vault first, add the mapping here,
  # THEN sync. Don't write directly to repo/guides/ — it'll be wiped on next sync.
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Ghostty Setup Guide for Claude Code.md::guides/ghostty-setup.md"
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Inviting Collaborators to mmf-claude-code.md::guides/inviting-collaborators.md"
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/AI-Assisted Scientific Analysis — Process Guide.md::guides/ai-assisted-scientific-analysis.md"
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/AI-Assisted Scientific Writing – Process Guide.md::guides/ai-assisted-scientific-writing.md"
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/AI-Assisted Writing — Reports, Manuscripts & Analysis.md::guides/ai-assisted-writing.md"
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Literature Intake & Integration Workflow.md::guides/literature-intake-and-integration.md"
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Pre-Submission Manuscript Review – Prompt Template.md::guides/pre-submission-manuscript-review.md"
  "$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Research Workflow.md::guides/research-workflow.md"
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

  # Convert Obsidian wikilinks to GitHub-renderable markdown so guides don't
  # show literal [[brackets]] when newcomers click into them from the README.
  # Shipped-guide refs become relative links; vault-only refs lose the
  # brackets and stay as plain text. Helper is idempotent.
  if [[ "$file" == *.md ]] && [[ -x "$REPO_ROOT/sync/sanitise_wikilinks.py" ]]; then
    python3 "$REPO_ROOT/sync/sanitise_wikilinks.py" "$file"
  fi
}

missing_sources=()

copy_and_sanitise() {
  local source="$1"
  local target="$2"
  local dest="$STAGE_DIR/$target"

  if [[ ! -e "$source" ]]; then
    echo "  SKIP: source missing — $source" >&2
    missing_sources+=("$source -> $target")
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

# Missing-source check — mappings whose local source doesn't exist. Distinct
# from orphans: an orphan is a repo file without a mapping; a missing source
# is a mapping where the local canonical file has gone missing. On --commit,
# missing sources cause the staged dir to be incomplete, which propagates as
# silent deletion of the corresponding repo content under `rm -rf` + cp.
# Codex red-team C10: block --commit unless caller passes --allow-missing.
echo ""
echo "--- Missing-source check ---"
if [[ ${#missing_sources[@]} -eq 0 ]]; then
  echo "  All mapped sources present locally."
else
  echo "  ${#missing_sources[@]} mapped source(s) are MISSING locally:"
  for entry in "${missing_sources[@]}"; do
    echo "    - $entry"
  done
  echo ""
  echo "  These are mappings in this script whose source path doesn't exist on"
  echo "  your machine. On --commit, the corresponding repo paths would be"
  echo "  deleted by the rm -rf + cp step (because the stage is incomplete)."
  echo ""
  echo "  If this is intentional pruning (you removed a skill/guide from your"
  echo "  vault and want to remove it from the repo too), re-run with both"
  echo "  --commit and --allow-missing."
  echo "  If this is unintentional (e.g. accidental delete, sync glitch),"
  echo "  restore the missing source first, then re-run."
fi

# Pre-flight: warn about orphans — files in the repo's target dirs that have no
# mapping in this script. On --commit, these are deleted by the `rm -rf <dir>`
# step before re-copy. This catches the case where someone wrote directly to
# the repo (e.g. guides/X.md) without adding a mapping; without this warning
# their work would be silently wiped on next sync.
echo ""
echo "--- Orphan check ---"
orphan_count=0
for dir in skills guides templates; do
  if [[ -d "$REPO_ROOT/$dir" ]]; then
    while IFS= read -r repo_file; do
      rel="${repo_file#$REPO_ROOT/}"
      if [[ ! -e "$STAGE_DIR/$rel" ]]; then
        echo "  WARNING: $rel is in repo but has no mapping — will be deleted by --commit"
        orphan_count=$((orphan_count + 1))
      fi
    done < <(find "$REPO_ROOT/$dir" -type f)
  fi
done
if [[ $orphan_count -eq 0 ]]; then
  echo "  No orphans — all repo files have a mapping."
else
  echo ""
  echo "  To preserve an orphan: write the canonical version in the vault, add a"
  echo "  mapping above (SKILLS/GUIDES/TEMPLATES), then re-run."
fi

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

if [[ "$COMMIT_MODE" == "true" ]]; then
  if [[ ${#missing_sources[@]} -gt 0 && "$ALLOW_MISSING" != "true" ]]; then
    echo ""
    echo "ABORT: --commit blocked because ${#missing_sources[@]} mapped source(s) are missing locally."
    echo "  See the Missing-source check above for the list."
    echo "  Either restore the missing sources, or re-run with --allow-missing"
    echo "  to acknowledge the pruning is intentional."
    exit 1
  fi
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
