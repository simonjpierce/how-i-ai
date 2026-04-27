# Contributing

This repo improves when the people using it contribute back. If a skill is missing, a guide is out of date, or you've built something the rest of us would find useful — open a PR.

## TL;DR

1. Branch off `main` (no forks needed — we all have repo access).
2. Make your change.
3. **Actually use it on a real task.** For a skill, run it by dropping the file into your own `~/.claude/skills/` and invoking it. For a guide, follow your own instructions from scratch.
4. Open a PR. Link the task output or describe what you tested.
5. Tag Simon for review (he's the primary reviewer for v1).

Small fixes land fast. Larger changes are worth a quick chat in Slack or on a call first so we don't end up with work that overlaps or doesn't land.

## How this repo stays in sync with Simon's local setup

For contributors, this mostly doesn't matter — direct merges to `main` work as you'd expect, including on `skills/`, `guides/`, and `templates/`. The detail worth knowing: Simon's local `~/.claude/skills/` is the working copy his Claude Code actually loads from, and it lives on his Mac rather than in this repo. After your PR merges, he runs `sync/sync-to-vault.sh --apply` (or `/update` does it automatically) to pull your change into his local copy. Git history credits you as PR author; the sync is bookkeeping.

If you want your own local `~/.claude/skills/` to stay current with merged PRs from other contributors, run `sync/sync-to-vault.sh --apply` from the repo root yourself; otherwise your local copies are whatever snapshot you cloned.

## What belongs here

**In scope:**
- Skills that work with our setup (Claude Code + Obsidian, optionally Codex/Gemini CLI).
- Process guides that explain how we work — lab notebook patterns, CMR workflows, manuscript review, literature intake.
- Templates (CLAUDE.md starters, skill boilerplates).
- Fixes to anything already in the repo: broken links, stale paths, incorrect commands.

**Out of scope:**
- Generic LLM advice or prompt engineering theory (plenty of good resources elsewhere).
- Obsidian plugin development or vault design — related, but a different repo.
- Personal workflows that don't transfer (Simon's exec-coach, nightly workhorse, morning briefings).
- Content that assumes private MMF information the repo hasn't established as shared context (check if unsure).

If you're not sure whether something belongs, open an issue describing it before doing the work.

## Adding or modifying a skill

A skill is a markdown file (`SKILL.md`) that Claude Code loads when invoked. The file has YAML frontmatter and a body.

**Frontmatter conventions:**

```yaml
---
name: skill-name
description: One-line description. When should Claude invoke this skill? Be specific about triggers — this is how Claude decides whether to use it.
---
```

- `name`: lowercase, hyphenated, matches the folder name.
- `description`: the single most important field. Claude reads this to decide whether the skill applies to the current task. Vague descriptions = the skill never fires. Describe the trigger (what Simon/the user says or does) as well as what the skill does.

**Body conventions:**

- Start with a one-paragraph summary of what the skill does.
- Step-by-step numbered instructions when there's a clear sequence.
- Plain English — instructions, not code blocks except where actual commands matter.
- Reference external dependencies explicitly (e.g. "requires `ffmpeg`", "requires Codex CLI").
- Include a short "When something goes wrong" section if failure modes are common — what to check first.

**Before you PR a skill:**

- Run it. Ideally on a real task, not a toy example.
- Include the output (or a link to a vault note containing the output) in the PR description.
- If the skill has a non-obvious failure mode you discovered while testing, add it to "When something goes wrong."

**Naming a new skill:** pick a verb or short phrase describing what it does (`transcribe`, `red-team`, `verify-citations`). Match the folder name to the `name` in frontmatter.

## Adding or modifying a guide

Guides live in `guides/` (and `getting-started/` for onboarding-sequence docs). A guide is a markdown explainer — longer than a skill, meant to be read rather than invoked.

- Write in NZ/UK English (organisation, behaviour, colour).
- Second person (you) rather than first-person plural (we) — it reads more directly.
- Assume the reader has Claude Code installed and working, unless the guide is in `getting-started/` and explicitly covers setup.
- Worked examples beat abstract instructions. Reference real MMF contexts where useful.
- If a guide points to external tools, link them once at first mention — don't bury the dependency.

**When to add a new guide vs. extend an existing one:**

- Extending: if the topic overlaps meaningfully with an existing guide (±30%), extend. Avoid fragmentation.
- New: if it's a genuinely different workflow, or the existing guide is already long enough that adding more hurts readability.

If unsure, ask in the PR description — a quick "should this be part of X or its own file?" is fine.

## Adding a template

Templates are starting points — something a new user copies and adapts, not something that works out of the box. Keep them minimal. Comment out or annotate sections that need customisation. Don't ship personal paths or credentials.

## PR conventions

**Branch naming:** `feature/<short-description>`, `fix/<short-description>`, `guide/<topic>`, or `skill/<skill-name>`. Lowercase, hyphenated.

**Commit messages:** present tense, descriptive. "Add transcribe skill" not "Added". One logical change per commit where reasonable.

**PR description — a minimum template:**

```
## What

<One or two sentences — what changes.>

## Why

<The motivation. What problem does this solve? What triggered it?>

## Tested by

<What you actually ran. Link a vault note with output if the test produced one.>
```

Keep the PR scoped. A PR that adds a skill AND refactors two others AND updates the README is three PRs in a trenchcoat.

## Review

- Simon is primary reviewer for v1.
- Small, obvious fixes (typos, broken links, one-line improvements): merge after one approval.
- New skills, guides, or larger changes: Simon reviews before merging.
- After you've had 3+ PRs accepted, you have merge rights on your own small fixes.

We're not doing formal CI or linting. Skills are markdown; the validation is a human reading them and, ideally, trying them.

## Opening an issue

Use issues for:

- "I want to propose X, worth doing?"
- "Y doesn't work for me, here's what I tried."
- "Should this live in the repo or not?"

Issues are cheap. Use them when you're unsure, before investing time in a PR that might not land.

## A note on private information

This is a private repo, but treat it as shared. Things to keep out:

- API keys, OAuth tokens, MCP credentials. Placeholders only in templates.
- Unpublished research data.
- Donor or partner information that hasn't been agreed to be shared with the collaborator set.
- Personal information about team members beyond what they'd share themselves.

If in doubt, leave it out. Easier than redacting later.
