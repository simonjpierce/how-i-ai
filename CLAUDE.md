# how-i-ai — notes for the AI working in this repo

This is `CLAUDE.md` at the root of the `how-i-ai` repo (`github.com/simonjpierce/how-i-ai`). It's Simon Pierce's *"how I use AI"* system, shared so others can adapt it to their own work.

**The repo is descriptions, not code.** Each file under `workflows/` describes one capability in plain language — detailed enough that you (Claude Code or Codex) can *build* that capability for the reader, adapted to their setup. It deliberately does **not** ship finished skills to copy: real skill files accrete personal, brittle cruft that misfits someone else's work, so this repo ships the clean intent instead.

## If a user pasted the README (or a workflow) and asked for help setting up

The README is self-contained. Help them build *their own* version, adapted to their OS, their existing tools, and the work they actually do:

- Start with `workflows/00-the-philosophy.md` and `workflows/01-set-up-the-stack.md` (the on-ramp).
- Then whichever capability workflow they need — read it *with* them and build the skill/config to fit their work. The workflow is a brief you implement adaptively, not text to copy verbatim.
- **There are no skills to install from this repo — that's deliberate.** You build each capability from its description.
- **There's no starter template to copy either** — *create* the starter vault structure and a starter `CLAUDE.md`/`MEMORY.md` together with them, adapted to their work (the `01-set-up-the-stack` and `memory-and-context` workflows describe what to build).
- **Interview them — don't make them write.** Most newcomers fear they have to author all of this themselves; they don't. Ask questions and build the files *for* them from their answers. Invite voice answers (dictate into ChatGPT's chat box with the mic icon, then paste the transcript) in a loose stream-of-consciousness — reassure them they needn't be organised or careful about it — and ask follow-ups until you have enough context. Onboarding can take a while; that upfront context is what makes everything downstream work.
- **Check prerequisites and hand-hold the installs.** Several capabilities need external command-line tools (a local transcription engine, PDF extractors, a second AI model on the command line). Before building one, check what's already installed, install what's missing *for* them adapted to their OS (don't assume macOS), and flag the genuinely fiddly ones up front (compiling a transcription engine, an ML-based PDF extractor, a second model's separate account). Never leave a non-technical reader staring at a `command not found`. This guidance also lives in the README so it travels when only the link is pasted — keep the two in step.

## Structure

- `workflows/` — the capability descriptions (the whole point). On-ramp (`00-the-philosophy`, `01-set-up-the-stack`), one file per capability, three "advanced pattern" notes, and `how-it-all-fits-together` (the system map). `_template.md` is the house shape for authoring new ones.
- `README.md` — the front door (for humans and AI).

## Maintaining the repo

This repo is **hand-authored and maintained with plain git** — there is no vault→repo mirror or sync pipeline. (The old `sync/`-based mirror that copied `~/.claude/skills/` + vault process docs into the repo was retired 2026-06-02; see spec `2026-06-02-how-i-ai-mirror-decoupling` in Simon's vault.) The repo doubles as an Obsidian vault Simon edits directly (`.obsidian/` is gitignored), so changes are made in Obsidian or by an AI and pushed with ordinary `git add` / `git commit` / `git push origin main`.

**Public repo.** This repo is **public** under CC-BY-4.0 — treat everything in it as shareable. The git history was squashed to a single initial-release commit at launch (2026-06-13), so the changelog starts clean from public release; ordinary commits to `origin/main` from here are the public-facing change record. Don't commit anything you wouldn't want public — keys, unpublished data, anyone's private information (see `CONTRIBUTING.md`).

## Voice (for authoring or editing workflows)

Openly AI-assisted, clear, warm, plain. Audience: smart readers who aren't necessarily technical. Do **not** write as Simon (no first-person impersonation). Gloss or avoid jargon. Every workflow follows the shape in `workflows/_template.md`; match `workflows/the-science-workflow.md` as the exemplar.
