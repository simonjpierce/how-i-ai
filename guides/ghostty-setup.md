---
audience: advanced-user
note: Advanced. Not part of `/onboard`. Skip unless you specifically want a Ghostty-based terminal workflow with hooks and a statusline.
---

# Ghostty Setup Guide for Claude Code

A self-contained guide to setting up Ghostty terminal with Claude Code tab-title management, notification sounds, and a context-usage statusline. Give this file to Claude Code and ask it to set everything up.

## What this sets up

1. **Ghostty config** — theme, font, working directory
2. **Tab title daemon** — shows what Claude is working on, adds a checkmark when done
3. **Notification hooks** — sounds when Claude finishes, asks a question, or needs permission
4. **Statusline** — shows model name and context window usage at the bottom of the terminal

## Prerequisites

- macOS (Apple Silicon or Intel)
- [Ghostty](https://ghostty.org) installed
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed (`npm install -g @anthropic-ai/claude-code`)
- `jq` installed (`brew install jq`)
- Source Code Pro font installed (`brew install --cask font-source-code-pro`)

---

## Step 1: Ghostty config

Write this to `~/Library/Application Support/com.mitchellh.ghostty/config`:

```
theme = Andromeda
font-family = Source Code Pro
font-size = 14
font-thicken = true
adjust-cell-height = 1
```

Optionally add a `working-directory` line if you want every new tab to open in a specific folder (e.g. your Obsidian vault):

```
working-directory = /path/to/your/working/directory
```

---

## Step 2: Hook scripts

Create the directory structure:

```bash
mkdir -p ~/.claude/hooks/lib
```

### `~/.claude/hooks/lib/ensure-title-daemon.sh`

Shared helper that starts the title daemon if it's not already running.

```bash
#!/bin/bash
ensure_title_daemon() {
  [ -z "$MY_TTY" ] && return 1
  local pidfile="/tmp/claude-title-daemon-${MY_TTY}.pid"
  if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
    return 0
  fi
  nohup ~/.claude/hooks/title-daemon.sh "$MY_TTY" "$PPID" >/dev/null 2>&1 &
  echo $! > "$pidfile"
  disown
}
```

### `~/.claude/hooks/title-daemon.sh`

Background daemon that sets the Ghostty tab title. Polls every 2 seconds. Shows a checkmark when Claude has been idle for 5+ seconds.

```bash
#!/bin/bash
TTY="$1"
CLAUDE_PID="$2"
DEBOUNCE=5
LAST_OUTPUT=""

[ -z "$TTY" ] || [ -z "$CLAUDE_PID" ] && exit 1

while kill -0 "$CLAUDE_PID" 2>/dev/null; do
  TITLE=$(cat "/tmp/claude-title-${TTY}" 2>/dev/null)
  if [ -n "$TITLE" ]; then
    DONE_FILE="/tmp/claude-done-${TTY}"
    SHOW_DONE=false
    if [ -f "$DONE_FILE" ]; then
      FILE_MOD=$(stat -f %m "$DONE_FILE" 2>/dev/null) || FILE_MOD=""
      if [ -n "$FILE_MOD" ]; then
        FILE_AGE=$(( $(date +%s) - FILE_MOD ))
        [ "$FILE_AGE" -ge "$DEBOUNCE" ] && SHOW_DONE=true
      fi
    fi
    if [ "$SHOW_DONE" = true ]; then
      TITLE="${TITLE#✅ }"
      TITLE="${TITLE#✅}"
      OUTPUT="✅ ${TITLE}"
    else
      OUTPUT="$TITLE"
    fi
    if [ "$OUTPUT" != "$LAST_OUTPUT" ]; then
      printf '\e]0;%s\a' "$OUTPUT" > "/dev/${TTY}" 2>/dev/null
      LAST_OUTPUT="$OUTPUT"
    fi
  fi
  sleep 2
done
```

### `~/.claude/hooks/clear-done-marker.sh`

Clears the checkmark when Claude starts working again. Runs on every tool use.

```bash
#!/bin/bash
MY_TTY=${TTY:-$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ')}
[ -f "/tmp/claude-done-${MY_TTY}" ] && rm -f "/tmp/claude-done-${MY_TTY}"
exit 0
```

### `~/.claude/hooks/notify-complete.sh`

Plays a sound and creates the done marker when Claude finishes a response.

```bash
#!/bin/bash
MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ')
[ -z "$MY_TTY" ] && exit 0

touch "/tmp/claude-done-${MY_TTY}"

osascript -e 'display notification "Claude Code has finished working." with title "Claude Code" sound name "Glass"' 2>/dev/null

. ~/.claude/hooks/lib/ensure-title-daemon.sh
ensure_title_daemon
exit 0
```

### `~/.claude/hooks/notify-question.sh`

Bell + notification when Claude asks you a question.

```bash
#!/bin/bash
printf "\a" > /dev/tty 2>/dev/null
osascript -e 'display notification "Claude has a question for you." with title "Claude Code" sound name "Tink"' 2>/dev/null
exit 0
```

### `~/.claude/hooks/notify-permission.sh`

Bell + notification when Claude needs permission to run a command.

```bash
#!/bin/bash
printf "\a" > /dev/tty 2>/dev/null
osascript -e 'display notification "Permission approval needed." with title "Claude Code" sound name "Tink"' 2>/dev/null
exit 0
```

Make all scripts executable:

```bash
chmod +x ~/.claude/hooks/*.sh ~/.claude/hooks/lib/*.sh
```

---

## Step 3: Statusline

### `~/.claude/statusline.sh`

Shows model name and context window usage in the Claude Code status bar.

```bash
#!/bin/bash
input=$(cat)

eval "$(echo "$input" | jq -r '
  "MODEL=" + (.model.display_name | @sh) +
  " CONTEXT_SIZE=" + (.context_window.context_window_size | tostring | @sh) +
  " CURRENT=" + ((.context_window.current_usage // null) | if . then (.input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens + .output_tokens | tostring) else "null" end | @sh)
')"

MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ')
TASK=""
if [ -n "$MY_TTY" ] && [ -f "/tmp/claude-title-${MY_TTY}" ]; then
  TASK=$(cat "/tmp/claude-title-${MY_TTY}" 2>/dev/null | head -1 | xargs)
fi

TASK_PREFIX=""
if [ -n "$TASK" ]; then
  TASK_PREFIX="${TASK} | "
fi

if [ "$CURRENT" != "null" ]; then
  PERCENT=$((CURRENT * 100 / CONTEXT_SIZE))
  REMAINING=$((100 - PERCENT))
  if [ "$REMAINING" -le 15 ]; then
    echo "[$MODEL] ${TASK_PREFIX}Context: ${PERCENT}% used | ${REMAINING}% LEFT - COMPACTING IMMINENTLY"
  elif [ "$REMAINING" -le 30 ]; then
    echo "[$MODEL] ${TASK_PREFIX}Context: ${PERCENT}% used | ${REMAINING}% LEFT - COMPACT SOON"
  else
    echo "[$MODEL] ${TASK_PREFIX}Context: ${PERCENT}% used | ${REMAINING}% remaining"
  fi
else
  echo "[$MODEL] ${TASK_PREFIX}Context: 0%"
fi
```

Make it executable:

```bash
chmod +x ~/.claude/statusline.sh
```

---

## Step 4: Claude Code settings

Add these entries to `~/.claude/settings.json`. If the file already exists, merge these sections into it. If it doesn't exist, create it with this content:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/clear-done-marker.sh",
            "timeout": 2
          }
        ]
      },
      {
        "matcher": "AskUserQuestion",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/notify-question.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/notify-permission.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/notify-complete.sh",
            "timeout": 5
          }
        ]
      }
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

---

## Step 5: Tab title integration

For Claude Code to set the tab title, it needs to write a short summary to a temp file. Add this to your Claude Code instructions (e.g. `~/.claude/CLAUDE.md`):

```
At the start of each session (or when the task changes significantly), set a short task summary as the Ghostty tab title:

MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "short task summary" > "/tmp/claude-title-${MY_TTY}"

Keep it to 3-6 words (e.g. "grant budget review", "debugging bundler"). Do this quietly.
```

---

## How it works

- **Tab titles**: Claude writes a task summary to `/tmp/claude-title-{tty}`. The title daemon reads it every 2 seconds and sets the Ghostty tab title.
- **Checkmark**: When Claude finishes, `notify-complete.sh` creates `/tmp/claude-done-{tty}`. After a 5-second debounce, the daemon prepends a checkmark to the title.
- **Clearing**: When Claude starts working again, `clear-done-marker.sh` removes the done marker, and the title reverts to the task summary.
- **Sounds**: `Glass` for completion, `Tink` for questions and permission prompts. All built-in macOS sounds.
- **Statusline**: Shows model name and context usage percentage. Warns at 70% and 85% used.

## Verification

After setup, start a new Claude Code session in Ghostty. You should see:
- A statusline at the bottom showing `[Model Name] Context: 0%`
- Notification sounds when Claude finishes or asks questions
- Tab title updates when Claude sets them
