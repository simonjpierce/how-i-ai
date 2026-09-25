# The daily coach

A way to turn "I have a hundred things to do and can't make myself start any of them" into "do this one thing — now this one — now this one," so the day actually moves instead of dissolving into overwhelm and a still-full inbox.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

A to-do list is a pile of everything, all visible at once, with no guidance on what to touch first. For a lot of people — especially anyone who fights procrastination or overwhelm — that pile is *paralysing*: the cost of deciding what to do next is itself enough to make you do none of it, or scatter across five half-things, or quietly avoid the one that matters. The list grows, the email backs up, and the gap between "what I meant to do today" and "what I did" becomes its own source of dread.

The move here is to stop treating your day as a list to stare at and start treating it as something an AI **coaches you through, one item at a time.** Two beats:

- **Plan the day.** Each morning the AI pulls together your real inputs — calendar, tasks, what's due, what you flagged last night, what's still open from yesterday — and produces a *short, ordered* list of what actually matters today. Not everything. The few things that move the needle, in the order to do them. The plan can be waiting for you: the maintainer's is built by a scheduled job before he's up, and a second model checks it against the sources before it opens.
- **Walk it, one task at a time.** Then it surfaces *one* task — just the next one — and helps you actually start it: the concrete first action, the file already open, the draft already begun. You do it (or consciously skip it), it marks it done, and *only then* does the next one appear. You're never looking at the whole pile, only at the single thing in front of you.

You can run more than one coached block a day. The maintainer runs two: a morning block for the main job, and a protected afternoon block for the work the main job would otherwise crowd out — which is how that second kind of work gets done at all.

The morning plan also looks ahead at the calendar. When a real meeting is coming up today or tomorrow and there's no brief for it yet, it says so and offers to build one: who's attending, what your notes and recent email say about them, what you promised last time, and a few points to raise. The maintainer tried the other way first, with a brief built automatically before every meeting, and dropped it. Asking only when a meeting matters turned out to be the version worth keeping.

The same pattern clears your inbox. Instead of "deal with email" (vague, infinite, avoidable), the AI surfaces the messages waiting on a reply and sorts them by importance: the few that matter today join the morning plan, and the rest get walked down later with a visible countdown, ten to zero. For each one it shows the message with a line of context and asks how you want to handle it; only then does it draft the reply, for you to edit and send. A finite, finishable thing with a defined finish line.

## How it runs

**The plan is built from your stuff, not invented.** The AI reads the inputs you already keep — your calendar, your task manager, your notes — and proposes the day; you're steering, not accepting a stranger's idea of your priorities. **One thing is "live" at a time.** The coach holds the rest of the list in reserve and shows you only the current task, with whatever it takes to lower the activation cost of starting — the first sentence written, the link opened, the question framed. **Completion is explicit and a little bit rewarded.** Each finished item is marked and counted; the inbox pass literally counts down to zero. The finish line is the point — crossing it is the reward, so it isn't buried. **Stopping early is fine.** If you get through six of ten, that's six done, not four failed — the framing never turns into guilt.

## What this does *not* do

It doesn't do the work for you, and it doesn't decide what matters *instead* of you — you can always reorder, skip, or veto, and the priorities come from your own inputs. It also isn't a nag or a tracker that judges you: the value is in *removing the friction of deciding, starting, and keeping count*, not in surveillance. And it won't send anything on your behalf — the inbox pass drafts replies; you read and send them yourself.

## Why this works

The active ingredient is the *one-at-a-time constraint.* Overwhelm is largely the cost of holding the whole list in your head plus the decision of what to do next; removing both — by showing exactly one chosen thing — is what makes starting possible. And a defined, finite finish line ("ten down to zero", "the five that matter today") converts an infinite, avoidable obligation into a bounded, finishable one. None of this requires willpower you don't have; it restructures the task so less willpower is needed.

## Note

This is a pattern, not a fixed implementation. What you feed the planner, whether you run one coached block or two, an email countdown, an evening review, or just one of them, how much "help me start" each task gets — all yours, and all optional. The durable idea is: *don't make yourself face the whole pile; have the AI plan from your real inputs and then put exactly one chosen thing in front of you at a time, with a finish line you can actually reach.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/the-daily-coach.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
