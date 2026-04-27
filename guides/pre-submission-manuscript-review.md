# Pre-Submission Manuscript Review — Prompt Template

> **Adapting this for your work.** This prompt template is field-agnostic — it works for any scientific manuscript across any discipline. The examples and stylistic notes were authored by Simon Pierce (marine biology / shark conservation), but no part of the prompt depends on your field. Use it as-is in Claude or any other AI tool.

A template for researchers to get thorough, journal-ready feedback on manuscripts before submission.

---

## How to Use This Prompt

### What this is for
This prompt is designed to get a comprehensive pre-submission review that mimics what a constructive peer reviewer would flag—catching methodological gaps, inconsistencies, and areas needing clarification *before* formal review, when they're easier to fix.

### File format considerations

**Word documents (.docx):** Claude can add tracked changes and comments directly to the document. Comments appear as proper Word comments with author attribution, and text suggestions appear as tracked insertions/deletions. This produces a document you can review in Word's standard review interface. This is the recommended approach when using Claude.

For ChatGPT or other AI tools that do not reliably support in-document tracked changes, request a **section-by-section review** that references specific headings, page or line numbers, or quoted snippets from the manuscript. This allows you to locate and implement suggested changes accurately, even without direct file annotation.

**Google Docs:** Direct in-line commenting isn't currently possible. Workarounds:
- *Best option:* Export your Google Doc as .docx (File → Download → Microsoft Word), upload that for review, then incorporate changes back into Google Docs
- *Alternative:* Request section-by-section commentary that references specific text, which you then action manually

### If your AI tool cannot edit the document directly

If your AI tool does not support tracked changes or in-line comments in .docx files, request the following instead:

- A **section-by-section review** organised by manuscript headings (e.g., Introduction, Methods, specific subsections)
- Each comment should:
  - Quote a short snippet of the relevant text (10–30 words), or
  - Reference the exact section, page, or line number
- Where appropriate, ask for **proposed replacement text** for key paragraphs (e.g., Methods or Discussion), provided separately so you can paste it in manually

This approach still allows for detailed, actionable feedback without relying on direct document editing.

### What makes this work well

1. **Provide expert input if you have it.** If a co-author or collaborator has already flagged concerns (even informal email feedback), include it. Domain-specific critique from specialists helps focus the review on real issues rather than generic suggestions.

2. **Specify your target journal.** This helps calibrate the review to appropriate expectations—methods rigour for a stats-heavy journal, accessibility for a general ecology journal, policy relevance for a conservation journal, etc.

3. **Flag your specific concerns.** If you already suspect the model selection is weak or the discussion is too long, say so. This focuses attention where you need it most.

4. **Request prioritised output.** A flat list of 30 suggestions is hard to action. Asking for priority tiers (high/medium/low or "likely reviewer flags" vs "nice to have") helps you triage revision time.

5. **Ask for in-line comments *and* a summary.** The in-line comments show exactly where issues occur; the summary helps you see the big picture and plan your revision strategy.

### Attachments to include
- Your manuscript (.docx preferred)
- Any existing feedback from co-authors or collaborators
- Relevant supplementary files if the review needs to check consistency (e.g., if your methods reference supplementary tables)

---

## The Prompt Template

Copy and adapt the following:

~~~
I'm preparing to submit the attached manuscript to [JOURNAL NAME]. The manuscript is [brief description: e.g., "a 14-year mark-recapture study on coastal shark population dynamics" or "a systematic review of marine protected area effectiveness"].

Please provide a thorough pre-submission review with the following outputs:

1. Either:
   - **In-line comments and tracked changes** added directly to the Word document (if your AI tool supports this), or
   - A **section-by-section annotated review** keyed to manuscript headings, with quoted text snippets to anchor each comment

2. **A summary document** organising the main feedback by priority:
   - High priority issues (likely to be raised by reviewers; should be addressed before submission)
   - Medium priority improvements (would strengthen the paper but not fatal if missed)
   - Minor/housekeeping items (typos, formatting, reference issues)

**Review focus areas:**
- Methodological rigour: Are the approaches appropriate and adequately justified? Are assumptions stated?
- Statistical reporting: Are model selection, diagnostics, and results reported to current standards?
- Internal consistency: Do the methods, results, figures, and tables all align?
- Logical flow: Is the argument clear from introduction through to conclusions?
- Gaps and oversights: What will reviewers likely flag as missing, unclear, or inadequately addressed?
- Scope and framing: Is the discussion appropriately bounded? Are claims supported by the results?

**Specific concerns I'd like you to examine:**
[Delete or adapt as relevant]
- Is the [specific analysis, e.g., "CMR model selection"] adequately justified?
- Does the [specific section] need more/less detail?
- Are there statistical assumptions I should check or acknowledge?
- Is consistency between [methods/results/figures] maintained throughout?
- [Add your own concerns]

**Context:**
- Target journal: [journal name and brief scope if helpful, e.g., "Endangered Species Research—conservation-focused, expects management implications"]
- Co-author/collaborator feedback: [attach or paste, or write "none"]
- Known limitations I'm already planning to address: [list, or "none—please flag anything you find"]

**Tone:** Constructive and collegial. This is a pre-submission improvement process, not an adversarial review. The goal is to pre-empt predictable reviewer critiques and strengthen the paper. Frame suggestions as "reviewers may ask..." or "consider adding..." rather than "this is wrong."

If using Claude, please read the attached docx **SKILL.md** file before making in-line changes to ensure comments and tracked changes are properly formatted.

If using ChatGPT or another AI tool that does not support tracked changes, provide comments keyed to manuscript section headings, and **quote the exact sentence or phrase you are referring to** before suggesting edits.
~~~


---

## After the Review

Once you receive the annotated document and summary:

1. **Start with the summary** to understand the scope of revisions needed
2. **Address high-priority items first**—these are the ones most likely to cause problems in peer review
3. **Work through in-line comments** using Word's review interface (or re-import to Google Docs)
4. **Use the "resolve" function** in Word/Docs to track your progress
5. **Consider a second pass** after major revisions if the document has changed substantially

### For high-stakes manuscripts: dual-model review via `/red-team`

The prompt template above produces a single-model, single-pass review. For manuscripts where the stakes justify deeper scrutiny (high-impact journals, grant applications, or papers with complex claims), consider running `/red-team` on the manuscript markdown instead. This provides:

- **Two independent reviews**: a Claude subagent using a structured rubric, then a Codex (GPT) second opinion using a deliberately different, open-ended approach
- **Convergence as signal**: issues flagged by both models (different architectures, different prompts) are high-confidence problems
- **Claim verification**: key factual claims spot-checked against primary sources via web search
- **Snapshot and rollback**: pre-edit snapshots so you can undo any changes

The `/red-team` approach takes longer (~15–20 minutes) but consistently catches issues that single-pass reviews miss — particularly structural weaknesses, scope overreach, and claims that sound authoritative but are poorly supported.

### Final grammar and style pass

After addressing all review feedback, run `/polish` on the manuscript markdown file (or the exported `.md` version). This catches residual grammar/spelling errors, style inconsistencies, and AI writing patterns that the content review may have missed. Use `--language en-GB` by default; switch to `en-US` if the target journal requires American English. The `/polish` skill is context-sensitive — it's more tolerant of passive voice and formal phrasing in scientific writing.

Good luck with the submission!