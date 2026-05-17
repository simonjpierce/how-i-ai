#!/bin/bash
# Tab-title hook — set the terminal tab title from /tmp/claude-title-<tty>.
#
# Convention: Claude (or you) writes a short task summary to
# /tmp/claude-title-<tty> at any point in a session. This hook reads that
# file and emits an ANSI title escape sequence to the parent terminal.
#
# Set the title at session start with something like:
#   echo "short task summary" > "/tmp/claude-title-$(ps -o tty= -p $PPID | tr -d ' ')"
#
# Registered on SessionStart (clears stale title from prior session) and
# PostToolUse:Edit|Write (refreshes after meaningful work).
#
# This is intentionally simple — no background daemon, no done-marker logic.
# If you want richer title behaviour (✅ on completion, persistent across
# Claude Code's own title writes), graduate to a daemon-based version.

# Discover the parent TTY. PPID points at the shell that launched Claude
# Code; its tty is what shows the tab title.
MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ')
[ -z "$MY_TTY" ] && exit 0

TITLE_FILE="/tmp/claude-title-${MY_TTY}"

# Read input (Claude Code pipes hook context as JSON on stdin). We don't
# need its content but must consume it so the pipe closes cleanly.
cat > /dev/null

# Determine the event — SessionStart should not require an existing title
# file (it can pre-seed an empty one); PostToolUse exits silently if no
# title is set. The HOOK_EVENT env var is provided by Claude Code.
HOOK_EVENT="${HOOK_EVENT:-PostToolUse}"

if [ ! -s "$TITLE_FILE" ]; then
    # No title set. On SessionStart, clear any stale title from a prior session.
    if [ "$HOOK_EVENT" = "SessionStart" ]; then
        printf '\e]0;%s\a' "Claude Code" > "/dev/${MY_TTY}" 2>/dev/null
    fi
    exit 0
fi

TITLE=$(cat "$TITLE_FILE")
[ -z "$TITLE" ] && exit 0

printf '\e]0;%s\a' "$TITLE" > "/dev/${MY_TTY}" 2>/dev/null
exit 0
