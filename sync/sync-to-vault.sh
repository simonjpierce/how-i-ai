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
#   ./sync/sync-to-vault.sh --apply    # apply if no local conflicts; HALT and
#                                      # list conflict files otherwise
#   ./sync/sync-to-vault.sh --force    # apply unconditionally (your local
#                                      # edits to conflict files will be lost)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Resolve VAULT_PATH and AI_WORKFLOW_DIR for guide-target mappings.
# Priority: env override > config.json discovery > Simon's hardcoded fallback.
# This matters because guides land inside the user's vault, not under
# ~/.claude/, so the script must know where the user's vault actually is.
# Codex red-team C5: previously this defaulted to Simon's hardcoded
# iCloud path, so a newcomer running /refresh-skills would create a fake
# "Simon's Vault" folder on their Mac.

if [[ -z "${VAULT_PATH:-}" ]]; then
  for cfg in "$HOME/.claude/projects"/*/config.json; do
    [[ -f "$cfg" ]] || continue
    # One python3 call returns both fields tab-separated. Two-call version was
    # flagged in red-team Step 8 ecosystem review (efficiency #1) — single call
    # also avoids the partial-write race between two json.load() calls.
    IFS=$'\t' read -r candidate candidate_aiwf < <(python3 -c '
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    v = d.get("vault", {}).get("path", "").strip()
    a = d.get("folders", {}).get("ai_workflow", "AI_WORKFLOW").strip() or "AI_WORKFLOW"
    print(f"{v}\t{a}")
except Exception:
    print("\tAI_WORKFLOW")
' "$cfg" 2>/dev/null) || true
    if [[ -n "${candidate:-}" ]]; then
      VAULT_PATH="$candidate"
      AI_WORKFLOW_DIR="$candidate_aiwf"
      break
    fi
  done
  if [[ -z "${VAULT_PATH:-}" ]]; then
    VAULT_PATH="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Simon's Vault"
    AI_WORKFLOW_DIR="05_AI WORKFLOW"
    echo "Note: no config.json with vault.path found — falling back to Simon's vault layout." >&2
  fi
fi
AI_WORKFLOW_DIR="${AI_WORKFLOW_DIR:-05_AI WORKFLOW}"
VAULT_PROCESSES="$VAULT_PATH/$AI_WORKFLOW_DIR/CLAUDE/Processes"

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
  "skills/refresh-skills::$CLAUDE_CONFIG/skills/refresh-skills"
  "skills/polish::$CLAUDE_CONFIG/skills/polish"
  "skills/todo::$CLAUDE_CONFIG/skills/todo"
  "skills/science-paper::$CLAUDE_CONFIG/skills/science-paper"
  "skills/research::$CLAUDE_CONFIG/skills/research"
)

TEMPLATES=(
  "templates/starter-claude-config::$CLAUDE_CONFIG/templates/starter-claude-config"
  "templates/starter-vault::$CLAUDE_CONFIG/templates/starter-vault"
)

GUIDES=(
  # Mirror of sync-from-vault.sh's GUIDES array, reversed (repo → vault). When
  # a contributor PR edits any of these guides in the repo, /refresh-skills
  # uses this array to pull the changes back into the user's vault. Keep in
  # sync with sync-from-vault.sh — dogfood Phase 14 enforces parity.
  "guides/ghostty-setup.md::$VAULT_PROCESSES/Ghostty Setup Guide for Claude Code.md"
  "guides/inviting-collaborators.md::$VAULT_PROCESSES/Inviting Collaborators to mmf-claude-code.md"
  "guides/ai-assisted-scientific-analysis.md::$VAULT_PROCESSES/AI-Assisted Scientific Analysis — Process Guide.md"
  "guides/ai-assisted-scientific-writing.md::$VAULT_PROCESSES/AI-Assisted Scientific Writing – Process Guide.md"
  "guides/ai-assisted-writing.md::$VAULT_PROCESSES/AI-Assisted Writing — Reports, Manuscripts & Analysis.md"
  "guides/literature-intake-and-integration.md::$VAULT_PROCESSES/Literature Intake & Integration Workflow.md"
  "guides/pre-submission-manuscript-review.md::$VAULT_PROCESSES/Pre-Submission Manuscript Review – Prompt Template.md"
  "guides/research-workflow.md::$VAULT_PROCESSES/Research Workflow.md"
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

if [[ "$MODE" != "--apply" && "$MODE" != "--force" ]]; then
  echo ""
  echo "Dry run. Re-run with --apply to pull these into your local canonical paths."
  echo ""
  echo "Conflict policy: --apply will HALT if any 'Changed' file above differs"
  echo "from your local copy (likely meaning you have local edits that would be"
  echo "lost). New files apply silently. Pass --force to override the halt"
  echo "(only do this once you've checked the diffs above and accepted the loss"
  echo "of your local edits, or committed them somewhere safe)."
  exit 0
fi

# --apply: halt on changed mappings unless --force, since each one is a
# potential conflict (your local copy diverges from the contributor's
# version that's about to land).
if [[ "$MODE" == "--apply" && ${#changed[@]} -gt 0 ]]; then
  echo ""
  echo "HALT: ${#changed[@]} file(s) have local edits that differ from the"
  echo "repo version. Pulling now would replace your local edits."
  echo ""
  echo "Files in conflict:"
  for mapping in "${changed[@]}"; do
    repo_rel="${mapping%%::*}"
    target="${mapping##*::}"
    echo "  - $repo_rel → $target"
  done
  echo ""
  echo "Resolve before re-running. Options:"
  echo "  (a) Commit your local edits to ~/.claude/ first, then re-run --apply."
  echo "      Your edits are preserved in git history and the conflict resolves."
  echo "  (b) If you don't need the local edits, re-run with --force to take"
  echo "      the repo version everywhere."
  echo "  (c) If you want to merge by hand: open the file pairs side-by-side"
  echo "      (the staged version sits at $STAGE_DIR while this script is"
  echo "      running, but the temp dir is removed on exit — copy out first)."
  exit 1
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
