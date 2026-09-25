# When a rule should be code

How to tell which of your standing instructions the AI will actually follow, and what to do about the ones it won't: turn them into small scripts that run at the moment the mistake would happen.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Most of teaching an AI how you work is writing rules down: in your standing-instructions file, in its memory, in the commands you save. That works remarkably well for judgement — tone, priorities, who's who. It fails, quietly and repeatedly, for a particular class of rule: the mechanical ones that have to fire at a specific moment, in every session, including the sessions that never read the file where you wrote them.

The maintainer measured this. Four fixes shipped in one week for recurring failures; three were documentation, one was a script. The script cut its failure class by 57%. All three documentation fixes did nothing, and one class got *worse* — five failures a week became thirteen — while its rule sat in two prominent places. The same shape repeated on three other problems over the following months, and for these mechanical rules the pattern held every time: **prose fixes measured at zero, a hook halved the class.** Measure your own recurring failures before generalising — but expect the same.

The reason is structural, not a failing of the model. A rule in a file addresses a reader who has already decided to act and happens to have the file loaded. Scheduled jobs, subagents and sessions deep in a task don't. A **hook** — a small script Claude Code runs automatically before or after a tool call, when you send a message, or when a session starts — sits in the execution path itself. Nothing has to remember it.

So the question to ask of every rule you find yourself writing twice is: *is this judgement, or is this mechanics?* Judgement stays prose. Mechanics becomes code.

## The pieces

- **Recognise the candidates.** The tell is repetition without improvement: the same friction logged three times; a rule you've reworded twice; anything that must reach unattended runs. Typical mechanics: "don't read that whole file", "quote this path", "never commit from that branch", "this file has a size cap", "don't write through that symlink", "check the folder isn't hiding nested files before you propose deleting it".
- **Warn or block — decide deliberately.** A *block* (exit code 2) stops the tool call and puts your message in front of the model. A *warn* lets it run and adds a note the model reads. The maintainer's rule: block only when the action was going to fail anyway or the harm is real and irreversible, and always carry the exact correct retry in the message — a blocked call in an overnight run must cost one tool call, not the whole task. Warn for everything legitimate-but-wasteful; a week of warnings trains the habit.
- **Fail open, always.** A hook that errors must exit silently and let the tool run. Missing dependency, unreadable input, a path that doesn't exist — none of these may ever become a false block. The guard exists to prevent one failure; it must never introduce another.
- **Talk to the model, not the terminal.** This one cost the maintainer months. A hook that prints advice and exits 0 writes to a channel the model does not read. Ten hooks fired 150 times a week into nothing, and their "fixes" were scored as working. Use the structured output field for model-facing context; check the harness documentation for its current name.
- **Write the "why" and a measurement target into the header.** Every hook opens with the failure it prevents, the evidence that prose didn't work, the date, and a falsifiable target: *"oversized-read failures below 5 a week at the next review."* A later session — or a later you — can then decide whether it earned its place instead of guessing.
- **Keep a firing ledger.** Wrap each hook in a tiny runner that counts silent fires and logs every warn, block or error with the session and tool. Without it, "which hooks have ever blocked anything?" is unanswerable, and dead hooks accumulate. With it, you can see which hooks earn their place — and then test the exact case before cutting one: a block that fired 348 times in a fortnight looked like pure cost, was downgraded, and went back to a block within the hour when a live test showed the hazard was still real.
- **Test the hooks themselves.** A hook that edits behaviour for every session is infrastructure. A small test harness that feeds each one sample inputs, plus a meta-hook that runs the tests whenever a hook file is edited, catches the broken guard before it silently blocks a night's work.

## What this does *not* do

It doesn't replace the written rules — most of what you teach the AI is judgement, and judgement belongs in prose it can reason with. It's not a way to lock the AI down; the maintainer's hooks mostly *warn*, and the few blocks all carry their own fix. And it isn't free: every hook is a script you own, so build one only after the repetition has proved the rule is mechanical, and cut it the moment the ledger shows it stopped earning its keep.

## Why this works

A rule in a file competes with everything else in the AI's context for attention, and loses at exactly the moments that matter — long sessions, unattended runs, subagents with a narrow brief. A hook doesn't compete. It runs. And because it runs the same way every time, you can measure it, which is what lets you keep the ones that work and delete the ones that don't — the discipline that keeps this from becoming a thicket.

## Note

This is a pattern, not a fixed toolkit. Which rules you promote, how many you're willing to maintain, whether you build the ledger and tests or just the hooks — all yours. The durable idea is: *judgement stays as prose the AI reasons with; mechanics that must fire every time becomes a small script in the execution path, with a written reason, a measurable target, and a fail-open guarantee.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/when-a-rule-should-be-code.md) lays out the maintainer's real version — the hook anatomy, the warn/block rules, the model-facing output channel, the ledger and the test harness — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
