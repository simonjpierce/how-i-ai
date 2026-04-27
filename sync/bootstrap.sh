#!/bin/bash
# bootstrap.sh — one-shot installer for mmf-claude-code starter skills + templates.
#
# Run this once after cloning the repo (or have Claude run it for you during
# /onboard). It copies the v0 starter skills and templates from this repo into
# ~/.claude/, where Claude Code will discover them on next restart.
#
# Re-run safety: identical sources skip silently. Differing sources save a
# timestamped .bak-<ts>/ backup of the existing target, then in interactive
# mode prompt before overwriting; in non-interactive mode the backup is kept
# and the new content is installed.
#
# Usage:
#   ./sync/bootstrap.sh           # interactive: prompts on diff
#   ./sync/bootstrap.sh --yes     # non-interactive: backup then overwrite
#   ./sync/bootstrap.sh --dry-run # show what would change, no writes

set -euo pipefail

# Platform check — currently macOS-only.
if [ "$(uname)" != "Darwin" ]; then
  echo "Error: bootstrap.sh is currently macOS-only." >&2
  echo "Windows and Linux support is on the v1 roadmap. If you want to run this anyway, ping Simon for a manual install." >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_CONFIG="$HOME/.claude"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

MODE="interactive"
case "${1:-}" in
  --yes|-y) MODE="yes" ;;
  --dry-run|-n) MODE="dry-run" ;;
  "") MODE="interactive" ;;
  *) echo "Usage: $0 [--yes|--dry-run]" >&2; exit 2 ;;
esac

STARTER_SKILLS=(
  onboard
  document
  session-start
  update
  review-friction
  refresh-skills
  todo
  science-paper
  research
  verify-citations
)

# install_path SRC DST LABEL
# - if DST missing: copy
# - if DST identical to SRC: skip
# - if DST differs: backup to DST.bak-<ts>, then (interactive: prompt; yes: overwrite; dry-run: log)
install_path() {
  local src="$1"
  local dst="$2"
  local label="$3"

  if [[ ! -e "$src" ]]; then
    echo "  WARN: $src missing, skipping" >&2
    return 0
  fi

  if [[ ! -e "$dst" ]]; then
    if [[ "$MODE" == "dry-run" ]]; then
      echo "  [dry-run] would install (new): $label"
    else
      mkdir -p "$(dirname "$dst")"
      cp -R "$src" "$dst"
      echo "  installed (new): $label"
    fi
    return 0
  fi

  if diff -rq "$src" "$dst" >/dev/null 2>&1; then
    echo "  unchanged: $label"
    return 0
  fi

  local backup="${dst}.bak-${TIMESTAMP}"
  case "$MODE" in
    dry-run)
      echo "  [dry-run] would backup → $backup and replace: $label"
      ;;
    yes)
      mv "$dst" "$backup"
      cp -R "$src" "$dst"
      echo "  replaced (backup at $backup): $label"
      ;;
    interactive)
      echo ""
      echo "  DIFF: $label has local changes. Top-level differences:"
      diff -rq "$src" "$dst" 2>&1 | head -10 | sed 's/^/    /'
      printf "  Replace with repo version? [y/N] (a backup will be saved to %s): " "$backup"
      read -r reply
      case "$reply" in
        [yY]|[yY][eE][sS])
          mv "$dst" "$backup"
          cp -R "$src" "$dst"
          echo "  replaced (backup at $backup): $label"
          ;;
        *)
          echo "  skipped: $label (your local copy is unchanged)"
          ;;
      esac
      ;;
  esac
}

echo "Installing mmf-claude-code starter content to $CLAUDE_CONFIG..."
echo "Mode: $MODE"
echo ""

# --- Templates ---
[[ "$MODE" != "dry-run" ]] && mkdir -p "$CLAUDE_CONFIG/templates"
echo "Templates:"
for tmpl in starter-claude-config starter-vault; do
  install_path "$REPO_ROOT/templates/$tmpl" "$CLAUDE_CONFIG/templates/$tmpl" "templates/$tmpl"
done

# --- Skills ---
[[ "$MODE" != "dry-run" ]] && mkdir -p "$CLAUDE_CONFIG/skills"
echo ""
echo "Skills:"
for skill in "${STARTER_SKILLS[@]}"; do
  install_path "$REPO_ROOT/skills/$skill" "$CLAUDE_CONFIG/skills/$skill" "skills/$skill"
done

echo ""
case "$MODE" in
  dry-run) echo "Dry run complete. Re-run without --dry-run to apply." ;;
  *) echo "Done. Restart Claude Code so the new skills are discovered, then invoke /onboard." ;;
esac
