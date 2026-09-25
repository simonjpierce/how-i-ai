# Clearing clutter from your workflows

A way to stop the commands you've built from slowly choking on their own history — so the one you reach for in six months is as crisp as the day you wrote it, instead of a wall of old notes the AI has to wade through to find the actual rule.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

There's a habit that makes a personal AI system get better over time: every time something goes wrong and you find a fix, you fix the relevant command straight away, so it never bites you twice. ([Growing your own capabilities](./growing-your-own-capabilities.md) is built on it.) The best form of that habit rewrites the step so it states the one best way now, rather than tacking a note on the end. But notes creep in anyway, and that has a cost that only shows up months later. Each is a little dated story: *"the PDF tool failed silently on 20 of 23 files on this date, so always check the output exists."* Useful the day you wrote it. But they pile up. A command that started as a clean page of instructions becomes a war diary, and the AI reading it has to push past a year of incident history to reach the three rules that actually matter today.

So the capture habit quietly runs up a debt. This workflow is the periodic repayment: every so often, take a command that's grown heavy and **distil it** — separate the live method from the accumulated history, keep the method crisp and in front, and move the history somewhere it's preserved but out of the way. The trick is doing that *without* dropping a rule that turned out to be load-bearing, which is where the safety check comes in.

## How it runs

- **Notice the costly ones.** You don't audit everything — most commands are fine. A weekly health check fixes the mechanical faults on the spot (a pointer to a file that's moved, a script that no longer exists) and ranks the commands by what they actually cost — how big each is times how often it's loaded — or by how much dated "learned this the hard way" material they've accreted relative to their actual instructions.
- **Sort the contents into layers.** Reading the bloated command, every line is one of a few things: the actual method (keep it, tighten it); a real rule that happens to be wrapped in a story ("*always check the output* — because that one time…" → keep the rule, drop the anecdote); pure history (a dated note with no live instruction — delete it, keeping one changelog line for the reason); or hyper-specific lore that only matters in one rare mode (move it to an appendix the command points to only when that mode comes up). The discipline is sorting at the level of individual sentences, because a single paragraph often mixes all four.
- **Delete the history; keep the reason.** Pure history comes out of the command — version control still has the old text if you ever need it. The changelog next to the command gets one line per change: what changed and why, never the old wording or the story. That one line is what stops a later session re-adding a rule that already failed. Niche lore moves to an appendix the command points to, so the body holds only what a fresh run needs.
- **Prove you didn't break it.** This is the part that makes the whole thing safe to do. Before the trimmed version replaces the original, an *independent* check confirms every operative rule still survives in the new body. The maintainer runs two passes: a mechanical one that checks every concrete command, path, and must/never line is still present byte-for-byte, and — the one that really matters — a second AI model (the Codex CLI) reading the old and new versions side by side, asked one question: *is there any rule in the old version whose behaviour is missing from the new one?* A changelog doesn't count as a home; the rule has to survive where it'll actually be read. If anything looks dropped, the missing rule goes back in and the checks run again; only a disagreement that needs a design or scope decision comes to a human. (This is the same second-model instinct as [the trust spine](./the-trust-spine.md), pointed at your own tools.)

## What this does *not* do

It isn't a bulk rewrite. It runs on a schedule — every fortnight the top-ranked command is slimmed, one at a time — and you don't approve each cut: the two-pass check is the gate, and only a real disagreement between the passes comes to you. (Starting out, reviewing each cut yourself is a sensible way to build trust in the check.) It also isn't a length limit: a command that's long because its *method* is genuinely big is fine and stays big. The target is history-per-instruction, not size. And it's explicitly the counterpart to the capture habit, not a replacement — you still write fixes in the moment; this is just the cleanup pass that habit never gives itself.

## Why this works

The capture habit is right at the moment of capture (you're mid-task, you just need it written down) and wrong as a long-term storage strategy (nobody curates as they go). Splitting those — capture cheaply now, distil deliberately later — lets each be good at its job. And the safety check is what makes it psychologically possible to prune at all: without an independent "you didn't drop anything" pass, trimming a command you rely on is nerve-wracking enough that most people just let it rot. The check turns a scary edit into a routine one.

## Note

This is a pattern, not a fixed pipeline. How you flag bloat, whether you keep a formal changelog or just a comment, whether you wire in a second model for the safety check or eyeball it — all yours, and all optional. The durable idea is: *the habit that keeps your tools sharp in the moment slowly dulls them over time, so give it a deliberate counterpart that prunes the history back out — with a check that proves nothing load-bearing went with it.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/clearing-clutter-from-your-workflows.md) lays out the maintainer's real version — the four-layer sort, the two-pass safety check, the bloat detector, the failure modes — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
