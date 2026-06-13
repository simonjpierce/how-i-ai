# Surfacing conflicts, not smoothing them

When you build up notes over months — research syntheses, project notes, a paper, a grant — you keep hitting moments where the evidence doesn't line up. Two papers disagree. A new study contradicts something you wrote last year. A number came from a conversation and was never checked against the primary record. This is the discipline for handling those moments without quietly losing what's unresolved.

This is an idea file. Paste it into Claude Code and it'll wire the convention into how it works with you: a marker it uses, where conflicts get recorded, and the core rule written into your standing instructions so it holds every session.

## The core idea

The tempting move, when evidence is in tension, is to pick a version in your head and write the note as if it were settled. It reads cleanly — and it silently destroys information. The next reader (including a future you) can no longer tell the question was ever open, or that the confident sentence is really a guess.

The fix is a small, strict habit: when something is uncertain or sources conflict, you *flag it* rather than resolve it. A short, consistent marker — this guide uses `TODO/VERIFY`, pick your own if you like — goes inline for an isolated unverified fact; a dedicated "Conflicts / needs review" section handles a multi-source disagreement that needs describing. The marker stays until the question is *genuinely* settled, and when it's settled you remove it and record how. The note then always reflects the true state of the evidence, not a false sense of consensus.

This matters more with an AI in the loop, not less. A model asked to integrate a new source will, left alone, smooth the disagreement into a fluent paragraph — false confidence is its default failure mode, and it's the thing scientists most rightly distrust. This convention is how you make "I'm not sure yet" a first-class, visible outcome instead of something that gets written over.

## How it runs

- **Flag, don't resolve.** The moment something is unverified or two sources clash, drop the marker — inline for a single fact, a "Conflicts / needs review" section for a real disagreement. Describe what's uncertain in plain language and cite the sources in tension. Don't attempt resolution yet.
- **Write conservatively in the meantime.** If the text has to be updated before the question closes, use cautious, *attributed* language — "Smith et al. (2024) suggest…", "appears to", "evidence is mixed" — rather than a flat assertion. Never delete an earlier claim without saying why.
- **Let time pass.** "Park it and wait for better evidence" is a valid, often correct outcome. Don't force convergence just to make a note look finished.
- **Revisit before anything ships.** Open markers get reviewed at the natural checkpoints — before a submission, a report, a talk — so an unverified fact never rides out into a high-stakes document.
- **Clear resolved markers promptly.** A `TODO/VERIFY` left on a question that's actually settled is as corrosive as a missing one — it creates false uncertainty and erodes trust in the whole record. When it's resolved, remove it and note what resolved it.

The one piece of machinery this needs is a way to *find the markers again*: a consistent token your tooling (or your eyes) can search for. An automated nightly scan is nice if you have one, but a plain search before any major output does the same job — the discipline is the point, not the automation.

## Put the principle in your standing instructions

Because this is a *behaviour* you want every session, its real home is your standing-instructions file (`CLAUDE.md`), not a doc you read once. When your AI sets this up, have it add a short governing line there — something like: *"When sources conflict or evidence is mixed, surface the disagreement rather than smoothing it away. Flag open questions with `TODO/VERIFY` rather than resolving them silently."* That one line, loaded automatically every session, is what turns the convention from a good intention into the AI's default. It belongs in standing instructions, not in learned memory — memory is for things the AI picks up over time, whereas this is a rule you're setting deliberately.

## What this does *not* do

It doesn't make the call for you — it keeps the question visible until *you* (or stronger evidence) settle it. It isn't a licence to leave everything open: markers are meant to be cleared, and a note that's all caveats and no conclusions is its own failure. And it's not just for "synthesis notes" — it applies to anything that makes a factual claim: project notes, drafts, plans, chapters.

## Why this works

Uncertainty is information. The instinct to tidy it away under time pressure is exactly what loses it — and an AI, eager to be helpful, tidies harder than you would. Making the open question explicit costs a marker and a sentence; recovering a silently-dropped one costs you a wrong claim in a paper. A record you can trust is worth more than a record that merely looks finished.

## Note

This is a convention, not a tool — there's nothing to install. Adopting it means three small choices: the marker token you'll use, where conflicts get recorded (inline vs a section), and how you'll find the markers again before something ships. Everything else is the habit itself. The durable idea is: *make uncertainty visible and attributed, leave it visible until it's genuinely resolved, then clear it cleanly.* Paste this to your AI, have it put the principle in your standing instructions, and hold the line from there.
