# Decision Log

Non-obvious choices that a future session might revisit — design decisions, scope choices, technical trade-offs. Routine or settled decisions belong somewhere else (or nowhere); this file is for the ones future-you (or future-Claude) might want to reconsider.

The `/document` and `/update` skills write entries here when decisions emerge during a session. You can also add entries by hand.

## Format

```
### YYYY-MM-DD: One-line summary of the decision

**Decision:** What was decided — concrete, specific.

**Why:** The rationale. Mention alternatives considered and why they lost.

**How to apply:** When this pattern should be re-used in future situations.

**Cost if reversed:** Cheap / moderate / expensive — what it'd take to undo.

**Revisit trigger:** What signal would mean reconsidering this. ("n/a, stable
choice" is a fine answer.)

**Captured in:** Files where this decision actually shows up — for grep later.
```

---

<!-- EXAMPLE ENTRY — delete when adding your first real one -->

### 1970-01-01: Chose Claude Code in Claude Desktop over terminal CLI

**Decision:** Use Claude Code via the Claude Desktop app rather than installing the terminal CLI / Ghostty stack.

**Why:** Two paths considered. (a) Desktop app — one-click install, GUI familiar from Claude.ai, voice input, no terminal literacy required. (b) Terminal CLI in Ghostty — easier hook configuration, integration with shell tools, advanced tab/notification UX. For a first-time setup with no immediate need for hooks, the desktop path has lower friction without giving up anything Claude itself does. Skills, CLAUDE.md, memory all work identically across both.

**How to apply:** Default to desktop for new domains or new users. Reach for terminal CLI only when there's a specific advanced-feature need (hooks, shell-tool integration, scripting).

**Cost if reversed:** Cheap. Install Ghostty + the CLI; same vault, same skills, same memory carry over.

**Revisit trigger:** First time you actually want to wire up a hook (auto-commit, link-checker, tab-title daemon, etc.) — terminal CLI is the easier path for hooks.

**Captured in:** vault root CLAUDE.md (default-surface preference); README for `mmf-claude-code` repo.
