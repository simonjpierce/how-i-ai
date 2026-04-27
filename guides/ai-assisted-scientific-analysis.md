# AI-Assisted Scientific Analysis — Process Guide

> **Adapting this for your work.** This guide is written by Simon Pierce, marine biologist at the Marine Megafauna Foundation, and the examples are drawn from MMF's whale shark / shark / marine mammal analyses. The *workflow* (lab-notebook discipline, the gate, manuscript separation, pre-submission checks) generalises to any scientific analysis. When reading: substitute your own domain and reference paths for the MMF-specific examples; the structure of the process is what to keep. The bundled `/science-paper` skill operationalises this guide — it routes manuscripts to your vault's MANUSCRIPTS folder and reads project paths from `config.json`.

---

# /science-paper skill — design notes

Captured from the Moz whale shark LIR paper session (4 April 2026).

## What the skill should do

Write a first draft of a scientific paper in standard journal format (Abstract, Introduction, Methods, Results, Discussion, References) from analysis notes, code, and reference papers.

### Lab notebook ≠ manuscript

The **analysis note** (e.g. `Analysis — Thailand Whale Shark LIR.md`) is a **lab notebook**: the authoritative record of the work. It captures full detail on data, methods, decisions, results, and initial analysis/interpretation — everything needed for complete reproducibility. Data summaries, parameter tables, cleaning steps, model outputs, interesting observations, statistical reasoning, and dead ends all belong here. It's written for future-us and for any collaborator who needs to understand or reproduce what was done. Detail is a feature, not a bug.

The **manuscript draft** (e.g. `Manuscript Draft — *.md`) is a separate document in journal format. It draws from the lab notebook but restructures for the reader: compressed, formal, no decision logs, no "we tried X and it didn't work." The manuscript references the analysis note for provenance, but doesn't replicate its structure.

**The lab notebook is the primary document.** During interactive analysis sessions, `/update` should point to the lab notebook — that's where results are captured as they're produced. The manuscript draft is a derivative product, written later from the completed notebook. The skill should never try to make the analysis note manuscript-shaped, or the manuscript notebook-shaped. They serve different audiences and have different lifespans.

## Patterns observed

### Inputs needed
- **Analysis note (lab notebook)** — the working document with all results, methods decisions, parameters, interpretive reasoning
- **Reference paper(s)** — for ecological context, prior work, citation style
- **Code repository** — for methods accuracy (what the code actually does vs what we think it does)
- **Red-team report** — if available, to preemptively address reviewer concerns in the text

### Common mistakes in first drafts
1. **Derived metrics used in Results but not defined in Methods** — αLIR, apparent survival formula, etc. Every metric needs a Methods definition before it appears in Results.
2. **Prior analyses mentioned in Introduction but not contextualised** — need to explain what they found AND how this work extends them.
3. **Circular validation presented as independent evidence** — if the classification was built from encounter history, tests derived from encounter history (resighting span, cross-period persistence) are not independent validation. Frame correctly as "characterisation" or "diagnostics". Independent tests use variables not in the classification (sex, size, seasonality).
4. **Model parameters overinterpreted** — π is a mixture weight, not a population fraction. N parameters are not additive daily abundances. Be precise about what the model parameterisation actually identifies vs what we'd like it to mean. When the best-fitting model's mechanism doesn't match the biology (e.g., Model H's "regular cycling" for a waypoint population where returns are rare and irregular), say so explicitly — the model fits the curve shape, not the process.
5. **Survival formula inconsistency** — continuous-time models use exp(-δt), not (1-δ)^t. Small numerical difference but mathematically wrong.
6. **Documentation ahead of code** — paper claims analyses the scripts don't reproduce (n_starts=5 vs 50). Verify scripts produce documented values before submission.
7. **Language too strong for the evidence** — "demonstrate", "genuine dichotomy", "permanently depart", "not demographically structured" are overclaims. Use "consistent with", "supports", "no detectable differences", "not detected again within the study window".
8. **Apparent survival ≠ true survival** — conflates mortality and permanent emigration. Cannot support claims about local vs regional threats without additional evidence.
9. **Structural bias in temporal composition** — counting unique individuals per year by class enriches later years for residents (they appear in multiple years). First-sighting-year analysis needed for unbiased temporal trends.
10. **Encounter-level tests on individual-level questions** — chi-squared on encounters inflates sample size for frequently-sighted individuals. Use individual-level metrics or stratified tests.
11. **Point estimates without uncertainty** — all key parameters need CIs or profile intervals. Readers can't evaluate claims without them.
12. **Missing figures** — posterior probability distribution, sighting frequency histogram, study area map. If the text repeatedly references a pattern, show it.

### Structure patterns
- Introduction: species context → site context → prior LIR work at this site → gap (heterogeneity assumption) → what this paper does
- Methods: data → standard LIR → extensions (split-period, bootstrap CIs, transience test, mixture, HMM, validation) → software
- **Results: run Test 3.SR before model fitting** as standard practice. When significant → justifies mixture models. When non-significant with low power (sparse data) → justifies single-population models. When non-significant with adequate power → suggests genuine homogeneity. Either outcome informs model selection. Report the test regardless of result.
- **Results: always start with a data description** — cleaned dataset summary (N encounters, N individuals, date range, key exclusions), then sighting frequency, then population structure (singleton %, resighting spans, transient/returning classification). This grounds the reader in the dataset before any model output. The descriptive results also set up why certain models are expected to perform well or poorly (e.g., high singleton rate → transient-dominated → Model D likely poor).
- Results continued: empirical LIR → standard models → extensions → classification → validation → temporal
- **Results: standard sensitivity steps** — (1) Bootstrap CIs (1000 replicates, individual resampling) for all key parameters — especially for parameters that appear poorly constrained. Report percentile CIs alongside MLEs. (2) Split-period effort sensitivity (50/50 median-encounter split) to test parameter stability across effort regimes. Stable parameters are robust findings; shifting parameters need cautious interpretation. Flag pathological estimates (e.g., H's 0.2% annual survival in short-window data) as model-data mismatch. These two diagnostics are complementary: bootstrap quantifies uncertainty within the full dataset; split-period reveals what each effort regime can identify.
- Discussion: heterogeneity interpretation → decline implications → methodological considerations → conservation

### Method-specific clarifications to anticipate

When a paper uses a method that differs from a closely related method applied to the same dataset (e.g., LIR vs CMR on the same photo-ID data), explicitly state why the analytical choices differ. Reviewers who know the companion paper will ask. Example: LIR uses only sighting-days (days with ≥1 identification) because it conditions on identified individuals — zero-sighting days are mathematically invisible. CMR explicitly models detection probability, so zero-sighting survey days are informative. If the companion paper used zero-sighting days, explain in Methods why this paper doesn't, rather than leaving the reviewer to wonder.

### Figure conventions (Simon's preferences)

These override Claude's defaults when generating plots for scientific papers:

1. **Y-axis headroom** — axis maximum should be visibly higher than the tallest data point/bar. Don't let data touch the top of the plot area. E.g., if max bar = 433, set ylim to 500.
2. **Uniform bar colour** — use one colour for all bars unless colour explicitly encodes a variable (e.g., classification, sex, site). Don't use colour to highlight a single bar (like singletons) — that's editorialising in the figure.
3. **All labels present** — title, axis labels, and annotations must render in the PDF. Test with the actual `pdf()` device, not just the R plot window. Common failure: margins too tight for `barplot()` built-in labels → use `title()` separately with adequate `mar`.
4. **Axis labels on the correct axes** — the independent/grouping variable goes on the x-axis, the count/measure goes on the y-axis. "Number of individuals" is a count → y-axis. "Number of sighting days" is the grouping → x-axis.

### Pipeline steps

1. **Descriptive phase** — clean data, build presence matrix, run descriptive analyses
2. **Independent model review** — after descriptive phase completes, run a Codex (or equivalent) independent review before model fitting. The V2 Moz analysis Codex review caught: wrong counts in docs (48→59), non-reproducible scripts, SE formula inconsistency, V1 comparison values wrong, stale terminology. These are errors that accumulate silently and are hard to catch in-session. Making this a standard step rather than ad-hoc is cheap insurance.
3. **Model fitting** — fit all models, run QAIC + CLIC, generate comparison tables
4. **Red-team** — full methodology review before proceeding to classification/validation
5. **Classification + validation** — HMM, ecological tests, temporal composition
6. **Manuscript drafting** — from completed analysis note

### Quality checks before delivery

**Completeness:**
- Every metric in Results has a Methods definition
- Every citation in text is in References (and vice versa)
- Every key parameter has uncertainty (CI or SE)
- Full model-selection table (all models, K, loglik, QAIC, ΔQAIC)
- Figures exist for every pattern described repeatedly in text

**Accuracy:**
- Code parameters match what the paper claims (run scripts, compare output)
- Survival/derived quantities use correct continuous vs discrete formulas
- Model parameters interpreted correctly for the parameterisation used (weights vs fractions, N vs abundance)
- Statistical tests report test statistics, df, effect sizes — not just p-values

**Calibration (language vs evidence):**
- Scan for overclaimed language: "demonstrate", "prove", "genuine", "clearly", "permanently", "not X" (when you mean "no detectable X")
- Apparent survival acknowledged as conflating mortality + permanent emigration
- Validation tests labelled as independent vs derived
- Non-stationarity explicitly addressed
- Right-censoring effects noted where relevant
- Mixture model acknowledged as an approximation, not proof of biological dichotomy
- Temporal trends checked for structural bias (e.g. repeat-sighting enrichment)

**Reproducibility:**
- Scripts reproduce all documented values from a cold start
- Data files, intermediate outputs, and analysis objects tracked in repo
- README has full replication steps with expected outputs

### Red-team integration
- The three-model red-team identified issues that should be preemptively addressed in the Discussion
- Common reviewer objections can be anticipated and defused in the text
- CLIC, time-varying detection, and M2 sensitivity should be mentioned as future work if not implemented

## Workflow
1. Read analysis note + reference papers + code
2. Confirm scope/audience with Simon
3. Write Methods first (what was actually done — anchored to code)
4. Write Results (from analysis note tables/numbers)
5. Write Introduction (contextualise with reference papers)
6. Write Discussion (interpret results, address limitations)
7. Write Abstract last (summarise everything)
8. Check: every Result has a Method, every Method has a Result, all citations present
9. Run /red-team on the draft (optional — catches errors before Simon edits)
