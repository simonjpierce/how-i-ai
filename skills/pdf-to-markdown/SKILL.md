---
name: pdf-to-markdown
description: Convert a PDF into clean markdown for Obsidian. Handles paragraph joining, table reconstruction, header/footer removal, hyphenation repair, footnotes, reference cleanup, and OCR artifacts. Use when the user says "convert this PDF", "extract this book", "PDF to markdown", or provides a PDF for conversion.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion
---

Convert a PDF document into clean, well-structured markdown. Optimised for single documents (papers, reports, chapters). Also handles multi-chapter books — see **Book mode** appendix.

$ARGUMENTS


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Vault paths

- **Default output:** `$VAULT_PATH/` (ask Simon for the target folder)

## Phase 1 — Extract

### 1.1 Identify the PDF

If `$ARGUMENTS` contains a file path, use it. Otherwise ask for the path. Verify the file exists.

### 1.2 Check extraction tools and get page count

**PATH note:** poppler tools (`pdftotext`, `qpdf`, `pdftoppm`, `pdfinfo`) are at `/opt/homebrew/bin/` and are NOT on the Bash tool's default PATH. Always use full paths.

```bash
"$HOME/.local/bin/marker_single" --help >/dev/null 2>&1 && echo "marker available"
/opt/homebrew/bin/pdftotext -v 2>/dev/null && echo "pdftotext available"
command -v ocrmypdf 2>/dev/null || "$HOME/.local/bin/ocrmypdf" --version >/dev/null 2>&1 && echo "ocrmypdf available"
/opt/homebrew/bin/qpdf --version 2>/dev/null && echo "qpdf available"
/opt/homebrew/bin/pdftoppm -v 2>/dev/null && echo "pdftoppm available"
/opt/homebrew/bin/pdfinfo "INPUT.pdf" | grep -E "Pages|Tagged|Creator"
```

**Tool cascade (use the best available):**
1. **marker** (best quality when it works): Layout analysis, tables, OCR, headings, footnotes, and image extraction — all handled natively. Outputs markdown + extracted images (JPEGs) to the output directory. Installed at `$HOME/.local/bin/marker_single` via pipx (`marker-pdf` package). First run downloads ~500MB of models. ~70s/page. **Reliability warning:** marker fails silently on many PDFs — produces empty output directories with no error. In one batch of 23 native-text PDFs, 20 produced empty output. Always verify marker output before relying on it.
2. **pdftotext** (always available, always reliable): Bundled with poppler. Lower quality — no layout analysis, tables destructured — but reliably extracts text from any native-text PDF. **Use as the guaranteed baseline** — run pdftotext first, then use marker output only where it's better.
3. **ocrmypdf** (for scanned PDFs): Adds a text layer to image-only PDFs. Installed at `$HOME/.local/bin/ocrmypdf` via pipx. Use before pdftotext on scanned documents.

**When to skip marker:** For short design-heavy PDFs (brand manuals, infographics, posters, marketing one-pagers) where extracted images would be logos, color swatches, or design mockups of limited reference value, pdftotext alone is usually sufficient. Marker's ~70s/page cost (~20 min for a 16-page manual) rarely pays off when the substantive content is text and the visual assets exist as source files elsewhere.

**Supplementary tools:**
- **qpdf**: Split multi-chapter PDFs by page range: `qpdf "SOURCE.pdf" --pages . START-END -- /tmp/chNN.pdf`. Ignore qpdf warnings.
- **pdftoppm**: Screenshot PDF pages as images when marker's figure extraction is poor: `pdftoppm -jpeg -r 150 -f PAGE -l PAGE "INPUT.pdf" /tmp/fig_prefix`. Bundled with poppler.

### 1.3 Extract text

**If marker is available:**
```bash
"$HOME/.local/bin/marker_single" "INPUT.pdf" --output_dir /tmp/pdf_marker/
```
Use `--page_range` for partial conversion (e.g., `--page_range 0,5-10,20` — zero-indexed). Use `--disable_image_extraction` if images aren't needed.

Marker outputs markdown + extracted images (JPEGs) to the output directory — but **check that the output directory is non-empty** before proceeding. If marker produced empty output, fall back to pdftotext. When it works, read the markdown output and assess quality. If it produced coherent paragraphs, reasonable headings, and intact tables, use it as the starting point — Phase 2 cleanup will be lighter.

**Handling extracted images:** Copy marker's extracted images to the vault output folder. Rename descriptively (e.g., `Figure_3_whale_shark_sightings.jpeg`). Update image references in the markdown to use relative paths (`![](Figure_3_whale_shark_sightings.jpeg)`). For figures that marker extracted poorly, use `pdftoppm` to screenshot the specific page instead.

**Always also extract with pdftotext** (even if marker is available — the layout mode is essential for table verification):
```bash
/opt/homebrew/bin/pdftotext "INPUT.pdf" /tmp/pdf_full.txt
/opt/homebrew/bin/pdftotext -layout "INPUT.pdf" /tmp/pdf_layout.txt
```
Regular extraction = primary source for body text. Layout-preserved = ground truth for **tables** (preserves column alignment).

### 1.4 Detect scanned vs native text

```bash
wc -w /tmp/pdf_full.txt
```

If the word-to-page ratio is very low (<20 words per page), the PDF is likely scanned/image-based. Alert Simon and suggest:
- `marker` (includes Surya OCR — handles this automatically)
- `"$HOME/.local/bin/ocrmypdf" INPUT.pdf INPUT_ocr.pdf` to add a text layer first, then re-extract

### 1.5 Assess document type

```bash
grep -n "^Chapter \|^CHAPTER " /tmp/pdf_full.txt | head -20
```

**Single document** (default): Proceed to Phase 2.
**Multi-chapter book**: Switch to the **Book mode** appendix below.

### 1.6 Create output file

Ask Simon for the output path/filename. Create the markdown file with:
- YAML frontmatter (title, authors if known, source PDF filename)
- Document title as H1

**Naming convention:** Descriptive title, e.g. `Pierce et al 2024 — Whale Shark Aggregations.md`

## Phase 2 — Cleanup

For single documents, Claude reads the extracted text and cleans it directly through Write/Edit calls. This is more reliable than scripted regex for individual documents because Claude understands context, can resolve ambiguities, and handles edge cases that break heuristics.

**If marker was used:** Start from marker's markdown output. Many of these steps will already be handled — skim each and fix only what marker got wrong.

**If pdftotext was used:** Read the full extracted text. Work through the document section by section, writing clean markdown.

### 2.1 Header/footer removal

Identify and remove repeating text that appears across page boundaries:
- Page numbers (bare numbers at regular intervals)
- Running headers (document/journal title, author names)
- Running footers (copyright lines, chapter titles)

**Detection:** Look for identical or near-identical short lines that repeat at regular intervals (~40–60 lines apart in pdftotext output, corresponding to page breaks).

### 2.2 Paragraph joining

pdftotext inserts hard line breaks at PDF line boundaries. Join these into proper paragraphs:
- Lines not ending with sentence-ending punctuation (`. ? ! :`) join with the next line
- **Don't join:**
  - Reference entries (`Author, A. B. YYYY.` pattern)
  - Figure/table captions (`Figure X.X`, `Table X.X`)
  - Section headings (numbered patterns `X.X.X`, ALL CAPS lines)
  - Lines inside tables
  - Genuine paragraph breaks (blank line, next line starts uppercase after a completed sentence)

### 2.3 Hyphenation and compound word repair

pdftotext handles end-of-line hyphens inconsistently:

**Dangling hyphens** — hyphen preserved at line break: `bio-\ndiversity`. Fix by joining: remove the line break (and the hyphen if the word isn't normally hyphenated).

**Merged compounds** — hyphen silently dropped: `computer-\nassisted` → `computerassisted`. Pervasive — expect 10–20+ per chapter. Scan for `[a-z][A-Z]` mid-word patterns after paragraph joining. Common examples:
- Author surnames: `NasbyLucas` → `Nasby-Lucas`
- Technical terms: `photoID` → `photo-ID`, `computerassisted` → `computer-assisted`
- Compound adjectives: `midAtlantic` → `mid-Atlantic`
- Exclude genuine camelCase: `GoPro`, `YouTube`, `MantaMatcher`, `BioScience`, `McMahon`

### 2.4 Unicode and artifact cleanup

- Remove soft hyphens (`\u00AD`), zero-width spaces (`\u200B`, `\uFEFF`)
- Normalise dashes: OCR variants of en-dash `–` and em-dash `—` → standard Unicode
- Remove control characters
- Fix `fi`, `fl`, `ff` ligature issues (OCR sometimes splits or garbles these: `ﬁ` → `fi`, `ﬂ` → `fl`)
- **marker-specific ligature substitution:** marker_single substitutes `ﬁ` (fi ligature, U+FB01) with `!` and `ﬂ` (fl ligature, U+FB02) with `"` in its output. These look plausible in context but are wrong. Fix with:
  ```python
  import re
  text = re.sub(r'(?<=[a-zA-Z])!(?=[a-zA-Z])', 'fi', text)
  text = re.sub(r'(?<=[a-zA-Z])"(?=[a-zA-Z])', 'fl', text)
  ```
  Run this before writing marker output to vault.

### 2.5 Section heading reconstruction

Academic PDFs commonly split headings across multiple lines:
```
12.6                          →  ## 12.6 Practical Considerations for Photo-ID
PRACTICAL CONSIDERATIONS
FOR PHOTO-ID
12.6.1                        →  ### 12.6.1 Photographic Equipment
Photographic Equipment
```

Reconstruct multi-line headings and assign correct markdown levels:
- H2 for major sections (`## 3. Methods`)
- H3 for subsections (`### 3.1 Study Area`)
- H4 for sub-subsections if needed
- Title-case the heading text (unless proper noun or abbreviation)
- Fix small-caps OCR garbling (`INtRODUCtION` → `Introduction`)

### 2.6 Table reconstruction

Tables are the highest-error area in PDF conversion.

**If marker was used:** Tables are usually already in markdown format. Verify cell counts and values against the layout-preserved pdftotext extraction (`/tmp/pdf_layout.txt`).

**If pdftotext only:**
1. Identify table locations in the regular extraction (scattered data lines)
2. Find the same table in the layout-preserved extraction — column alignment is preserved there
3. Reconstruct as proper markdown table
4. Verify every cell value against the layout source

**Complex tables** (merged cells, multi-row headers, spanning columns): standard markdown can't represent these. Options:
- HTML table (most faithful)
- Simplified flat markdown table with a note about the original structure
- Ask Simon which approach to use

### 2.7 Figure captions

Figures mid-page cause captions to interleave with body text. Separate and format as blockquotes:

```markdown
> **Figure 3.2** Distribution of whale shark sightings across the study period (2015–2022). Points represent individual encounters; colour indicates season.
```

Rejoin the body text fragments that were split around the figure.

### 2.8 Footnote handling

Convert footnote markers and text to markdown notation:
- Superscript markers in body text → `[^1]`
- Footnote text collected from page bottoms → `[^1]: Footnote content here.`
- Place all footnote definitions at the end of the document (or end of section if the document is very long)

### 2.9 Reference section cleanup

Launch a **sonnet subagent** for the reference section. Regex is unreliable for references (multi-word surnames, "et al." mid-line, conference proceedings with commas, etc.).

The subagent should:
1. Read the References section from the markdown file
2. Split lines containing multiple merged references (after a reference ends with page range/DOI, a new author name begins)
3. Join references split across lines (author names detached from publication details)
4. Ensure each reference is on its own line
5. Fix obvious OCR errors in author names, years, and DOIs

### 2.10 Remaining OCR artifact fixes

Final pass for:
- Scientific names: restore italics where identifiable (*Rhincodon typus*)
- Broken DOIs and URLs (re-join across line breaks)
- Ligature artifacts not caught in 2.4
- Any remaining garbled text

### 2.11 OCR correction policy

Before finalising, confirm with Simon: should obvious OCR typos be corrected (e.g., `Palaenotology` → `Palaeontology`) or preserved verbatim? Default: correct obvious errors, flag ambiguous cases with `<!-- TODO/VERIFY: ... -->`.

## Phase 3 — Verification

### 3.1 Verification subagent

Launch a **sonnet subagent** to compare the cleaned markdown against the raw extracted text. The agent checks:

1. **Missing content:** Paragraphs or sentences in the source but absent from markdown
2. **Table accuracy:** Cell-by-cell comparison against layout-preserved text (highest error area)
3. **Reference completeness:** Missing refs, wrong years/authors, garbled entries
4. **Numbers and data:** Measurements, statistics, percentages that differ from source
5. **Garbled text:** OCR artifacts, wrong words, mangled sentences

The agent reports findings by severity:
- **Critical:** Missing sections, systematic table errors, wrong data
- **High:** Wrong cell values, missing references
- **Medium:** Content gaps, minor OCR artifacts
- **Low:** Formatting preferences, faithfully reproduced source errors

### 3.2 Fix verified errors

Apply corrections based on the verification report. For table errors, rebuild from layout-preserved source. Run a targeted re-check on any critical items after fixing.

## Phase 4 — Wrap up

### 4.1 Report

Summary of:
- Pages processed, output file location
- Tables rebuilt
- References cleaned
- Items requiring manual review (if any)

### 4.2 Temp files

Note locations of temp files (`/tmp/pdf_*`) for reference. Cleaned up on reboot.

---

## Book mode (multi-chapter documents)

When the PDF is a multi-chapter book, the workflow scales up with Python scripts and parallel subagents for consistency and speed.

### B.1 Split into per-chapter files

Map chapter boundaries. Two approaches:

**PDF-level split (preferred when page ranges are known):** Use `qpdf` to extract per-chapter PDFs, then run marker on each:
```bash
mkdir -p /tmp/pdf_chapters/
/opt/homebrew/bin/qpdf "SOURCE.pdf" --pages . START-END -- /tmp/pdf_chapters/ch01.pdf
"$HOME/.local/bin/marker_single" "/tmp/pdf_chapters/ch01.pdf" --output_dir /tmp/pdf_marker_ch01/
```

**Text-level split (when page ranges are unknown):** Split from the full pdftotext extraction:
```bash
sed -n 'START,ENDp' /tmp/pdf_full.txt > /tmp/pdf_ch01.txt
```

Create backup directory:
```bash
mkdir -p /tmp/pdf_backup/
```

### B.2 Create initial chapter files

For each chapter:
- YAML frontmatter (title, authors if per-chapter, chapter number)
- Chapter title as H1
- Author names if per-chapter (common in edited volumes)
- Raw body text

**Naming convention:** `Ch XX — Chapter Title.md`

### B.3 Automated cleanup (Python scripts)

For books, write Python cleanup scripts to ensure consistent heuristics across all chapters.

**Script 1 (`/tmp/cleanup_pass1.py`):** Paragraph joining, unicode cleanup, header/footer removal, hyphenation repair. Implements the heuristics from Phase 2 steps 2.1–2.4.

Key functions to implement:
- `ends_sentence(line)` — `.`, `?`, `!`, `:`, or closing paren/quote after punctuation
- `line_continues(line)` — starts lowercase, doesn't match structural patterns
- `is_reference_start(line)` — detects reference entry beginnings
- `is_table_fragment(line)` — detects lines that are part of a table

**Script 2 (`/tmp/cleanup_pass2.py`):** Page-break split joining.
- Pattern: non-empty line + blank line + continuation (starts lowercase, or current line ends `,`/`;`)
- Guard: don't join if continuation is a heading/caption/new paragraph
- **Do NOT use a greedy continuation loop** — join only the two parts across the blank line, then stop and advance

**Test both scripts on a representative chapter before running on all files.**

```bash
python3 /tmp/cleanup_pass1.py "$OUTPUT_DIR"
python3 /tmp/cleanup_pass2.py "$OUTPUT_DIR"
```

### B.4 Per-chapter manual fixes (parallel subagents)

Launch a **sonnet subagent per chapter** for issues scripts can't handle:
- Table reconstruction (from layout-preserved text)
- Section heading reconstruction (multi-line headings — see Phase 2.5)
- Figure caption separation (see Phase 2.7)
- Compound word fixes (`[a-z][A-Z]` patterns — see Phase 2.3)
- OCR artifact fixes

Each subagent gets:
- Path to the markdown file
- Path to the per-chapter raw text file
- Path to the layout-preserved PDF text (`/tmp/pdf_layout.txt`) for tables
- Specific known issues for that chapter (from a quick scan)

### B.5 Reference cleanup subagents

Launch **sonnet subagent(s)** for reference sections — one per chapter, or one for the whole book if references are consolidated.

### B.6 Verification (parallel subagents)

Launch a **sonnet subagent per chapter** for verification (same checks as Phase 3.1). Compile findings by severity and present consolidated report.

### B.7 Fix and wrap up

Apply corrections from verification. Run targeted re-verification on chapters with critical errors. Report per-chapter summary including tables rebuilt, references fixed, and items needing manual review.

---

## Post-run improvement

After completing the task, briefly assess skill performance:
- Did any step fail, need workaround, or produce poor results?
- Were there missing steps or unclear instructions?

If patterns emerge (not one-off issues), update this skill file with fixes. Log genuinely surprising friction to the Friction Log.

---

## Known failure modes

1. **Greedy paragraph joining:** After joining a page-break split, do NOT continue joining subsequent lines. Join only the two halves, then stop.
2. **Broken compound words from line breaks:** pdftotext merges hyphenated line-end words without the hyphen. Expect 10–20+ per chapter. Scan for `[a-z][A-Z]` patterns. Common: author surnames (`NasbyLucas`), technical terms (`photoID`), compound adjectives (`midAtlantic`).
3. **Multi-line section headings:** Academic PDFs split headings across 2–3 lines. Scripts often mis-parse these, producing garbled output like `## 12.6 12.6.1 Practical Considerations`. Reconstruct from original text.
4. **Figure captions interleaved with body text:** Caption text lands between sentence fragments. Separate the caption, rejoin the split body text.
5. **Reference merging:** Multiple references merge onto single lines during paragraph joining. Use subagent, not regex.
6. **Table column shifts:** PDF tables get destructured non-linearly by pdftotext. Always rebuild from `-layout` extraction. Verify every cell.
7. **Multi-column layouts:** Text from different columns may interleave. Layout-preserved extraction helps; may need manual reconstruction.
8. **Missing content at page boundaries:** pdftotext sometimes drops text near figures that span page boundaries. Flag gaps rather than silently skipping.
9. **Scanned PDFs with no text layer:** pdftotext returns near-empty output. Need OCR first — marker handles this automatically; otherwise use `ocrmypdf`.
10. **Ligature characters:** `ﬁ`, `ﬂ`, `ﬀ` may survive as single Unicode characters or get garbled. Normalise to ASCII equivalents.
11. **Apostrophe in vault path:** Use double-quoted strings in shell commands.
12. **BSD grep on macOS lacks `-P`:** Use the Grep tool instead of `grep -P`.
13. **Marker Pydantic warning on Python 3.14:** `marker_single` emits a `UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14` warning to stderr. This is cosmetic — marker still works correctly. Ignore it.
14. **Encyclopedia-style PDFs with adjacent entries:** PDFs of individual entries may include overflow text from neighbouring entries. Trim to the entry of interest by finding its title heading and the next entry's heading. For end-trimming, be conservative — ALL CAPS detection for "next entry" headings can fire on internal section headers. Better to include a small amount of trailing overflow than to truncate the entry.
15. **marker silent failures:** marker_single can produce empty output directories with no error message, even on native-text PDFs. Always check that the output .md file exists and is non-empty before using it. In batch processing, expect some PDFs to fail.
16. **Content filtering on batch processing:** When using subagents to process multiple documents containing content about exploitation, hunting, or historical harm (e.g., whaling, shark finning), the accumulated context can trigger content filters. Workaround: use Python scripts for the mechanical extraction/cleanup steps, or limit each subagent to a single document.
17. **poppler tools not on default PATH:** `pdftotext`, `qpdf`, `pdftoppm`, `pdfinfo` are at `/opt/homebrew/bin/` and not on the Bash tool's PATH. The tool-check commands in Phase 1.2 use full paths — ensure you use `/opt/homebrew/bin/pdftotext` etc. in all Bash calls, not bare `pdftotext`.
18. **marker ligature substitution:** marker_single outputs `!` in place of `ﬁ` (fi ligature) and `"` in place of `ﬂ` (fl ligature). These are plausible characters in context and easy to miss. Fix with regex in Python before writing to vault — see step 2.4.

## Scaling notes

- **Single document** (~16 pages): ~10–15 minutes. Extract → direct cleanup → verification → fix.
- **Multi-chapter book** (~345 pages, ~19K lines): ~35–45 minutes.
  - Automated cleanup: ~5 min
  - Manual fixes: ~10 min (parallel subagents)
  - Verification: ~10 min (parallel subagents)
  - Fixes: ~10 min (parallel subagents)
- Tables are the dominant error source. Budget extra time for table-heavy documents.
- Marker extraction significantly reduces cleanup time for single documents (many steps already handled).
- A 40–80% line reduction (raw → cleaned) is typical for academic PDFs with hard line wraps.
