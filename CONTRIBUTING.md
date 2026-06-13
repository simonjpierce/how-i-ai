# Contributing

This repo is **descriptions, not code**: each file under `workflows/` describes one capability in plain language, detailed enough that someone's AI agent (Claude Code or Codex) can build that capability for them, adapted to their own setup. It deliberately doesn't ship finished skills — so contributing here means improving the *descriptions*, not adding implementations.

If a workflow is unclear, out of date, or missing a capability worth describing, open a PR.

## TL;DR

1. Branch off `main` (`workflow/<topic>` or `fix/<short-description>`, lowercase-hyphenated).
2. Make your change to a file under `workflows/` (or the README).
3. **Sanity-check it the right way:** paste the workflow into your own Claude Code or Codex and confirm it builds something sensible and adapted to your setup. The workflow's job is to be buildable from the description alone.
4. Open a PR describing what you changed and what you tested.
5. Tag Simon for review.

Small fixes land fast. For a larger change (a whole new workflow), a quick note first avoids overlap.

## What belongs here

**In scope:**
- New or improved **workflows** — plain-language descriptions of a capability that works with the stack (Claude Code or Codex + Obsidian, optionally Codex/Gemini CLI as a second model).
- Fixes to anything already here: unclear wording, stale references, broken links, a description that doesn't actually build.

**Out of scope:**
- Shipping finished skill files / code to copy — that's the thing this repo deliberately *doesn't* do.
- Generic LLM advice or prompt-engineering theory (covered well elsewhere).
- Highly personal workflows that don't transfer to others.
- Anything assuming private information not already established as shareable here.

If you're unsure whether something belongs, open an issue first.

## Writing a workflow

A workflow is a single markdown file under `workflows/`. It describes a capability so the reader's AI can build it.

- Follow the shape in [`workflows/_template.md`](./workflows/_template.md) and match the voice of [`workflows/the-science-workflow.md`](./workflows/the-science-workflow.md) (the exemplar): **openly AI-assisted, not written as Simon**; clear, warm, plain; jargon explained or avoided.
- The **whole document is the paste-able artifact** — there's no separate fenced "paste this" block.
- Keep enough concrete, buildable detail that the reader's agent can actually construct the capability (name the real tools/services/mechanisms) — but strip personal plumbing (exact flags, hardcoded paths, account specifics). Describe the *intent*, cleanly.
- Domain-agnostic where possible. Worked examples are welcome, but the pattern should transfer beyond any one field.
- NZ/UK English (organisation, behaviour, colour). Second person ("you"), not "we".
- Link external tools once, at first mention.

## PR conventions

- **Branches:** `workflow/<topic>`, `fix/<short-description>`. Lowercase, hyphenated.
- **Commits:** present tense, descriptive ("Add deep-research workflow", not "Added").
- **Keep PRs scoped** — one logical change.
- **PR description:** what changed, why, and how you sanity-checked it (ideally: "pasted into Claude Code, it built X").

Simon is the primary reviewer. Small obvious fixes can merge after one approval; new workflows get a review first. No formal CI — workflows are markdown, validated by a human reading them and trying them.

## A note on private information

Treat everything here as shareable — it's Simon's general approach to working with AI, and the repo may be opened more widely over time. Keep out:

- API keys, OAuth tokens, credentials.
- Unpublished research data.
- Donor, partner, or team-member information not already agreed to be shared.

If in doubt, leave it out — easier than redacting later.
