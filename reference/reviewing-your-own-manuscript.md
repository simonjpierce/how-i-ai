# Reference — Reviewing your own manuscript

> **What this is.** The actual method behind [the *Reviewing your own manuscript* workflow](../workflows/reviewing-your-own-manuscript.md), cleaned of the maintainer's personal specifics (real paths, names, journals, species). It's a **starting point to adapt, not a drop-in command** — your field, your tools, and how your analyses are stored are all shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Throughout, "a second model" means an independent AI reachable on the command line, run **read-only** — the maintainer uses OpenAI's Codex CLI. "Your analysis files" means the code and data outputs behind the paper; "your notebook" means whatever running record holds the analysis decisions. The replication half of this is its own reference — [the replication audit](../workflows/the-replication-audit.md) — and is summarised here only where the two interlock.

## Freeze the inputs first

Pin one version as the reviewed state: the manuscript text, the analysis code, the data outputs, and the notebook behind them. Save that starting version. In the editing sequence, each reviewer reads the version produced after the previous reviewer's accepted fixes; in a comments-only review, everyone reads the same unchanged draft. Either way you know exactly what each fix applies to. Convert the manuscript to plain markdown if it isn't already, so each model can read the whole thing.

## The passes (several lenses, deliberately independent)

The value is independence, so each pass runs without seeing the others' findings — don't leak one model's review into another's prompt.

- **Your main model, full effort.** Reads the whole draft bringing what it knows of the field and prior literature: statistical validity, claims-vs-evidence, structure and internal consistency, empty sections and placeholder figures, numeric mismatches.
- **Two more models, each with the same brief.** The maintainer's default panel is three reviewers — Claude Opus, Claude Fable and Codex's Astra, all at high effort — given one identical brief that includes an open-ended "fresh eyes" question. On your own paper they run one after another, with the agreed fixes folded in between, so each reads the improved text and can catch a regression an earlier fix introduced. Different model families can spot different weaknesses; agreement between reviewers helps you prioritise, but every finding is still checked against the manuscript, data or source. Don't assume fixed strengths: in the maintainer's own comparison one model was best at forensic number-checking, another at checking facts against outside sources, a third at overall coverage. Test yours; the ranking shifts between releases.
- **A named-expert lens, written into the shared brief.** (It began as a separate pass; putting it in the brief gives every reviewer the lens.) Each reviewer reads the methods *as a specific, methods-relevant authority would* — from first principles, hostile to unstated assumptions, skeptical of any claim the data don't force. Naming the *right* kind of expert (matched to the dominant method — capture-recapture, movement models, occupancy, mixed models, whatever your paper leans on) pulls the model closer to real reviewer standards than a generic "senior reviewer". **The persona is an internal rigour-eliciting device, never an attribution** — you never claim a named living person reviewed the paper; if you describe the pass, it's "reviewed against [subfield] best practice".
- **A scientific-rigour layer — the highest-value passes.** This asks the harder question the surface review skips: *is this the right analysis, and should the conclusion be believed.* Make each its own step, because AI reviewers lead with surface fixes unless pointed straight at inferential validity:
  - **Design validity** — pseudoreplication (repeat measurements of the same individual treated as independent), wrong error structure, multiplicity (how many covariates/models were screened vs reported), autocorrelation, effort-confounding, model-specific goodness-of-fit.
  - **Claims vs evidence** — causal verbs on correlational data; "no effect" that's really just low power; extrapolation beyond the sampled range; a *label* that over-claims (calling rarely-returning animals "resident").
  - **Numeric self-consistency** — recompute statistics from reported test-statistic and df; reconcile every count, percentage and total across abstract, methods, results, tables and figures.

## The must-fix throttle (why it exists)

Several hostile models across many passes will hand you 60 comments. A draft buried under 60 nitpicks is worse than no review — the real problems drown in style notes, and you can't tell which is which. So gate before you surface anything:

- **Tag every finding by severity:** *must-fix* (blocks submission — a wrong statistic, an unsupported causal claim, an arithmetic error, an integrity issue) / *should-fix* (strengthens) / *optional* (style and taste).
- **A finding only reaches must-fix with ≥2-of-3 model agreement, or one model's explicit high confidence.** A single model's lone stylistic gripe is demoted to optional, not surfaced as urgent.
- **Surface the must-fixes first, one at a time** — highest-leverage issue, the recommended fix, then the next — rather than dumping the full pile. The throttle is what turns a wall of comments into a short list of things that actually matter.

## Re-verify every number and citation yourself

A number going into a submitted paper must not rest on a model's say-so — this is the cheapest high-value check there is. Take each count, total, and "X in the table doesn't match Y in the text" the review surfaced and confirm it against the actual outputs: re-sum the column, re-read the source line. Two traps to expect: a model that flags "X doesn't reconstruct from Y and Z" is often *wrong* because estimator internals don't match its assumed formula — check against the committed output file, not the reviewer's reconstruction; and a *displayed-rounding* mismatch is a precision note, not an arithmetic error. Run citation verification over the reference list too — a fabricated or mangled citation is exactly the kind of thing that survives your own re-reading.

## The replication audit (re-run, don't just re-read)

The passes above read the *prose*. This half checks the *work behind it* — see [the replication audit](../workflows/the-replication-audit.md) for the full method; in brief: is the code and data behind every figure and number actually in a repository someone could re-run, does it actually run (declared dependencies installable, not just listed), does each in-text number trace to a committed script-to-output, and — the high-yield, often-missed one — does what the Methods section *says* the model does match what the code *actually does*? A reviewer's "X is missing from the model" must be checked against the code, never accepted from the text alone. Submission is the moment reproducibility stops being optional: a reviewer may ask, and you want the answer to already be yes.

## Fold the fixes in — but the science stays yours

Because it's *your* paper, the accepted fixes go straight into the draft, not into a note for someone else. But the boundary is firm, and it's the whole point: **the review flags and suggests; you decide.**

- **Mechanical and clearly-correct edits apply directly** — wording, verified arithmetic typos (with the before/after shown) — *but only while the draft still matches the AI's last saved version*, or you've explicitly authorised it. If you've edited the draft since, or no saved baseline exists, it proposes the edits instead of making them.
- **Anything that touches the science flags for your explicit approval** — a number change, a citation swap, a causal-verb or hedge change, a contested interpretation, a framing choice. These never auto-apply, even when the surrounding prose is safe to edit. A number is only ever changed to a *verified* value.
- **Anything needing a re-run, content removal, or a headline reframe is a judgement call** that comes to you. Reject what you disagree with, with a reason. It surfaces and recommends; it doesn't get to overrule you on your own results.

This is not a substitute for your co-authors, supervisors, or the journal's reviewers — it's the pass that fixes the *obvious* objections in private, cheaply, before those people spend their attention on the hard stuff.

## What stays yours

How many models you run and how adversarial you make them; which second (and third) model you call; whether you add a field-conventions pass; how much you let the AI fold directly versus bring to you; the exact must-fix threshold. The transferable spine is just: *you can't review your own paper objectively, so borrow independence — several models attacking it read-only, every number and citation re-checked, the analysis re-run not just re-read — gate hard so only the findings that matter surface, and fold the fixes in yourself before a real reviewer finds them.*
