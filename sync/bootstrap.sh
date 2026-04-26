#!/bin/bash
# bootstrap.sh — one-shot installer for mmf-claude-code starter skills + templates.
#
# Run this once after cloning the repo (or have Claude run it for you during
# /onboard). It copies the v0 starter skills and templates from this repo into
# ~/.claude/, where Claude Code will discover them on next restart.
#
# Idempotent: safe to re-run. Existing skill directories are replaced atomically
# with the repo version.
#
# Usage:
#   ./sync/bootstrap.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_CONFIG="$HOME/.claude"

STARTER_SKILLS=(
  onboard
  document
  session-start
  update
  review-friction
)

echo "Installing mmf-claude-code starter content to $CLAUDE_CONFIG..."

# --- Templates ---
mkdir -p "$CLAUDE_CONFIG/templates"
for tmpl in starter-claude-config starter-vault; do
  src="$REPO_ROOT/templates/$tmpl"
  dst="$CLAUDE_CONFIG/templates/$tmpl"
  if [[ ! -d "$src" ]]; then
    echo "  WARN: $src missing, skipping" >&2
    continue
  fi
  rm -rf "$dst"
  cp -R "$src" "$dst"
  echo "  templates/$tmpl → $dst"
done

# --- Skills ---
mkdir -p "$CLAUDE_CONFIG/skills"
for skill in "${STARTER_SKILLS[@]}"; do
  src="$REPO_ROOT/skills/$skill"
  dst="$CLAUDE_CONFIG/skills/$skill"
  if [[ ! -d "$src" ]]; then
    echo "  WARN: $src missing, skipping" >&2
    continue
  fi
  rm -rf "$dst"
  cp -R "$src" "$dst"
  echo "  skills/$skill → $dst"
done

echo ""
echo "Done. Restart Claude Code so the new skills are discovered, then invoke /onboard."
