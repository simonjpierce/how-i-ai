# 05 — Set up your vault

> **For Claude, not for the user.** This document is read by Claude when a newcomer pastes the README's three-step prompt. The user themselves doesn't need to read it.

When a user pastes a prompt asking you to walk them through setting up `mmf-claude-code`, follow this doc. The flow:

## What `/onboard` does

`/onboard` is the bridge skill that takes a user from "nothing installed" to "working Claude system." It runs a short discovery interview (5–7 questions, ~10–15 minutes), then writes a personalised CLAUDE.md cascade, starter MEMORY.md, log files, kickoff note, and config.json into the user's vault. It optionally walks through per-domain folder setup and schedules a follow-up routine in 2 weeks for the nightly self-improvement loop.

## How to run it

**Step 1 — install the skill** to the user's local Claude Code config:

```bash
mkdir -p ~/.claude/skills/onboard
cp <repo-clone>/skills/onboard/SKILL.md ~/.claude/skills/onboard/SKILL.md
```

If the user followed the README and you cloned this repo to a temp directory, `<repo-clone>` is that path. If not, clone it now:

```bash
git clone --depth 1 https://github.com/marinemegafauna/mmf-claude-code.git /tmp/mmf-claude-code-onboard
```

While you're at it, copy the templates so `/onboard` finds them locally:

```bash
mkdir -p ~/.claude/templates
cp -R /tmp/mmf-claude-code-onboard/templates/starter-claude-config ~/.claude/templates/
cp -R /tmp/mmf-claude-code-onboard/templates/starter-vault ~/.claude/templates/
```

Also install the four other v0 skills the user will benefit from immediately — `/document`, `/session-start`, `/update`, `/review-friction`:

```bash
for skill in document session-start update review-friction; do
  mkdir -p ~/.claude/skills/$skill
  cp -R /tmp/mmf-claude-code-onboard/skills/$skill/* ~/.claude/skills/$skill/
done
```

**Step 2 — invoke `/onboard`.** The skill will take it from there: it handles pre-flight (auto-approval mode check, filesystem-write capability), detects fresh-vs-existing vault, runs the discovery interview, writes all the files, runs the optional domain pass, and schedules the self-improvement follow-up at +14 days.

## If the environment can't write files

If you're running in Claude Chat (claude.ai web) rather than Claude Code, you won't have filesystem access — `/onboard` can't write the files it needs to. Stop the flow and instruct the user:

> *"To finish this setup I need filesystem access, which Claude Chat doesn't have. Open Claude Desktop, switch to Claude Code in the desktop app (it's included on the same Pro plan you already have), and paste the README prompt again. I'll resume from there."*

Don't try to fake the install in a Chat-only environment. The user needs to be in Claude Code.

## After `/onboard` finishes

The skill ends with a personalised `Getting Started.md` open in the user's Obsidian vault. That's their first read. Don't chain into other skills — they'll take it from there.
