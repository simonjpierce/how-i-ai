# Reference — The daily coach

> **What this is.** The actual method behind [the *daily coach* workflow](../workflows/the-daily-coach.md), cleaned of the maintainer's personal specifics (real paths, file names, machine schedules, the in-house agent fleet). It's a **starting point to adapt, not a drop-in command** — your day is shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the moving parts.
>
> Three related rituals share one design here: a **morning plan** (plan the day, then coach through it — the main work plus the handful of emails that matter today), an **afternoon block** (protected time for the work the main job crowds out, finishing with a count-down of the remaining replies), and an **evening review** (set tomorrow's few priorities, hand non-urgent work to an overnight worker). Email isn't a ritual of its own: messages are sorted by importance, and the important replies join the morning while the rest are cleared in the afternoon. Throughout, "your task manager" is wherever your to-dos live (the maintainer uses Things 3); "your notes" is your daily/working notes; "the right area" means routing an item to whoever owns it — for the maintainer that's a fleet of per-domain agents, but a folder, a tag, or a single person works just as well.

## The shared DNA

All three rituals run the same two-beat loop: **plan from real inputs**, then **walk it one thing at a time**. Build that engine once and the rituals are thin profiles over it — same gather-and-coach machinery, different inputs and different finish lines. The morning and afternoon coaches in particular are worth running off literally one shared procedure with a profile switch, so a fix to one improves both.

## The morning plan: gather → synthesise → coach

**Gather the day's real inputs first — never invent the plan.** Pull from the sources you already keep: the calendar (a week ahead), the task manager (what's flagged for today, what's overdue, what's coming), a daily log or notes file, anything you flagged the night before, and whatever's still open from yesterday. A short script that collects all of this into one structured blob keeps the gather fast and repeatable. The rule that makes it trustworthy: the plan is **built from the human's own inputs**, so they're steering, not accepting a stranger's idea of their priorities.

**Synthesise into a short, ordered list — not everything.** This is the step that does the work. From the full pile, the AI produces the *few* things that actually move the day, in the order to do them — a handful, not the whole backlog. Weight the ranking toward what's genuinely time-sensitive (a real deadline, someone waiting on a reply) and what the human explicitly flagged; let lower-value items fall below the line rather than padding the list. Write the result to one stable file the human can see and edit through the day.

**Let it run before you're up.** The gather and the synthesis don't need the human present. The maintainer's run as a scheduled job at dawn, and a second model checks the draft plan against the sources before it's opened — so the day starts from a checked list, not a blank prompt. A voice memo recorded later can still change the live plan: it's folded in item by item, never by rebuilding the plan and losing what's already ticked off.

**A fixed warm-up block helps starting.** A small, predictable opening set — a handful of short, timeboxed tasks of known shape — lowers the cost of the very first action of the day. Starting is the hardest moment; a familiar warm-up removes the "what first?" decision entirely.

**Then coach through it, one task at a time.** Surface *one* task — just the next one — and lower the activation cost of starting it: write the concrete first action, open the file, begin the draft. The human does it (or consciously skips it), the AI marks it done, and *only then* does the next task appear. They never face the whole pile, only the single thing in front of them. Advance **only on the human's signal** — one "next" moves exactly one step.

## The afternoon block: protect the work the main job eats

**A second coached block, same engine, different inputs.** If one kind of work always loses to the main job — for the maintainer, photography, his websites and life admin lose to running a non-profit — give it its own block and its own short plan, built from the specialists (or folders) for those areas, and coach it the same way, one item at a time. The plan is drafted early and refreshed at midday, so it reflects what happened in the morning.

**Prepare ahead while the human works.** While they're on the current item, the AI prepares the next one in the background — gathering the material, starting the draft — so each new item starts half-done.

**Size to the time actually left.** The block knows where the next calendar commitment falls and offers something that fits before it, rather than opening a big item that can't be finished.

## The evening review: set tomorrow, hand off the overnight work

**Review what got done, then pick tomorrow's few priorities.** At end of day the AI reads what closed today and what's coming, and walks the human through a small set of candidate priorities for tomorrow — one at a time, each with a why-now and a proposed outcome, approve / adjust / drop / defer. The output is a short, explicit list of what matters tomorrow.

**Hand non-urgent work to an overnight worker — but only what's delegable.** Substantial prep that compresses hours of work — a research pass, a long draft, an analysis — can be queued for an autonomous overnight run, so it's waiting in the morning review queue. Two guardrails earn their keep: a **quick task the human could do in five minutes is a to-do, not an overnight job** (don't burn an overnight slot on a three-minute email), and anything needing a live login or the human's hands (sending, browser auth, in-person steps) is **not** delegable — surface it to do, never run it unattended.

**Capture rejections durably, so the same wrong thing doesn't resurface.** When the human drops or corrects a candidate ("that's already done", "this isn't mine to do"), record it as a lasting exclusion — not just a one-night skip — or tomorrow's plan proposes it all over again.

## The email countdown: read-but-unanswered, ranked, counted down

**Find the genuinely-awaiting-a-reply messages — backlog-aware, not just unread.** The signal is **the last message in the thread is not from you**, regardless of read state. The dropped ball — read it, meant to reply, never did — is exactly what to catch, and read/unread misses it entirely. Don't cap to the last day: an older unanswered message weights *up*, not down. Exclude the things that never need a reply (newsletters, receipts, automated notifications). Then rank what's left by importance: the few that matter today go into the morning plan; the rest wait for the afternoon countdown.

**Ask before drafting — and never send.** Nothing is drafted unattended. The AI shows each message with a line of context and asks how the human wants to handle it; only then does it draft, in the right voice (declaring which voice guide it's using). A reply that takes a position drafts to a view the human has already recorded, or is written as a question — it never borrows the sender's framing as their view. This is **draft-only, always**: the AI writes the reply into your notes, never into the mail or chat client, never as a real draft on the server, and **never sends**. The human reads, edits, and sends from the real thread themselves. Read-only on every external service — no archiving, labelling, or marking-read on their behalf.

**Walk them down with a visible countdown.** Present one message at a time and count down — ten to zero — so an otherwise-infinite obligation ("deal with email") becomes a finite, finishable thing with a defined finish line. Re-check each thread is still unanswered right before the human sends it; between drafting and walking, they may have replied themselves or a new message may have landed.

## The design principles that make it work

These are why the rituals help with overwhelm and procrastination, not incidental polish — keep them whatever else you change:

- **One task live at a time.** Overwhelm is largely the cost of holding the whole list in your head *plus* deciding what's next. Showing exactly one chosen thing removes both. This is the active ingredient; protect it.
- **A finite, defined finish line.** "The five that matter today", "ten down to zero" — a bounded, reachable end converts an infinite obligation into a finishable one.
- **Explicit completion, a light reward.** Mark each item done and count it. Crossing the finish line *is* the reward, so don't bury it.
- **Stopping early is fine — never guilt.** Six of ten done is six done, not four failed. The framing never becomes a nag or a tracker that judges; the value is in removing friction, not surveillance.
- **Built from the human's inputs, steered not dictated.** The AI proposes from your real sources; you can always reorder, skip, or veto. It doesn't decide what matters *instead* of you, and it doesn't do the work for you.
- **Turn generation into evaluation.** Reviewing a draft is far cheaper than producing one from a blank page. Pre-fill, pre-format, open the file, begin the draft — push the activation cost toward zero everywhere.

## What stays yours

Which inputs feed the planner, whether you run all three rituals or just one, how much "help me start" each task gets, what your overnight worker can and can't be trusted with, how the inbox countdown is framed — all adapt to your setup. The transferable spine is just: *don't make yourself face the whole pile; have the AI plan from your real inputs and then put exactly one chosen thing in front of you at a time, with a finish line you can actually reach — and on the inbox, it drafts, you send.*
