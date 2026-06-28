<!--
WORKFLOW TEMPLATE — the idea-file shape every workflow follows.

Conventions (from the locked exemplars `the-science-workflow.md` + `00-the-philosophy.md`):
- VOICE: openly AI-assisted, not ghostwritten as the maintainer. Clear, warm, plain.
  Audience = smart readers who are NOT necessarily technical — explain or avoid jargon
  (no unexplained "RAG", "MCP", "context window", "fan-out"; gloss any term you keep).
  Never patronising.
- SHAPE: prose, not a tutorial. The WHOLE document is the paste-able artifact —
  there is NO separate fenced "paste this block". A short top note does that job.
- LINKS: GitHub-relative only (./other-workflow.md), and ONLY to files that actually exist
  in the repo. No absolute local paths. A workflow MAY link to its deeper companion in
  ../reference/<same-slug>.md (the sanitised actual method) — add that as a footer link at
  the end of the doc. There are still no ../skills/ targets: even a reference is a
  DESCRIPTION to adapt, not a shipped skill to copy. The workflow itself stays self-contained
  (describe the capability fully enough that the reader's agent can build it from the workflow
  alone); the reference is an optional deeper layer, not a dependency.
- LENGTH: ~45-70 source lines for a single capability — a workflow with a first-class
  trust/verification layer can run longer; the system map longer still. The thing to cut
  is maintainer-specific plumbing (exact flags, paths, account specifics), not substance.
- CONCRETENESS: NAME the actual tools/services the maintainer uses — QMD, Unpaywall, the
  Codex CLI, whisper, pdftotext, etc. — so a reader or new AI gets a real starting point,
  not a guessing game. A capability left as "a local search tool" or "a second model on
  the command line" is too abstract: the tool NAME is substance and stays; only the
  plumbing AROUND it (flags, paths, scripts, account specifics) gets cut. Where it helps,
  give a realistic expectation too (e.g. "~5% of paywalled refs have a free OA copy").
  Two exceptions: (1) genuinely conceptual/philosophy docs (00-the-philosophy, the-trust-
  spine) where the point is the idea, not a tool — don't force names there; (2) when the
  concrete tool already has its own workflow doc, link out to it rather than re-naming
  inline. NOTE: a doc can satisfy the LENGTH "cut plumbing" rule and STILL be too generic
  — this is the separate check that catches that. (Added 2026-06-18 after an audit found
  ~6 docs that said "do X" without naming how the maintainer actually does it.)
- Delete this comment block in real workflows.
-->

# <Capability name — plain, not the slash-command>

<One sentence: what this lets you do and why it matters — the outcome, not the mechanism.>

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

<The failure mode it fixes, then the fix, in plain prose. State the one principle the whole thing rests on. This is the heart of the doc — most of the value is here.>

## The pieces  *(or "How it runs" — use whichever fits)*

<The moving parts, or the day-to-day flow. Use **bold lead-ins** for distinct steps/operations (e.g. **Capture.** … **Verify.** …). Describe the maintainer's actual practice descriptively where it helps ("In practice this runs with…"), never as first-person impersonation.>

## What this does *not* do

<The boundary. What it deliberately leaves to the human's judgement; what it won't do for you. This section is where you head off the "the AI will do X for me" misread — and, for capability workflows, where you make clear it scaffolds the work without replacing the human's expertise.>

## Why this works  *(optional — include when the rationale isn't obvious)*

<One short paragraph on the underlying reason it pays off.>

## Note

This is a pattern, not a fixed implementation. <Name the things that are the reader's to shape — tools, folder layout, how far they take it — and stress they're optional/modular.> The durable idea is: *<the one-line takeaway>.* Paste this to your AI and build the version that fits how you work.
