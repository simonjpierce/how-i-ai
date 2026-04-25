# MMF Claude Code

Shared Claude Code skills, guides, and templates for the Marine Megafauna Foundation team and close research collaborators.

Simon has built a deep Claude Code setup over the past year — skills, process docs, templates, automations — that have reshaped how he writes, analyses data, and runs the organisation. This repository is how that setup gets shared with the rest of us, and iterated on collectively.

If you've just got Claude Code working for the first time, start at [`getting-started/`](./getting-started/).

## Who this is for

The MMF science team and collaborators — the people working with Simon on research, writing, and operations who use (or want to use) Claude Code in that work.

This is **not** a public resource. The content references MMF projects, funders, and internal workflows, and assumes you have context from working with Simon.

## Quick start

**If you want the philosophy and the big picture first:**
Read [`getting-started/00-how-simon-ais.md`](./getting-started/00-how-simon-ais.md). It's the overview — how the whole setup fits together, why it looks the way it does, and which pieces you can adopt without the others. Roughly a ten-minute read. Most people will want to start here.

**If you've never used Claude Code and want to just install and go:**
Start with [`getting-started/01-install-claude-code.md`](./getting-started/01-install-claude-code.md) and work through the numbered guides (01 → 04). You'll be using your first skill on a real task inside 30 minutes.

**If you know Claude Code and want to try a skill:**
Browse [`skills/`](./skills/). Each skill has a `SKILL.md` with a one-line description. Copy the ones you want into your own `~/.claude/skills/` directory — see [`getting-started/04-adopting-skills.md`](./getting-started/04-adopting-skills.md) for the two-command install.

**If you've written a skill you think others would find useful:**
See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the PR workflow. Small improvements welcome; large changes best discussed first.

## Repository map

```
mmf-claude-code/
├── getting-started/    Numbered onboarding guides — read in order if you're new
├── skills/             Installable Claude Code skills (one folder per skill)
├── guides/             Deeper-dive workflow docs — lab notebook, CMR, manuscript review
├── templates/          CLAUDE.md starters and a skill boilerplate
└── sync/               The script Simon uses to mirror his vault's skills into this repo
```

## The stack

This setup assumes:

- **[Claude Code](https://docs.claude.com/claude-code)** — the underlying tool, available as a desktop app or CLI. Skills are markdown files loaded from `~/.claude/skills/` and work identically in either.
- **[Obsidian](https://obsidian.md)** — where notes live. Most guides reference Obsidian workflows, but the skills themselves don't require it.
- **[Codex CLI](https://github.com/openai/codex)** (optional) — ChatGPT's equivalent, useful for a second-opinion peer review from inside Claude Code. `/red-team` uses it when available.
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** (optional) — free for 1,000 requests/day. Used as a third reviewer by `/red-team`.

Individual skills document their own dependencies in their `SKILL.md`.

## Living repo disclaimer

This repository mirrors a real, evolving setup. Things change. If a skill looks out of step with how Simon's actually working, or a guide references a command that's been renamed, open an issue or PR — that's how we keep it current.

## Licence

- **Code** (scripts, skills, hook configs): [MIT](./LICENSE).
- **Prose** (guides, README, templates): [CC-BY-4.0](./LICENSE-CC-BY-4.0).

Private repository; licence terms apply in the event that content is later extracted and shared externally.
