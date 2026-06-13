# Transcription

Turn talking — meetings, interviews, field notes, a voice memo on a walk — into clean, readable text with the action items already pulled out, instead of an audio file you'll never play back.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (which transcription tool, where files land) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

*What you'll need: a local transcription engine, which your AI can install for you — but it's the one genuinely fiddly piece, so let it handle the setup rather than wrestling it yourself. The multi-speaker labelling step additionally needs a free Hugging Face account and access token; skip that step entirely if you only ever record yourself.*

## The core idea

Speech is the fastest way to get a thought out of your head and the worst way to store it. A recording is a dead end: to get anything back out, you have to sit and re-listen in real time, which nobody does. So the thinking evaporates.

The fix is to make spoken input a *first-class source* — something that flows into your notes as readable, usable text, automatically. You record; it gets transcribed; and then, crucially, it gets *shaped into something you'd actually read* rather than dumped as a wall of raw words.

"Shaped" means a few specific things: speaker labels where there's more than one voice, topic headings so you can skim, the rambles and false starts tidied up *without changing what was said* — and the part that earns its keep, the **action items and ideas lifted out** and sent where they belong, so nothing said out loud quietly gets lost.

That turns three otherwise-throwaway moments into durable material almost for free: a meeting becomes a clean record plus your to-do list; an interview or talk becomes a transcript you can quote and search; and thinking out loud — a voice note on a morning walk — becomes a written input you can actually build on.

## How it runs

**Record however suits the moment** — the pipeline doesn't care what made the audio, only that a file lands somewhere it can find it. Two capture paths cover most of it. For anything live and two-sided — a video call, a meeting, an interview — the piece most people don't know to look for is an *audio-routing app* that records the other side of the conversation *and* your own microphone at once, into one file; the maintainer uses [Audio Hijack](https://rogueamoeba.com/audiohijack/) (macOS), set to drop each recording into a folder the pipeline watches. For thinking out loud — a voice note on a morning walk — your phone's or watch's built-in voice-memo app is all you need; the clip syncs back to your computer and gets picked up the same way. Whatever you record with, the rest of the pipeline is identical from here.

**Transcribe locally.** A speech-to-text model that runs on your own machine — Whisper, specifically the [`whisper.cpp`](https://github.com/ggml-org/whisper.cpp) build, which is fast on a modern laptop and leans on its graphics chip — turns the audio into raw text without the recording ever leaving your computer. That keeps sensitive material (anything to do with money, staff, or health) off other people's servers, and it's free to run as often as you like.

**Label the speakers — only when there's more than one.** For a multi-voice recording, a separate "who spoke when" model (the maintainer uses [pyannote](https://github.com/pyannote/pyannote-audio)) tags each stretch of speech, so a meeting comes back as a readable back-and-forth instead of an undifferentiated wall. Skip it for a solo dictation — there's one voice to label, so it's pure overhead.

**Format it.** The AI then does the readable-document pass: topic sections and light clean-up that keeps every point intact. It pulls out *your* to-dos and ideas and files them — to-dos to your task manager, ideas to wherever you keep them — so the record and the actions both exist without you transcribing anything by hand.

**Keep the raw text underneath.** The cleaned-up version sits on top; the original verbatim transcript is preserved below it. If the formatting ever drops or garbles something, the source of truth is one scroll away — you're never trusting the tidy version blind.

One optional refinement, worth it only if you have a recurring cast: off-the-shelf transcription reliably mangles the same handful of names, places, and specialist terms that come up in your world every week. You fix this in two places, and the order matters: feed the transcriber a short vocabulary list up front to bias the spelling — *and*, because that alone won't stop a name losing out to a more common sound-alike (your colleague Justine keeps coming back as Christine), run a second pass *after* transcription that re-checks the text against a list of names you maintain and corrects the usual mistakes. The post-transcription pass is the part that actually works; the vocabulary hint by itself isn't enough. Each new misspelling you spot gets added to the list, so the system quietly gets more accurate the more you use it. Skip this entirely if your recordings are plain everyday English — it's pure overhead unless names are actually a problem.

A dictated note in the morning is a natural way to kick off [the agent fleet](./the-agent-fleet.md); a formatted interview transcript is good raw material for [writing](./writing-and-review.md).

## What this does *not* do

It produces a faithful transcript, not a summary — it preserves what was said and doesn't quietly drop or paraphrase content away. The clean-up tidies grammar and false starts; it must not invent words, fill inaudible gaps with guesses, or smooth meaning into something that wasn't said. Overlapping voices and unclear passages get *flagged*, not fabricated. And it captures *your* action items for *your* task list — other people's commitments stay in the written record, not in your to-dos.

## Note

This is a pattern, not a fixed toolchain. The parts that are yours to shape: how you capture the audio, which local transcription model you run, whether you bother with speaker labelling at all, how much formatting you want, where the action items and ideas go, and whether the recurring-names correction layer is worth building. It assumes Claude Code as the main driver. The durable idea is: *make speech a real source — transcribe it locally, shape it so you'll actually read it, and lift out what needs doing.* Paste this to your AI and build the version that fits how you talk and work.
