 # Contributing

This repo improves when the people using it contribute back. If a skill is missing, a guide is out of date, or you've built something the rest of us would find useful — open a PR.

## Two kinds of PR

The content under `skills/`, `guides/`, and `templates/` is **mirrored** from Simon's vault and `~/.claude/skills/` by `sync/sync-from-vault.sh`. That script fully replaces those directories on each run — so any change merged into them directly would be overwritten by the next sync.

- **Proposal PRs** — changes to files under `skills/`, `guides/`, or `templates/`. These are reviewed like any PR, but if accepted, they are **closed (not merged)**: Simon applies the approved change to the canonical vault/`~/.claude/` source, and the next `sync-from-vault.sh --commit` run brings it into the repo. You'll see your contribution appear on `main` shortly after acceptance, via a sync commit rather than a merge commit.
- **Direct-merge PRs** — changes to anything else (README, CONTRIBUTING, the sync script itself, top-level `LICENSE`, `.gitignore`). These merge normally.

Tell the two apart by where the file lives. If unsure, flag it in the PR description.

## TL;DR

1. Branch off `main` (no forks needed — we all have repo access).
2. Make your change.
3. **Actually use it on a real task.** For a skill, run it by dropping the file into your own `~/.claude/skills/` and invoking it. For a guide, follow your own instructions from scratch.
4. Open a PR. Link the task output or describe what you tested. Note in the description whether this is a Proposal PR or a Direct-merge PR.
5. Tag Simon for review (he's the primary reviewer for v1).

Small direct-merge fixes land fast. Larger proposal PRs or workflow changes are worth a quick chat in Slack or on a call first so we don't end up with work that overlaps or doesn't land.

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
- Small, obvious direct-merge fixes (typos, broken links, one-line README improvements): merge after one approval.
- New skills or guides (proposal PRs): Simon reviews. If accepted, he applies the change to his vault/`~/.claude/` and closes the PR as "landed via sync" — the content appears on `main` on the next `sync-from-vault.sh --commit` run.
- After you've had 3+ PRs accepted (direct-merge or landed-via-sync), you have merge rights on your own small direct-merge fixes.

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
