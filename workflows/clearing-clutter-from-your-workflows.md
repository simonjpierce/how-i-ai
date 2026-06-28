# Clearing clutter from your workflows

A way to stop the commands you've built from slowly choking on their own history — so the one you reach for in six months is as crisp as the day you wrote it, instead of a wall of old notes the AI has to wade through to find the actual rule.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

There's a habit that makes a personal AI system get better over time: every time something goes wrong and you find a fix, you write the fix straight into the relevant command, so it never bites you twice. ([Growing your own capabilities](./growing-your-own-capabilities.md) is built on it.) It's the right habit — but it has a cost that only shows up months later. Each of those fixes is a little dated story: *"the PDF tool failed silently on 20 of 23 files on this date, so always check the output exists."* Useful the day you wrote it. But they pile up. A command that started as a clean page of instructions becomes a war diary, and the AI reading it has to push past a year of incident history to reach the three rules that actually matter today.

So the capture habit quietly runs up a debt. This workflow is the periodic repayment: every so often, take a command that's grown heavy and **distil it** — separate the live method from the accumulated history, keep the method crisp and in front, and move the history somewhere it's preserved but out of the way. The trick is doing that *without* dropping a rule that turned out to be load-bearing, which is where the safety check comes in.

## How it runs

- **Notice the bloated ones.** You don't audit everything — most commands are fine. A light, periodic check flags the few that have grown past the point where their size starts to cost you: either they've simply gotten long, or they've accreted a lot of dated "learned this the hard way" notes relative to their actual instructions. That flag is a *suggestion to look*, never an automatic rewrite.
- **Sort the contents into layers.** Reading the bloated command, every line is one of a few things: the actual method (keep it, tighten it); a real rule that happens to be wrapped in a story ("*always check the output* — because that one time…" → keep the rule, drop the anecdote); pure history (a dated note with no live instruction — move it out); or hyper-specific lore that only matters in one rare mode (move it to an appendix the command points to only when that mode comes up). The discipline is sorting at the level of individual sentences, because a single paragraph often mixes all four.
- **Relocate, don't delete.** The history moves to a companion changelog file next to the command; the niche lore moves to an appendix. Nothing is lost — it's *moved*, so the command body holds only what a fresh run needs, and the provenance is still there if you ever need to ask "why is this rule here?"
- **Prove you didn't break it.** This is the part that makes the whole thing safe to do. Before the trimmed version replaces the original, an *independent* check confirms every operative rule still survives in the new body. The maintainer runs two passes: a mechanical one that checks every concrete command, path, and must/never line is still present byte-for-byte, and — the one that really matters — a second AI model (the Codex CLI) reading the old and new versions side by side, asked one question: *is there any rule in the old version whose behaviour is missing from the new one?* A changelog doesn't count as a home; the rule has to survive where it'll actually be read. If the two passes disagree, or anything looks dropped, it stops and asks a human. (This is the same second-model instinct as [the trust spine](./the-trust-spine.md), pointed at your own tools.)

## What this does *not* do

It does not run on its own. Distilling a command is a full rewrite of something the rest of your system depends on, so it's always a human-approved, supervised pass — the most the automated part does is *raise its hand* and say "this one's looking heavy." It also isn't a length limit: a command that's long because its *method* is genuinely big is fine and stays big. The target is history-per-instruction, not size. And it's explicitly the counterpart to the capture habit, not a replacement — you still write fixes in the moment; this is just the cleanup pass that habit never gives itself.

## Why this works

The capture habit is right at the moment of capture (you're mid-task, you just need it written down) and wrong as a long-term storage strategy (nobody curates as they go). Splitting those — capture cheaply now, distil deliberately later — lets each be good at its job. And the safety check is what makes it psychologically possible to prune at all: without an independent "you didn't drop anything" pass, trimming a command you rely on is nerve-wracking enough that most people just let it rot. The check turns a scary edit into a routine one.

## Note

This is a pattern, not a fixed pipeline. How you flag bloat, whether you keep a formal changelog or just a comment, whether you wire in a second model for the safety check or eyeball it — all yours, and all optional. The durable idea is: *the habit that keeps your tools sharp in the moment slowly dulls them over time, so give it a deliberate counterpart that prunes the history back out — with a check that proves nothing load-bearing went with it.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/clearing-clutter-from-your-workflows.md) lays out the maintainer's real version — the four-layer sort, the two-pass safety check, the bloat detector, the failure modes — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
