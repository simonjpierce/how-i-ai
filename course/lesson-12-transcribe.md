# Lesson 12 — `/transcribe`

Drop in an audio file, get a formatted transcript with speaker labels, topic sections, and action items.

The lesson reads on its own. A short screencast — me transcribing a real meeting recording end-to-end — will pair with it when recorded.

## What it does

Runs whisper-cli on an audio file (or formats an already-raw transcript), then post-processes the result: speaker labels, topic-level subheadings, action items extracted into a dedicated section. Output is a tidy markdown file in your inbox, ready to act on or file under a project.

Supports `.mp3`, `.m4a`, `.wav`, `.aiff`, and URLs to audio.

## When to use it

- Meetings you've recorded (Zoom, Audio Hijack, your phone).
- Voice memos that have outgrown their app.
- Interview recordings.
- Any audio where the content matters and you don't want to listen to it twice.

## Try it

```
/transcribe /path/to/your/audio.m4a
```

Or drag the file into the Code tab and ask Claude to transcribe it. The skill picks up dependencies automatically — if `whisper-cli` isn't installed, it'll tell you the brew command to run.

## Quality notes

- **Speaker diarization** (telling speakers apart) requires `pyannote`. If it's not installed, you'll get a transcript without speaker labels — still useful, just one less feature.
- **Audio quality matters.** Phone recordings of in-person meetings are fine; remote calls with bad mics will produce more errors.
- **Names get mangled sometimes.** Whisper guesses at proper nouns. Skim the output and fix names before filing.

## What's next

[Lesson 13 — `/pdf-to-markdown`](./lesson-13-pdf-to-markdown.md). The complement to `/transcribe` — converting written reference material into vault-friendly markdown.
