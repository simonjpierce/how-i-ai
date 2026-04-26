---
audience: claude
---

# 05 — Set up your vault

> **For Claude, not for the user.** This document is read by Claude when a newcomer pastes the README's three-step prompt. The user themselves doesn't need to read it.

When a user pastes a prompt asking you to walk them through setting up `mmf-claude-code`, follow this doc.

## What `/onboard` does

`/onboard` is the bridge skill that takes a user from "nothing installed" to "working Claude system." It runs a short discovery interview (5–7 questions, ~10–15 minutes), then writes a personalised CLAUDE.md cascade, starter MEMORY.md, log files, kickoff note, and config.json into the user's vault. It optionally walks through per-domain folder setup and schedules a follow-up routine in 2 weeks for the nightly self-improvement loop.

## Pre-flight: confirm filesystem access

Before installing anything, confirm you can write to the user's filesystem. If you're running in **Claude Chat** (claude.ai web) rather than **Claude Code**, you cannot write files — stop now and instruct the user:

> *"To finish this setup I need filesystem access, which Claude Chat doesn't have. Open Claude Desktop, switch to Claude Code in the desktop app (it's included on the same Pro plan you already have), and paste the README prompt again. I'll resume from there."*

Don't try to fake the install — the user needs to be in Claude Code.

## Step 1 — clone the repo and run the bootstrap

The repo ships a single bootstrap script that installs the v0 starter skills (`/onboard`, `/document`, `/session-start`, `/update`, `/review-friction`) and templates (`starter-claude-config`, `starter-vault`) into `~/.claude/`.

First, pre-flight check the user's environment:

```bash
command -v git >/dev/null 2>&1 || { echo "ERROR: git not installed. Install Xcode Command Line Tools first: xcode-select --install"; exit 1; }
command -v bash >/dev/null 2>&1 || { echo "ERROR: bash not available"; exit 1; }
```

If `git` is missing, halt and tell the user to install Xcode Command Line Tools, then re-paste the prompt. Don't try to install for them.

Then clone to a stable location (not `/tmp/`, which gets cleaned at reboot — the kickoff note's "describe-to-Claude PR" affordance later will need this clone to still exist). Use `~/.claude/repos/`:

```bash
mkdir -p ~/.claude/repos
if [ -d ~/.claude/repos/mmf-claude-code ]; then
  git -C ~/.claude/repos/mmf-claude-code pull --quiet
else
  git clone --depth 1 https://github.com/marinemegafauna/mmf-claude-code.git ~/.claude/repos/mmf-claude-code
fi
bash ~/.claude/repos/mmf-claude-code/sync/bootstrap.sh --yes
```

If the `git clone` fails with `fatal: repository not found`, the user doesn't have access — the repo is private. Tell them: *"Looks like you need GitHub access to the `marinemegafauna/mmf-claude-code` repo. The simplest path is `gh auth login` if you have the GitHub CLI installed (or run `brew install gh` first), then I'll re-run the clone. If you don't have a GitHub account at all, ask Simon to add your account."* Don't proceed without the clone.

(`--yes` runs the bootstrap non-interactively — it backs up any existing local edits to `*.bak-<timestamp>` directories and replaces with repo content. If the user has been making local edits to skills they want to keep, they can run without `--yes` later for the interactive prompt-on-diff path.)

If the `git clone` fails with `fatal: repository not found`, the user doesn't have access — the repo is private. Tell them: *"Looks like you need GitHub access to the `marinemegafauna/mmf-claude-code` repo. Run `gh auth login` first (or ask Simon to add your GitHub username), then I'll re-run the clone."* Don't proceed without the clone.

The bootstrap script is re-run safe: identical sources skip, differing sources save a timestamped `.bak` backup and prompt before overwriting (interactive). It prints what it installs and ends with a "restart Claude Code" instruction.

## Step 2 — restart Claude Code

Newly added skills aren't discovered until Claude Code restarts. Tell the user:

> *"I've installed the starter skills. Quit Claude Code and reopen it (or restart the desktop app), then come back and say 'continue' so I can run `/onboard`."*

## Step 3 — invoke `/onboard`

Once the user confirms they've restarted, invoke `/onboard`. The skill handles pre-flight (auto-approval mode check, filesystem-write capability), detects fresh-vs-existing vault, runs the discovery interview, writes all the files, runs the optional domain pass, and schedules the self-improvement follow-up at +14 days.

## After `/onboard` finishes

The skill ends with a personalised `Getting Started.md` open in the user's Obsidian vault. That's their first read. Don't chain into other skills — they'll take it from there.
