# How it all fits together

Here's how I actually use this system across a working day. Seeing the whole shape of a reasonably mature (albeit rapidly iterating) system might help to make the individual pieces make more sense.

This is an orientation piece, not a setup task. It's the next few pages that start you building the foundations of your own system. (Though paste this page URL into Claude Code if you want to talk through how this shape would map onto your own work.)

## The core idea

Going forward, we'll often discuss each workflow as a single capability — writing a paper, doing 'deep research' on a topic, transcribing a meeting, or setting the AI to do autonomous work while you pop out for a walk. On their own, each can be very useful. The real magic, though, happens when the processes work together. 

## A day in the life

Here's my actual rhythm when I'm at home.

**Early, before I'm even at the desk.** Overnight, the system cleaner has already completed a full shift. A handful of scheduled jobs run while I sleep: new material that came in during the day (saved articles, papers, voice notes) gets pulled into the vault and filed; a self-improvement pass reviews yesterday's system errors and folds in small fixes; backups and health checks run. By the time I'm awake, the overnight housekeeping is done.

**My morning walk.** I talk — a stream-of-consciousness voice note in Apple Voice Memos app; no structure, just whatever's on my mind. It's basically verbal journalling to help cage my monkey brain. Then, as I finish up, the AI runs a [transcription step](./transcription.md) that turns it into an Obsidian note, and the system reads it: anything that's a task lands on my to-do list, thought bubbles land in my idea file for the AI to think about and make a plan for, and the main objectives I'm thinking about help set my AI's context for the day. I didn't have to organise any of this; I just thought out loud like a crazy person. A lot like a crazy person, in fact.

**The AI helps plan my day.** When I'm at my desk, I open a Claude Code session and run /today. That starts two processes. First, it **orients** — the AI reads the latest session handoffs from yesterday and my current-projects file to refresh its memory on what I'm working on, so the AI already knows exactly where we're up to. Then it **synthesises**: it fans out to the **agent fleet** — a set of domain specialists, one each for my science, fundraising tasks, external communications, photography plans, admin tasks, and executive oversight of our non-profit. Each agent reviews its own folder of notes in the vault and surfaces what it thinks needs my attention; then the chief of staff agent collates all those jobs, weighs them against one another, and hands me the **single most important first task** — not a wall of twenty bullet points, one thing, typically with the recommended action already worked out or a draft already created for me.

**I work, one thing at a time.** Each task gets done with whichever capability fits it, and the variety across a day is wide:

- a **paper or analysis** — run the numbers, write the section, with every figure traceable back to the data and every citation [checked against a real source](./the-science-workflow.md) rather than trusted;
- a question worth a few hours — point it at [deep research](./deep-research.md) and get back a cited, cross-checked report instead of a confident guess;
- a piece of writing that matters — a draft, then [an independent critique from a second model](./writing-and-review.md), then a polish, so it's been pressure-tested before anyone else sees it;
- a meeting or a talk — [transcribed](./transcription.md) into clean notes with the action items pulled out;
- a stack of PDFs — [turned into clean text in the vault](./pdf-to-markdown.md) so their content is searchable and quotable;
- the routine stuff that still eats a morning — meeting prep, a board pack, a supporter update, a forecast check before a dive — each one a short command that assembles the draft from what's already in the vault.

I finish a task, come back, and the chief of staff hands me the next one. The flow is always *do the thing → return → get the next thing*, never *stare at a list and decide what to do*.

**The record keeps itself.** This is the part that makes the next day cheap. As I work, the system writes down the decisions and the reasoning and keeps my project notes current — and at the end of a session a handoff step distils what happened: what was done, what's still open, what the next session should read first. The hard-won corrections ("don't do it that way", "always check this first") get distilled into the AI's long-term memory so I'm not re-litigating them next week. Tomorrow starts from where today actually ended, not from a cold start.

**Evening.** A short review looks at what's queued and what's worth running unattended — the things that don't need me in the loop, just time and attention to detail. I pick a few and hand them to [the overnight workhorse](./the-overnight-workhorse.md).

**Overnight, again.** The workhorse works the queue while I sleep — a first draft here, a research dig there, an analysis that just needed running — and the cycle closes: the next morning, the vault is richer than it was, the specialists review *that* richer state, and the day starts from a better place than the one before.

**And quietly, underneath all of it:** the [self-improvement loop](./the-self-improvement-loop.md) is watching for friction — anything that was harder than it should have been — and turning the recurring annoyances into fixes. The system that runs my day is also, slowly, improving the system that runs my day.

## The range of what it handles

The point of the day above isn't any single capability — it's the *breadth*. The same vault-and-AI setup covers work that would normally be scattered across a dozen apps:

- **Knowledge work** — research, analysis, writing, and review, all with the source material and the reasoning kept in the vault.
- **Communication** — drafting emails, updates, and reports in a consistent voice (the system keeps voice references and reads the right one before it writes), always as a draft I send myself, never sent automatically.
- **Operations** — the recurring obligations of actually running things: meeting prep, board material, periodic reviews, the admin that has a shape but no interest.
- **Intake** — pulling in the firehose of incoming material (articles, papers, voice notes, transcripts) and filing it where it'll be found again.
- **Its own upkeep** — when a process is worth formalising, it gets written up as a reusable workflow and pressure-tested by a second model before it's trusted; when something keeps going wrong, the self-improvement loop fixes it. The system is maintained the same way the work is done.

Not all of this arrives at once, and most of it you'd never build deliberately — it accretes, one capability at a time, because each one was worth having on its own.

## Zooming out: the loops

If you squint, the whole thing is a handful of **loops** running on different rhythms, all reading and writing the same vault:

- a **daily work loop** (plan → do → capture), the one you live in;
- a **content loop** for things that accumulate toward a deliverable (a paper, a newsletter, a talk) over days or weeks;
- an **intake loop** that pulls new material — articles, transcripts, papers, voice notes — into the vault and files it;
- a **planning loop** (morning fleet → first task; evening review → overnight queue) that decides what gets attention and when;
- a **maintenance layer** — backups, health checks, and the self-improvement loop — that keeps the system honest without your attention.

You don't have to know all of them to use the system. (The maintainer's own notes break this into a dozen-odd named loops; that's bookkeeping for keeping a large system coherent, not something a newcomer needs.) The takeaway is just that the parts aren't a pile of tricks — they're loops that compound, because each one leaves the shared memory better than it found it.

## Where to start

Not here. You build *up* to this picture; you don't assemble it in a weekend. The path that works:

1. The foundation — [set up the stack](./01-set-up-the-stack.md) (the vault, the editor, the AI).
2. **One** capability you'll use this week — pick the workflow that matches your most common task.
3. Add the next piece only when you feel the need for it. The agent fleet and the overnight workhorse are worth it once you have enough going on that *planning what to do* and *waiting for things to finish* are themselves a cost worth automating away.

The system earns its keep gradually. Each piece is useful alone; the compounding is the reward for sticking with it.

## Note

This is a description of a pattern, not a blueprint to copy line for line. Your day looks different, your loops are different, your domains are different — mine happen to be science, conservation, and photography; yours won't be. The durable idea is the one thing every piece shares: *capabilities that each leave the shared memory richer, sequenced so the routine work gets out of your way.* Read it for the shape; build the version that fits your life.

---

## Next step

**→ [Set up the stack](./01-set-up-the-stack.md)** — the foundation this all runs on: somewhere to keep your notes, and an AI that can read and write them.
