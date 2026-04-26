---
audience: user
---

# 01 — Install Claude Code

Claude Code has two interfaces: a **desktop app** (graphical, friendlier to start with) and a **CLI** (terminal, more flexible for scripting and automation). They run the same engine and share configuration — pick whichever fits how you work, or install both.

## Prerequisites

- **macOS.** The team is on macOS and the guides in this repo assume that. Both interfaces support Windows too (Linux: CLI only — you're on your own).
- **An Anthropic account on a paid plan.** Ask Simon before buying a personal subscription — MMF has an organisation plan he can add you to. Claude Code requires Pro, Max, Team, or Enterprise.

## Option A — Desktop app

A point-and-click interface with a sidebar for parallel sessions, a diff viewer, an integrated terminal, file editor, and live app preview. No Node.js needed — the app bundles Claude Code. Requires macOS Ventura 13.0 or later.

1. Download from [claude.com/download](https://claude.com/download) and run the installer.
2. Launch Claude from your Applications folder and sign in with your Anthropic account.
3. Click the **Code** tab at the top centre. The other two tabs are **Chat** (general conversation, similar to claude.ai) and **Cowork** (autonomous background agents). You'll mostly live in Code.
4. Click **Select folder** and point it at a project directory. Pick a small project you know well for the first run.

If clicking Code prompts you to upgrade or sign in online, your account isn't on a paid plan yet — check with Simon.

## Option B — CLI

Terminal-based. More keyboard-driven, scriptable, and the only option if you want to wire Claude Code into hooks or automation pipelines.

**Terminal of choice.** macOS Terminal.app works fine. Simon uses [Ghostty](https://ghostty.org) — faster, nicer-looking, GPU-accelerated. Optional, but worth installing if you'll spend much time at a terminal.

**Node.js 18 or newer.** Check with `node --version`. If missing or too old: `brew install node` (or `brew upgrade node`).

Install Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
```

Most of the install time is waiting for npm. Confirm it worked:

```bash
claude --version
```

You should see something like `2.1.x`.

## First run

**Desktop:** with the Code tab open and a folder selected, type what you want Claude to do (e.g. "find a TODO in this repo and fix it"). Claude shows a diff for each proposed change; you click accept or reject.

**CLI:** from any project directory, run `claude`. The first run walks you through sign-in (opens a browser for OAuth), picks a default model, and drops you at the interactive prompt — a single `>` on a line.

## Sanity check

In either interface, type `/` and pause. You should see a list of slash commands — `/help`, `/clear`, `/model`, `/config`, and so on. If you see it, Claude Code is working.

To leave the CLI: type `/exit`, or Ctrl-C twice. To leave the desktop app: close the window.

## What's next

Read `02-use-code-not-chat.md` before doing any real work. Claude Code is the right tool for most research tasks, but only if you know which Claude you're actually talking to.

## If something breaks

- **Desktop app won't launch** ("unidentified developer") → System Settings → Privacy & Security → "Open Anyway".
- **Desktop Code tab shows 403 or asks you to upgrade** → your account isn't on a paid plan yet, or sign-in didn't complete. Restart the app after signing in online.
- **CLI: "command not found: claude"** after install → your `npm global bin` directory probably isn't on `$PATH`. Run `npm config get prefix`; add `$(npm config get prefix)/bin` to your shell's PATH.
- **CLI: Node version too old** → `brew upgrade node` and re-run the install command.
- **Sign-in loop or "couldn't verify"** → make sure your browser isn't blocking redirects from `auth.anthropic.com`.
- **Anything else** → message Simon in Slack with the exact error text (screenshot is fine).
