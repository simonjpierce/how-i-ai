---
name: verify-citations
description: Verify citations in a scientific manuscript against Semantic Scholar, CrossRef, and OpenAlex. Flags fabricated papers, wrong authors/years, and missing DOIs. Consults the local Paperpile mirror (DOI-based) before external sources. Use when the user says "/verify-citations", "check citations", "verify references", or "citation audit". Accepts a file path as $ARGUMENTS.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

Verify that references in a scientific manuscript are real and correctly attributed by querying academic APIs.

## When something goes wrong

When a step fails or needs a workaround, update this skill file with what you learned BEFORE continuing. Add failure modes, correct wrong assumptions. This takes 30 seconds and prevents the same friction next time.

## Steps

### 1. Identify the manuscript

Use `$ARGUMENTS` as the file path. If empty, ask the user which manuscript to verify.

If given a relative path, resolve against the vault root:
```
$VAULT_PATH/
```

Read the file and confirm it has a References/Bibliography section.

### 2. Run the verification script

The verifier is bundled with this skill at `$HOME/.claude/skills/verify-citations/verify_citations.py` (only requires Python 3 + standard library).

```bash
python3 "$HOME/.claude/skills/verify-citations/verify_citations.py" "MANUSCRIPT_PATH" -o /tmp/citation-report.md
```

**Lookup waterfall:** for any reference with a DOI, the script first consults the local Paperpile mirror at `02_MARINE MEGAFAUNA/REFERENCE LIBRARY/Paperpile Library/` — these are Simon's curated, ground-truth records. Hits short-circuit the external waterfall entirely. References without a DOI (or with a DOI not in the mirror) fall through to Semantic Scholar → CrossRef → OpenAlex with ~1s between queries. In-library hits also run an author + year sanity check; a mismatch with the curated record raises a new `CONFLICT` status (the library disagrees with the manuscript).

To disable in-library lookup (emergency override, e.g. mirror suspected stale): pass `--no-paperpile` or set `VERIFY_CITATIONS_NO_PAPERPILE=1`.

For a 30-reference paper with ~half resolvable in-library, expect ~30 seconds total instead of ~90.

**If the script fails:**
- `urllib.error.URLError` — network issue; retry once after 5s
- Empty output — the references section wasn't detected; check the heading format (expects `## References` or similar H2)
- Parse errors on many refs — the reference format may be non-standard; read the References section and feed individual refs to the script with `--refs-only`
- `[paperpile] build-status not ready` — the mirror is mid-rebuild or unavailable; the script silently falls back to the external waterfall (this is correct behaviour, not an error)

### 3. Review the report

Read `/tmp/citation-report.md` and present results to the user, organised by severity:

1. **Not Found** — highest priority. These may be fabricated. For each:
   - Do a WebSearch to try to find the paper manually
   - If found, note why the API missed it (unusual title, very new, book chapter)
   - If not found anywhere, flag as **likely fabricated**

2. **Conflict (in-library)** — highest signal. The cited DOI matches a paper in Simon's curated Paperpile library, but the manuscript's author or year disagrees with the curated record. Library is the source of truth — likely a citation error in the manuscript:
   - First-author mismatch: usually a copy-paste error from another citation, or wrong DOI altogether
   - Year mismatch (>1 year): could be the manuscript citing the preprint while listing the published year, or vice versa — check the wikilink to the paper note

3. **Partial Match** — review each issue:
   - Author mismatch: check if it's a formatting difference (e.g. hyphenated name) vs a real error
   - Year mismatch: ±1 year is common for preprint→published transition; >1 year is suspicious

4. **Verified** — no action needed. If `Paperpile (in-library)` is the source, the report includes a wikilink to the curated paper note for easy follow-up.

### 4. Present summary

Give the user a concise summary:
- Total refs, in-library coverage count, verified count, issues count
- List each problem reference with the specific issue and recommended fix
- If DOIs were found for references that lack them, offer to patch them automatically:
  ```bash
  python3 "$HOME/.claude/skills/verify-citations/verify_citations.py" "MANUSCRIPT_PATH" --patch-dois
  ```
  This rewrites the manuscript in-place, inserting DOIs where the API found them. Show Simon a diff of the changes before confirming.

### 5. Post-run self-assessment

- How many references were NOT_FOUND? If >20% of refs, investigate whether the reference format confused the parser.
- How many references resolved in-library (Paperpile)? If <10% on an MMF-relevant manuscript, the manuscript may be citing outside Simon's curated library — worth noting, but not a problem.
- Were there CONFLICT entries? Each one is high-signal — flag prominently.
- Were there API failures? Note any that should be retried.
- Did any VERIFIED results look suspicious on closer inspection?

## Known limitations

- **No DOI in cited reference** → in-library lookup is skipped for that ref; external waterfall runs as today. The mirror has ~75% DOI coverage so this is usually fine.
- **Book chapters and reports** rarely appear in Semantic Scholar or CrossRef. NOT_FOUND doesn't always mean fabricated — grey literature, government reports, and book chapters have lower API coverage.
- **Very recent papers** (last 1-2 months) may not be indexed yet.
- **Title matching** uses word overlap, not exact match. Short or generic titles may produce false matches.
- The parser expects author-year format (`Author (Year) Title. Journal`). Numbered reference styles (e.g. `[1]`) need manual extraction with `--refs-only`.
