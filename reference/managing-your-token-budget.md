# Reference — Managing your token budget

> **What this is.** The actual method behind [the *Managing your token budget* workflow](../workflows/managing-your-token-budget.md), cleaned of the maintainer's personal specifics (real paths, names, machine state). It's a **starting point to adapt, not a drop-in** — your plan, your models and your session shapes differ, so read it *with* your AI and build the version that fits. The workflow says *why*; this says *how*, concretely enough that your agent doesn't have to rediscover the numbers.
>
> Terms used throughout: the **context** is everything the AI holds for one conversation and re-reads on every turn. A **hook** is a small script Claude Code runs automatically at a fixed moment (before a tool call, when you send a message, before compaction). **Tokens** are the unit the quota is counted in; roughly 3.5–4 characters each for English text.

## The cost model — measure this first

Before building anything, get the picture from your own session logs. Claude Code keeps every session as a JSONL transcript under `~/.claude/projects/`, and every assistant message carries a `usage` block: `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`. Sum them per session and you have the bill.

What the maintainer's numbers looked like when this work started, one week:

| Measure | Value |
|---|---|
| Total tokens | 5.5 billion |
| Of which cache re-reads | 95% |
| Costliest single session | 486M (ran all day at 400k+ context) |
| Fixed context before the first turn, interactive | ~14k of standing instructions + ~11k skill catalogue + hook output |

Three conclusions fall out and drive everything below: cost ≈ **context size × turns**; the **fixed per-turn load** (instructions, skills, catalogue) is paid on every turn of every session; and **one long session** at high context outweighs the whole scheduled fleet.

Build a **weekly report** from those transcripts and schedule it (the maintainer's runs Saturday 00:30, just before the weekly system review, adapted from a public gist, `kieranklaassen/claude-token-usage`). Report: totals by project; the ten costliest sessions, each with its first prompt so you can tell what it was; subagent count and tokens per session; cache ratios. Add two sections of your own once the mechanisms below exist: **skill carry cost** — for each skill, body size × number of turns it was loaded, over 14 days (this ranking, not raw size, found the real offenders: a 30k-token close-out skill loaded for 11,000 turns because a save command invoked it every time); and **read-guard savings** — tokens the blocked reads would have added, minus what the cheap-model reads cost.

## Layer 1 — see it

**Status line.** Claude Code's `statusLine` setting runs a script on every refresh and shows its one line of output under the prompt. The input JSON includes `model.display_name`, `context_window.context_window_size` and `context_window.current_usage` (sum its four token fields). Print `[Model] Task | Context: 42% used | 58% remaining`, switching the wording to `COMPACT SOON` under 30% remaining and `COMPACTING IMMINENTLY` under 15%. Optional: read a short task label from a per-terminal file so the line also says what the session is doing. In the desktop app the usage ring does the same job; skip this layer there.

**The nudge hook** (`UserPromptSubmit` event). Each time you send a message the hook receives `transcript_path`. Read the *tail* of that file (the last ~400KB is plenty), find the most recent assistant `usage` block, sum input + cache creation + cache read — that's the current context size. Two guards: stop scanning at a compaction-boundary record (`isCompactSummary` / `compact_boundary`), or the first message after a compaction reports the *old* size; and keep a per-session state file so the nudge fires once at the threshold and then only every step of further growth, not every message. Output `hookSpecificOutput.additionalContext` — text the *model* reads, not you.

Maintainer's settings: threshold 300k, step 100k. The message is an instruction to ask, not information to relay: *"Context is ~340k tokens and every turn re-reads all of it. At the next pause ask — never auto-run — with a one-key option: 'Context is over 30%. Run the checkpoint now? 1. Yes 2. Not yet'. On 1, run it and hand back the compaction command. Do not interrupt a task mid-step for this."* The purely advisory version ("mention this once") was measured for a week and did nothing — 59 of 97 sessions crossed 300k and ran a median 158 more turns; 17 compacted. An auto-run version fixed that but fired at the wrong moments too: the maintainer hit it while wrapping up a thread that was about to get a full close-out anyway, and pulled it back to a question. The working shape is: the model must ask, every time, with an answer that costs one keystroke; the human decides. Fail-open: any error in the hook exits 0 silently.

## Layer 2 — reset on purpose, without losing anything

Compaction summarises the conversation; what it drops is conversation detail, what survives is files. So a reset is only safe *after* a save. Wire it as one command:

- **A checkpoint command** (the maintainer's is `/update`): writes the session handoff note (what was done, what's next, working files), flushes decision and friction logs, updates any process docs touched — then prints a ready-to-paste `/compact Focus on <the current thread>`. The human presses it. See [the session loop reference](./the-session-loop.md) for what the handoff note holds.
- **A goodbye command** (`/document`) is separate and heavier — it runs only when a session actually ends. The maintainer found the close-out ran six times a day at 250–400k context, mostly as mid-session saves; splitting checkpoint from goodbye, and moving the heavy learning steps (friction scan, memory distillation, skill-candidate review) to *one* nightly pass over the day's transcripts, removed most of that cost.
- **Two compaction hooks.** `PreCompact` (trigger `auto`): remind the model that if in-flight work matters, run the checkpoint first. `SessionStart` with matcher `compact`: print the latest handoff entry back into the fresh context, with "re-read any working files named above before continuing".

Measured effect of a deliberate reset: ~430k → ~110k context; every following turn roughly 70% cheaper.

## Layer 3 — keep bulk out

**The read guard** (`PreToolUse` on `Read`, and a twin on `Bash`). Deny (exit 2) an *unbounded* read of a file of 500+ lines. "Unbounded" means the file tool with no `limit`, or `cat`/`less`/`more`/`head -n 5000` with nothing downstream. Pass anything targeted: a pipeline (`cat f | grep`), `head`/`tail` at default length, `sed -n 'X,Yp'`, paths inside your skills/hooks/agents folders, and anything the parser can't resolve to a real file (fail-open). The denial message is never a dead end — it carries both exits verbatim:

1. *For understanding the file against a question:* dispatch the **bulk-reader** subagent (below).
2. *For editing or quoting:* retry with `limit: 500, offset: 0` and page.

Two more tiers below the block, warn-only: a byte cap (the tool's own 256KB limit) and a **density** trigger — files over ~400 bytes per line and ~75KB, which sail under a line count and still blow the token cap. Log every block (`timestamp, lines, bytes, path, tool`) to a ledger so the weekly report can price the saving.

This was the class where documentation demonstrably failed: two prose rules about scoping reads made the failure count go *up* (5 → 13 a week) while a single hook halved its class. The lesson generalises — a rule that must reach unattended sessions and subagents has to be code in the execution path, not advice in a file they may not load.

**The bulk-reader subagent.** A subagent definition with `model: sonnet` and a short system prompt: read the listed files in full (paging if needed), answer only the question asked, structured bullets led by an exact anchor (heading, field, date, line), no preamble, flag line numbers as approximate, and end with a "tool/approach failures" section so the parent can fix its instructions. Dispatched with the question, not with "summarise this". Do **not** send it edits, debugging, safety judgements or anything where exact wording matters. The pattern is Spotify Engineering's "shunt" plugin (September 2026), which reported ~90% token reduction on the same idea.

**Output hygiene** (`PreToolUse` on `Bash`, warn-only). Flag shapes whose output lands whole and stays: `git diff`/`git show` without `--stat`/`--name-only`/a path; `git log` without `-n`/`--oneline`; `pytest` without `-q` or a trailing `| tail`; `ls -R`, `tree`, `find <dir>` without `-name`/`-maxdepth`; `cat <file>` piped to anything that isn't a filter. Warn, don't block: these are legitimate; the aim is to train the bounded habit, which a week of warnings does.

## Layer 4 — slim the fixed load

Everything here is paid on every turn, so small cuts compound.

- **Distil bloated skills** — the method is [Clearing clutter from your workflows](./clearing-clutter-from-your-workflows.md). Clause-level distillation alone gave ~10% on the maintainer's largest skills.
- **Tier two-mode skills by phase.** This gave ~70%. A daily-planning skill had a *build the briefing* mode and a *coach through it* mode; the body kept only the shared spine (~5k tokens) and each phase moved to its own file, loaded only when that phase runs. Same shape for a close-out skill (checkpoint path in the body, full goodbye in an appendix) and a weekly review (source index in the body, sources in an appendix). Rule for what may move: a rule may live in an appendix only if the body carries a pointer *at the point that mode begins* — otherwise it's lost, not tiered. Results across six skills: 34k→5k, 34k→17k, 30k→10k, 39k→17k, 32k→23k, 16k→9k.
- **Shorten skill descriptions.** The catalogue of every skill's `description:` is injected into every turn of every session. Cutting 54 descriptions to one tight sentence each took the catalogue from 9.4k to 4.8k tokens. Keep the trigger phrases (they're what routing keys on), drop the history.
- **Cap the always-loaded memory file at write time.** Claude Code's auto-memory index has a hard ceiling (200 lines / 25,000 characters at the time of writing); over-cap content silently fails to load. A `PreToolUse` hook on `Write|Edit` warns at ~94% and denies at ~99% with a concrete "move this to a topic leaf and leave a one-line pointer" instruction. Tiering applies here too: the index holds one-line pointers; detail lives in leaf files loaded only when their trigger fires.
- **Know when to stop.** The maintainer measured a distillation pass over the standing-instruction files themselves: 3% saving. Not installed — the files are dense operative rules, and a 3% gain didn't justify touching the AI's core instructions unreviewed. Record the negative result so the idea isn't re-proposed monthly.

## Layer 5 — right model, right entry cost

- **Routing.** The top model orchestrates: judgement, voice, final calls. A fast cheap model takes bulk reads and extraction (the bulk-reader). A second provider's CLI model — the maintainer uses OpenAI's Codex — takes review passes, code builds and autonomous overnight work on its *own* weekly quota (its effort paced automatically — high by default, stepped down only while the week's usage runs ahead of pace — because that quota runs out too). Mid-tier models review and run background subagents. The trap: a `general-purpose` subagent inherits the session's model. If you want cheap, say `model: sonnet` in the agent definition.
- **A lighter start for mechanical jobs.** Every `claude -p` run pays the working folder's instruction cascade, the skill catalogue and all hook output before its first turn. Measured on a single-turn Sonnet probe: 62k tokens from the main vault root; 45k from a minimal folder (a 15-line instruction file: where the vault is, path hygiene, spelling) with the vault attached by `--add-dir`; 34k adding `--disable-slash-commands`. Note `--add-dir` does *not* load the attached folder's instruction files — so this is only for jobs that need none of them, and any job whose prompt relies on vault-relative paths or edits prose a human reads stays on the full cascade. At ~440 unattended runs in 36 hours, median 55k context and 20 turns each, this was the largest single saving in the review that found it.

## Layer 6 — stop files growing without bound

The files the system reads most are the ones it appends to most. A nightly **rotation** job moves old entries out of the live decision log, daily log and handoff log into dated archive shards (capped at 1.5MB each so they don't trip commit-size guards), leaves an index/count line behind, and asserts *characters moved == characters removed* before the live file is committed — shards are written first, so a crash can only duplicate, never lose. A write-time guard caps the one register that is read by every planning session. And the density tier of the read guard (above) catches the file that stays short in lines but grows wide.

## Layer 7 — the review loop

- **Weekly**: the token report above, on a schedule, into your notes.
- **Monthly**: a review session that takes *one* layer of the system (the scheduled loops; the agents; the interactive session) and asks of each piece what it produced against what it cost, using the report and a first-turn-context measurement (parse the first assistant `usage` block per session; split scheduled from interactive). The maintainer's two such reviews closed nine substantive items in a day, including the lighter-start finding. It stays a session a human runs, not another report generator — "machinery that maintains machinery" was itself a finding.
- **Occasionally**: run an external skill-quality check over your own skills. Anthropic's public `skill-creator` skill evaluated 57 of the maintainer's and found real defects in 30 (a verify step writing one path and reading another; a skill pointing at an absent browser). Not a token measure directly, but broken skills burn turns.

## What didn't work, so you can skip it

- **Advice instead of code**, for anything that must reach unattended sessions: measured at zero or negative effect three times (read scoping, memory-file size, symlink writes). Hooks halved their classes each time.
- **An advisory nudge** the human is expected to act on: ignored. Make the model carry the rule.
- **Distilling the standing instructions**: 3%. Left alone.
- **Treating a second frontier model as the "cheap" tier**: it isn't cheap, it's *separate*. Only a genuinely smaller model reduces spend; a peer model on another quota adds capacity.

## What stays yours

Thresholds (300k/100k, 500 lines, 400 bytes/line), which model is cheap on your plan, whether you build every hook or adopt the habits by hand, how much rotation your logs need — all adapt to your setup. The transferable spine: *measure from your own transcripts first; make the size visible; put the "reset now" rule in the model's context rather than your memory; block bulk reads and route them to a cheap model; tier what loads every turn; give mechanical jobs a light start; and review one layer a month against what it actually produced.*
