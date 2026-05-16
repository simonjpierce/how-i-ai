# Graduation

You've worked through the course. You have:

- Claude Desktop + Obsidian installed and connected.
- A personalised `CLAUDE.md` cascade describing who you are and how you work.
- The core skills under your belt: `/session-start`, `/document`, `/todo`, `/update`.
- Track-specific skills if you went through Part 2.
- At least one real piece of work done the new way.

That's the working system. **Everything below is optional** — pick what's useful when you want it, ignore the rest until the moment arrives. Don't try to adopt all of it at once.

## Optional skills (not in the course)

These ship in [`skills/`](../skills/) but didn't get a video lesson. Each has a `SKILL.md` describing what it does — browse when curious, install when needed.

- **`/mmf-brand`** — MMF brand identity (colours, typography, logos, layout) applied to any MMF-facing artefact. Useful if you produce MMF slides, posters, infographics, or donor materials.
- **`/polish`** — grammar and style checks via LanguageTool + Vale. Useful if you write a lot and want a second-pass mechanical proofread.
- **`/review-friction`** — walk through `[OPEN]` Friction Log entries one at a time. Run weekly when the list grows.
- **`/refresh-skills`** — pull contributor improvements from this repo into your local `~/.claude/`. Run occasionally to stay current.

## Deeper workflow guides

These live in [`guides/`](../guides/) — longer, less prescriptive, written for when you want to go deep on a specific kind of work:

- **`ai-assisted-writing.md`** — practical workflows for reports, manuscripts, and analyses.
- **`ai-assisted-scientific-writing.md`** — manuscript-focused. Deep research → outline → drafting → literature audit → citation verification → pre-submission review.
- **`ai-assisted-scientific-analysis.md`** — the lab-notebook discipline that `/science-paper` operationalises. **Required reading** before your first publishable analysis.
- **`literature-intake-and-integration.md`** — keeping a "living" reference library that's steadily enriched with new papers over time.
- **`research-workflow.md`** — three modes of research (deep / inline / automated) and when each fits.
- **`pre-submission-manuscript-review.md`** — a field-agnostic prompt template for thorough manuscript review.
- **`ghostty-setup.md`** — for the moment you want to graduate from the desktop app to a terminal-based workflow with hooks and automation.
- **`inviting-collaborators.md`** — Simon-facing; the flow for adding someone to this repo.

## Templates

[`templates/`](../templates/) holds starting points worth copying when relevant:

- **`starter-claude-config/`** — what `/onboard` writes during install. Useful to read if you're curious about defaults; useful to copy from if you want to reset.
- **`starter-vault/`** — a minimal vault layout you can use as a reference for organising your own.

## Building your own skills

The most powerful thing you can do with this system is **make it yours.**

The next time you walk through a workflow with Claude and you know you'll repeat it, ask:

> *"Make this a skill."*

Claude will write the `SKILL.md` for you, asking what to call it and when it should be invoked. The skill drops into `~/.claude/skills/` and is yours from then on. If it's useful to the rest of the team, open a PR adding it to this repo's `skills/` folder — see [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Hooks and automations

The next layer down is *deep* — Claude Code running on a schedule, hooks firing on events, the system maintaining itself overnight. Out of scope for v1 of this repo; ask Simon directly when you're curious.

## Feedback

The course gets better when it gets used. If a lesson didn't land, an example was confusing, a video was too short or too long, or a step felt obvious-to-Simon-but-not-to-you — open an issue or PR. Small fixes land fast.

The course is also a living document — as the underlying skills evolve, the lessons that cover them follow. When a skill changes substantively, its lesson should change too. That sweep usually happens after the next `/refresh-skills` run.
