---
name: transcribe
description: Transcribe and format audio recordings or raw transcripts. Accepts audio files (.mp3, .m4a, .wav, .aiff), raw transcript .md files, or URLs to audio. Runs whisper-cli, formats with speaker labels and topic sections, and extracts TODOs/IDEAs. Also use when the user says "transcribe this", "format this transcript", "transcribe this recording", or "transcribe this audio".
allowed-tools: Read, Write, Bash, Edit, Glob, Grep, AskUserQuestion, Agent, mcp__qmd__query, mcp__qmd__get
---

Transcribe audio and/or format raw transcripts into readable Obsidian notes. Takes a file path or URL as `$ARGUMENTS`.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.

### Known persistent misrecognitions

Whisper's `--prompt` biases orthography, not phoneme selection — so prompt-listed names still lose to phonetically similar, higher-frequency alternatives. The durable fix is Step 3b-iii (post-hoc roster-constrained LLM correction); these two cases are the canonical examples:

- **"Justine" → "Christine"** (2026-03-30): Indonesia trip admin. Handled by roster `whisper_misreads: [Christine]` on Justine's entry.
- **"Krista" → "Chris"** (2026-04-04): Kaikoura sperm whale researcher. Handled by roster `whisper_misreads: [Chris, Christa, Christer]` on Krista van der Linde's entry. (R4 prompt hygiene applied 2026-04-19: dedupe'd "Chris" in PROMPT; moved Krista + Justine dead last in the PROMPT tail.)

### PROMPT vocabulary limitation — phonetically similar names

PROMPT hints do not reliably override Whisper's phoneme-level preference when two names share a similar sound pattern (e.g. -stine/-stine, -elle/-ella). A name being in the PROMPT is **not a guarantee** it will be transcribed correctly. Step 3b-iii handles this by running a roster-constrained LLM correction pass over the decoded transcript; the roster's `whisper_misreads` field is where observed failures are codified so they flag automatically on future runs.

### Corrector LLM canonicalises to the wrong roster entry — when the right entry is missing

Observed 2026-04-22 (Full Circle Moz meeting). Whisper produced `OMIN`; the corrector with Mozambique meeting context found `Oman` in the roster (a real MMF programme), and confidently applied `OMIN → Oman`. Actual referent was **Pomene** — a Mozambican coastal Marine Reserve missing from the roster at the time. Phonetic+semantic match to a real entry beats "no entry exists" every time, so the correction looked plausible and only got caught on review.

**During Step 3b-iii review**, scan the high-confidence corrections list for any case where the surrounding context belongs to a different region/programme than the canonicalised target. Examples to flag: "Oman" in a meeting about Mozambican CCPs; "Tanzania" in an Indonesia funding discussion; a person from one country programme appearing in another country's meeting. Then re-check the verbatim and roster — if the right referent is missing from the roster, add it with explicit disambiguation notes against the false-positive entry, and correct the formatted version. Full case write-up in `05_AI WORKFLOW/CLAUDE/Processes/Meeting Transcription Pipeline.md` *Failure modes / gotchas*.

### Phonetic near-homophones between two real roster entries (Stefan / Steffen pattern)

Observed 2026-04-24 (Full Circle Tanzania meeting). Whisper rendered **Steffen Bergholz** (MMF Board, ship-strike / ESG partnership, owner of the AIS/shipping-viz website) as `Stefan` throughout. The phonetic pre-screen did NOT flag it, because `Stefan` matches the roster entry **Stefan Bach** (Maersk Oil, Qatar Whale Shark Research Project) exactly. The LLM never saw the token, so no correction was attempted. The error only surfaced when Simon reviewed the formatted transcript and said "Steffen not Stefan."

This is a different failure mode from the OMIN/Pomene case: there, the right referent was missing from the roster. Here, both the correct referent (Steffen) and the false-positive referent (Stefan Bach) were already in the roster, but phonetic pre-screen treats an exact match to any entry as "no ambiguity."

**Mitigation #1 — roster:** for any entry whose canonical first name collides phonetically with another entry's canonical, add the other name to `whisper_misreads` with a tight context-based disambiguation note (already done for Steffen: `whisper_misreads: [Stefan, Stephen, Steven]`, context specifies shipping/ESG/AIS context → Steffen, Qatar/Maersk/oil context → Stefan Bach). This forces all `Stefan` tokens to the LLM for in-context decision.

**Mitigation #2 — author-side (this skill):** NEVER hallucinate surnames or full names in the `--context` string passed to `correct_transcript.py`. The LLM treats `--context` as ground truth. In the 2026-04-24 meeting I passed `"AIS website project for Stefan Pieterse"` — I invented the surname "Pieterse" entirely. This biased the LLM away from flagging `Stefan → Steffen` because my context claimed Stefan was the right referent. **Rule: use only first names actually spoken in the transcript, and only surnames that appear verbatim in the transcript or in your pre-existing knowledge of the session. When unsure, use just the first name or omit the person altogether.**

**Same failure observed 2026-04-29 (Brisbane post-board voice memo).** Whisper rendered "Mark Mark Erdmann" (duplicate Mark; Mark Erdmann is in the PROMPT). Actual referent was **Mark Hackney** (MMF board chair) — the speaker was discussing MMF *board updates* as a format reference. I passed `"Mark Erdmann (marine biologist regular updates reference)"` in `--context`, again inventing the framing. The corrector matched the existing "Mark Erdmann" token to the existing roster entry under context I had biased. **Both Mark Hackney and Mark Erdmann are first-name homophones in the roster** — same Stefan/Steffen pattern, different surnames. Author-side rule is now even tighter: when the transcript contains a *first name only* that has multiple roster matches, do NOT include any surname in `--context` even if you "think" you know — let the LLM see the ambiguity. Better still, omit the person entirely from `--context` and rely on roster context tags. The right thing for the Brisbane memo would have been `--context "Brisbane solo voice memo after MMF board meeting; topics: board pack workflow, comms/fundraising strategy"` — no person names at all in that string for the comms-pipeline section.

**Mitigation #3 — review pattern:** during Step 3b-iii review, for every *proper-name* high-confidence correction AND every *proper-name* non-correction (i.e. a first name that matched a roster entry exactly), cross-reference the meeting-topic context against the roster entry's `context` field. If the topic doesn't match (e.g. a `Stefan` reference in an AIS/shipping context flags the roster's Stefan Bach as a Qatar oil contact), treat as ambiguous and surface for review.

### Roster YAML failure on corrector load — quote multi-clause `context:` values

Observed twice in one corrector run on 2026-04-29 (MMF board meeting). Symptom: `correct_transcript.py` exits 1 immediately with `yaml.scanner.ScannerError: mapping values are not allowed here` pointing at a `context:` value containing `: ` (colon-space). Root cause: any unquoted `context:` value with a colon in the prose parses as a nested mapping. The roster header has a "YAML gotcha" note that warns against this; even with the warning, it's an easy slip.

**Recurring sources of the failure:**
1. **Author error** — adding a `context:` value with a `disambiguate by context: ...` or `NOTE: ...` clause without wrapping in quotes.
2. **Linter / auto-modification** — when an entry's role changes (e.g. `Mark Hackney → Board Chair`), an auto-process appears to inject disambiguation language into related entries (e.g. `Mark Erdmann`'s context now reads `... NOT Mark Hackney (Board Chair) — disambiguate by topic: ...`). The auto-modification doesn't validate YAML.

**Pre-flight validator (use when corrector fails YAML):** parse each `## <Section>` fenced YAML block independently with `yaml.safe_load`, plus regex-scan all unquoted `context:` lines for the `: ` substring. The two violations on 2026-04-29 were caught instantly. Inline pattern:

```python
import re, yaml
text = open(ROSTER).read()
for name, body in re.findall(r"^## ([A-Za-z]+)\s*$.*?```yaml\s*\n(.*?)\n```", text, re.DOTALL | re.MULTILINE):
    try: yaml.safe_load(body); print(f"{name}: OK")
    except Exception as e: print(f"{name}: FAIL", e)
for ln, line in enumerate(text.splitlines(), 1):
    m = re.match(r"^(\s+)context:\s+(.+)$", line)
    if m and not m.group(2).startswith('"') and ": " in m.group(2): print(f"L{ln}: {line[:160]}")
```

**Fix:** wrap the offending value in double quotes (`context: "..."`). Don't try to thread the needle by rephrasing prose to avoid `: ` — the cost of quotes is zero.

**Author-side rule for THIS skill when adding to the roster:** any `context:` value containing more than one clause (period, em-dash, colon) → wrap in double quotes by default.


## Steps

### 1. Detect input type

Examine `$ARGUMENTS` to determine the input type:

- **Audio file** (`.mp3`, `.m4a`, `.wav`, `.aiff`, `.opus`, `.ogg`) → go to Step 1b. Note: `transcribe.sh` only accepts `.mp3`, `.m4a`, `.wav`, `.aiff` directly. For `.opus`/`.ogg` files, convert first with `ffmpeg -i "INPUT" -ar 16000 -ac 1 "/tmp/transcribe_converted.wav"`, run transcribe.sh on the wav, then clean up the temp file.
- **Video file** (`.mp4`, `.mov`, `.mkv`, `.webm`) → extract audio first with `ffmpeg -i "INPUT" -vn -acodec libmp3lame -q:a 2 "/tmp/transcribe_extracted.mp3"`, then go to Step 1b with the extracted MP3. Clean up the temp file after transcription. Note: `transcribe.sh` rejects video files directly — audio extraction is required.
- **Markdown file** (`.md` in `00_INBOX/TRANSCRIPTS/` or elsewhere) → go to Step 3 (context gathering). This is a raw transcript that needs formatting only.
- **YouTube URL** → tell the user to use `/youtube` instead (it has video-specific steps like relevance review and embedded player). Stop here.
- **Direct audio URL** (URL ending in `.mp3`, `.m4a`, `.wav`, etc.) → go to Step 1b
- **Other URL** → go to Step 1b
- **Empty or missing** → ask the user for the file path or URL

### 1c. Multiple files representing one continuous recording

If the user passes multiple audio paths or signals that the recording is split across files ("5 files", "split across files", "continuous monologue across files", "all one conversation"), treat them as a single conversation rather than independent recordings:

1. **Confirm file order** with the user. Filenames may not sort lexicographically — e.g. `Bris 10 May 1.m4a` ... `Bris 10 May 5.m4a` does, but if there are 10+ files `1, 2, 3, ..., 10` will break naive sort. Don't assume.
2. **Transcribe sequentially, not in parallel.** whisper-cli competes for the same Apple Silicon GPU; parallel runs slow each other down. Cleanest pattern is a single background bash `for` loop:
   ```bash
   for n in 1 2 3 4 5; do
     "/Users/simonjpierce/Music/Audio Hijack/transcribe.sh" "/path/to/Title ${n}.m4a"
   done
   ```
   Run in background, monitor progress with `tail -f` over the output file scoped to start/finish markers.
3. **Combine the raw `.md` outputs** into one canonical raw transcript at `00_INBOX/TRANSCRIPTS/YYYY-MM-DD — Title (Whisper raw).md` with `<!-- File N of M -->` comments between fragments and YAML frontmatter listing the source `.m4a` files in a `files: [...]` array.
4. **Archive individual fragments.** Move each per-file `.md` + `.json` pair to `00_INBOX/TRANSCRIPTS/Archive/<descriptive-folder>/` so they don't clutter the inbox.
5. **Run the corrector once on the combined raw** (Step 3b-iii). A single pass over the full conversation gives better contextual disambiguation than per-fragment passes — the corrector LLM sees the whole topic flow, including names introduced in one fragment and used in another.
6. **Format as a single continuous note** with topic headings (Step 4) — do NOT preserve file-fragment boundaries in the formatted output. Speakers don't think in file boundaries, only in topics.

Confirmed 2026-05-10: Brisbane Post-Sharks International monologue split across 5 files (`Bris 10 May 1.m4a` – `Bris 10 May 5.m4a`, ~27 MB total). Sequential transcription via `for` loop in background bash, single corrector pass on the combined raw, topic-organised formatted output.

### 1b. Solo or multi-speaker? (audio inputs only)

Before transcription, ask the user: **"Solo recording or multi-speaker meeting?"**

This determines whether pyannote diarization is attempted. Diarization adds significant processing time. Most recordings are solo voice memos — skip diarization for those entirely.

- **Solo** (default) → transcribe without diarization
- **Multi-speaker** → transcribe with `--diarize` flag (attempts pyannote if venv is functional)

If the user invoked this from Telegram with a voice memo or explicitly said "my voice notes" / "monologue" / similar, infer solo and skip this question.

### 2. Transcribe with Whisper (local audio file)

Run the existing transcription script:

```bash
# Solo (default):
"/Users/simonjpierce/Music/Audio Hijack/transcribe.sh" "AUDIO_FILE_PATH"

# Multi-speaker (adds pyannote diarization):
"/Users/simonjpierce/Music/Audio Hijack/transcribe.sh" --diarize "AUDIO_FILE_PATH"
```

This handles ffmpeg conversion, whisper-cli with domain vocabulary, and hallucination loop stripping. The `--diarize` flag enables pyannote speaker diarization (requires functional venv). Output lands in `00_INBOX/TRANSCRIPTS/` as a `.md` file.

The script may take several minutes for long recordings. Run it and wait for completion.

After transcription, note the output path and go to Step 3.

### 2b. Download + transcribe (direct audio URL)

Download the audio file to a temp location:

```bash
curl -L -o "/tmp/transcribe_download.mp3" "URL"
```

Then run the transcription script on the downloaded file (add `--diarize` only if multi-speaker):

```bash
"/Users/simonjpierce/Music/Audio Hijack/transcribe.sh" "/tmp/transcribe_download.mp3"
```

Clean up the temp file after:

```bash
rm -f "/tmp/transcribe_download.mp3"
```

Go to Step 3.

### 2c. Other URL (yt-dlp attempt)

Try downloading audio with yt-dlp:

```bash
yt-dlp -x --audio-format mp3 -o "/tmp/transcribe_download.%(ext)s" 'URL'
```

If this succeeds, find the downloaded file and run the transcription script on it (as in Step 2b, with `--diarize` if multi-speaker). If it fails, report the error and suggest the user download the audio manually and re-run with a local file path.

Go to Step 3.

### 3. Gather context

Read the raw transcript file.

**If multi-speaker** (from Step 1b), ask the user (using AskUserQuestion, one question at a time):

1. **Meeting name and date** — e.g. "Madagascar whale shark paper discussion, 11 Feb 2026"
2. **Speakers** — Who was in the meeting? Names and roles/affiliations.
3. **Topic/project** — What was the meeting about?
4. **Geographic region** — Is there a specific region, country, or site being discussed?

**If solo**, ask:

1. **Recording name and date** — e.g. "Voice notes after Tofo field trip, 8 Mar 2026"
2. **Topic** — What is the recording about?
3. **Geographic region** (if applicable)

Skip speaker-related questions for solo recordings.

### 3b. Context expansion and vocabulary confirmation

Once the user answers:

**Step 3b-i: Load existing vocabulary.** Read the `PROMPT` variable from `/Users/simonjpierce/Music/Audio Hijack/transcribe.sh` (grep for `^PROMPT=`). This contains all domain terms Whisper already knows. Parse it into a working set so you can distinguish "already handled at transcription" from "new term that needs manual correction."

**Step 3b-ii: Cross-reference against the Transcription Roster.** The canonical source of truth for people, species, locations, and organisations is:

```
05_AI WORKFLOW/CLAUDE/Processes/Transcription Roster.md
```

This file replaces the inline staff list that used to live in this skill. Read it when the meeting involves people or domain terms you want to confirm. Each entry has `canonical`, `aliases`, `whisper_misreads`, and `context` fields.

**Step 3b-iii: Run the automated correction pass.** Instead of manually spotting Whisper errors, run the roster-constrained LLM corrector. Pass the session-level context you gathered in Step 3 via `--context` so the LLM can disambiguate between roster entries (e.g. which Jessica, which Chris) using the speaker-stated topic:

```bash
~/bin/transcription/venv/bin/python3 ~/bin/transcription/correct_transcript.py \
    "PATH_TO_TRANSCRIPT.md" \
    --context "ONE-LINER: region, topic, key people (e.g. 'Mozambique whale shark meeting with Clare, Nakia, Olivia' or 'Kaikoura voice memo, sperm whale fieldwork')"
```

How it works:

1. **Phonetic pre-screen.** Two passes over the transcript:
   - Pass A — capitalised tokens → People / Organisations roster (with sentence-start suppression so every "The", "When", "So" doesn't flag).
   - Pass B — all tokens, case-folded → Species / Locations roster (catches lowercase "whale shark", "mobula" in running prose).
   - Metaphone equality OR Jaro-Winkler ≥ 0.85 + length-ratio ≥ 0.5 + JW sanity floor ≥ 0.3 (kills codepage collisions like "dive" ↔ "Tofo").
   - Known misreads in the roster always flag (bypasses sentence-start suppression).
2. **LLM pass.** Single Claude Opus call with the full roster as context + the flagged spans with ±2 lines of surrounding context. Returns strict JSON: `{corrections: [...], ambiguous: [...]}`.
3. **Apply + log.** High-confidence corrections applied by word-boundary regex on the flagged line. A `## Correction log` section is appended to the end of the transcript listing every applied correction, plus any ambiguous or low-confidence cases for Simon's review.

Dry-run first if you want to preview without modifying the file:

```bash
~/bin/transcription/venv/bin/python3 ~/bin/transcription/correct_transcript.py "PATH" --dry-run
```

**After the correction pass runs**, present ambiguous cases to Simon **one at a time** (per `feedback_sequential_decisions.md`) using AskUserQuestion. For each ambiguous case:

1. Show the line with ±1 line of context.
2. Show the candidate canonical forms with their context tags.
3. Ask which (if any) applies.
4. Apply the choice before moving to the next ambiguous case.

**If you observe a new persistent misread** during review (e.g. Whisper consistently renders "Nakia" as "Naki" in Mozambique contexts), add it to that roster entry's `whisper_misreads` list in `Transcription Roster.md` so it's caught automatically next time. This is the roster-maintenance feedback loop.

**After ANY edit to `Transcription Roster.md`**, validate YAML before continuing. Two reruns in the past 7 days were caused by unquoted colons in `context:` values (Stefan/Steffen disambiguation, Mark Hackney/Erdmann disambiguation). Run:

```bash
/opt/homebrew/bin/python3 -c "
import re, yaml
text = open('$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Transcription Roster.md').read()
fail = False
for name, body in re.findall(r'^## ([A-Za-z]+)\\s*\$.*?\`\`\`yaml\\s*\\n(.*?)\\n\`\`\`', text, re.DOTALL | re.MULTILINE):
    try: yaml.safe_load(body)
    except Exception as e: print(f'{name}: FAIL', e); fail = True
for ln, line in enumerate(text.splitlines(), 1):
    m = re.match(r'^(\\s+)context:\\s+(.+)\$', line)
    if m and not m.group(2).startswith('\"') and ': ' in m.group(2):
        print(f'L{ln}: unquoted colon-space in context — {line[:160]}'); fail = True
print('OK' if not fail else 'FIX BEFORE CONTINUING')
"
```

If anything fails, wrap the offending `context:` value in double quotes immediately. Do not continue with corrector runs until this passes.

After the correction pass completes, continue to Step 4 (format the transcript). The correction log remains at the bottom of the file as an audit trail — don't strip it during formatting.

### 4. Format the transcript

**4a. Add YAML frontmatter.** Before formatting the body, prepend frontmatter to the transcript file. This is required for exec-coach and other automations to detect the transcript type.

For **solo** recordings:
```yaml
---
date: YYYY-MM-DD
source: voice-memo
recorded: YYYY-MM-DDTHH:MM
transcribed: YYYY-MM-DDTHH:MM
type: monologue
---
```

For **multi-speaker** recordings:
```yaml
---
date: YYYY-MM-DD
source: meeting
recorded: YYYY-MM-DDTHH:MM
transcribed: YYYY-MM-DDTHH:MM
type: meeting
speakers: [Speaker A, Speaker B]
---
```

Use the date/time from the user's context answers (Step 3). `transcribed` is the current timestamp. The `date:` field is required — the monthly/weekly review bundlers use it for automated date detection (avoids filename parsing).

**4b. Format the body.** Read the process doc and follow it:

```
$VAULT_PATH/05_AI WORKFLOW/CLAUDE/Processes/Meeting Transcription Pipeline.md
```

Follow all formatting rules, the mandatory processing approach (plan → write in 40-80 line sections), speaker identification guidance, and output structure from that file. The context and vocabulary from Step 3 inform the corrections.

**Solo recording adaptation**: For solo recordings, skip speaker labels. Format as clean prose under topic headings. Remove filler words, fix false starts, combine fragments — but preserve all content and meaning. Still use the incremental editing approach (40-80 lines per edit) from the prompt file.

### 4c. Enforce standard filename

Rename the transcript file to the standard format: `YYYY-MM-DD — Title.md`

- **Date** from the frontmatter `date:` field (Step 3c)
- **Title**: descriptive, title case. For meetings: the meeting name from Step 3 (e.g., "Exec Meeting with Sarah"). For solo: the recording name (e.g., "Morning Monologue")
- Use an em dash (`—`) as the separator

Examples:
- `2026-03-10 — Exec Meeting with Sarah.md`
- `2026-03-20 — Morning Monologue.md`
- `2026-03-16 — Grey Nurse Points to Populations Meeting.md`

Use Bash `mv` to rename the file. If the file already follows this convention, skip. If a companion `.json` file exists with the old name, rename it too.

This standardisation means the review bundlers (monthly/weekly) can rely on frontmatter `date:` for date detection, and the filename is human-readable in the file browser without needing to parse date patterns.

### 5. Run post-processing (automatic)

After formatting is complete, automatically run all post-processing steps without asking. Do not prompt the user for which steps to run — just do them all:

1. **TODO extraction** — extract Simon's action items to Things 3 (other people's items go in a transcript section only). Use the exact invocation pattern from the `/todo` skill — positional args, called via `python3`:
   ```bash
   /opt/homebrew/bin/python3 /Users/simonjpierce/bin/obsidian_reviews/things3_helper.py "TITLE" "NOTES"
   ```
   Do NOT call the script path directly (no `+x` bit, no shebang → `Permission denied`). Do NOT pass `--title`/`--notes` flags (script rejects them with "looks like a flag"). Percent-encode spaces (`%20`) in any vault-link URL placed in the notes.
2. **IDEA extraction** — extract longer-term ideas to IDEA.md
3. **Verification subagent** — independent check for missed items or over-extraction
4. **Vault updates — auto-apply** — scan for info that updates existing vault docs and apply directly (default from 2026-04-21). Record the applied changes in an audit-trail note at `01_LIFE OS/REVIEW QUEUE/APPLIED UPDATES/Applied Updates — [Meeting Name] (YYYY-MM-DD).md` so Simon can audit later. Fall back to the old staging behaviour (`REVIEW QUEUE/PROPOSED UPDATES/` + Things 3 review task) only for high-risk proposals (named-entity swaps, role reversals, factual contradictions, significant rewrites, or anchor-verification failure >30%). See the Meeting Transcription Pipeline Step 7 for full rules.

Follow the instructions in the process doc for each step (TODO/IDEA format, verification subagent prompt, vault-update applied-note structure). Run the verification and vault update subagents in parallel where possible.

### 6. Whisper vocabulary update (local audio only)

**Only run this step if the input was a local audio file** (Step 2 was used, not Steps 2b/2c or a raw .md file).

Review the corrections made during formatting. If there are terms Whisper consistently got wrong that aren't already in the `PROMPT` variable in `/Users/simonjpierce/Music/Audio Hijack/transcribe.sh`, present the suggested additions during Step 3b-iii (vocabulary confirmation). Once Simon confirms the vocabulary list (or doesn't object to the suggestions), add them to the PROMPT variable in `transcribe.sh` automatically — the review is the approval. Do not ask for a separate go-ahead to edit the file.

### 7. Confirm and show result

Show:
- Input type (audio file / raw transcript / downloaded URL)
- Output file path
- Number of sections/headings in the formatted transcript
- Post-processing steps completed
- Any vocabulary suggestions for `transcribe.sh` (if applicable)

### 8. MMF board-deck accumulation scan (when MMF-relevant)

If the transcript is MMF-related (team meeting, funder call, partner call, board-side call — touches an MMF project, programme, funder, partner, team member, or board-level event), scan it for content suitable for the next-quarter board update. The intent is continuous accumulation of the next quarter's slide-deck markdown so meeting prep is curate-and-polish, not draft-from-zero. See `05_AI WORKFLOW/CLAUDE/Processes/MMF Board Updates — Workflow.md` § *Continuous slide-deck accumulation* for the full design.

**Skip the scan entirely if** the transcript is a personal call, non-MMF context (Planet Ocean / photography / Sony partnership), or a purely scientific discussion that doesn't touch board-level matters. When in doubt, skip — the weekly workhorse compile will catch anything missed via project-note review.

**Locate the next-quarter draft slide-deck file:**

```bash
ACCUM_DIR="$VAULT_PATH/02_MARINE MEGAFAUNA/MMF BOARD"
ACCUM_FILE=$(grep -l "^status: accumulating" "$ACCUM_DIR"/*"Slide Deck Content"*.md 2>/dev/null | head -1)
```

If `ACCUM_FILE` is empty, no accumulating draft exists yet. Behaviour depends on whether the transcript is itself an MMF Board Meeting (filename or meeting name contains "MMF Board Meeting"):

- **If the transcribed meeting IS an MMF Board Meeting** — surface this as an explicit prompt in Step 7's confirmation summary (not a silent flag). Format: `Board-deck accumulation: no accumulating draft for the next quarter — want me to seed the skeleton now? The board meeting just concluded is the natural quarter-rollover moment. Reply 'seed' to create it (you'll need to give me the next meeting date), or 'skip' to handle later.` This converts a recurring post-meeting TODO ("create next-quarter accumulating draft skeleton") into a clear in-flow prompt. Still don't auto-create — Simon's call on the next-meeting date and the regional/holding-bin structure remains a deliberate gate. Just lower the cost of forgetting. Confirmed need 2026-04-29 (boardmeeting-29apr-transcribe): the prior session's What's-next had "create next-quarter skeleton" as item 4 and it had still not happened by post-meeting transcription time.
- **If the transcribed meeting is any other MMF context** (Moz HODs, Full Circle progress, expedition planning, etc.) — silent flag remains correct. `Board-deck accumulation: no draft found at <ACCUM_DIR>` in the post-run summary, skip the append, no prompt. The "Simon's call at quarter start" rule applies here.

**Trigger phrase categories.** See the workflow doc § *Trigger phrase reference* table. Project lifecycle / funding / outputs / people / partnerships-governance / risk-regulatory.

**For each board-relevant item that fires:**
- Apply the four-question test from `memory/feedback_board_content.md` *Headlines only* section (completed deliverable? would change a board decision? summarisable in one sentence with one number? would Simon mention it in a 30-second verbal update?). At least 2 of 4 should pass.
- Identify the relevant holding-bin section in the draft (regional or cross-cutting heading).
- **If no matching section exists** (e.g. transcript discusses a country/programme that isn't currently a board-deck section, like Oman or Thailand/Andaman Sea on 2026-05-11): do NOT autonomously create new region/cross-cutting sections — that's a deck-design decision for Simon. Instead, flag the item explicitly in the Step 7 summary under a "Board-deck candidates without a home" line, naming the item and the suggested new section. Simon decides whether to add the section at the curation step.
- Append a draft paragraph in narrative-prose style per `memory/feedback_board_content.md` *Slide deck text density* section. US English. 2–4 sentences. Numbers embedded inline.
- Tag with: `<!-- draft <YYYY-MM-DD> from transcript: <transcript filename> -->`
- Don't ask Simon for confirmation per item — the append is autonomous. Weekly workhorse compile and Simon's prep-time review are the curation layers.

**Report in the step 7 summary:** `Board-deck accumulation: appended N items to <draft file>` (or `skipped — content not MMF-board-relevant` / `skipped — no accumulating draft found`).

## Guidelines

- **Output folder**: `00_INBOX/TRANSCRIPTS/` for all transcript types.
- **Faithful transcript**: The formatting step restructures and cleans up, but preserves all substantive content. This is not a summary.
- **32K output limit**: Always use the incremental editing approach (40-80 lines per section). Never attempt to write the entire formatted transcript in a single tool call.
- **Leading whitespace**: Raw Whisper output often has leading spaces. If an Edit fails to match, use `xxd` to inspect exact bytes.
- **Hallucination loops**: 3+ consecutive identical lines are a Whisper artefact. The transcription script strips these, but check for any that slipped through.
- **File path quoting**: The vault path has spaces and an apostrophe. Always double-quote paths in shell commands.
- **Shared script**: `transcribe.sh` is also used by the voice memo processor (`~/bin/obsidian_reviews/voice_memo_processor.py`). Vocabulary changes to the PROMPT variable improve both the meeting transcription and voice memo pipelines.

## Permissions

For the skill to run without approval prompts, `~/.claude/settings.local.json` needs:

```json
"Bash(*)",
"Read($VAULT_PATH/**)",
"Edit($VAULT_PATH/**)",
"Write($VAULT_PATH/**)",
"Glob($VAULT_PATH/**)",
"Grep($VAULT_PATH/**)"
```

## Post-run improvement

After completing the task, briefly assess skill performance:
- Did any step fail, need workaround, or produce poor results?
- Were there missing steps or unclear instructions?

If patterns emerge (not one-off issues), update this skill file with fixes. Log genuinely surprising friction to the Friction Log.
