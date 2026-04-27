# MMF Claude Code

A complete Claude Code system for thinking knowledge work — memory across sessions, behavioural defaults, log-driven self-customisation. Built up by Simon over the past year and shared here for the MMF team and close collaborators. Block 30 minutes total: ~10 minutes downloading apps, then a 10–15 minute interview where Claude asks you questions. **No reading required.**

**Currently macOS-only.** Windows and Linux support is on the v1 roadmap. If you're on Windows or Linux and want to set this up anyway, ping Simon for a manual install — `/onboard` will halt cleanly otherwise.

## How to set this up

You don't need to read this repo to use it. Three steps:

1. **Install [Claude Desktop](https://claude.com/download).** Claude Code is included on a Pro plan ($20/month) and any higher tier. **MMF science team:** Simon should have added you to the MMF org plan before sending this link — if you sign in and the Code tab still says "upgrade," reply to him with a screenshot. **Close collaborators outside MMF:** Pro is the right plan; the higher tiers aren't necessary.
2. **Click the "Code" tab** in the desktop app (you'll see Chat, Cowork, and Code tabs). Despite the name, "Code" isn't just for programming — it's the only tab that can read and write files on your Mac. Click **Select folder** and pick any folder for now (your Documents folder is fine — Claude will move you to the right one in a minute).
3. **Paste this prompt** into the Code tab:

   ```
   Walk me through setting up the system at github.com/marinemegafauna/mmf-claude-code on my machine. I'm new to all of this — please hand-hold me through it, asking me one question at a time.
   ```

Claude takes it from there — a short interview (~10–15 min) and you end up with a working vault, a personalised CLAUDE.md cascade, behavioural defaults, log files, and a kickoff note in your inbox. If you'd rather dictate than type, macOS's built-in dictation works (press Fn twice in any text field). ChatGPT's voice mode is also good if you have a Plus account.

## Who this is for

The MMF science team and close collaborators — the people working with Simon on research, writing, and operations who use (or want to use) Claude Code in that work.

This is **not** a public resource. The content references MMF projects, funders, and internal workflows, and assumes you have context from working with Simon.

## Already using Claude Code?

If you have an existing setup and want to browse rather than reinstall:

- **The big picture and philosophy** — [`getting-started/00-how-simon-ais.md`](./getting-started/00-how-simon-ais.md). Architectural overview; ~10 min read.
- **Browse skills** — [`skills/`](./skills/). Each `SKILL.md` has a one-line description. Two-command install: see [`getting-started/04-adopting-skills.md`](./getting-started/04-adopting-skills.md).
- **Deeper workflow docs** — [`guides/`](./guides/).
- **Contribute** — [`CONTRIBUTING.md`](./CONTRIBUTING.md). Small improvements welcome; large changes best discussed first.

If you want to read the architecture before/instead of running `/onboard`:

- `00-how-simon-ais.md`, `01-install-claude-code.md`, `02-use-code-not-chat.md` are written for humans — they explain what Claude Code is and why this setup is shaped the way it is.
- `03-your-first-skill.md`, `04-adopting-skills.md`, `05-set-up-your-vault.md` are written for Claude to follow during onboarding — you can read them, but they're scripts, not explainers.

## Repository map

```
mmf-claude-code/
├── getting-started/    Numbered onboarding guides + tactical setup doc Claude reads during /onboard
├── skills/             Installable Claude Code skills (one folder per skill)
├── guides/             Deeper-dive workflow docs — Ghostty setup, lab notebook, manuscript review
├── templates/          Starter vault and `~/.claude/` templates that ship with /onboard
└── sync/               The script Simon uses to mirror his vault's skills and templates into this repo
```

## The stack

**Required:**

- **[Claude Code](https://docs.claude.com/claude-code)** — the underlying tool, available as a desktop app or CLI. Skills are markdown files loaded from `~/.claude/skills/` and work identically in either. The `/onboard` flow defaults to the desktop app for newcomers; the terminal CLI is the path for advanced users wanting hooks and shell-tool integration (see [`guides/ghostty-setup.md`](./guides/ghostty-setup.md)).
- **[Obsidian](https://obsidian.md)** — where notes live. Most guides reference Obsidian workflows, but the skills themselves don't require it. `/onboard` walks you through Obsidian install if you don't have it yet.

**Optional (install later if you want them):**

- **[Codex CLI](https://github.com/openai/codex)** — ChatGPT's equivalent, useful for a second-opinion peer review from inside Claude Code. `/red-team` uses it when available.
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — free for 1,000 requests/day. Used as a third reviewer by `/red-team`.

Individual skills document their own dependencies in their `SKILL.md`.

## Living repo disclaimer

This repository mirrors a real, evolving setup. Things change. If something looks broken, stale, or contradicts another doc, open an issue or PR — that's how we keep it current.

## Licence

- **Code** (scripts, skills, hook configs): [MIT](./LICENSE).
- **Prose** (guides, README, templates): [CC-BY-4.0](./LICENSE-CC-BY-4.0).

Private repository; licence terms apply in the event that content is later extracted and shared externally.
