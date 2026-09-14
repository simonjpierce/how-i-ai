# Reference — When a rule should be code

> **What this is.** The actual method behind [the *When a rule should be code* workflow](../workflows/when-a-rule-should-be-code.md), cleaned of the maintainer's personal specifics. A **starting point to adapt, not a drop-in** — hook event names and output fields are the harness's and change; check current Claude Code documentation for the exact field names before building.
>
> A **hook** is a script Claude Code runs at a fixed moment. The events used here: `PreToolUse` (before a tool call — can block), `PostToolUse` (after), `UserPromptSubmit` (when you send a message), `SessionStart` (with an optional matcher for post-compaction), `PreCompact`, `Stop` (when the model ends its turn — can block the turn and demand more). Each is registered in `settings.json` with an optional tool matcher (`Bash`, `Read`, `Write|Edit`).

## The decision: prose or code

| Sign | Verdict |
|---|---|
| The rule needs context to apply (tone, priority, who's involved) | Prose — instructions, memory |
| The rule has fired as friction 3+ times despite being written down | Code |
| The rule must reach scheduled jobs or subagents that don't load your instruction files | Code |
| The action would fail anyway and only the error message is bad | Code — a *block* that names the fix |
| The action is legitimate but wasteful | Code — a *warn* |
| You're about to reword a rule for the second time | Stop; measure; probably code |

The evidence that settled this for the maintainer, from a weekly fix-efficacy table: one week, four fixes — the one code fix cut its class 57%; all three prose fixes were flat or worse (one class 5 → 13 a week). Repeated for memory-file overflow (prose: file grew 190 → 193 lines in a night; hook: trend reversed), symlink writes (three months of prose moved 10 → 7 a week; a hook made the next attempt correct first time), and read scoping.

## Anatomy of a hook

Every hook the maintainer keeps has the same skeleton:

```bash
#!/bin/bash
# <name>.sh — one line: what it prevents.
#
# WHY THIS IS CODE AND NOT PROSE: the failure, the prose attempts and what they
# measured, the date.
# WARN or BLOCK, and why.
# FAIL-OPEN CONTRACT: which internal errors exit 0 silently.
# MEASUREMENT TARGET: <class> below <n>/week at the next review.

# Optional gate: skip on any machine that isn't the maintainer's
# (so the config can be shared without dragging personal hooks along).
command -v jq >/dev/null 2>&1 || exit 0
input=$(cat) || exit 0
# ... parse tool_input from the JSON on stdin; inspect; decide ...
exit 0
```

Rules the skeleton encodes:

- **Fail open.** Missing `jq`/`python3`, unparseable stdin, a path that doesn't exist, a symlink that won't resolve — all exit 0 with no output. A guard must never turn "file absent" into a warning that reads like "file too large".
- **Parse, don't grep.** Read `tool_input.command` / `tool_input.file_path` from the JSON; tokenise shell commands with `shlex` rather than regex on the raw string, and skip heredocs and command substitutions (they're targeted by construction).
- **Heredoc trap.** If the Python body arrives via `<<'PY'`, the hook JSON must travel in an environment variable — piping it is silently shadowed by the heredoc. The maintainer's first read-guard blocked nothing for exactly this reason.

## Warn versus block

- **Block (exit 2, message on stderr)** when: the action would fail regardless (a write through a symlink, an over-cap memory write); or the harm is real and hard to undo (a recursive delete on an unenumerated folder, a commit on the wrong branch, sending an email). The message **must** contain the exact corrected call: *"retry with `limit: 500, offset: 0`"*, *"the real path is …"*. Test: an unattended run that hits this block loses one tool call and continues.
- **Warn (exit 0 plus model-facing context)** for the legitimate-but-costly: unbounded `cat`, `git diff` without `--stat`, a path that should be quoted. A week of warnings changes the habit; a block here would strand overnight work.
- **Re-check the block when the harness changes.** One block (a `cd` into the working folder, guarding against the shell directory leaking into later calls) became pure cost when the harness started resetting the directory after every call: 348 fires in 14 days, all false. The ledger surfaced it; it was downgraded to a warn the same day.

## The model-facing channel

A `PreToolUse` hook that `echo`s and exits 0 writes to the *terminal*, which the model never reads. Verified both ways in one session: the correct message appeared on stdout in a manual test, and the real run showed the error with no hook message attached. Ten hooks had fired ~150 times a week into that dead channel, and three fix-efficacy entries had been scored against advice that was never delivered.

Use the structured output — currently `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "…"}}` on stdout — for anything a *warn* wants the model to see. Blocks (exit 2 + stderr) already reach the model and need no conversion. Put the envelope in one shared `warn.sh` helper so every hook uses the same shape, and note in each converted hook that its earlier measurements were against undelivered advice.

## The firing ledger

A transparent wrapper, registered in `settings.json` as `lib/ledger-run.sh <hook>`: passes stdin/stdout/stderr and the exit code through unchanged, and on top

- appends one byte per *silent* fire to `state/firing-counts-YYYY-MM/<hook>` (a builtin redirect, no extra process);
- appends one TSV line per *non-silent* fire to `state/firing-ledger-YYYY-MM.tsv`: timestamp, event, hook, outcome (`block` / `warn` / `out` / `error`), exit code, session, tool, excerpt.

Best-effort throughout: if the ledger can't write, the hook still runs and its result is still relayed. A small report script answers "which hooks have blocked anything in 30 days?" — the question that lets you prune. Don't wrap hooks that speak unconditionally (session-start context) or only notify; their firing tells a pruning pass nothing.

## Testing the hooks

- `hooks/tests/test-<hook>.sh`: feed the hook crafted JSON inputs (the shape that should block, the shape that should pass, malformed input) and assert exit code and output.
- A **meta-hook** on `PostToolUse` for `Edit|Write`, filtered to files under the hooks directory, runs that hook's tests immediately after it's edited — so a broken guard is caught in the session that broke it, not overnight.
- A **stop-time check** (`Stop` event) that reads the model's final message for a claimed workaround with no fix applied, and blocks once asking for the fix. Same idea pointed at the *habit* of fixing the source.

## Hooks the maintainer runs, by event (for shape, not to copy)

- `SessionStart`: print the latest handoff entry + a fast health pre-flight; on the `compact` matcher, re-inject the handoff.
- `UserPromptSubmit`: context-size nudge at 300k tokens; standing per-prompt reminders.
- `PreToolUse Bash`: secrets in a commit; stash guard; path quoting; push-suppression guard; email-send guard; recursive-delete enumeration; commit-branch check; unbounded read block; output hygiene.
- `PreToolUse Read`: unbounded read of 500+ lines → block with two exits.
- `PreToolUse Write|Edit`: memory-file size cap (warn 94%, deny 99%); symlink redirect; path check for files that belong in the notes vault.
- `PostToolUse Edit|Write`: link check, frontmatter check, Python syntax check, hook-test runner.
- `PreCompact` / `Stop`: save reminder; workaround check; verification check; open-loop path check.

## What stays yours

Which rules you promote, the thresholds, whether you gate personal hooks so the config can be shared, and how much test scaffolding you want. The transferable spine: *measure before promoting; fail open; block only with the fix in the message; speak on the channel the model reads; write the why and a target in the header; keep a ledger so you can prune.*
