# Reference — One session that runs the others

> **What this is.** The actual method behind [the *One session that runs the others* workflow](../workflows/one-session-that-runs-the-others.md), cleaned of the maintainer's personal specifics. A **starting point to adapt, not a drop-in.** It assumes the Claude desktop app's Code tab, where one session can start, message, read, and archive others; the behaviour described is what the maintainer saw in November 2026 and the app changes often, so test each point before relying on it.

## What the seat is given

The orchestrator is an ordinary session with a standing instruction file, not special software. Its instructions say, in order:

1. **Who it is.** "You run the day's work as linked sessions, check each session's turn against the files, direct the upkeep session, and relay the user's decisions word for word. You do not do the work yourself, and you do not fix breakdowns yourself."
2. **Where its state lives.** A restart note (below), a check log, and a short knowledge file of lessons, all in the notes vault.
3. **The hard limits** (see "What is never relayed").

It runs on the strongest model available; child sessions default to the next model down at high reasoning effort unless the user names another. The user's own words set this, and the seat records them with the date so a later session can't mistake a default for a ruling.

## Starting a session

The app offers a tool for starting a session with a title, a brief, a model, and an effort level. What the maintainer's seat does every time:

- **Say what it is first.** One bold title line and one sentence in the chat before the call, so the user sees what is being started and why.
- **Write a brief that stands alone.** The new session has none of the conversation. A brief carries: the user's own words that prompted it (quoted, with the date); the task; the files and folders to read first; how to proceed; the limits; what done looks like; and "do not message the orchestrator — your end-of-turn report reaches it automatically".
- **Name the limits in the words that matter.** "Nothing is sent, posted, published live, or written to a shared document or chat." An early brief that said only "nothing is sent" left a session free to edit a shared document.
- **Record it.** New work gets a line in the projects list in the same turn, or it is invisible to the next day's plan.

Two quirks worth knowing, both seen in November 2026:

- **A new session started at a lower effort than requested.** The app launched fresh sessions at medium effort whatever was passed, and applied a change only from the next turn. The working route: start the session with a one-line holding message ("reply ready and wait"), set its effort with the session-settings tool, then send the real brief as the second message. The process list does not show the effort a turn used; the session's own transcript does.
- **Sessions can't be started from every kind of turn.** A start was refused on a turn triggered by a timer or by another session's report, and while the user was driving the seat from a phone. So work that needs a new session waits for a message typed at the desktop, and the seat says so in one line; it does not work around the refusal.

## Checking a report

A note arrives when a child ends a turn, quoting the first few hundred characters of its report. The seat treats it as a pointer.

| The report says | The seat checks |
|---|---|
| "Committed and pushed" | The commit is on the remote's main branch (`git branch -r --contains <hash>`), and nothing local is unpushed |
| "Draft is in your mail drafts" | Reads the draft back: recipient, subject, and attachments |
| "Fix is live" | Fetches the live page and looks for the changed text |
| "File written" | The file exists, at that path, with the stated sections |
| "You approved this" | Finds the user's typed message in that session's transcript, and the question it answered |
| A count, total, or statistic | An independent re-count, by a different model where possible |

The last-but-one row matters most. A session will sometimes describe a past approval more broadly than it was given, or say it will ask and then proceed. The seat reads the transcript for the user's own words and the question they replied to. When it can't find them, it tells the user what it saw and asks the session to quote its authority — it does not undo anything itself. (When the approval does exist, it says so and withdraws the alarm.)

When reading another session's transcript, mask long unbroken strings before printing anything: users paste keys into windows.

One review, one fix pass is the rule for ordinary work. A builder builds, one independent check asks "would this fail or lose something in ordinary use?", the builder fixes what it finds, and the work proceeds. Re-review is kept for three cases: jobs that run unattended and change notes, calendar, or money; numbers in scientific outputs; and changes to shared machinery.

## The two timers

Both are scheduled prompts inside the seat's own session. In the maintainer's setup they are session-only and expire after seven days, so the first step of the daily check is to list the timers and re-create any that are missing or about to lapse.

**The daily check** (early morning) walks a numbered list kept in the vault. The rule for every item is *outcomes, not exit codes*: not "did the job run" but "did the draft reach the drafts folder", "is today's plan dated today and free of leftover clutter", "did the open-questions count fall". Each number is measured that morning; a figure copied from yesterday's log once cost a correction. Breakdowns go to the upkeep session as one ranked message with the evidence, ending "keep going through the list without stopping between items unless one needs the user's decision, stated in full" — a hand-off that names only the next item makes that session stop and wait an hour for the next nudge.

**The hourly check** runs one small script that prints, for each main session, its last activity, anything the user typed there in the last hour, and its latest report; then the plan usage figure. Its prompt ends "silent turn unless something changed that the user would act on". It never messages a session the user is mid-conversation in.

Both append one dated line to a check log. Times come from the clock (`date`), run in the same step that writes the line; estimated times drifted by up to two hours in a long session and were then copied into other notes.

## Questions and approvals

- **One question per message**, as the heading of the message, then why it matters, then numbered options with the recommended one first. A bare-number reply is echoed back ("your '1' answers …") before acting.
- **A pending question is restated in full or not mentioned.** A hook on the seat blocks replies that refer to an open question without restating it.
- **What is never relayed.** A "publish", a "send", a write to a shared database, or any approval that lowers a safeguard. The seat restates the child's question in its own reply, links the child's window, and says the answer must be typed there. In the maintainer's setup, the app's automatic permission check on the child judges the user's own latest message in that session, so a relayed go-ahead was refused anyway. Without that check, this rule is the only thing stopping a relayed yes.
- **What is relayed.** Answers that only steer drafting or preparation, passed word for word in quotation marks with the date.

## Closing sessions out

A session the seat started, whose work is finished with nothing waiting on the user, is asked to run the end-of-session routine (see [the session loop](../workflows/the-session-loop.md)). Anything that routine would ask the user is written into its handoff entry instead. The seat checks the close-out's commit and handoff entry, then archives the session. Three at a time at most, since their commits share one repository. Sessions the user is using as a running conversation, or that hold a decision for them, are theirs to close.

For daily agent runs: one session per agent per day, yesterday's closed and archived before today's starts.

## The restart note

One note, newest entry first, each entry stamped from the clock: what is running (with session ids), what is closed, the ordered queue of questions for the user, dated actions, and the first jobs for the next check. The seat re-reads its two newest entries after every summary of its conversation. Standing rules are listed only with the user's own words and the date beside them; a choice the seat made itself is labelled as its own drafting choice, so it can't harden into a rule the user never gave.

## Watching the budget

The app reports the plan's weekly usage and how full each session's working memory is. The seat reads both every hour. Past a threshold the user set (the maintainer's is three-quarters of the week), it stops starting new work and asks one question: move to another plan you hold, or wait for the reset. Any session past about 40% full gets a mid-session save at its next pause (see [managing your token budget](../workflows/managing-your-token-budget.md)).

## What went wrong, and the rule that came from it

- **A session told to rest can't wake itself.** If a step is tied to a clock time, the seat does the check itself or messages the session then.
- **"Resume" sent while a test run was still going** started a second run on top of it. Check live processes and read the session's last message first; send the nudge in a later step.
- **A status page said a paused job was "working".** Registers are pointers; the check reads the output.
- **Two sessions for the same agent** were open at once after a publish step was handed to yesterday's session. One session per agent, and the run that prepares a fix publishes it.
- **The seat wrote a rule it had made up as if the user had said it.** Hence the quote-and-date requirement above.
- **A report was relayed whole.** The user wants the highest-value item, then the next once that one is settled.

## What stays yours

Which work gets a session; every approval that sends, publishes, pays, or writes somewhere shared; the model and effort settings; the usage threshold; and whether a session is finished. The seat's job is to make each of those a short, well-posed question — and to make sure nothing else needs you.
