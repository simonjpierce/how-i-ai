# Memory examples — Tier 1 and Tier 2 explained

This folder holds **example Tier 2 memory leaves** (`*.md.example`) plus this README. The README is documentation for contributors and curious users; it isn't installed into anyone's vault by `/onboard`. The `.example` files alongside it ARE installed (with the suffix kept, so they're dormant until a user renames them).

> *This file lives in the repo only. `/onboard`'s memory-examples copy rule matches `*.md.example` — a plain `README.md` doesn't propagate to per-project memory folders.*

## What auto-memory is

Auto-memory is a small set of markdown files that Claude Code reads automatically at the start of every session. They live at:

```
~/.claude/projects/<project-key>/memory/
```

The project key is the user's absolute vault path, sanitised with every non-alphanumeric character replaced by a hyphen. For `/Users/jane/Documents/My Vault` that's `-Users-jane-Documents-My-Vault`.

`/onboard` writes the starter `MEMORY.md` here, plus copies of the `.example` leaves from this folder.

## Two tiers, two purposes

The memory system has two layers, and the distinction matters:

### Tier 1 — always-on, inline in MEMORY.md

The top section of `MEMORY.md` (the file directly in the `memory/` folder). Loaded into context on every single session.

**What goes here**: rules that should fire regardless of task. Interaction style, response shape, filing conventions, hard guardrails. *"Number every question."* *"No .md files outside the vault."* *"Open new drafts in Obsidian automatically."*

**Budget**: the loader caps `MEMORY.md` at **200 lines / 25 KB**. Past that, the file is truncated silently — entries below the cutoff are invisible to Claude. Target ≤150 lines to preserve headroom. If Tier 1 is approaching the cap, move context-triggered rules out to Tier 2 leaves rather than compressing the always-on section past usefulness.

### Tier 2 — context-triggered, separate leaf files

Individual markdown files in the same `memory/` folder, indexed (one-line pointer each) at the bottom of `MEMORY.md`. **Not auto-loaded.** Claude reads them only when their trigger fires.

**What goes here**: rules that only matter in specific contexts. *"READ before drafting any email"*, *"READ before any meeting prep note"*, *"READ before work in the photography domain"*.

The index entry in `MEMORY.md` looks like this:

```markdown
- [Email drafting & voice](memory/feedback_email_voice.md) — **READ before drafting any email** or when receiving voice calibration edits.
```

When Claude is about to draft an email and sees that line in the index, it knows to Read the leaf before generating prose. The leaf itself can be long — there's no per-leaf size cap, only the always-on cap on `MEMORY.md`.

## When to use which

| Situation | Tier 1 or Tier 2? |
|---|---|
| Applies to *every* response (style, format, never-do rules) | Tier 1 |
| Applies only when a specific tool/skill/domain/file type is in play | Tier 2 |
| Applies always but is long (>5 lines of nuance) | Tier 2 with a Tier 1 pointer |
| Single-use note about a current task | Neither — use a vault file |
| Tracks system state that changes (active automations, pending reviews) | Neither — use a vault file |

The most common mistake is putting context-triggered rules in Tier 1 because they feel important. Important + context-specific = Tier 2 leaf. Tier 1 is for things that fire literally every session.

## The `.example` suffix

The two leaves shipped with `/onboard` (`feedback_email_voice.md.example` and `tool_quirks.md.example`) carry an `.example` suffix specifically to keep them dormant. Claude doesn't load files whose names end in `.example`; the indexing in `MEMORY.md` also doesn't point at the suffixed name.

To activate one, the user:

1. Edits the file's contents with their own real rules
2. Renames it to drop the `.example` (e.g. `feedback_email_voice.md.example` → `feedback_email_voice.md`)
3. Adds (or uncomments) the one-line pointer in `MEMORY.md`'s Tier 2 index

The suffix avoids the worst failure mode of starter scaffolding: example placeholders being treated as live rules.

## Style guide for entries

Whatever tier:

- **Lead with the rule itself.** No preamble. *"Number every question 1., 2., 3."* not *"It's helpful to..."*.
- **Add a `**Why:**` line.** A one-sentence rationale, often a past incident or strong preference. Lets future-you (or future-Claude) judge edge cases instead of blindly following.
- **Add a `**How to apply:**` line.** When and where this rule kicks in. Tier 2 leaves often skip this if the trigger sentence already covers it.
- **Date breakthrough rules.** Optional but useful for the "Why" — "Confirmed 2026-05-17 after [incident]" is much more revisable than "Confirmed by experience."
- **Compress ruthlessly in Tier 1.** Every word costs context. Tier 2 leaves can breathe.

## File naming

Loose convention. The starter uses these prefixes:

- `feedback_*.md` — behavioural rules (do this, don't do that, voice calibration)
- `reference_*.md` — pointers to external systems (where Linear lives, what Grafana dashboard to check)
- `project_*.md` — context about ongoing work (active campaigns, current papers)
- `user_*.md` — facts about the user's role, preferences, knowledge
- `tool_*.md` — system quirks (the example `tool_quirks.md.example` covers this case)

These are loose. The important thing is the file's `description:` frontmatter field — that's what Claude scans to decide whether the leaf is relevant.

## How memory grows over time

The system is designed for incremental growth, not big-bang authoring:

1. You start with the seeded Tier 1 inline plus two example Tier 2 leaves.
2. As you correct Claude on something, Claude asks whether to remember it.
3. Always-on corrections → appended to Tier 1.
4. Context-triggered corrections → either added to an existing Tier 2 leaf, or a new leaf is created (with its index pointer in `MEMORY.md`).
5. When Tier 1 approaches the cap, you (or Claude during `/document` end-of-session) move the least-always-on rules to Tier 2 leaves.

Most users find the system stabilises around 100–150 lines of Tier 1 and a handful of Tier 2 leaves. The exact shape depends on what you do.

---

*See also: `~/.claude/CLAUDE.md` (global behavioural defaults) and `<vault>/CLAUDE.md` (vault-level identity and preferences). These three layers — global CLAUDE.md, vault CLAUDE.md, auto-memory — are the three layers Claude reads automatically every session.*
