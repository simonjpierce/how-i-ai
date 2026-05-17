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

# --- Hooks ---
# Individual hook scripts installed file-by-file (rather than as a tree) so
# users who have their own ~/.claude/hooks/ folder keep their existing scripts
# untouched. Each script is copied via install_path and chmod +x.
echo ""
echo "Hooks:"
[[ "$MODE" != "dry-run" ]] && mkdir -p "$CLAUDE_CONFIG/hooks"
HOOK_SRC_DIR="$REPO_ROOT/templates/starter-claude-config/hooks"
if [[ -d "$HOOK_SRC_DIR" ]]; then
  for hook_src in "$HOOK_SRC_DIR"/*.sh; do
    [[ -f "$hook_src" ]] || continue
    hook_name="$(basename "$hook_src")"
    install_path "$hook_src" "$CLAUDE_CONFIG/hooks/$hook_name" "hooks/$hook_name"
    if [[ "$MODE" != "dry-run" && -e "$CLAUDE_CONFIG/hooks/$hook_name" ]]; then
      chmod +x "$CLAUDE_CONFIG/hooks/$hook_name"
    fi
  done
else
  echo "  WARN: $HOOK_SRC_DIR missing, skipping hooks"
fi

# --- Settings (merge, not replace) ---
# settings.json is merged (not overwritten) so users who already configured
# their own plugins, statusLine, MCP servers, env vars, etc. keep all of that.
# The merge helper handles deep-merge semantics for hooks (appending without
# duplicating commands) and permissions (template values win for the keys
# it sets; unrelated keys preserved).
echo ""
echo "Settings:"
SETTINGS_TEMPLATE="$REPO_ROOT/templates/starter-claude-config/settings.json.template"
MERGE_SCRIPT="$REPO_ROOT/templates/starter-claude-config/scripts/merge-settings-json.py"
if [[ -f "$SETTINGS_TEMPLATE" && -f "$MERGE_SCRIPT" ]]; then
  if [[ "$MODE" == "dry-run" ]]; then
    echo "  [dry-run] would merge settings.json.template into $CLAUDE_CONFIG/settings.json"
  else
    python3 "$MERGE_SCRIPT" --template "$SETTINGS_TEMPLATE" \
      --target "$CLAUDE_CONFIG/settings.json" 2>&1 | sed 's/^/  /'
  fi
else
  echo "  WARN: settings.json.template or merge helper missing, skipping settings merge"
fi

echo ""
case "$MODE" in
  dry-run) echo "Dry run complete. Re-run without --dry-run to apply." ;;
  *) echo "Done. Restart Claude Code so the new skills are discovered, then invoke /onboard." ;;
esac
