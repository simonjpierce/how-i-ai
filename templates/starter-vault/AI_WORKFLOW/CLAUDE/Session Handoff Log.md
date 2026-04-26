# Session Handoff Log

When a session ends with work in progress, append an entry here. The next session reads this first to pick up where you left off.

The `/document` skill writes these entries automatically. You generally don't write them by hand — but you can edit them after the fact if something was missed.

## Format

```
## YYYY-MM-DD — One-line summary of what happened
<!-- session:short-tag -->

**Framing:** What kicked off the session — the problem you were solving, the
context you walked in with.

**What was done:**
1. First substantive thing.
2. Second.
3. ...

**Current state:** Complete / In progress (next step: ...) / Blocked on (...)

**Follow-up on prior "What's next":** Open threads from previous sessions —
acknowledge what was and wasn't picked up.

**What's next:** Open threads going forward — what to tackle next session.
```

The HTML comment `<!-- session:tag -->` is for grep — short identifying tag, kebab-case, helps find related entries later.

---

<!-- EXAMPLE ENTRY — delete when adding your first real one -->

## 1970-01-01 — Example: ran first /onboard, set up vault and three domain folders
<!-- session:onboard-install -->

**Framing:** First-time setup. New to Claude Code. Walked through `/onboard` from the README's three-step prompt; aim was a working vault with cascade and skills wired up.

**What was done:**
1. Installed Claude Desktop, signed in (Pro plan), opened Claude Code.
2. Ran the discovery interview — six questions, ~12 minutes.
3. Vault created at `~/Documents/Obsidian Vault`. Root CLAUDE.md and Getting Started.md written.
4. Opted into the domain-folder pass — three folders created with their own CLAUDE.md each.
5. Scheduled the self-improvement loop follow-up for two weeks out.

**Current state:** Complete. System ready to use.

**Follow-up on prior "What's next":** N/A (first session).

**What's next:** Try `/transcribe` on a real meeting recording. Add at least one entry to Decision Log this week. Run `/review-friction` next Sunday.
