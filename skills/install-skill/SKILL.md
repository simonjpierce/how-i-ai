---
name: install-skill
description: Install a single on-demand skill from the `mmf-claude-code` repo into `~/.claude/skills/`. Use when the user types `/install-skill <name>`, follows a course lesson that references this command, or asks how to add a specific skill they don't have yet.
allowed-tools: Read, Bash
---

The starter pack ships with six universal skills (`/onboard`, `/document`, `/session-start`, `/update`, `/review-friction`, `/refresh-skills`). Everything else lives in the repo but is **on-demand** — you install it only when you need it. This skill is the on-demand installer.

The Part 2 course lessons open with `/install-skill <name>` so you can follow a lesson by typing one command rather than copy-pasting `cp -R` lines.

## When something goes wrong

When a step fails or needs a workaround, update this file with what you learned BEFORE continuing the workaround.

## Steps

### 0. Set tab title (Ghostty only)

```bash
[ -d /Applications/Ghostty.app ] && MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "install skill" > "/tmp/claude-title-${MY_TTY}"
```

### 1. Parse the argument

The skill name comes from the user's invocation: `/install-skill research` → name is `research`. If no name is given, list the available on-demand skills (see step 3) and ask the user to pick one.

Normalise: lowercase, strip any leading slash. Reject names containing slashes or `..` (path traversal guard).

### 2. Locate the repo clone

The default location is `~/.claude/repos/mmf-claude-code/` (set by `/onboard`'s bootstrap step). Check it exists and is a git repo:

```bash
REPO="$HOME/.claude/repos/mmf-claude-code"
if [ ! -d "$REPO/.git" ]; then
  echo "No clone found at $REPO."
  echo "Either re-run /onboard, or ask the user where they cloned the repo."
  exit 1
fi
```

If the clone exists but is more than ~7 days behind `origin/main` (check `git log -1 --format=%ct origin/main` vs current time), suggest `git -C "$REPO" pull` first so the user installs the latest version. Don't pull silently — confirm first.

### 3. Validate the skill exists

```bash
SKILL_DIR="$REPO/skills/$NAME"
if [ ! -d "$SKILL_DIR" ] || [ ! -f "$SKILL_DIR/SKILL.md" ]; then
  echo "No skill named '$NAME' in the repo."
  echo "Available on-demand skills:"
  for d in "$REPO/skills"/*/; do
    n="$(basename "$d")"
    case "$n" in
      onboard|document|session-start|update|review-friction|refresh-skills) ;;
      *) [ -f "$d/SKILL.md" ] && echo "  - $n" ;;
    esac
  done
  exit 1
fi
```

If the user typed a starter skill name (one of the six already installed by bootstrap), tell them it's already part of the starter pack and they don't need to install it — but still offer to re-install if they actually meant to refresh it.

### 4. Check the install target

```bash
TARGET="$HOME/.claude/skills/$NAME"
if [ -e "$TARGET" ]; then
  # Already installed — diff and offer options.
  if diff -rq "$SKILL_DIR" "$TARGET" >/dev/null 2>&1; then
    echo "/$NAME is already installed and matches the repo version. Nothing to do."
    exit 0
  fi
  echo "/$NAME is already installed and differs from the repo version."
fi
```

If the target exists and matches, exit cleanly. If it exists and differs, present numbered options:

1. **Take the repo version** (recommended for first-time installs that already partially landed) — back up the existing copy to `$TARGET.bak-<timestamp>`, then install the repo version.
2. **Keep my version** — exit without touching anything. Tell the user `/refresh-skills review-installed` will surface upstream changes as a diff report if they want to see what's different.
3. **Compare them** — show a `diff -u` summary (cap ~30 lines), then re-ask.

### 5. Copy the skill into place

```bash
mkdir -p "$HOME/.claude/skills"
cp -R "$SKILL_DIR" "$TARGET"
# Re-apply executable bit on any .sh inside the skill folder.
find "$TARGET" -type f -name '*.sh' -exec chmod +x {} \;
```

### 6. Tell the user it's ready

```
Installed: /<NAME>
Location: ~/.claude/skills/<NAME>/

Next step: quit Claude Code (Cmd-Q) and reopen so the new skill is discovered.
After that, type /<NAME> at the prompt to use it.
```

If the skill has obvious dependencies (Codex CLI, Gemini CLI, Things 3, etc. — visible in its SKILL.md), surface a one-line note pointing the user at any setup they'll need separately. Don't try to install dependencies for them.

## Guidelines

- **One skill per invocation.** If the user wants to install several, run the skill several times.
- **Don't pull on their behalf.** If the repo clone is stale, ask before pulling; don't silently run `git pull`.
- **No silent overwrites.** If the target exists and differs, the user picks the path.
- **Don't touch `settings.json`.** This skill only installs the SKILL.md folder. Hooks and settings stay where they are.

## Post-run improvement

After completing an install, briefly assess:
- Was the option set in step 4 the right one? Any time the user wanted a fourth option?
- Did the dependency-surfacing step (6) miss anything obvious?
- Did the user understand that they need to restart Claude Code?

Update this skill if patterns emerge.
