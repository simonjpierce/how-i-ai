# Managing your token budget

A set of habits and small automations that let you run an AI system all day, every day, on a fixed subscription — without the quota running out on Thursday and without the AI quietly getting slower and vaguer as its working memory fills up.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Every subscription plan has a ceiling on how much the AI can read and write in a week. Once you use an agent seriously — long sessions, scheduled jobs overnight, a fleet of specialists — you hit it. The instinct is to blame the big jobs. The maintainer's measurements said otherwise: **the cost of a session grows with its context size multiplied by the number of turns**, because on every single turn the AI re-reads *everything* already in the conversation — the instruction files, the loaded skills, every file it opened, every command's output. In one measured week, 95% of all tokens were those re-reads. A session that ran all day at a large context cost more than the whole overnight fleet.

So the lever is not "do less". It is **keep the working memory small, and keep it small for fewer turns**. Everything below is one of three moves: *see* how full the context is; *keep bulk out* of it in the first place; and *reset* it deliberately, without losing the work, once it gets big.

## The pieces

- **See it.** A one-line status bar under the terminal shows the model and how full the context is (`Context: 42% used`). Nothing changes behaviour like a number you can see. The desktop app has the same thing as a ring next to the model picker.
- **Get nudged at the line.** A small hook watches the context size on each message. When it crosses a threshold (the maintainer uses 400k tokens, then again every 100k), it tells the AI — not you — to raise it at the next pause: one line, "Context is over 40%. Save and reset now? 1. Yes 2. Not yet". You answer with a keystroke. The AI carries the reminder so it fires in the moment, every time; you keep the decision, because sometimes you are three replies from closing the session and a save-and-reset in the middle is exactly wrong.
- **Save, then reset — one command.** The reset is compaction: the conversation is summarised to free room. Compaction alone loses detail, so pair it with the save step from [the session loop](./the-session-loop.md): a mid-session checkpoint command writes the handoff note and the logs, then hands back the compaction command ready to run. One keystroke, nothing lost, and every turn after it costs roughly a third of what it did. The maintainer measured a reset from ~430k tokens of context to ~110k. A separate hook re-injects the latest handoff after compaction so the AI picks up exactly where it was.
- **Keep bulk out: don't read long files whole.** Reading a 2,000-line transcript into the conversation is not thinking, it's plumbing — and it then gets re-read on every later turn. A hook blocks any unbounded read of a long file (500+ lines, whether via the file tool or `cat` in the shell) and offers two exits: a cheap, fast model (Sonnet) reads the file and returns a dense answer to the question, or the main model reads a bounded slice for edits and quotes. The same idea covers command output: a warning fires on a bare `git diff`, a full test run without `-q`, a recursive directory listing — anything whose output would land whole in the context and stay there.
- **Slim what loads every turn.** Skills (your saved commands) are re-read on every turn while they're active, and the *catalogue* of skill names and descriptions is in every turn regardless. The maintainer cut five large skills by 50–85% — mostly by moving the history out (see [Clearing clutter from your workflows](./clearing-clutter-from-your-workflows.md)) and by *tiering*: a two-mode skill loads only the mode in use, so a morning-coaching session carries 12k tokens of instructions instead of 34k. Shortening 54 skill descriptions halved the catalogue. And the always-loaded memory file has a hard size cap enforced by a hook at write time, because over-cap content silently doesn't load.
- **Right model for the job.** Your top model orchestrates, judges and writes. Bulk reading, file summarising and routine extraction go to a fast, cheap model in a subagent. A second provider's command-line model (the maintainer uses OpenAI's Codex CLI) runs on a *separate* quota, so review passes and autonomous builds cost nothing from the main pool. Watch one trap: subagents inherit the main session's model unless told otherwise, so a "cheap" helper is only cheap if you say so.
- **Give unattended jobs a lighter start.** Every scheduled job pays a fixed entry cost before its first turn: system prompt, instruction files, hook output, the skill catalogue. Measured on the maintainer's setup: 62k tokens from the main working folder, 34k from a minimal folder with skills disabled — for a mechanical job that never invokes one. Hundreds of such runs a week made that the largest single saving found.
- **Stop files growing without bound.** The logs the system writes and reads most — decision log, daily log, handoff log — are rotated nightly: old entries move verbatim to archive files, an index line stays behind, and a byte-count check proves nothing was lost. Files that get *dense* (a project register with 600-character lines) trip the read guard too, because tokens follow characters, not line count.
- **Measure weekly, review monthly.** A weekly script (Saturday, just before the weekly system review) reads the AI's own session logs and reports the week's totals, the costliest sessions with their opening prompt, subagent overhead and cache ratios — plus which skills actually cost the most (body size × turns loaded, not just size) and whether the read guard is paying for itself. Once a month, a review session picks one layer of the system and asks what it produced against what it cost. That's where most of the above came from.

## How to build the display, the nudge and the save

The first three pieces work as one unit, and they are the ones to build first. Ask your AI to build each from the description below; all three are small. In Claude Code the display and the nudge are registered in the settings file (`~/.claude/settings.json`); the save is a custom command.

**1. The display (a status line).** Claude Code's `statusLine` setting runs a script every time the screen refreshes and shows the one line it prints under the prompt.

- The script receives a block of JSON. It needs three fields: `model.display_name`, `context_window.context_window_size`, and `context_window.current_usage` (add up its four token counts: input, cache creation, cache read and output).
- Print one line: `[Model] Context: 42% used | 58% remaining`.
- Change the wording as the room runs out. The maintainer's says `COMPACT SOON` under 30% remaining and `COMPACTING IMMINENTLY` under 15%.
- Before the first reply there is no usage yet, so print `Context: 0%`.
- In the desktop app, skip this: the usage ring beside the model picker shows the same number.

**2. The nudge (a hook on each message you send).** Register a script on the `UserPromptSubmit` event. It runs each time you send a message, and whatever it returns as `hookSpecificOutput.additionalContext` is read by the AI, not shown to you.

- The script is handed the path of the session's transcript file (`transcript_path`). Read only the end of that file (the last 400 KB is plenty), find the most recent reply's `usage` block, and add input, cache creation and cache read tokens. That sum is the current context size.
- Stop scanning if you reach a compaction marker (`isCompactSummary` or `compact_boundary`). Without that, the first message after a reset reports the old size.
- Keep a small state file per session holding the size at the last nudge. Fire once at the threshold, then only after each further step of growth. The maintainer uses 400,000 tokens (40% of a 1M window) and a 100,000 step.
- Word the message as an instruction to ask, not a fact to pass on: *"Context is about 440k tokens and every turn re-reads all of it. At the next pause, ask: 'Context is over 40%. Save and reset now? 1. Yes 2. Not yet'. Never run it unasked, and don't interrupt a task mid-step."*
- Make it fail quietly: on any error the script exits without output, so a broken nudge never blocks a message.

Two versions did not work. A nudge that only told the AI to *mention* the size was ignored for a week. One that ran the save automatically fired at the wrong moments. A question the AI must ask, answered with one keystroke, is the shape that held.

**3. The save (one command, then one paste).** Write a command for the mid-session save (the maintainer's is `/update`). It brings the notes for the current work up to date, writes the handoff entry described in [the session loop](./the-session-loop.md), and ends by printing a ready-made compaction line: `/compact Focus on <the current thread; re-read the handoff entry after compacting>`. You paste that line and the conversation shrinks, with the work already in files.

- Keep it lighter than your end-of-day close-out. The learning steps (reviewing what went wrong, tidying memory) belong to the goodbye, not to every save.
- Add a `SessionStart` hook with the matcher `compact` that prints the latest handoff entry back into the fresh conversation, so the AI picks up where it left off.

**Check it works.** Lower the threshold to something small, send a few messages, and confirm the AI asks the question once, then stays quiet until the context has grown by a full step. Say yes, run the save, paste the compaction line, and check that the display drops and the AI can tell you what it was doing.

## What this does *not* do

It doesn't make the AI do less work, and it isn't a length limit on anything. A skill that's long because its method is long stays long; a session that needs 400k of context for one hard problem gets it. The target is *waste*: bulk that entered the context and was never needed, history re-read a thousand times, a mechanical job carrying a scholar's briefing. Nor is it worth doing before you feel the ceiling — a person on an entry plan doing one task at a time needs none of it. And it isn't a substitute for the notes: the reason a reset is safe at all is that the work already lives in files, not in the conversation.

## Why this works

Because the cost is multiplicative, small fixed savings compound. Taking 20k tokens out of what loads every turn saves 20k *per turn*, across every turn of every session, forever. Blocking one long read saves its size on that turn and on every turn that follows it in that session. And a deliberate reset at 300k, rather than waiting for the automatic one near the ceiling, is the difference between an afternoon costing 400M tokens and 150M — for the same work. The measurement is what keeps the rest grounded: two of the maintainer's proposed savings turned out to be worth 3% and were deliberately not built.

## Note

This is a pattern, not a fixed toolkit. Your thresholds, which model counts as "cheap" on your plan, whether you build the hooks or just adopt the habits — all yours, and each piece stands alone. The durable idea is: *the AI re-reads everything on every turn, so watch the size, keep bulk out, and reset on purpose — with the work already written down so the reset costs you nothing.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/managing-your-token-budget.md) lays out the maintainer's real version — the hook shapes, the thresholds, the measurement scripts, and the things that didn't work — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
