# Working with a co-author

*When two people write a paper and both have an AI, the shared repository becomes the paper's home base. This is how to set the ground rules so the two assistants help each other instead of overwriting each other.*

## The core idea

The moment a second person joins a paper, the usual setup breaks. You have a copy, they have a copy, and both of your AI assistants are confidently working from whichever version happens to be on that laptop. Nobody is lying; the record has just forked.

The fix is to name one place as home base — a shared repository both of you can write to — and then tell *both* assistants, in writing, how to behave towards it. That written brief is the whole trick, and it's worth putting in the repository itself so it can't be lost in a chat.

Four rules cover almost everything:

- **Pull before you start, push when you stop.** Every session begins by picking up whatever the other person's assistant did since last time. Assume the shared copy is ahead of yours.
- **One running notebook, one entry per piece of work.** A dated, append-only file at the top of the repository saying what was done, what came out, what was decided and where the evidence lives. It's how a collaborator — or you in three weeks — gets back up to speed without a phone call.
- **Add, don't overwrite.** Your assistant writes its own files and edits the shared ones you've agreed on. It does not silently change the other author's data, scripts, or notes.
- **Nothing is deleted — superseded material moves to an archive folder.** When a corrected dataset replaces the old one, the old one stays, clearly marked as not the working version. A collaborator coming back in a month needs to see what changed, not find a hole.

Keep the repository's front page honest as a map: what each folder is, what the current working file is, what's in flight. It's the first thing the other person's AI reads.

## How it runs

**Write the brief down and put it in the repository.** Telling your co-author on a call how their assistant should behave doesn't survive the call. Have your AI write them a short setup file — what home base is, what to install, what to run at the start and end of a session, what it should never do on its own — and commit it alongside the work. They paste it into their assistant once and ask it to keep the standing parts; from then on both assistants are running the same rules. It's also the honest test of whether your own setup is teachable: if you can't write it down, it isn't a system yet.

**Record the working calls in short stretches and feed each one in while you're still talking.** See [Transcription](./transcription.md) — the segment-by-segment pattern turns a call into a working session where the AI reads back a plan, you both correct it, and you say "yes" out loud before moving on. Each decision lands in the notebook with the speaker and the date.

**Tell the assistant what it must not decide.** When it's classifying or correcting records on your behalf, give it a hard boundary: don't look at images, don't guess when the text is ambiguous, and "unsure" is a correct answer that costs nothing. An assistant that resolves ambiguity to be helpful quietly manufactures data. The hard cases come to a person, with a link to the source record so checking is one click.

## Sharing the method without sharing the paper

Collaborators will ask to see work well before it's ready, and the honest answer — "not yet" — costs you goodwill and repeat conversations. There's a better third option: split the *method* out from the *paper*.

While the analysis is still in progress, have your AI build a small, separate, public repository that carries just the reusable part: the classification scheme or protocol, how to enter data, worked examples, and what to report. Write it site-neutral — for anyone in your field, not tuned to your own study area — and assume the reader may not use AI at all, while telling them how to if they want to. Then point people at that, and keep the working repository private.

It pays three ways. Your collaborators can start straight away instead of waiting for you. Their feedback comes back while you can still act on it, which makes the published method better. And when the paper does come out, the thing people actually need in order to use it already exists, is already tested by real users, and is already the natural home for whatever protocol or tool you build next. Every rule you settle in the main analysis gets copied across as a dated change to the public version — that's the loop that keeps it honest.

## What this does *not* do

It doesn't replace talking to your co-author. The repository and the notebook carry the record; the calls carry the judgement. And it doesn't make the AI a co-author: every decision in the notebook has a human's name on it.
