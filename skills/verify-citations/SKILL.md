---
name: verify-citations
description: Verify citations in a scientific manuscript against Semantic Scholar, CrossRef, and OpenAlex. Flags fabricated papers, wrong authors/years, and missing DOIs. Use when the user says "/verify-citations", "check citations", "verify references", or "citation audit". Accepts a file path as $ARGUMENTS.
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

The verifier is bundled with this skill at `$HOME/.claude/skills/verify-citations/verify_citations.py` (only requires Python 3 + `requests` — both installed by `/onboard` pre-flight).

```bash
python3 "$HOME/.claude/skills/verify-citations/verify_citations.py" "MANUSCRIPT_PATH" -o /tmp/citation-report.md
```

The script queries three APIs per reference (Semantic Scholar, CrossRef, OpenAlex) with ~1s between queries. For a 30-reference paper, expect ~60-90 seconds total.

**If the script fails:**
- `urllib.error.URLError` — network issue; retry once after 5s
- Empty output — the references section wasn't detected; check the heading format (expects `## References` or similar H2)
- Parse errors on many refs — the reference format may be non-standard; read the References section and feed individual refs to the script with `--refs-only`

### 3. Review the report

Read `/tmp/citation-report.md` and present results to the user, organised by severity:

1. **Not Found** — highest priority. These may be fabricated. For each:
   - Do a WebSearch to try to find the paper manually
   - If found, note why the API missed it (unusual title, very new, book chapter)
   - If not found anywhere, flag as **likely fabricated**

2. **Partial Match** — review each issue:
   - Author mismatch: check if it's a formatting difference (e.g. hyphenated name) vs a real error
   - Year mismatch: ±1 year is common for preprint→published transition; >1 year is suspicious

3. **Verified** — no action needed, but note any missing DOIs that could be added

### 4. Present summary

Give the user a concise summary:
- Total refs, verified count, issues count
- List each problem reference with the specific issue and recommended fix
- If DOIs were found for references that lack them, offer to patch them automatically:
  ```bash
  python3 "$HOME/.claude/skills/verify-citations/verify_citations.py" "MANUSCRIPT_PATH" --patch-dois
  ```
  This rewrites the manuscript in-place, inserting DOIs where the API found them. Show Simon a diff of the changes before confirming.

### 5. Post-run self-assessment

- How many references were NOT_FOUND? If >20% of refs, investigate whether the reference format confused the parser.
- Were there API failures? Note any that should be retried.
- Did any VERIFIED results look suspicious on closer inspection?

## Known limitations

- **Book chapters and reports** rarely appear in Semantic Scholar or CrossRef. NOT_FOUND doesn't always mean fabricated — grey literature, government reports, and book chapters have lower API coverage.
- **Very recent papers** (last 1-2 months) may not be indexed yet.
- **Title matching** uses word overlap, not exact match. Short or generic titles may produce false matches.
- The parser expects author-year format (`Author (Year) Title. Journal`). Numbered reference styles (e.g. `[1]`) need manual extraction with `--refs-only`.
