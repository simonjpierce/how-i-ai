# Memory and context

Make the AI actually *know* you — your role, your preferences, how you like things done, and what it has learned from working with you — so it shows up to every session already on the same page instead of being a brilliant stranger each time.

This is an idea file. Paste it into Claude Code to build a version for your own setup; it'll fill in the specifics (file locations, folder names) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

A fresh AI session starts blank. It doesn't know you write in British spelling, that you hate bullet-point walls, that "the report" means a particular thing in your world, or that last Tuesday you told it — twice — to stop doing the thing it's about to do again. By default you re-teach all of it, every session, forever. That re-teaching tax is the failure mode this fixes.

The fix is to give the AI a small amount of context it reads **automatically, at the start of every session** — so it walks in already briefed. There are two distinct kinds, and keeping them separate is what makes the whole thing work:

- **Standing instructions** — what *you* set, deliberately. Who you are, your role, your spelling and tone, how you like options presented, where things live, what it should never do. This is stable. You write it once (or have the AI draft it from a five-minute interview) and revise it occasionally.
- **Learned memory** — what the *AI* accumulates over time. The correction you made last week, the preference it inferred, the gotcha it hit and shouldn't hit twice. This grows from use, and the AI maintains it.

Both load at the start of every session, so the AI starts informed. The payoff compounds: the more it knows, the less you re-explain, and the sharper its judgement gets about *your* work specifically.

## The pieces

**A standing-instructions file — layered, not one giant block.** Most agents look for a conventionally-named instructions file at startup (in Claude Code it's `CLAUDE.md`; your agent will tell you what it uses). The trick that makes this scale past a single project is to *layer* it: a top-level file for who you are and how you work, and smaller files placed inside each major area of your work that add only that area's context. When the AI works in your "research" folder it picks up your research conventions; in "finances", the financial ones. Each layer adds detail without repeating what's above, and you only ever load the context that's relevant to where you're working — so the AI's attention isn't diluted by rules that don't apply.

**A learned-memory file — the durable record of lessons.** One file the AI reads every session that holds the preferences and corrections it has picked up, plus pointers to deeper notes it pulls in only when relevant. The discipline that keeps it useful: it stays *short and high-signal*. A learned-memory file that becomes a dumping ground stops being read carefully — and most agents only load the first slice of it anyway, so anything past that point silently never loads at all. So it's kept lean on purpose: the always-loaded core holds the handful of rules that fire in *every* session, and anything that only matters for a specific kind of task is pushed out to a separate note that gets pulled in just when that task comes up.

**A clear division of labour between the two.** Standing instructions hold *behaviour* — what the AI should do, who you are, your settled preferences. Learned memory holds *facts and corrections* — what's been discovered through use. Keeping facts out of the instructions file and behaviour out of the memory file stops the two from drifting into contradiction, which is the quiet way this kind of system rots.

## How it runs

You start small. Even a few lines of standing instructions — who you are, what you do, how you like to work — beats a blank slate, and the AI can draft the first version by interviewing you. Then it grows through ordinary use: when you correct the AI, or it notices a preference, or it trips over something worth not tripping over twice, that lesson gets distilled into the learned-memory file — a sentence or two, not a transcript. Over weeks, the layered instructions and the accumulated memory together mean the AI rarely needs re-briefing. It already knows.

The maintenance is light but real. Every so often — at the end of a working session is a natural moment — you (or the AI, prompted) prune: merge near-duplicate lessons, drop ones that no longer apply, move anything that only matters occasionally out of the always-loaded core and into a pulled-in-on-demand note. Lean is a practice, not a one-time setup.

## What this does *not* do

It's not a dumping ground. Both files stay lean on purpose — context that loads every single session has to earn its place, or it drowns out the rules that matter (and you may quietly hit a length limit past which nothing loads at all). It's not set-and-forget either: the standing instructions evolve as you notice what you keep having to repeat, and the learned memory needs occasional pruning or it bloats. And it isn't a *personality* — it's working context, the stuff a good human assistant would simply remember about you, written down so a fresh session inherits it.

## Why this works

The expensive part of working with an AI isn't any single task — it's re-establishing context, over and over. This pattern pays that cost once and amortises it across every future session. And the split between standing instructions and learned memory matters more than it looks: settled preferences you set deliberately and rarely change; corrections accumulate messily through use. Stored together they'd fight each other. Kept apart — behaviour in one place, learned facts in another, both lean — each stays trustworthy, and a session that starts already knowing you is a colleague rather than a stranger.

## Note

This is a pattern, not a fixed format. What counts as a standing instruction versus a learned lesson, how finely you layer the instruction files, where the memory file physically lives, how aggressively you prune — all yours to shape, and you can start with just the top-level instructions file and add layers only when one area genuinely needs its own context. It assumes an agent that loads instruction and memory files at startup, which Claude Code does by convention. The durable idea is: *give the AI a little context it reads every session — what you set, plus what it has learned — so it always shows up knowing you.* Paste this to your AI and write the first version together.
