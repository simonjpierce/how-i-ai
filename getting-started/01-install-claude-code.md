# 01 — Install Claude Code

Claude Code is a CLI — you run it in the terminal. First install takes about fifteen minutes on a clean Mac, most of which is waiting for npm.

## Prerequisites

- **macOS.** The rest of the team is on macOS and the guides in this repo assume that. Claude Code runs on Windows and Linux too, but you're on your own for those.
- **Node.js 18 or newer.** Check with `node --version`. If missing or too old: `brew install node` (or `brew upgrade node`).
- **An Anthropic account.** Ask Simon before buying a personal subscription — MMF has an organisation plan he can add you to.

## Install

```bash
npm install -g @anthropic-ai/claude-code
```

Confirm it worked:

```bash
claude --version
```

You should see something like `2.1.x`.

## First run

From your home directory or any project directory:

```bash
claude
```

The first run walks you through sign-in (opens a browser for OAuth), picks a default model, and drops you at the interactive prompt. The prompt is a single `>` on a line.

## Sanity check

At the prompt, type `/` and pause. You should see a popup or inline list of slash commands — `/help`, `/clear`, `/model`, `/config`, and so on. If you see it, Claude Code is working.

Type `/exit` to leave (or Ctrl-C twice).

## What's next

Read `02-use-code-not-chat.md` before doing any real work. Claude Code is the right tool for most research tasks, but only if you know which Claude you're actually talking to.

## If something breaks

- **"command not found: claude"** after install → your `npm global bin` directory probably isn't on `$PATH`. Run `npm config get prefix`; add `$(npm config get prefix)/bin` to your shell's PATH.
- **Node version too old** → `brew upgrade node` and re-run the install command.
- **Sign-in loop or "couldn't verify"** → make sure your browser isn't blocking redirects from `auth.anthropic.com`.
- **Anything else** → message Simon in Slack with the exact error text (screenshot is fine).
