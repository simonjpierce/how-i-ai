# One session that runs the others

Keep one long-running conversation as your chief of staff: it starts each piece of work in a session of its own, checks what comes back against the files, and brings you only what needs you — so you can have a dozen things moving without holding a dozen conversations in your head.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Once the AI is useful, the bottleneck moves to you. Five sessions are each waiting for a nudge, each one's report sounds confident, and you become the person who remembers which is which, checks whether "done" is true, and types "carry on" all day. The work scales; your attention doesn't.

The fix is to put one session between you and the rest. In the Claude desktop app's Code tab (as of November 2026, in the maintainer's version — check that yours has it), a session can start other sessions, message them, read their transcripts, and is told automatically whenever one of them finishes a turn (one round of work in reply to a message). This needs the desktop app: sessions in a terminal, or in Codex, can't message one another, so there the nearest version is one session that hands work to helpers inside itself. So one session — the maintainer calls it the chief of staff — becomes the only one you talk to about the day as a whole. It doesn't do the work. It hands work out, reads what comes back, and decides what reaches you.

The whole arrangement rests on one principle: **the orchestrator (the chief-of-staff session) starts, checks, and relays; it never decides for you and never approves on your behalf.** Everything below follows from that.

## The pieces

- **The seat.** One session, kept running for weeks, on your most capable model, because its job is judgement: what matters today, whether a report holds up, and what you need to hear. It's an ordinary session given a standing instruction file: who it is, where its notes live, and its hard limits. The maintainer opens it in the desktop app and can also reach it from his phone through the app's Remote Control. Everything else is a child of this session and shows in the same sidebar, where you can open, steer, or stop any of them yourself.
- **Starting work.** When you ask for something bigger than a few steps, the chief of staff starts a session for it with a written brief: the task, the files, what done looks like, and the limits (nothing sent, nothing published, and no one's personal details to outside services). The brief has to stand alone, because the new session knows nothing about the conversation it came from. Child sessions run on a cheaper model than the seat unless you say otherwise.
- **Reports are claims, not proof.** Each time a child finishes a turn, a short note arrives. The chief of staff checks it before telling you anything: is the file there, is the commit on the backup copy, does the live page show the change, did the count get re-counted. A child's "done and pushed" is where the checking starts. This is the part that earns the arrangement its keep; in the maintainer's use the numbers are usually right, and what the check catches is wording that claimed more than the work showed.
- **Two timers.** A daily check each morning walks a written list of the system's jobs and asks what each one produced, since a job can exit cleanly having done nothing. An hourly check reads what every session did in the last hour. Both are written prompts the session runs on a schedule, and most of the time they end in silence. In the maintainer's version of the app these timers live only inside the session and lapse after seven days, so the morning check's first step is to re-create any that are missing or about to run out.
- **A fixer that isn't the orchestrator.** Breakdowns the morning check finds go, with evidence, to a separate long-running session whose job is system upkeep. The chief of staff finds and ranks; the other session repairs. Keeping those apart stops the seat disappearing into a debugging session while your day goes unwatched.
- **Agents that work their own lists.** Each morning the chief of staff starts one session per specialist agent (see [the agent fleet](./the-agent-fleet.md)) — in the maintainer's version of the app a timer can't open a new session, so the starts wait for the first message he types at the desktop. Each one plans from its own list, does what it can without you, has the result independently checked, and reports. Finished sessions are asked to write their closing notes, checked once more, and archived the same day, so yesterday's sessions don't pile up.
- **One question at a time.** Children's questions and its own queue up with the chief of staff, which puts them to you one per message, each restated in full with numbered options and a recommendation first. A bare "session X has a question" is not allowed: either the whole question, or nothing until there's room for it.
- **Approvals happen where they act.** A go-ahead to publish a website, send a message, or write to a shared database is typed by you in the window of the session that will do it. The chief of staff restates the question for you and tells you where to answer; it does not pass your "yes" along. A relayed approval is one copy-paste away from an approval you never gave.
- **A restart note.** A session this long fills its working memory and gets summarised many times. So it keeps a dated note of its own state — what's running, what's waiting on you, and what's due on which day — and re-reads it after every summary (see [the session loop](./the-session-loop.md) and [managing your token budget](./managing-your-token-budget.md)).

## What this does *not* do

It doesn't make decisions that are yours, and it's deliberately bad at pretending to. Copy, money, anything about a person, or anything that leaves your machine: those come to you as a question. It doesn't replace reading the important things yourself; it tells you which things those are. It isn't free — a long-running seat on a strong model, plus a session per piece of work, uses a real share of a subscription, and the maintainer watches a weekly usage figure for that reason. And it isn't a day-one tool. It pays off once you already have several pieces of work running most days and written rules for what the AI may and may not do without you.

## Why this works

A session only works while a turn is running; when it stops, it waits until something wakes it. Left alone, every session is waiting on you. The orchestrator is the thing that wakes them — with the next step, a check, or your answer — and the thing that turns a dozen confident reports into the two that needed your eyes. The rule that it never approves on your behalf is what makes it safe to let it do everything else.

## Note

This is a pattern, not a fixed toolkit. How many sessions you run, which models, how often the timers fire, how much the seat may start without asking — all yours. Start with the seat and one child session, and add the timers once you're tired of asking "what's everything doing?". The durable idea is: *one session hands out the work, checks every report against the files, and brings you one decision at a time — and your approvals are always typed where they take effect.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/one-session-that-runs-the-others.md) lays out the maintainer's real version — the brief, what the two timer checks look for, how a report is checked, the restart note, and the things that went wrong — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
