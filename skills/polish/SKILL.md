---
name: polish
description: Run grammar and style checks on markdown files using LanguageTool and Vale, then apply fixes. Use when the user says "polish this", "proofread this", "check grammar", "style check", or "clean up this writing". Accepts a file path as $ARGUMENTS.
allowed-tools: Read, Write, Bash, Edit, Glob, Grep, AskUserQuestion
---

Run LanguageTool (grammar/spelling) and Vale (style/prose quality) on a markdown file, then review and apply fixes.

## Adapting this for your work

This skill ships ready-to-use but assumes:
- **LanguageTool** installed at `/opt/homebrew/bin/languagetool` (`brew install languagetool`).
- **Vale** installed at `/opt/homebrew/bin/vale` (`brew install vale`), with config at `~/.vale.ini`.
- **NZ/UK English** as the default (`--language en-GB`). Switch to `en-US` for US-audience documents.

The voice-matching pass (step 7) is gated on `features.is_simon` in your per-vault `config.json` and is skipped on standard installs. To enable voice matching for your own writing patterns, see `guides/ai-assisted-writing.md` for how to build a voice reference.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Steps

### 1. Identify the file

Use `$ARGUMENTS` as the file path. If empty, ask the user which file to polish.

If given a relative path, resolve it against the user's vault root from `~/.claude/projects/<project-key>/config.json` (`vault.path`).

Read the file first to understand the content and context.

### 2. Run both tools

Run LanguageTool and Vale in parallel:

```bash
languagetool --language en-GB "FILE_PATH" 2>&1
```

```bash
vale "FILE_PATH" 2>&1
```

**LanguageTool notes:**
- Always use `--language en-GB` (NZ/UK English is Simon's default).
- If the file is for a US audience (e.g. US grant application), use `--language en-US` instead — check the file content or ask.

**Vale notes:**
- Uses the config at `~/.vale.ini` (write-good + proselint styles).
- Vale exits with code 1 when it finds issues — this is normal, not an error.

### 3. Triage the results

Combine results from both tools. Categorise each finding:

**Fix** — clear errors that should be corrected:
- Spelling mistakes
- Grammar errors (subject-verb agreement, tense, etc.)
- Missing or incorrect punctuation that changes meaning

**Consider** — style suggestions worth reviewing but context-dependent:
- Passive voice (sometimes appropriate in scientific writing)
- Wordy phrases
- Weasel words (sometimes deliberate hedging in evidence-based writing)

**Skip** — false positives and noise:
- Domain-specific terms flagged as spelling errors (species names, place names, technical terms)
- Markdown syntax flagged as issues
- Style suggestions that conflict with the document's intended tone
- write-good's E-Prime suggestions (avoid "is/was/be") — these are too aggressive for most writing. Only flag if the density of to-be verbs is genuinely excessive.
- Suggestions that would change the author's voice or meaning

### 4. Present findings

Show the user a concise summary grouped by category:

```
## Polish results for [filename]

### Fixes (N items)
- Line X: "sentance" → "sentence" (spelling)
- Line Y: "grammer" → "grammar" (spelling)
- Line Z: missing comma before "and" in compound sentence

### Consider (N items)
- Line X: "was written" — passive voice (appropriate here? scientific context)
- Line Y: "very important" — could strengthen by being more specific

### Skipped (N items)
- N domain terms / N markdown false positives / N style noise
```

### 5. Apply fixes

Ask the user which categories to apply:
- **Fixes**: apply all, or review individually?
- **Consider**: review each one?

Then apply approved changes using Edit. Group nearby fixes into single edits where possible to minimise tool calls.

### 6. AI writing detection pass

Scan the text for common signs of AI-generated writing (adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)). This catches patterns that LanguageTool and Vale miss. Report findings as a separate section.

#### Overused AI vocabulary

Flag high-density use of these words/phrases (one or two is fine; clusters are a tell):

**High-signal words** (almost always AI when clustered): *delve*, *tapestry* (figurative), *nestled*, *vibrant*, *testament*, *pivotal*, *landscape* (figurative), *intricate/intricacies*, *interplay*, *meticulous/meticulously*, *garner*, *underscore* (as verb), *foster/fostering*, *showcase/showcasing*, *bolstered*, *enduring*

**Medium-signal words** (common in AI, but sometimes legitimate): *crucial*, *enhance*, *align with*, *highlight* (as verb), *emphasizing*, *encompassing*, *cultivating*, *valuable insights*, *resonate with*, *diverse array*, *groundbreaking*, *renowned*, *commitment to*, *rich* (as intensifier), *profound*, *boasts* (meaning "has"), *exemplifies*

#### Structural patterns

- **Superficial significance claims** — sentences that inflate importance using "-ing" participles: "highlighting its importance", "underscoring its significance", "reflecting broader trends", "contributing to the field". These add no information.
- **The "Despite challenges" formula** — "Despite its [positive attributes], [subject] faces challenges..." followed by vague optimism. Rigid and formulaic.
- **Elegant variation** — avoiding repeating a word by cycling through synonyms ("the whale shark... this gentle giant... the spotted fish... the ocean's largest resident"). One or two alternatives is natural; systematic avoidance of repetition is an AI tell.
- **Rule of three** — "adjective, adjective, and adjective" or "short phrase, short phrase, and short phrase" used to make superficial analysis appear comprehensive.
- **Negative parallelisms** — "Not just X, but Y", "It's not about X — it's about Y" used to appear balanced and thoughtful. Occasional use is fine; systematic use is a tell.
- **Copula avoidance** — replacing simple "is" or "has" with "serves as", "stands as", "features", "offers", "represents", "marks". AI copyedits specifically do this.
- **Weasel attributions** — "Experts argue", "Observers note", "Industry reports suggest" without naming specific sources.
- **Promotional/puffery tone** — "natural beauty", "in the heart of", "diverse range of experiences", "commitment to excellence". Travel-guide or press-release register where it doesn't belong.
- **Excessive em dashes** — AI text overuses em dashes for emphasis in a formulaic, sales-like way. Some em dashes are natural; a high density is a tell.
- **Title case in headings** — AI defaults to capitalising all main words in headings. Most vault writing uses sentence case; flag where the user's other writing uses sentence case but the current text doesn't.

#### What to do with findings

Present AI writing findings in a separate `### AI writing patterns (N items)` section in the results, grouped by type. For each finding, show the specific text and suggest a rewrite that sounds more natural. These should be presented as **Consider** items — Simon decides which to fix.

**Don't flag:**
- Single instances of common words (one "crucial" in 800 words is fine)
- Patterns that are natural for the document type (passive voice in scientific writing, formal register in grant applications)
- Simon's established voice patterns — read the Voice Reference if available

### 7. Voice check — author writing patterns (gated on `features.is_simon`)

This step is **gated on `features.is_simon`** in the per-vault `config.json`. Read the user's project config; if `is_simon` is `false`, skip this step entirely (the full voice-reference workflow is Simon-specific and depends on his published writing samples; standard installs don't ship voice references). If `is_simon` is `true`, continue.

When the text is Simon's writing (essays, manuscripts, blog posts, grant applications — not internal notes or process docs), check it against the appropriate voice reference:

- **Scientific/academic writing** (manuscripts, book chapters, grant applications, whale shark essays): `05_SYSTEM/Voice References/Voice Reference — Simon Pierce (Whale Shark Book).md`
- **Web/photography/travel writing** (blog posts, naturetripper, simonjpierce.com, photography essays): `05_SYSTEM/Voice References/Voice Reference — Simon Pierce (Planet Ocean).md`

Read the applicable voice reference, then scan the text for mismatches. The checks below are drawn from the scientific voice reference — adapt based on which reference applies. Focus on:

#### Words and phrases Simon doesn't use

Flag any of these — they're absent from Simon's published writing and signal AI drafting:

- "delve into" / "dive into" → he uses "explore" or "investigate"
- "tapestry" / "rich tapestry"
- "It's important to note that" → he just states the point
- "shed light on" → he uses "inform" or "clarify"
- "underscores" (as verb)
- "crucial" / "critical" → he prefers "important", "significant", or "key"
- "plays a pivotal role" → "is important for" or "has a major influence on"
- "multifaceted", "navigate" (metaphorical), "landscape" (metaphorical)
- "leverage" (as verb), "a testament to", "paradigm shift"
- "this begs the question"
- "Firstly, secondly, thirdly" → he uses "First," "Second," etc.
- "In conclusion" as a section opener
- Filler: "It is worth noting that", "It should be mentioned that"

#### Structural mismatches

- **Question-as-hook openings** — Simon leads with context, not questions
- **Conclusion-first framing** — Simon builds to conclusions from evidence
- **Excessive subheadings** — Simon uses substantial sections, not a heading every 2–3 paragraphs
- **Bullet points in body text** — Simon writes continuous prose; lists only in tables or formal frameworks
- **Neat "key takeaways" summaries** — his sections flow into each other
- **Single-sentence paragraphs** used frequently — they're rare emphasis tools in his writing
- **Definition-first section openings** — he starts with context and purpose

#### Positive voice signals to check for

These aren't requirements, but their absence in longer text may indicate the voice has drifted:

- "Unfortunately" as a bad-news pivot
- Concessive pivots ("However," / "That said,")
- Evidence-first argument structure (data → interpretation → caveats → hedged conclusion)
- "We are not aware of" rather than "no studies exist" for knowledge gaps
- Measured hedging: "suggests", "appears to be", "it is plausible that"
- Dry, parenthetical humour where appropriate

#### What to do with findings

Present voice findings in a `### Voice check (N items)` section, grouped by type. For each finding, show the specific text and suggest a rewrite that matches Simon's patterns. Present as **Consider** items.

**Don't flag:**
- Voice patterns that are appropriate for the document type (e.g., more formal register in grant applications is fine)
- Single instances in long documents — look for patterns and clusters
- Text that Simon wrote himself and clearly intended (check git blame or ask if unsure)

**When no voice reference applies:** If the text is web content, internal notes, or a domain where no voice reference exists, skip this step. Note in the output: "Voice check skipped — no applicable voice reference for this document type."

### 8. Optional re-run

After applying fixes, offer to re-run both tools to confirm the file is clean. Only do this if substantial changes were made.

## Context-sensitive behaviour

- **Scientific writing** (papers, manuscripts, grant applications): Be more tolerant of passive voice, technical jargon, and formal phrasing. These are conventions, not errors.
- **Web content** (blog posts, articles): Flag passive voice and wordiness more aggressively. Readability matters more here.
- **Internal notes** (vault docs, process notes): Light touch. Only flag genuine errors, not style preferences.
- **US English context**: Switch LanguageTool to `--language en-US`. Watch for organisation/organization, behaviour/behavior, colour/color etc. — these are not errors in the other dialect.

## Tool locations

- LanguageTool: `/opt/homebrew/bin/languagetool`
- Vale: `/opt/homebrew/bin/vale`
- Vale config: `~/.vale.ini`
- Vale styles: `~/.vale/styles/` (write-good, proselint)

## Failure modes

- **LanguageTool is slow on large files** — it loads a JVM. For files over ~500 lines, warn the user it may take 10-20 seconds.
- **Domain terms flagged as misspellings** — cross-reference against the file content. Marine biology terms (e.g. Rhincodon typus, mobulid, elasmobranch) are not errors.
- **Vale E-Prime noise** — the write-good E-Prime rule flags every use of "is", "was", "be", etc. This generates excessive noise for most documents. Suppress these unless the user specifically asks for E-Prime checking.
- **Markdown syntax** — both tools may flag markdown formatting. Ignore these.

## Post-run improvement

After completing the task, briefly assess skill performance:
- Did any step fail, need a workaround, or produce poor results?
- Were there missing steps or unclear instructions?
- Did the output meet expectations, or should the process be adjusted?

If the assessment identifies a non-controversial improvement — a better instruction, a missing step, a template update — apply it to this skill file immediately. Do not document improvements as recommendations for a future session. The goal is that every run leaves this skill slightly better than it found it.
