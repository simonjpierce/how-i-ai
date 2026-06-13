# How it all fits together

Before you set anything up, here's where it's all heading: how I actually use this system across a working day. I'm a marine biologist who also runs a conservation foundation and shoots underwater, and over the last few months this has quietly become the way I get almost everything done. None of it appeared at once — it built up one capability at a time — but seeing the whole shape first makes the individual pieces make sense.

This is an orientation piece, not a setup task. You don't build any of this yet; you read it to picture the rhythm, then the next pages start you on the foundation. (Paste it into Claude Code if you want to talk through how this shape would map onto your own work.)

## The core idea

Every other workflow is a single capability — writing a paper, doing deep research, transcribing a talk, the morning agent fleet, the overnight workhorse. On their own, each is useful. The point of the system is what happens when they interlock, with one thing tying them together: **the vault is the shared memory that all of them read and write** (see [the philosophy](./00-the-philosophy.md)). Nothing here is a separate app passing messages around — it's a folder of files that every part of the system uses as its common ground. A morning routine writes a plan into the vault; an overnight job reads that plan; a capability you run at 2pm leaves a note that tomorrow's routine picks up. No integrations, no glue code — just files that everything reads and writes.

## A day in the life

Here's the rhythm I actually live in. I'm offering it to make the shape concrete, not as a template to match — your day has different shapes in it.

**Early, before I'm even at the desk.** Overnight, the system has already done a shift. A handful of scheduled jobs run while I sleep: new material that came in during the day (saved articles, papers, voice notes) gets pulled into the vault and filed; the self-improvement pass reviews yesterday's friction and folds in small fixes; backups and health checks run. By the time I'm up, the overnight housekeeping is done and the vault is current — what's left is decisions.

**On the morning walk.** I talk — a stream-of-consciousness voice note, no structure, just whatever's on my mind. Back at the desk, a transcription step turns it into text, and the system reads it: anything that's a task lands on my task list, anything that's an idea lands in my idea file, and the rest becomes context for the day. I didn't have to organise any of it; I just thought out loud.

**The day plans itself.** I open a session and run my morning routine. It does two things. First it **orients** — reads the latest session handoff, my current-projects file, and the accumulated memory, so the AI already knows exactly where everything stood when I last stopped. Then it **synthesises**: it fans out to the **agent fleet** — a set of domain specialists, one each for the science, the fundraising, the communications, the photography, the admin, and the running of the organisation — each of which reviews its own corner of the vault and surfaces what needs attention; then the chief of staff collates all of it, weighs it against what's actually due, and hands me the **single most important first task** — not a wall of twenty bullet points, one thing, with the recommended action already worked out.

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
