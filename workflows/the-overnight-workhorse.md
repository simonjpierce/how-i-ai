# The overnight workhorse

A way to hand off the work that doesn't need you watching — research, first drafts, analysis — so it runs while you sleep and you wake up to results to review, instead of spending your day waiting on the AI.

*This is an advanced pattern — worth reaching for once your core setup is humming and real work is piling up, not something to build on day one. It shows the shape; when you're ready, paste it into Claude Code to wire up the queue and the overnight run.*

## The core idea

A lot of useful work doesn't actually need you in the loop while it happens. Pulling together background research, turning a finished analysis into a first-draft section, summarising a stack of documents — these take time but little judgement *during* the doing. There's no reason to spend your daytime attention babysitting them.

So you separate two moments. At the **end of the day**, you decide what's worth running unattended and add it to a queue. Overnight, an autonomous process — the **workhorse** — works through that queue. In the **morning**, you review what it produced. Your day stays for thinking and deciding; the slow, unattended work happens while you're asleep.

The important discipline: the workhorse runs **what's in the queue, and only that.** It never invents its own projects in the night. You fill the queue each evening, and a few trusted automations add to it too — each one a kind of job you've already agreed it may do, such as the small next steps on your projects that need no decision from you.

## The pieces

- **The evening review** — a short end-of-day pass where you look at what got done, what's coming, and what's worth the overnight compute. In the maintainer's setup this is a command (`/tonight`) that walks through it and writes the night's priorities down.
- **The queue** — a simple list of tasks for the workhorse, each with enough instruction to be done without you there to answer questions. Some entries are parked on purpose — shaped for a moment you can't hand off yet — so mark those as parked with a reason, or they read as work the runner kept failing to reach and you end up promoting them on a false premise.
- **The workhorse** — the unattended runner. It picks up the queue and works through it; when the queue is empty it stops (or waits for more), rather than freelancing.
- **The morning review** — you read the drafts and results, keep what's good, redirect what isn't.

## How it runs

In the evening you review the day and queue what's worth doing overnight — clearly enough that the task can run without you. The workhorse runs through the night, task by task, and leaves its output in your vault. In the morning you review: the drafts are starting points, not finished work, so you read them with an editor's eye.

Because the tasks have to be self-contained (no one's there to clarify at 2am), writing a good queue entry is a skill in itself — say exactly what you want, where the inputs are, and what "done" looks like. Your AI can help you write them.

Write that "done" as one concrete, checkable sentence, and keep it as a field on the task rather than burying it in the prose. It earns its keep twice: the runner hands it to the worker as an explicit stop condition, and afterwards a separate pass checks the output against it before the task counts as finished. Without it, both the doing and the checking fall back to guessing what you meant — which is how you end up with tasks marked complete and nothing useful behind them.

Give every unattended run a way to end that doesn't depend on you remembering. An overnight run has a natural edge, so give it a morning cutoff. A run you start during the day has no such edge, and a stuck one will happily keep re-planning for ten hours, burning quota while you assume it finished long ago. A clock is a blunt guard there — it either cuts off a healthy long run or lets a stuck one burn hours — so add a watchdog that watches progress instead: it stops the run when nothing has been delivered for hours, when the worker has gone silent, when several planning passes in a row find nothing to do, or when the queue keeps refilling itself.

When any guard trips, no new work starts, whatever is in flight is allowed to wrap up cleanly, the queue is checked for anything malformed, and a record is written that says why it stopped — even if nothing got done. An empty record tells you the run happened and produced nothing, and a stall record is how you tell a stuck run from a clean finish. After a stall, hold off restarting until the queue has actually changed (or a long timeout passes), so the same stuck run doesn't loop.

Two silent failures are worth designing against, because neither announces itself. A malformed queue entry can be invisible to the runner: it sits in the queue looking perfectly fine and is simply never picked up, so check that a newly-queued task actually registers as runnable before you trust it to the night. And the overnight run should be owned by your machine rather than by the chat session you started it from — a run that is a child of that session dies when the session does, often hours in, with nothing in the logs to say why.

## What this does *not* do

It's not hands-off autonomy you can't see. Everything in the queue has a named source, and everything that comes out lands in tomorrow's plan, so the drafts are waiting for you there — and nothing is ever sent to anyone on your behalf. You don't sign off each item, though: the brake on unattended work is a budget and a ranking, not your time. It also won't do work that needs your judgement *as it happens* (a delicate email, a real analytical decision) — those belong in your day, not the queue. Treat it as a tireless junior that does the legwork and hands you drafts.

## Note

This is a pattern, not a fixed tool. How you trigger the run, where the queue lives, how much you queue, how unattended you let it be — all yours. The durable idea is: *the work that doesn't need you watching shouldn't cost you daytime; queue it, sleep, review.* Paste this to your AI and build the version you'll actually trust.

---

*Want the actual method? [The reference](../reference/the-overnight-workhorse.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
