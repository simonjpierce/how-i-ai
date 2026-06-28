# Reference — The session loop

> **What this is.** The actual method behind [the *Session loop* workflow](../workflows/the-session-loop.md), cleaned of the maintainer's personal specifics (real paths, names, machine state). It's a **starting point to adapt, not a drop-in command** — your notes vault and AI setup are shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Two terms: an AI's **context window** is its short-term working memory for one conversation — it's wiped when the chat ends, so nothing in it survives to tomorrow. **Compaction** is when a long session's history is auto-summarised to free up room mid-conversation; useful, but it can drop the thread you were mid-way through. Both are why the durable files below matter: the chat is fragile, the notes are not.

## The core habit

An AI session starts blank — it has no memory of the last one. So the work can't live in the conversation; it has to live in a small set of durable notes the conversation flows through. Three moves, run every session:

- **Orient at the start** — the AI reads where you actually left off before doing anything.
- **Capture as you go** — decisions, friction, and open questions get written down *during* the work, not reconstructed at the end.
- **Hand off at the end** — a short closing note tells the next session where things stand and what to do first.

The maintainer keeps these notes as plain markdown in an Obsidian vault, but any folder of text files your AI can read and write will do.

## The handoff log — the spine

One running file, newest entry on top. Each session, before anything else, the AI reads the **top two or three entries** and the current state of the active project — then gives you a two-line "here's where we are." That's the whole orientation; it costs seconds and means you never re-brief from scratch.

At session end, the AI **prepends** a new entry: what was done, current state (complete, or what's pending), what the next session should do or read first. Prepending is the load-bearing detail — *the next session reads the top of this file first*, so the most recent context is the first thing it sees.

**Open every entry with a one-line focus pointer.** The first line names the single immediate next action — a `> read this first` banner. This is the insurance against compaction: if a long session's memory gets summarised away mid-thread, the next start lands on the right thing instead of the top of a generic log. Cheap when it's not needed, decisive when it is.

**One caution with parallel sessions.** If you run more than one AI session at once, two of them can write to the handoff log between one's read and its write — the second write clobbers the first. The robust fix is to splice the new entry in with a single read-modify-write (one short script that reads the file, inserts after the intro, writes once), rather than an edit anchored on a line that may have moved. Tag each entry with a short session marker so a concurrent run knows which entries are *yours* to update versus a sibling's to leave alone.

## The two logs — so decisions and snags aren't re-litigated

- **Decision log.** What you chose *and the reasoning*, dated. This is what stops a future session silently re-opening a settled question or contradicting it. When a decision is provisional, note a revisit-by date so it gets re-examined rather than ossifying.
- **Friction log.** Anything that broke, took a workaround, or wasted time — so the same snag doesn't bite twice. Give each entry a consistent status tag (open / stuck / resolved) on its own heading line, so a start-of-session scan can surface anything that's been sitting open too long and offer to walk it. Resolved entries move to an archive section; don't leave a stale "still open" flag eroding trust in the record.

**Open questions get a marker, not a guess.** When something is unverified or two sources disagree, the AI leaves a short searchable tag in the note (something like `TODO/VERIFY:`) and writes in cautious, attributed language rather than quietly picking a version. An honest "this is still open" beats a confident sentence hiding a guess — and a resolved marker gets cleared promptly so it doesn't go stale.

## Pausing a thread cleanly (resume cold)

Separate from the end-of-session handoff: a way to set down *one half-finished sub-thread* mid-stream so a fresh session — even on another machine — picks it up cold. The move writes a small **state-of-play note** for that topic: what it is, where it got to, what's next, and a self-contained "pickup prompt" written for an AI with zero conversation context (full paths, the concrete first action, no in-jokes). Pair it with a reminder pointing back to the note. One topic, one note — resuming and re-pausing updates the same note rather than spawning a v2.

This is distinct from the full end-of-session handoff (which sweeps everything) and from daily planning (a separate "what should I work on" ritual). Use it when you're parking a specific piece of work, not winding down the whole session.

## The end-of-session sweep

The closing pass does three things beyond writing the handoff entry: it **distils any durable lesson** — a preference, a gotcha, a thing that worked — into the AI's longer-term memory so it sticks across sessions; it **brings related documents back into agreement**, because a decision made in one place usually needs to ripple to two or three others; and it **walks any loose ends** so each gets either closed now or an explicit, visible disposition. That last part matters: a wrapped session reads as "done," so an unfinished item with no owner rots silently. Give every open loop a named next step.

The doc-sync sweep works far better if your main project note carries a small **artifacts list** — a few lines naming every file, folder, or output the project owns and where each lives. With that list the AI reconciles exactly those files instead of guessing from a search, fixes the mechanical drift itself, and pauses to ask you only about judgement calls (rewriting a description, removing content, changing scope). Keeping the list current is the one bit of upkeep that makes every future sweep reliable.

## What stays yours

Where the logs live, how formal the closing pass is, which marker token flags an open question, whether you keep separate files or one combined notebook — all adapt to your setup. The transferable spine is just: *start from where you left off, capture honestly as you go, hand off cleanly with the next action on top — so the work is one continuous body instead of a pile of disconnected chats.* It only pays off if the capture is honest: a handoff that papers over the messy bits, or a "resolved" tag on a question that's still open, makes the next session worse, not better. Aim for a record you can trust, not a tidy-looking one.
