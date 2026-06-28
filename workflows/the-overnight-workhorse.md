# The overnight workhorse

A way to hand off the work that doesn't need you watching — research, first drafts, analysis — so it runs while you sleep and you wake up to results to review, instead of spending your day waiting on the AI.

*This is an advanced pattern — worth reaching for once your core setup is humming and real work is piling up, not something to build on day one. It shows the shape; when you're ready, paste it into Claude Code to wire up the queue and the overnight run.*

## The core idea

A lot of useful work doesn't actually need you in the loop while it happens. Pulling together background research, turning a finished analysis into a first-draft section, summarising a stack of documents — these take time but little judgement *during* the doing. There's no reason to spend your daytime attention babysitting them.

So you separate two moments. At the **end of the day**, you decide what's worth running unattended and add it to a queue. Overnight, an autonomous process — the **workhorse** — works through that queue. In the **morning**, you review what it produced. Your day stays for thinking and deciding; the slow, unattended work happens while you're asleep.

The important discipline: the workhorse runs **what you queued, and only that.** It doesn't go off and invent its own projects in the night. You decide the work; it does the work; you review the work.

## The pieces

- **The evening review** — a short end-of-day pass where you look at what got done, what's coming, and what's worth the overnight compute. In the maintainer's setup this is a command (`/tonight`) that walks through it and writes the night's priorities down.
- **The queue** — a simple list of tasks for the workhorse, each with enough instruction to be done without you there to answer questions.
- **The workhorse** — the unattended runner. It picks up the queue and works through it; when the queue is empty it stops (or waits for more), rather than freelancing.
- **The morning review** — you read the drafts and results, keep what's good, redirect what isn't.

## How it runs

In the evening you review the day and queue what's worth doing overnight — clearly enough that the task can run without you. The workhorse runs through the night, task by task, and leaves its output in your vault. In the morning you review: the drafts are starting points, not finished work, so you read them with an editor's eye.

Because the tasks have to be self-contained (no one's there to clarify at 2am), writing a good queue entry is a skill in itself — say exactly what you want, where the inputs are, and what "done" looks like. Your AI can help you write them.

## What this does *not* do

It's not hands-off autonomy you can't see. You decide everything that goes in the queue, and you review everything that comes out — nothing ships without you. It also won't do work that genuinely needs your judgement *as it happens* (a delicate email, a real analytical decision) — those belong in your day, not the queue. Treat it as a tireless junior that does the legwork and hands you drafts.

## Note

This is a pattern, not a fixed tool. How you trigger the run, where the queue lives, how much you queue, how unattended you let it be — all yours. The durable idea is: *the work that doesn't need you watching shouldn't cost you daytime; queue it, sleep, review.* Paste this to your AI and build the version you'll actually trust.

---

*Want the actual method? [The reference](../reference/the-overnight-workhorse.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
