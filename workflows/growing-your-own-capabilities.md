# Growing your own capabilities

Turn the work you keep repeating into reusable capabilities your AI can run on command — so your system doesn't stay the size it started, it grows itself one capability at a time.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Everything else in this repo describes a capability you might want. This one describes how new capabilities come to *exist* — and it's the part that matters most for getting to a system as capable as the one in [how it all fits together](./how-it-all-fits-together.md). The trap is to think the power is in the *list* of things your AI can do. It isn't. The power is in the **engine that keeps adding to the list** — because a system that mints its own new capabilities, week after week, ends up somewhere a fixed toolkit never reaches.

The mistake newcomers make is the opposite one: they try to build a big library of polished commands up front, copying someone else's. Those commands are over-fitted to the person who wrote them, they go stale, and you spend your effort maintaining tools you don't use. The capabilities that earn their place are the ones that *grow out of your actual work* — and they grow on a gradient, from a loose note to a trusted command, only formalising as far as the work justifies.

So the move is to stop treating "build a tool" as a separate project and instead let capabilities **accrete from friction and repetition.** You do a thing once as a normal task. The third time you find yourself doing it, you notice — and that noticing is the trigger to capture it.

## How it runs

The gradient has a few stops. You move a capability along it only as far as you actually need:

- **Notice the repeat.** The signal is doing the same shaped task a third time — the same kind of research dig, the same way you like a transcript formatted, the same checks before you trust a draft. Either you spot it, or you ask the AI to watch for it; either way, that's the cue to write it down rather than do it from scratch again.

- **Describe it before you build it.** Have the AI write the workflow up as a plain-language note first — what it does, the steps, what "done" looks like — not as code or a formal command. A description is cheap to change, and you'll change it a lot in the early days. (This whole repo is built on that principle: descriptions, not finished code, precisely because descriptions stay adaptable.)

- **Let it stabilise through use.** Run the described workflow a few more times by hand. Each run sands it — you find the missing step, the wrong default, the bit that needed a judgement call. Resist formalising early; a command frozen too soon just locks in the rough version.

- **Promote it to a command once the steps stop changing.** When the description has settled — you've used it several times and you're not editing it any more — ask the AI to turn it into a reusable command (in Claude Code these are *skills*: a short name like `/transcribe` that runs the saved workflow). Now it's one word instead of a re-explanation. Keep the plain description alongside it as the reference; the command is just the fast path to the same thing.

- **Fold the lesson home.** Whatever you learned building it — a preference, a default, a gotcha — gets written into your standing instructions or the AI's memory, so it shapes future work, not just this one command. (See [memory and context](./memory-and-context.md).)

**For capabilities that change the system itself, add one more step: a second model reviews the plan before you build.** Most new capabilities are low-stakes — if a formatting workflow is slightly wrong, you fix it next run. But some changes touch the machinery everything else depends on: a shared script, a command other commands call, a rule that fires every session. For those, write the change up as a short plan and have an *independent* second model (a different AI — the maintainer uses OpenAI's Codex on the command line) pressure-test it *before* implementation. A second model reading a plan cold catches the holes the first one talked itself past — the edge case, the thing that breaks two workflows downstream. Cheap insurance against a confident change that quietly breaks something. This is the same instinct as [the self-improvement loop](./the-self-improvement-loop.md), applied to building new things rather than fixing broken ones.

## What this does *not* do

It doesn't mean front-loading a big toolkit — the opposite. Start with **zero** saved commands and let the first one appear only when a task has proved, by repetition, that it's worth saving. It also isn't the AI inventing capabilities behind your back: you decide what's worth capturing and how far to formalise it; the AI carries the writing and the building. And promotion is a one-way ratchet you control, not an obligation — plenty of useful workflows live their whole life as a plain description you paste in when you need them, and never become a command at all. Formalise only what repetition has earned.

## Why this works

The reason most personal tool collections rot is that they're built ahead of need — polished, then abandoned. This inverts that: nothing gets formalised until use has proved it, so every command in your system is one you actually run, shaped by real practice rather than a guess about what you'd want. And the capabilities compound — each one you add is a faster building block for the next, so the system that builds your system gets quicker over time too. The engine that mints capabilities is itself a capability, and it's the one worth having first.

## Note

This is a pattern, not a fixed pipeline. The stops on the gradient are yours to shape — how long you leave a workflow as a description, whether a given capability ever becomes a command, when a change is "big enough" to warrant a second-model review. The durable idea is: *let capabilities grow out of repeated work, describe before you build, formalise only what use has earned — and your system keeps getting more capable on its own.* Paste this to your AI and build the version that fits how you work.
