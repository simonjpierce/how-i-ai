---
name: science-paper
description: Structure scientific analysis sessions with lab notebook discipline, and draft manuscripts from completed notebooks. Two modes — "lab notebook" (activate at session start for interactive analysis, enforces update-after-each-step gate) and "manuscript" (draft a paper from a completed analysis note). Use when the user says "/science-paper", "lab notebook mode", "start the lab notebook", "draft a manuscript", "write the paper", or when beginning any data analysis session that will produce publishable results. Also trigger when the user asks to "activate" or "get running" the science-paper approach.
---

Scientific analysis and writing skill. Two modes: **lab notebook** (interactive analysis sessions) and **manuscript** (paper drafting from completed notebooks).

Takes `$ARGUMENTS`:
- No args or `lab` → lab notebook mode
- `manuscript` or `draft` + a file path → manuscript drafting mode
- A file path alone → infer mode from the file (analysis note → lab notebook, completed note → manuscript)

## Adapting this for your work

This skill ships ready-to-use but assumes the conventions below. Override by editing this file or by adding values to your per-vault `config.json`:

- **Manuscripts folder** — defaults to `<vault>/MANUSCRIPTS/` (read `vault.path` from `~/.claude/projects/<project-key>/config.json`). If your vault uses a domain layout (e.g. `<domain>/MANUSCRIPTS/`), choose the right domain folder when creating the project. Ask the user if unsure.
- **GitHub namespace** — defaults to your authenticated GitHub user (`gh api user --jq .login`). If you publish under an org (e.g. a lab account), set it explicitly when creating the repo.
- **Google Drive folder** — optional. The skill creates a Drive subfolder for shareable artifacts only if you have Google Drive set up locally; skip cleanly if no Drive folder is mounted. Adapt the path to your account.
- **Citation verification** — uses the bundled `/verify-citations` skill (which queries Semantic Scholar, CrossRef, OpenAlex). No external scripts required.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step.

---

## Mode 1: Lab Notebook

Activate at the start of an interactive analysis session. The analysis note is the **primary document** — the authoritative record of the work. It captures full detail on data, methods, decisions, results, and interpretation. Detail is a feature, not a bug.

### Setup

1. **Create or locate the project folder.** Each manuscript gets its own folder under a `MANUSCRIPTS/` directory in the vault — typically `<vault>/MANUSCRIPTS/` for a single-domain vault, or `<domain>/MANUSCRIPTS/` for a vault with domain folders. Read `vault.path` from `~/.claude/projects/<project-key>/config.json` and pick the appropriate location (ask if ambiguous). Name the project folder descriptively (e.g., `Whale Shark Transience/`, `Acoustic LIR/`). If one already exists for this project, use it.

2. **Create or locate the analysis note (lab notebook).** Lives in the project folder. Template:

   ```markdown
   ---
   title: "Analysis title"
   date: YYYY-MM-DD
   status: In progress
   dataset: source description
   source_paper: "citation if applicable"
   manuscript: "Manuscript Draft — Topic"
   ---

   # Analysis title

   ## Research Questions
   ## Context
   ## Data
   ## [Analysis sections — added as work proceeds]
   ## What's next
   ## Artifacts
   ```

3. **Create the manuscript draft.** Also in the project folder. Scaffolding only — drafting happens after the analysis is complete (Mode 2):

   ```markdown
   ---
   title: "Manuscript title"
   date: YYYY-MM-DD
   status: Not started
   journal: TBD
   authors: TBD
   lab_notebook: "Analysis — Topic"
   ---

   # Manuscript title

   Drafting happens after the lab notebook is complete. See Analysis — ....
   ```

4. **Create a code repo for the analysis.** Any analysis code gets its own version-controlled repo. Pre-flight `gh` (GitHub CLI) availability before deciding which path to take:

   ```bash
   if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
     GH_AVAILABLE=true
   else
     GH_AVAILABLE=false
   fi
   ```

   **If `GH_AVAILABLE=true` (preferred):** create a private GitHub repo. Default to the authenticated user's namespace; use an org if the user publishes under one (ask if unsure):

   ```bash
   GH_USER=$(gh api user --jq .login)
   gh repo create "$GH_USER/<project-name>" --private
   git clone "https://github.com/$GH_USER/<project-name>.git" "$HOME/repos/<project-name>"
   ```

   **If `GH_AVAILABLE=false` (no `gh`, or not authenticated):** create a local-only git repo. Tell the user *"GitHub CLI isn't installed/authenticated, so I'm creating a local-only repo at `~/repos/<project-name>/`. To later push to GitHub: install `gh` (`brew install gh`), authenticate (`gh auth login`), then add a remote with `cd ~/repos/<project-name> && gh repo create --source=. --private --push`."* Then:

   ```bash
   mkdir -p "$HOME/repos/<project-name>"
   cd "$HOME/repos/<project-name>"
   git init -q
   ```

   In either case, set up the directory structure: `scripts/`, `data/cleaned/`, `outputs/`. Don't block the rest of `/science-paper` setup on remote-repo creation — the lab notebook + local git history are the rigorous core; remote push is a backup convenience.

5. **(Optional) Create a Google Drive folder** for shareable artifacts (figures, tables, supplementary material). Skip if Google Drive isn't mounted locally. Adapt this path to your account:
   ```
   ~/Library/CloudStorage/GoogleDrive-<your-email>/My Drive/Manuscripts/<Project Name>/
   ```
   Create subdirectories: `Figures/`, `Tables/`, `Supplementary/`. This is where publication-quality outputs go for co-author sharing.

6. **Create a figures folder in the vault project folder** for Obsidian embedding:
   ```
   <vault-project-folder>/figures/
   ```
   When analysis produces plots, save them here (PDF + PNG). They can then be embedded in the lab notebook using `!figures/plot_name.png` for inline preview while reading the notebook in Obsidian. Also copy to the Google Drive folder for external sharing if you set one up.

7. **Add all files to the Artifacts table** — lab notebook, manuscript, GitHub repo, Google Drive folder, vault figures folder, source data paths, reference papers.

8. **Register with /update.** The `/update` skill reads the Artifacts table to find associated documents. By listing everything in Artifacts, `/update` will automatically check, maintain, and push code changes. No additional configuration needed — the Artifacts table is the contract.

9. **Announce the gate.** Confirm to the user: "Project folder, lab notebook, manuscript, {GitHub|local-only} repo, and Google Drive folder set up. Lab notebook gate active — I'll update the analysis note after each step before proceeding." (Substitute "GitHub" if `GH_AVAILABLE=true` was set in step 4, "local-only" otherwise.)

7b. **Create `sync_figures.sh`** in the repo root. This script copies all figures from the repo `outputs/` to the vault and Google Drive in one command:

   ```bash
   #!/bin/bash
   # sync_figures.sh — copy figures from repo outputs to vault and Google Drive
   # Generated by /science-paper skill. Paths are project-specific.

   REPO_OUTPUTS="$(cd "$(dirname "$0")" && pwd)/outputs"
   VAULT_FIGURES="<vault-project-folder>/figures"
   GDRIVE_FIGURES="<gdrive-manuscripts-folder>/Figures"
   DPI=200  # PNG conversion resolution

   copied=0
   converted=0

   # Copy existing PNG/SVG files directly
   for ext in png svg; do
     for f in "$REPO_OUTPUTS"/*."$ext"; do
       [ -f "$f" ] || continue
       name=$(basename "$f")
       cp "$f" "$VAULT_FIGURES/$name" 2>/dev/null && ((copied++))
       cp "$f" "$GDRIVE_FIGURES/$name" 2>/dev/null
     done
   done

   # Convert PDFs to PNG for Obsidian inline display, and copy PDFs to Drive
   for f in "$REPO_OUTPUTS"/*.pdf; do
     [ -f "$f" ] || continue
     name=$(basename "$f" .pdf)
     if command -v pdftoppm &>/dev/null; then
       pdftoppm -png -r "$DPI" -singlefile "$f" "$VAULT_FIGURES/$name" && ((converted++))
       pdftoppm -png -r "$DPI" -singlefile "$f" "$GDRIVE_FIGURES/$name" 2>/dev/null
     else
       cp "$f" "$VAULT_FIGURES/$name.pdf" 2>/dev/null && ((copied++))
     fi
     cp "$f" "$GDRIVE_FIGURES/$name.pdf" 2>/dev/null
   done

   echo "Synced $copied files + converted $converted PDFs to PNG (${DPI} DPI)"
   ```

   Fill in the actual paths during setup. Make executable: `chmod +x sync_figures.sh`.

### Saving figures

R scripts save plots to the repo `outputs/` directory as usual. Then:

```bash
./sync_figures.sh
```

This converts PDFs to PNGs (200 DPI, via `pdftoppm`) for Obsidian inline display, copies existing PNGs/SVGs directly, and syncs PDFs to Google Drive. Run it after any analysis step that produces plots, or as part of `/update`. Requires `pdftoppm` (from poppler: `brew install poppler`).

After syncing, embed in the lab notebook at the relevant analysis step: `!figures/plot_name.png`

### The gate (hard rule)

**Every analysis step must go through the joint two-model gate below before proceeding to the next step.** This is non-negotiable. "Step" means any operation that produces a result: data cleaning, a statistical test, model fitting, a comparison, an interpretation.

Each step has four phases: (1) **joint method planning** with Codex *before* execution, (2) **execution**, (3) **numerical verification** with Codex *after* execution, then (4) the **notebook update**. The pre-step catches methodology errors (wrong test for the data, missing diagnostic, biased subset, ignored confound — things a numerical check can never see). The post-step catches execution/transcription errors (right test, wrong number copied to notebook). Both are needed; they catch different failure classes.

#### 1. Pre-step — joint method planning with Codex

Before writing any code or running any analysis for this step:

a. **State the proposed approach explicitly.** Write a structured plan covering: *what you're doing*, *the method you'll use*, *why you picked that method*, *the assumptions you're making*, *what output you expect*.

b. **Dispatch to Codex (bare `gpt-5.5`, xhigh from config) as an independent peer reviewer.** Write the prompt to `/tmp/sci-paper-method-review.md`:

   ```
   You are an independent statistical/methodological peer reviewer for a scientific analysis. The lead analyst (Claude Opus) is about to take the step described below. Read the prior notebook context and the proposed step, then:

   1. INDEPENDENTLY propose a method for this step — what would YOU do given the same question and data? Don't anchor on Opus's choice; reason from scratch.
   2. CRITIQUE Opus's proposal — what assumption is being made? What alternative method might be stronger? What prerequisite test or diagnostic is missing? What confound is being ignored?
   3. VERDICT: ALIGNED (your method matches Opus's) | CAVEAT (Opus's method is acceptable but with the caveat that ...) | DIVERGENT (you would do something different — explain).

   Cite the notebook section / data column / prior step that grounds your reasoning. No hand-waving — be specific.

   ## Notebook context (prior steps)
   <paste the relevant prior notebook sections>

   ## Data structure
   <paste data dictionary, head of the relevant data frame, or schema>

   ## Proposed step
   - What I'm doing: <...>
   - Method: <...>
   - Why this method: <...>
   - Assumptions: <...>
   - Expected output: <...>
   ```

   Dispatch:

   ```bash
   codex exec --full-auto --skip-git-repo-check --sandbox read-only \
     "Read /tmp/sci-paper-method-review.md and follow the instructions exactly." \
     < /dev/null
   ```

   - Model + reasoning effort come from `~/.codex/config.toml` (bare `gpt-5.5` + xhigh — the only model variant accessible via CLI on a ChatGPT account; `-fast`/`-pro` return 400). Do NOT pass `-m` or `-c model=...`.
   - `--sandbox read-only`: the method-review pass must not modify files; only reads notebook context + data dictionary.
   - `< /dev/null`: mandatory in Codex v0.130.0 — prompt-as-positional-arg still tries to read stdin and hangs without an explicit close. See `memory/reference_codex_cli.md`.

c. **Adjudicate based on Codex's verdict:**
   - **ALIGNED** → proceed to phase 2 (execution).
   - **CAVEAT** → present Codex's caveat to Simon. If trivial (e.g. report an additional diagnostic alongside), note in the notebook and proceed. If substantive (e.g. add a sensitivity analysis), pause for Simon's call.
   - **DIVERGENT** → present BOTH methods to Simon with the trade-offs each model identified. Do **not** proceed unilaterally. Simon decides.

d. **Sonnet/manual fallback**: if Codex CLI is unavailable or errors, spawn a Sonnet subagent with the same peer-review prompt. If Sonnet also fails, surface the methodological choice to Simon directly with the peer-review questions answered as best Opus can. Never skip the pre-step gate silently.

#### 2. Execute the step

Run the agreed-upon analysis. Save outputs to `outputs/` per the repository convention.

#### 3. Post-step — numerical verification with Codex

Before writing the notebook update:

a. **State what numbers you are about to write** (sample sizes, p-values, effect sizes, parameter estimates, CIs, etc.).

b. **Dispatch Codex (bare `gpt-5.5`, xhigh from config) as a numerical verifier.** Write the prompt to `/tmp/sci-paper-number-check.md`:

   ```
   You are verifying numerical claims for a scientific analysis. Below are numbers Claude Opus is about to write to the lab notebook. Verify each against the actual code output.

   For each claim:
   1. Locate the corresponding line(s) in the actual output file (path provided). Quote the output verbatim with file:line reference.
   2. State whether the quoted output supports the claim Opus is making.
   3. If you cannot find the source for a claim, return DISCREPANCY with reason.

   **Bare assertions without verbatim output quotation are treated as FAILED verification.** Quote the actual output text — do not produce your own answer from scratch.

   Verdict per claim: APPROVED | DISCREPANCY (with details).

   Script: <path to script that produced the output>
   Output file(s): <path(s) to output file(s) — console log, CSV, model summary, etc.>
   Claims to verify:
   - <claim 1, with the value Opus is about to write>
   - <claim 2>
   - ...
   ```

   Dispatch via the same `codex exec` syntax (no `-m` / `-c model=...` overrides). Same flags: `--full-auto --skip-git-repo-check --sandbox read-only` + `< /dev/null` to close stdin.

c. **Adjudicate**:
   - **All APPROVED** → write the notebook update and proceed.
   - **Any DISCREPANCY** → pause. Re-read the actual output yourself. If Codex misread the output, document why and proceed. If Opus's claim was wrong, fix the claim before writing the notebook.

d. **Sonnet/manual fallback**: same as pre-step. Never skip the post-step gate silently.

#### 4. Notebook update

Each update includes:

- **What was done** (method, parameters, script used)
- **What was found** (numbers, tables, key statistics)
- **What it means** (interpretation, implications for next steps)
- **Outputs** (file paths for scripts, data files, plots)
- **Method review** — one line on Codex's pre-step verdict: ALIGNED / CAVEAT (summary) / DIVERGENT (and how it was resolved)
- **Verification** — one line confirming all numerical claims passed Codex's post-step check, or a note on any discrepancy and how it was resolved

This makes the two-model collaboration auditable: a future reader (or peer reviewer) can see that both models signed off on each step's method and numbers.

### What belongs in the lab notebook vs. not

**In the notebook:** Data summaries, parameter tables, cleaning steps, model outputs, interesting observations, statistical reasoning, dead ends, decision rationale, sensitivity checks, all key numbers with context.

**Not in the notebook:** Verbose tool output, raw data dumps, intermediate debugging. Summarise these; don't paste them.

### Conventions

- **Tables for structured results.** Parameter estimates, model comparisons, data summaries — use markdown tables, not prose.
- **Status field.** Update the YAML `status` field after each major step to reflect current state.
- **What's next section.** Maintain a running list. Strike through completed items with `~~text~~`. Add new items as they emerge.
- **Artifacts table.** Maintain a `## Artifacts` table listing all associated files (scripts, data, outputs, related docs, repos). Add new files as they're created.

### At session end

Run `/update` (which now includes code backup — committing and pushing to GitHub). The analysis note should already be current if the gate was followed.

---

## Mode 2: Manuscript

Draft a scientific paper from a completed analysis note. The manuscript is a **derivative product** — it draws from the lab notebook but restructures for the reader. It should never replicate the notebook's structure.

### Inputs needed

1. **Analysis note (lab notebook)** — the primary source of all results and methods
2. **Reference paper(s)** — for ecological context, prior work at the site, citation style
3. **Code repository** — to verify what the code actually does vs. what the notebook says
4. **Red-team report** — if available, to preemptively address reviewer concerns

### Confirm scope with the user

Before writing, confirm:
- Target journal and format
- Author list and order
- Which results to include (the notebook may contain more than the paper needs)
- Any specific framing or narrative the user wants

### Writing order

1. **Methods** — anchored to the code, not memory. Read the scripts and describe what they do.
2. **Results** — from the analysis note tables and numbers. Every metric in Results must have a Methods definition.
3. **Introduction** — contextualise with reference papers. Prior work at this site → gap → what this paper does.
4. **Discussion** — interpret results, address limitations, management implications.
5. **Abstract** — last. Summarise everything.

### Structure patterns

- **Results: run Test 3.SR before model fitting** as standard practice. Report regardless of result — either outcome informs model selection.
- **Results: start with data description** — cleaned dataset summary, sighting frequency, population structure. This grounds the reader before any model output.
- **Results: standard sensitivity steps** — (1) Bootstrap CIs for all key parameters. (2) Split-period effort sensitivity if applicable.
- **Discussion structure:** heterogeneity interpretation → ecological implications → methodological considerations → conservation/management.

### Common mistakes to avoid

These are patterns that produced reviewer-catchable errors in prior manuscripts:

1. **Derived metrics used in Results but not defined in Methods.** Every metric needs a Methods definition before it appears in Results.
2. **Circular validation presented as independent evidence.** If classification was built from encounter history, tests derived from encounter history are not independent. Frame as "characterisation" or "diagnostics."
3. **Model parameters overinterpreted.** Mixture weight pi is not a population fraction. N parameters are not additive daily abundances. Be precise about what the parameterisation identifies vs. what we'd like it to mean.
4. **Survival formula inconsistency.** Continuous-time models use exp(-delta*t), not (1-delta)^t.
5. **Documentation ahead of code.** Verify scripts produce the documented values before submission.
6. **Language too strong for the evidence.** Avoid "demonstrate", "genuine dichotomy", "permanently depart". Use "consistent with", "supports", "no detectable differences."
7. **Apparent survival ≠ true survival.** Conflates mortality and permanent emigration.
8. **Point estimates without uncertainty.** All key parameters need CIs or profile intervals.

### Figure conventions

1. **Y-axis headroom** — axis maximum visibly higher than tallest data point.
2. **Uniform bar colour** — one colour unless colour encodes a variable.
3. **All labels present** — test with actual `pdf()` device. Use `title()` separately with adequate margins.
4. **Correct axis assignment** — count/measure on y-axis, grouping variable on x-axis.

### Quality checks before delivery

**Completeness:**
- Every Result has a Method; every Method has a Result
- Every citation in text is in References (and vice versa)
- Every key parameter has uncertainty
- Full model-selection table present
- Figures exist for every pattern described repeatedly in text

**Accuracy:**
- Code parameters match paper claims (run scripts, compare output)
- Correct continuous vs. discrete formulas
- Statistical tests report test statistics, df, effect sizes — not just p-values
- **Citation verification** — run the bundled `/verify-citations` skill on the manuscript file. It queries Semantic Scholar, CrossRef, and OpenAlex and writes a report flagging NOT_FOUND references as potentially fabricated. Run before red-team or co-author review.

**Calibration:**
- Scan for overclaimed language
- Apparent survival acknowledged as conflating mortality + permanent emigration
- Non-stationarity explicitly addressed
- Mixture model acknowledged as approximation, not proof of biological dichotomy

**Number consistency:**
- **Cross-document number check.** Grep key quantities (sample sizes, date ranges, model parameters, percentages) across the analysis note, manuscript draft, and scripts. Flag any mismatches. Example: the analysis note says "868 individuals" but the manuscript says "846" — that's an error that propagates silently across documents. Run this check before sharing with co-authors:
  ```bash
  # Extract key numbers from each document and compare
  for term in "individuals" "encounters" "sighting days" "period-pairs"; do
    echo "=== $term ==="
    grep -in "$term" ANALYSIS_NOTE MANUSCRIPT SCRIPT_OUTPUT | head -5
  done
  ```
  Adapt the search terms to the specific analysis. The goal is to catch copy-paste drift between the lab notebook (source of truth), the manuscript (derivative), and the code output (ground truth).

- **Optional structural Codex review of the manuscript.** For manuscripts with substantive analysis claims (mixture models, survival, capture-recapture, anything Codex's source-line verification would catch), run `/codex-review <manuscript-path>` BEFORE `/red-team`. This dispatches a single-target Codex pass that verifies every claim in the manuscript against the lab notebook + scripts cited, returning structured drift/missing/miswired findings. Stronger than the grep-based number check above for catching cross-document logical drift (e.g. a Methods section describes a model variant the Results don't actually report, or a Results sentence cites a parameter that no script outputs). Per-step Codex gates above already cover individual analysis steps; `/codex-review` covers the manuscript-as-a-whole.

**Reproducibility:**
- Scripts reproduce all documented values from a cold start
- Data files and analysis objects tracked in repo

### Regression-test conventions (added 2026-05-11)

When a fix REFACTORS an existing function by extracting a helper:

- **Test at BOTH levels.** Unit tests on the helper catch its own logic; end-to-end tests on the wrapper catch its control flow around the helper (indentation, `continue`/`return` placement, branch reachability, orphan `else` clauses left over from the original structure). Helper-only tests can pass while the wrapper is silently broken.
- **Failure history (2026-05-11):** `scan_proposal_decisions()` got 9 unit tests on its new `_extract_decision_section()` helper. All passed. Wrapper had a control-flow bug — structured-status parsing block unreachable after a `continue` — that misclassified every non-empty `## Decision` as `unreviewed` for hours until Codex's review of a different spec audited surrounding state and caught it. End-to-end tests on the wrapper would have caught the regression on the same `python3 run_regression_tests.py` pass that gave the green light to ship.
- **Heuristic:** count call sites of the helper inside the wrapper. If > 0 (which is always for a freshly extracted helper), the wrapper needs at least one test fixture per branch that consumes the helper's output (typically: empty result, populated result, edge case). The wrapper test should NOT mock the helper — it should run end-to-end through both.

This convention applies to any obsidian_reviews script with a helper+wrapper structure (`self_improve.py`, `nightly_workhorse.py`, `domain_expert_sweep.py`, etc.), not just /science-paper analyses.

### Post-draft

After completing the draft:
- Run `/verify-citations` on the manuscript — don't wait for red-team to catch fabricated references
- Offer to run `/red-team` on it
- Create a `/todo` for the user to review the draft
- Check the [Wikipedia AI writing tells](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) list if a humanisation pass is wanted

---

## Post-run self-assessment

After completing either mode, briefly assess:
- **Lab notebook mode:** Was the gate followed consistently? Were any results produced without being documented? Was the Artifacts table maintained?
- **Manuscript mode:** Does every Result have a Method? Were any common mistakes (list above) present in the draft? Did the code verification step catch any discrepancies?

Flag issues found to the user.
