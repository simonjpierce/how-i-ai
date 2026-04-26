# MMF Claude Code

A complete Claude Code system for thinking knowledge work — memory across sessions, behavioural defaults, log-driven self-customisation. Built up by Simon over the past year and shared here for the MMF team and close collaborators. Set up in about 15 minutes. **No reading required.**

## How to set this up

You don't need to read this repo to use it. Three steps:

1. **Install [Claude Desktop](https://claude.ai/download).** Sign in with a Pro plan or higher (Claude Code is included in Pro at $20/month — the higher tiers aren't required).
2. **Open Claude Code** from the desktop app.
3. **Paste this prompt:**

   > Walk me through setting up the system at github.com/marinemegafauna/mmf-claude-code on my machine. I'm new to all of this — please hand-hold me through it, asking one question at a time.

Claude takes it from there — a short interview (~10–15 min) and you end up with a working vault, a personalised CLAUDE.md cascade, behavioural defaults, log files, and a kickoff note in your inbox. You can dictate the answers via ChatGPT's voice transcription if you'd rather not type.

## Who this is for

The MMF science team and close collaborators — the people working with Simon on research, writing, and operations who use (or want to use) Claude Code in that work.

This is **not** a public resource. The content references MMF projects, funders, and internal workflows, and assumes you have context from working with Simon.

## Already using Claude Code?

If you have an existing setup and want to browse rather than reinstall:

- **The big picture and philosophy** — [`getting-started/00-how-simon-ais.md`](./getting-started/00-how-simon-ais.md). Architectural overview; ~10 min read.
- **Browse skills** — [`skills/`](./skills/). Each `SKILL.md` has a one-line description. Two-command install: see [`getting-started/04-adopting-skills.md`](./getting-started/04-adopting-skills.md).
- **Deeper workflow docs** — [`guides/`](./guides/).
- **Contribute** — [`CONTRIBUTING.md`](./CONTRIBUTING.md). Small improvements welcome; large changes best discussed first.

The numbered onboarding guides (`getting-started/01–04`) and the tactical setup doc (`getting-started/05-set-up-your-vault.md`) are written for Claude to read when walking a newcomer through the install above. You can read them directly if you want the architecture detail, but you don't have to.

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

This setup assumes:

- **[Claude Code](https://docs.claude.com/claude-code)** — the underlying tool, available as a desktop app or CLI. Skills are markdown files loaded from `~/.claude/skills/` and work identically in either. The `/onboard` flow defaults to the desktop app for newcomers; the terminal CLI is the path for advanced users wanting hooks and shell-tool integration (see [`guides/ghostty-setup.md`](./guides/ghostty-setup.md)).
- **[Obsidian](https://obsidian.md)** — where notes live. Most guides reference Obsidian workflows, but the skills themselves don't require it. `/onboard` walks you through Obsidian install if you don't have it yet.
- **[Codex CLI](https://github.com/openai/codex)** (optional) — ChatGPT's equivalent, useful for a second-opinion peer review from inside Claude Code. `/red-team` uses it when available.
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** (optional) — free for 1,000 requests/day. Used as a third reviewer by `/red-team`.

Individual skills document their own dependencies in their `SKILL.md`.

## Living repo disclaimer

This repository mirrors a real, evolving setup. Things change. If a skill looks out of step with how Simon's actually working, or a guide references a command that's been renamed, open an issue or PR — that's how we keep it current.

## Licence

- **Code** (scripts, skills, hook configs): [MIT](./LICENSE).
- **Prose** (guides, README, templates): [CC-BY-4.0](./LICENSE-CC-BY-4.0).

Private repository; licence terms apply in the event that content is later extracted and shared externally.
