# AI-Assisted Scientific Writing — Process Guide

> **Adapting this for your work.** Examples are drawn from Simon Pierce's marine biology / shark conservation manuscripts and grants. The *process* — Deep Research → outline → iterative drafting → literature audit → citation verification → pre-submission review — is field-agnostic and works for any scientific manuscript. Substitute your own field, target journals, and reference paths for the MMF-specific examples. The bundled `/verify-citations`, `/research`, `/red-team`, and `/science-paper` skills implement the most repeatable steps; the rest of this guide describes the human side of the workflow.

---

## How to Use This Guide

You don't need to read this entire guide before getting started. Instead, let Claude walk you through the process step by step.

### Quick Start

1. **Copy this prompt** into a new Claude conversation (Claude Desktop):

```
I'm a scientist starting to write a scientific paper using AI assistance. Please read this guide and then walk me through the process step by step:

https://publish.obsidian.md/simonjpierce/AI-Assisted+Scientific+Writing+%E2%80%93+Process+Guide

Start by asking me about my paper topic, type (review, primary research, grant application, report), target journal, and what stage I'm at (just starting, have some notes, have a draft, etc.). Then guide me through the appropriate next steps based on the workflow in the guide. Explain each step clearly before we do it, and check in with me regularly to make sure I understand what we're doing and why.
```

2. **Answer Claude's questions** about your topic and current progress
3. **Follow along** as Claude guides you through each stage of the workflow

### What to Expect

Claude will:
- Ask about your paper topic, type, target journal, and current materials
- Help you decide whether to start with Deep Research or another approach
- Guide you through initial compilation, iterative refinement, and verification
- Explain each step in plain language before you do it
- Remind you of key pitfalls (especially citation verification)
- Adapt the workflow to your specific situation

### Why This Approach Works

This guide is comprehensive – it covers many scenarios and edge cases. But you don't need to absorb all of it upfront. By having Claude read the guide and walk you through it interactively, you get:

- **Just-in-time learning**: Each concept explained when it's relevant to your current step
- **Personalized guidance**: The workflow adapted to your topic, materials, and experience level
- **Active coaching**: Someone to ask questions to as you go

The rest of this document provides the detailed reference material that Claude will draw on to guide you.

---

## Introduction

This guide documents a workflow for using AI assistants (Claude, ChatGPT, etc.) to draft and refine scientific papers — review articles, primary research manuscripts, grant applications, and technical reports. It synthesises lessons learned from multiple writing projects, including an elasmobranch photo-identification review manuscript for *Reviews in Fish Biology and Fisheries*.

The approach described here is not about having AI "write your paper for you" — rather, it's about leveraging AI as an intelligent research assistant that can accelerate literature synthesis, identify gaps, suggest structure, and refine prose while you maintain scientific direction and quality control. The core workflow (skeleton → bullet outline → author review → multi-platform research sweep → prose → citation audit) applies to any substantial scientific writing project, with emphasis varying by document type.

---

## Core Principles

### 1. You Are the Expert; AI Is the Assistant

The human researcher provides:
- Domain expertise and scientific judgment
- Knowledge of what claims can be made with confidence
- Understanding of the field's conventions and controversies
- Final verification of all citations and factual claims
- The narrative arc and key messages

The AI provides:
- Rapid synthesis and organization of information
- Consistent prose generation at scale
- Identification of structural gaps or redundancies
- Literature search and summarization support
- Tireless revision across multiple iterations

### 2. Keep Prompting Before Diving In

Think of Claude as a smart research assistant for manuscript construction and iteration. **Keep prompting improvements before diving into the text yourself.** It's far more efficient to ask Claude to restructure a section, add missing content, or adjust scope than to make those changes manually. Your role is to direct the process, catch errors, and refine the final product – not to do the heavy lifting of prose generation.

### 3. Iterative Refinement Over Single-Shot Generation

The best results come from multiple passes:
1. **Structural planning** – outline and scope
2. **Section drafting** – rough content generation
3. **Content review** – verification and gap-filling
4. **Integration** – ensuring coherent flow
5. **Polish** – style, citations, and formatting

Each pass involves human review and redirection. Expect to course-correct frequently.

### 4. Multi-Platform Research Sweep

Once the bullet outline is stable, dispatch parallel research queries to multiple AI platforms to maximise literature coverage and catch gaps. Each platform has different training data, search capabilities, and reasoning strengths — cross-referencing their outputs provides broader coverage than any single tool.

**The workflow:**
1. **Create platform-specific prompts** from Claude Code at the Phase 1 scoping checkpoint (the last interactive moment before autonomous work begins). Two prompts, tailored to each platform's strengths:
   - **Claude Desktop** (Research mode): Exhaustive paper discovery, quantitative extraction, obscure/regional references, identification of published challenges or rebuttals. List 5–10 specific papers or authors to search for.
   - **ChatGPT Deep Research**: Epistemic verification — distinguish hard evidence from inference, flag contested claims, extract granular quantitative detail from papers the pipeline finds. Ask what a typical pipeline might miss.
2. **Deliver prompts efficiently** — copy the first prompt to clipboard via `pbcopy`, print a one-liner for the second. The author can launch both external searches immediately while Claude Code runs autonomously.
3. **Run both in parallel** while continuing prose drafting in Claude Code.
4. **Collect results** — drop output files into the project folder or paste key findings back into Claude Code.
5. **Run structured comparison** — launch an Opus subagent for each external output that compares it against the draft, producing: (a) new data points not in the draft, (b) factual contradictions, (c) epistemic improvements, (d) studies to verify. This structured comparison (proven in the `/research` skill Phase 5b) is far more reliable than ad-hoc reading.
6. **Verify new citations** — any references introduced by external models must be verified via WebSearch before integration. Subagent citation hallucination is a known risk (3 fabricated author attributions in one session). Check: paper exists, author names correct, journal/year match, claimed finding actually appears in the paper.
7. **Integrate** — apply confirmed findings to the draft with author approval.

**What each source catches (from empirical comparison on whale shark book chapters):**

| Source | Catches | Misses |
|--------|---------|--------|
| **Claude Code pipeline** | Style-matched drafts, good breadth from parallel subagents, vault integration | Misses quantitative detail from cited papers, foundational older references, obscure journals |
| **Claude Desktop Research** | Obscure/historical references, exhaustive quantitative extraction, contradiction identification | Writes in review style, less epistemic discipline |
| **ChatGPT Deep Research** | Granular numbers from papers already cited, epistemic synthesis across findings, careful inference-bounding | Can hallucinate citations |
| **Reference document comparison** | Citation errors, domain-expert framing, contextual benchmarks (e.g. "is this value typical?"), methodological caveats | Limited to what the reference covers |

All four are complementary. For high-stakes writing (book chapters, major reviews, grant applications), use all four. For routine work, the pipeline alone is usually sufficient with one external pass if time allows.

**Prompt templates** should be saved in the project folder for reuse. These can be re-run periodically as the manuscript develops to catch newly published papers.

### Voice Reference

Before drafting, create or locate a voice reference document for the lead author. AI-generated prose has characteristic tells (elevated vocabulary, conclusion-first framing, dramatic em-dashes, "delve into", "tapestry", "underscore") that domain experts notice immediately. A voice reference extracted from the author's published work prevents these patterns from entering the draft.

**Creating a voice reference:**
1. Identify 3–5 published pieces by the lead author in a similar register (e.g., other chapters in the same book, papers in similar journals)
2. Dispatch a subagent to read all pieces and analyse: sentence structure and rhythm, tone and register, argumentation style, citation integration patterns, distinctive words/phrases, and patterns to avoid
3. The output should include specific quoted examples and a "What NOT to do" section listing AI-tell words absent from the author's prose
4. Save alongside the manuscript (e.g., `Voice Reference — [Author].md`)

**Using a voice reference:**
- Provide it to any subagent or external model writing prose for the project
- After drafting, run a voice comparison: dispatch a subagent with both the draft and the voice reference to identify passages that don't match
- Apply voice edits before content review — it's easier to fix voice in a structurally sound draft than to fix structure in a voice-matched draft

**Example:** For the whale shark book 2nd edition, a voice reference was extracted from 5 published chapters (reproduction, population ecology, threats, conservation, outstanding questions) and used to voice-edit two new chapter drafts. The voice review identified 45 specific edits across the two chapters, including AI-tell words ("illuminating" → "hugely informative", "underscores" → "illustrates"), conclusion-first framing that should be evidence-first, and a cynical closing that should have been cautiously optimistic.

### 5. Author-in-the-Loop Iterative Review

The most effective workflow for scientific writing is not "AI drafts, human polishes" but an ongoing dialogue where the author provides domain corrections, structural feedback, and factual updates as the document develops. Concretely:

- **Skeleton → bullet outline → prose**: Start with headings, then add one bullet per paragraph summarising the key point and citations. The author reviews and corrects the outline *before* prose is written — catching structural issues early is far cheaper than rewriting finished paragraphs.
- **Author voice notes and corrections**: The author dictates corrections, additions, and reframings as they review the outline. AI captures these as structured notes (in an author feedback file) and applies them to the manuscript. This preserves the author's voice and domain expertise while AI handles the mechanical integration.
- **Parallel research agents**: When the author flags a gap or a claim to verify (e.g., "check whether porbeagle sharks have been photo-IDed"), AI dispatches background research agents and integrates findings without blocking the main review flow.
- **Differentiate catalogue-quality vs match-quality**: Not all content needs the same rigour at every stage. Bullet outlines need to be directionally correct; final prose needs verified citations. Match the verification effort to the stage.

This iterative loop — where the author steers and corrects while AI executes and researches — produces better results than either working alone, and avoids the common failure mode of AI-generated text that sounds authoritative but contains subtle domain errors.

### 6. Scientific Writing Principles

These principles guide how AI should interact with the author on scientific manuscripts:

- **Treat the author as an expert peer**, not a student. AI should challenge claims when warranted, not explain basics.
- **Additive edits by default.** Targeted expansions and local refinements tied to new evidence, not wholesale regeneration. Full rewrites require explicit instruction.
- **Preserve the author's voice.** Avoid generic "review paper tone" unless asked. The author's writing style, interpretive framing, and prior conclusions should be respected and built upon.
- **Surface uncertainty, don't smooth it away.** When evidence is mixed or sources disagree, flag the disagreement rather than forcing consensus. Use `TODO/VERIFY` for unresolved questions.
- **Citation discipline.** Every factual claim needs a citation. Flag unsupported claims with `[CITATION NEEDED]`. Never fabricate references — if uncertain, say so.
- **Unpublished data conventions for reviews.** Reviews should cite published evidence. For non-author contributions, use "pers. comm." (requires permission). For author contributions, use "pers. obs." (personal observation) or "unpubl. data" (unpublished data). Never "pers. comm." your own co-authors.
- **Evergreen notes are living documents.** Scientific synthesis notes may evolve over years. Changes should be additive and traceable. Prior interpretations preserved unless explicitly revised.

### 7. Trust But Verify

AI assistants can fabricate citations, misattribute findings, or make confident-sounding claims without adequate support. **Every factual claim and citation must be verified against primary sources.** This is non-negotiable for scientific writing.

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 0: DEEP RESEARCH (Initial Compilation)                   │
│  - Use ChatGPT Deep Research or similar for broad literature    │
│  - Generate comprehensive initial notes with citations          │
│  - Export to markdown in your knowledge management system       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: PREPARATION                                           │
│  - Gather existing materials (prior reviews, notes, references) │
│  - Define scope, target journal, word limits                    │
│  - Identify key themes and knowledge gaps                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: PLANNING (Plan Mode)                                  │
│  - AI explores codebase/documents to understand context         │
│  - Collaborative outline development                            │
│  - Skeleton → bullet outline → author review loop               │
│  - Identify structural decisions requiring input                │
│  - Exit plan mode with approved approach                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2b: MULTI-PLATFORM RESEARCH SWEEP                        │
│  - Dispatch parallel queries to Claude Desktop + Codex/ChatGPT  │
│  - Cross-reference results against outline                      │
│  - Integrate new papers and gap analysis via author review gate  │
│  - Continue prose drafting in Claude Code in parallel            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: DRAFTING                                              │
│  - Section-by-section generation                                │
│  - Regular human review checkpoints                             │
│  - Citation tracking and verification                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 4: REFINEMENT                                            │
│  - Content expansion or reduction to target length              │
│  - Gap-filling with web search for recent literature            │
│  - Integration of human expertise and corrections               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 4b: CRITICAL REVIEW (/red-team + citation audit)         │
│  - Claude subagent structured review (per section or full MS)   │
│  - Codex independent review (callable from Claude Code)         │
│  - Reference document comparison: if an authoritative review    │
│    exists on the same topic, compare draft against it for       │
│    gaps, citation errors, and framing improvements              │
│  - Citation quality audit: parallel agents assess every paper   │
│    by journal quality, methodology, citations, author flags     │
│  - Citation verification: WebSearch all externally-sourced refs │
│    to catch hallucinated author names (known systematic risk)   │
│  - Primary source verification: check org emails, GitHub,       │
│    platform docs for authoritative figures (not just papers)    │
│  - Claim verification: fact-check key statistics via web search │
│  - Voice comparison: check draft against voice reference        │
│  - Triage and apply improvements with author approval           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 5: FINALIZATION                                          │
│  - Reference list verification                                  │
│  - Journal formatting compliance                                │
│  - Final human review and sign-off                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 0: Deep Research (Initial Compilation)

The starting point depends on what exists. Two common entry points:

**Entry A — Prior publications as canonical text.** If the author has published previous versions of the work (e.g., earlier reviews in a series, book chapters, or related papers), these serve as the primary source material. The author's own published text provides voice, structure, and validated content that AI builds upon — not a blank-page generation problem. This was the approach used for the Photo-ID V3 review, which built on Pierce et al. (2018).

**Entry B — Deep Research compilation.** When starting from scratch or surveying a new field, a comprehensive literature compilation using AI tools designed for research synthesis creates the raw material that subsequent phases will refine.

### Why Start with Deep Research?

Review papers require broad literature coverage – often hundreds of papers across multiple subtopics. Manually compiling this is time-consuming. AI research tools excel at:
- Rapidly surveying literature across a defined topic
- Identifying key papers and authors
- Synthesizing themes across many sources
- Generating structured notes with citations

This initial compilation provides a foundation – imperfect but comprehensive – that you then refine with domain expertise.

### Tools for Deep Research

**`/research` skill** (recommended when vault has existing material on the topic):
- Deep vault scan with wikilink graph expansion — builds on what you already know
- Three-model parallel web research (Claude + Codex + Gemini)
- Structured claim registries with source attribution and confidence scoring
- Claim verification against primary sources
- Produces a formal report with TL;DR, confidence map, and follow-up questions
- Best for: topics where the vault already has substantial material (e.g., updating a review in a domain you've published in)

**ChatGPT Deep Research**, **Claude with Extended Thinking**, or similar tools (Perplexity, Elicit, Consensus):
- Designed for multi-source research synthesis
- Can search academic databases and synthesize findings
- Generates structured output with citations
- Handles broad, exploratory queries well
- Extended thinking modes allow deeper reasoning on complex synthesis tasks
- Best for: topics where the vault has little or no prior material, or when you want maximum breadth on a new field

The specific tool matters less than the approach: use a capable AI with web search/research capabilities to generate comprehensive initial notes, then refine iteratively. For established research domains where your vault has years of accumulated notes, `/research` will outperform external tools because it integrates that prior knowledge.

**When to use which:**
- `/research`: Literature compilation in your domain, where vault context adds value. Produces a standalone report.
- Deep Research/Extended Thinking: Surveying a new field, finding papers you don't know about, maximum breadth
- Standard chat/Claude Code: Refining specific sections, editing prose, structural reorganization, working with files on your system

### Example Deep Research Prompt

```
I'm writing a comprehensive review on photographic identification (photo-ID)
of sharks and rays for a peer-reviewed journal. This is intended as an update
to previous reviews (Marshall & Pierce 2012; Pierce et al. 2018).

Please conduct a thorough literature review covering:

1. Historical development of photo-ID methods for elasmobranchs
2. Current species coverage and applications
3. Methodological challenges and limitations
4. Recent advances in AI/machine learning for photo-ID
5. Lessons from marine mammal photo-ID that apply to sharks/rays
6. Future directions and emerging opportunities

For each section:
- Identify key papers and findings
- Note methodological approaches
- Highlight gaps in current knowledge
- Include relevant citations

Focus on peer-reviewed literature, with emphasis on work since 2018.
```

### Processing Deep Research Output

The output from Deep Research will typically be:
- Comprehensive but rough
- Well-cited but citations need verification
- Structured but may not match your desired organization
- Detailed in some areas, thin in others

**Next steps:**
1. Copy the output to a markdown file in your knowledge management system (e.g., Obsidian)
2. Review for obvious gaps or misunderstandings
3. Note which citations you can verify vs. need to check
4. Identify sections that need expansion or reduction
5. Flag areas where your expertise contradicts the AI's synthesis

### Example: Photo-ID Review Process

For the elasmobranch photo-ID review, the process was:

1. **Deep Research task** (ChatGPT): "Compile comprehensive notes on photo-identification of sharks and rays, covering methodology, species applications, AI advances, and future directions"

2. **Export to Obsidian**: Copied the ~15,000-word output to a markdown file in the working vault

3. **Initial review**: Identified duplicate sections, structural issues, and areas needing expert input

4. **Structured planning** (Claude Code): Brainstormed structure, target journal, author list, and case studies. Wrote a design spec with section-by-section word budgets, key references per section, and an update workflow for incremental paper integration.

5. **Skeleton → bullet outline → author review**: Created headings and subheadings (Phase 1), then added one bullet per paragraph with key points and citations (Phase 2). Author reviewed the bullet outline verbally, providing domain corrections (e.g., correcting which features are used for white shark ID, adding recapture probability as a constraint, noting that standardisation requirements are evolving with AI). Corrections captured in an author notes file and applied to the outline before any prose was written.

6. **Parallel research agents**: During the review, dispatched background agents to verify specific claims (video framerate for photo-ID, porbeagle shark photo-ID literature, bilateral matching methods). Results integrated into the outline and research notes without blocking the main review flow.

7. **Iterative refinement** (Claude Code): Multiple rounds of:
   - Author feedback on structure and content
   - Research agent dispatch for verification
   - Outline updates incorporating corrections
   - Cross-referencing against source documents (2018 chapter, meeting transcripts, book chapters)

8. **Verification**: Cross-check all citations against primary sources (ongoing — intensifies as prose is drafted)

### Advantages of This Two-Tool Approach

**Deep Research strengths:**
- Broad literature coverage
- Good at finding papers you don't know about
- Generates substantial initial content quickly
- Handles exploratory "survey the field" tasks well

**Claude/chat assistant strengths:**
- Precise editing and revision
- Following specific formatting requirements
- Iterative refinement based on feedback
- Working with documents in your local file system
- Maintaining context across long editing sessions

Using both tools leverages their respective strengths: Deep Research for initial compilation, Claude Desktop or Claude Code for iterative refinement and precision editing.

---

## Claude Interfaces: Choosing the Right Tool

Claude is available through multiple interfaces. As of early 2026, the capabilities have converged substantially – most interfaces now support file editing, web search, and extended thinking. The choice depends more on workflow preferences than fundamental capability differences.

### Interface Comparison

| Feature | Claude.ai (Web) | Claude Desktop App | Claude Code (Terminal) |
|---------|----------------|-------------------|----------------------|
| Web search | Yes | Yes | Yes |
| File uploads | Yes (paste/upload) | Yes | Yes |
| Read/edit local files | No | Yes | Yes |
| Projects for context | Yes | Yes | Working directory context |
| Extended thinking | Yes | Yes | Yes |
| Plan mode | No | No | Yes (structured approval) |
| Command execution | No | Limited | Yes (word counts, git, etc.) |
| Best for | Quick tasks, mobile | General use, file editing | Complex projects, automation |

### Desktop and Code: Both Support File Editing

Both **Claude Desktop** and **Claude Code** can now read and edit local files directly. This means the copy-paste workflow is no longer required for either:

1. Claude reads your manuscript file directly
2. Claude makes edits in place
3. You review changes in your editor (Obsidian, VS Code, etc.)
4. Changes persist across sessions

### When to Choose Claude Code

Claude Code offers additional capabilities that may matter for complex projects:

**Plan mode** – For substantial structural changes, plan mode lets Claude analyze the document and propose a revision strategy before making changes. You approve the plan before execution begins.

**Full command execution** – Claude Code can run shell commands (word counts, git operations, file searches across directories), which is useful for managing larger projects or integrating with version control.

**Terminal integration** – If you work primarily in a terminal environment, Claude Code fits naturally into that workflow.

### When Claude Desktop is Sufficient

For most scientific writing workflows, Claude Desktop's file editing capabilities are sufficient:
- Reading and editing markdown files in your Obsidian vault or local directories
- Making iterative revisions to manuscripts
- Maintaining context across editing sessions

The simpler interface may be preferable if you don't need command-line tools or plan mode.

### Pricing Considerations

Claude Code may require a **Premium plan** subscription (~$100/month as of early 2026). Features are rapidly trickling down from Code to Desktop (often within days to weeks of initial release), so it's worth checking what Claude Desktop can accomplish before defaulting to Code. For occasional scientific writing projects, Desktop may be entirely sufficient; Claude Code becomes more valuable for frequent, intensive editing workflows or projects requiring command-line integration.

### Example Prompts (Desktop or Code)

These prompts work in either Claude Desktop or Claude Code when working with local files:

```
"Please change the citation format in Section 3 from APA to Springer style"
```

```
"Read the manuscript and remind me where we left off"
```

```
"Reduce this section from 2,500 words to 1,500 while preserving key citations"
```

### Recommended Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  INITIAL COMPILATION                                            │
│  Tool: Any Claude interface with web search, or Deep Research   │
│  Task: Generate comprehensive initial notes with citations      │
│  Output: Save to markdown file in your knowledge system         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ITERATIVE REFINEMENT                                           │
│  Tool: Claude Desktop or Claude Code (direct file access)       │
│  Tasks:                                                         │
│  - Structural reorganization                                    │
│  - Section-by-section editing                                   │
│  - Citation format conversion                                   │
│  - Word count management                                        │
│  - Gap-filling with web search                                  │
│  - Scope adjustments based on your expertise                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  VERIFICATION                                                    │
│  Tool: You + reference manager + Google Scholar                 │
│  Task: Verify all citations against primary sources             │
└─────────────────────────────────────────────────────────────────┘
```

### When to Use Claude.ai (Web)

Use the web interface when:
- You're brainstorming before you have a document
- Quick questions that don't require file edits
- Mobile access
- You don't have local file access set up

### Caveats

**Citation verification remains essential.** Deep Research tools can hallucinate citations just like standard chat assistants. Every citation must be verified before submission.

**Domain expertise is irreplaceable.** The AI may miss recent developments, misunderstand field-specific nuances, or include content outside your intended scope. Your expertise guides what to keep, revise, or remove.

**The output is a starting point, not a final product.** Expect to substantially revise the Deep Research output through multiple iterations.

---

## Phase 1: Preparation

### What to Gather Before Starting

**Essential materials:**
- Previous reviews or papers in the series (if applicable)
- Key references you want to cite
- Notes on topics to cover
- Target journal guidelines (word limits, structure, citation format)
- Any existing draft material

**Context to provide to the AI:**
- Your role and expertise ("I'm a marine biologist specializing in...")
- The paper's purpose ("This is the third review in a series...")
- Target audience ("For researchers and managers...")
- Key constraints ("12,000 word limit", "Springer citation format")
- What makes this review timely ("AI advances since 2018...")

### Example Opening Prompt

```
I'm writing a review paper on [TOPIC] for [JOURNAL]. This builds on
previous reviews by [AUTHORS, YEARS] and focuses on advances since
[DATE].

Key themes I want to cover:
1. [Theme 1]
2. [Theme 2]
3. [Theme 3]

I have attached/provided:
- My previous review from [YEAR]
- Notes on [TOPIC]
- Key references I want to include

Target: ~[X] words, [CITATION FORMAT] format.

Please review these materials and help me develop an outline for
the new review.
```

---

## Phase 2: Planning Mode

### When to Use Plan Mode

Use plan mode when:
- The task involves multiple sections or complex structure
- You need the AI to explore existing documents before proposing changes
- There are architectural decisions that require your input
- You want to see the full approach before committing to execution

### Effective Planning Prompts

**For initial exploration:**
```
Enter plan mode. Please review my existing draft and:
1. Identify the current structure and any duplicate/redundant sections
2. Assess completeness relative to recent literature
3. Identify gaps that need filling
4. Propose a revision plan for my approval
```

**For structural decisions:**
```
I need to decide on the level of technical detail for the AI section.
Options:
A) Deep technical coverage (CNN architectures, loss functions, etc.)
B) Moderate technical coverage (key methods, practical implications)
C) High-level overview (what AI enables, without technical detail)

Please assess what's appropriate for [JOURNAL] and recommend an approach.
```

### The Plan Document

A good plan document includes:
- **Current state assessment** – what exists, what's working, what's not
- **Proposed changes** – specific, actionable items
- **Decision points** – questions requiring human input
- **Execution order** – which tasks depend on others
- **Verification criteria** – how to confirm success

---

### Recommended Project Files

Maintain these files alongside the manuscript for structured collaboration:

| File | Purpose |
|------|---------|
| `MANUSCRIPT — [Title].md` | The working manuscript |
| `SPEC — [Project] Design.md` | Design spec (structure, authors, decisions, workflow) |
| `RESEARCH NOTES — [Project] Literature.md` | Compiled findings from all research agents and audits |
| `AUTHOR NOTES — [Author] feedback.md` | Running log of author corrections, domain knowledge, and voice-dictated feedback. Structured by date and topic. Captures corrections that should persist across sessions. |
| `CITATION QUALITY AUDIT — Summary.md` | Quality ratings (HIGH/MEDIUM/LOW) for every cited paper, with per-paper notes |
| `PROMPT — Claude Desktop Research Query.md` | Reusable research prompt for Claude Desktop |
| `PROMPT — Codex Research Query.md` | Reusable research prompt for Codex/ChatGPT |
| `PAPERS/` | Drop new papers here for the incremental update workflow |
| `PROPOSED UPDATES/` | Where update proposals land for author review |

Not all files are needed for every project — scale to complexity. A short methods paper may need only the manuscript and author notes; a major review benefits from all of them.

---

## Phase 3: Drafting

### Section-by-Section Approach

Don't ask for the entire paper at once. Work section by section:

```
Let's draft Section 3: Current State and Applications.

This section should cover:
- Species coverage expansion since 2012
- Applications across research domains (population estimation,
  movement ecology, reproductive biology, conservation)
- Integration with video survey methods (BRUV + photo-ID)
- Citizen science contributions

Key references to incorporate: [LIST]

Aim for ~1,500 words. Use Springer citation format (Author Year)
without commas.
```

### Handling Citations

**Critical rule:** AI assistants frequently hallucinate citations. Establish clear protocols:

```
When adding citations:
1. Only cite papers I've provided or that you can verify exist
2. If you're uncertain about a citation, flag it with [NEEDS VERIFICATION]
3. Don't fabricate author names, years, or findings
4. If a claim needs a citation but you don't have one, note [CITATION NEEDED]
```

**During review:**
```
Please list all citations used in this section so I can verify them
against my reference database.
```

### Prompts for Different Content Types

**For synthesis/overview sections:**
```
Synthesize the current state of [TOPIC], drawing on the references
I've provided. Focus on themes and patterns rather than exhaustive
species-by-species coverage.
```

**For methodological sections:**
```
Explain [METHOD] at a level appropriate for researchers who may
implement it. Include practical considerations, not just theory.
```

**For critical analysis:**
```
Assess the limitations of [APPROACH]. What are the genuine challenges,
and what solutions are emerging? Avoid both uncritical enthusiasm and
unfounded skepticism.
```

**For future directions:**
```
Based on the gaps identified in earlier sections, what are the most
promising research directions? Prioritize feasibility and conservation
relevance.
```

---

## Phase 4: Refinement

### Managing Word Count

**For reduction:**
```
This section is currently ~2,500 words and needs to be ~1,500.
Condense while preserving:
- Key methodological points
- All citations
- The main argument structure

Remove:
- Redundant examples
- Excessive background that's covered elsewhere
- Tangential content
```

**For expansion:**
```
This section is thin at ~800 words. Expand to ~1,200 by:
- Adding more detail on [SPECIFIC TOPIC]
- Including discussion of [ASPECT NOT YET COVERED]
- Strengthening the link to [RELATED SECTION]
```

### Gap-Filling with Literature Search

```
Search for recent papers (2023-2026) on [SPECIFIC TOPIC]. I want to
ensure this section reflects current advances, not just literature
I already know.

Focus on:
- Novel methods being applied
- Gaps in current shark/ray research that other fields have addressed
- Emerging opportunities

Provide citations I can verify.
```

### Handling Corrections

When you identify errors:
```
This claim is incorrect: [QUOTE]. The actual situation is [CORRECTION].
Please revise this paragraph and check whether the error propagates
elsewhere in the document.
```

When claims need support:
```
The statement "[QUOTE]" needs peer-reviewed support. Either:
1. Add an appropriate citation if you can verify one exists
2. Reframe as a hypothesis/possibility rather than established fact
3. Remove if unsupportable
```

---

## Phase 5: Finalization

### Reference Verification

```
Please generate a complete list of all in-text citations used in
the manuscript, in alphabetical order. I will cross-check against
the reference list.
```

```
The reference list includes [AUTHOR YEAR] but I cannot find this
citation in the text. Either:
1. Show me where it's cited
2. Remove from reference list if unused
```

### Format Compliance

```
Check this manuscript against [JOURNAL] requirements:
- Abstract word limit: [X]
- Keywords: [X required]
- Section structure: [REQUIREMENTS]
- Citation format: [FORMAT]
- Reference format: [FORMAT]

Flag any compliance issues.
```

### Final Polish

Run `/polish` on the manuscript file. This runs LanguageTool (grammar/spelling, `--language en-GB` by default; use `en-US` for US-targeted journals), Vale (style via write-good + proselint), and an AI writing detection pass. The skill triages findings into Fix / Consider / Skip and presents them for approval before applying.

For scientific writing, `/polish` is configured to be more tolerant of passive voice, technical jargon, and formal phrasing — but it will still catch genuine errors, inconsistent terminology, and AI writing patterns that could undermine credibility.

Also review the complete manuscript for:
- Consistent terminology (photo-ID vs photographic identification)
- Smooth transitions between sections
- Appropriate scholarly tone throughout
- Any remaining redundancy between sections

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Uncited Claims

**Problem:** AI generates confident-sounding statements without citation support.

**Solution:**
- Explicitly instruct AI to flag unsupported claims
- Review each section specifically for citation coverage
- Ask: "Which statements in this section need citations but don't have them?"

### Pitfall 2: Fabricated References

**Problem:** AI invents plausible-sounding but non-existent papers. A subtler variant: the AI finds a real finding but attributes it to fabricated authors. In one session, 3 of ~110 references had correct findings but wrong author names ("Park & Lee 2025" and "Vo et al. 2025" for a paper actually by Ahn et al. 2025; "Lutz et al. 2020" for Dziergwa et al. 2019). The findings were verifiable — the attributions were not.

**Solution:**
- Verify every citation against Google Scholar, Web of Science, or your reference manager
- Be especially suspicious of recent papers (2023+) — AI training data may not include them
- When AI suggests a reference, ask for the DOI or URL to verify
- For any references introduced by external model comparisons, run a dedicated verification subagent (WebSearch each citation to confirm author names, journal, and year)
- **Pattern to watch for:** correct finding + wrong author name. The finding verification passes but the attribution is fabricated. Always verify author names independently of findings.

### Pitfall 3: Scope Creep

**Problem:** Content expands beyond the review's defined scope.

**Solution:**
- Define scope clearly at the outset
- When AI adds new content, ask: "Is this within scope for our review?"
- Maintain a "parking lot" for interesting but out-of-scope ideas

### Pitfall 4: Generic AI Prose

**Problem:** Writing sounds generic or lacks the author's voice. Common AI tells include elevated vocabulary ("delve", "tapestry", "underscore", "illuminate"), conclusion-first framing, dramatic em-dashes, anthropomorphism, and sloganistic triplets.

**Solution:**
- Create a voice reference from the author's published work (see "Voice Reference" section above) — this is the single most effective defence
- Run a voice comparison subagent after drafting to catch specific deviations
- Run `/polish` with its AI writing detection pass to flag remaining tells
- Ask for revision: "This sounds too generic. Make it more direct and specific."
- **Key principle:** fix voice before content. It's easier to edit content in a voice-matched draft than to fix voice in a content-complete draft.

### Pitfall 5: Over-Reliance on AI Knowledge

**Problem:** AI's knowledge has a cutoff date and may miss recent developments.

**Solution:**
- Use web search for topics requiring current information
- Provide AI with recent papers you want incorporated
- Don't assume AI knows the latest developments in fast-moving fields

---

## Prompting Patterns That Work

### The "Expert Colleague" Frame

```
You are an expert in [FIELD] helping me draft a review for [JOURNAL].
I'm the lead author with final responsibility for content accuracy.
Please [TASK].
```

### The "Specific Constraint" Pattern

```
Write [SECTION] with these constraints:
- Length: ~[X] words
- Must include: [REQUIRED ELEMENTS]
- Must cite: [KEY REFERENCES]
- Avoid: [WHAT TO EXCLUDE]
- Tone: [DESCRIPTION]
```

### The "Iterative Refinement" Pattern

```
Here's my feedback on the draft:
1. [SPECIFIC ISSUE 1] – please [FIX]
2. [SPECIFIC ISSUE 2] – please [FIX]
3. [POSITIVE FEEDBACK] – keep this approach

Revise and show me the updated version.
```

### The "Verification Request" Pattern

```
Before I accept this section:
1. List all citations used
2. Flag any claims that need stronger support
3. Identify any content that might be out of scope
4. Confirm word count
```

---

## Session Management for Long Documents

### Context Preservation

Large documents may exceed AI context windows. Strategies:

1. **Work in focused sessions** – one section or task per session
2. **Provide summaries** – "We've completed Sections 1-4, now working on Section 5"
3. **Use the document as source of truth** – keep the manuscript file updated; AI can re-read it
4. **Document decisions** – maintain a plan file with key decisions recorded

### Multi-Session Projects

```
This is a continuation of our review paper project. Previously we:
- Completed Sections 1-4
- Decided to use moderate technical detail for the AI section
- Target word count is ~12,000

Today's focus: Section 6 (Marine Mammal Lessons)

Please read the current manuscript state at [PATH] before we proceed.
```

---

## Cross-Platform Review: Getting a Second Opinion

Once you're fairly happy with the manuscript, run it through multiple review lenses:

**Option 1: `/red-team` skill.** The `/red-team` skill provides a structured critical review via a Claude subagent, followed by an independent Codex review (now callable directly from within Claude Code). This is the most efficient option — it handles the multi-platform review automatically, including subagent quality checks and a triage workflow for applying suggestions. Use this for section-by-section review during drafting, or for a full-manuscript pass before submission.

**Option 2: Manual cross-platform review.** For additional perspectives beyond `/red-team`, or when you want a different framing, consider asking another AI system to act as an expert reviewer. Different AI platforms have distinct training data, reasoning approaches, and stylistic tendencies — using multiple systems means you benefit from genuinely different perspectives rather than reinforcing a single model's blind spots.

### Why This Works

Each major AI platform has been trained differently:
- **Claude** (Anthropic) – tends toward careful, nuanced analysis with attention to structure and logical flow
- **ChatGPT** (OpenAI) – often provides direct, actionable feedback with broad general knowledge
- **Gemini** (Google) – may offer different perspectives, particularly on technical or data-heavy content

By developing your manuscript primarily with one system (e.g., Claude) and then asking another (e.g., ChatGPT) to review it critically, you get:
- Fresh perspective unconstrained by the original drafting conversation
- Different interpretation of ambiguous passages
- Alternative suggestions for structure or emphasis
- Identification of issues the first system may have introduced or overlooked

### Example Review Prompt

When your manuscript is near-final, paste it into a different AI platform with a prompt like:

```
You are an expert peer reviewer in [your field]. Please provide a constructive, critical review of this manuscript as if reviewing for a high-quality journal.

Focus on:
- Logical flow and argument structure
- Gaps in coverage or reasoning
- Clarity and accessibility for the target audience
- Specific suggestions for improvement (not just identification of problems)

Be direct and specific. I want genuine critique, not reassurance.

[Paste manuscript here]
```

### Practical Tips

- **Do this late in the process** – after you've done substantial refinement, not on early drafts
- **Be specific about the review focus** – if you have particular concerns (e.g., "Is Section 4 too technical?"), ask about them directly
- **Treat suggestions as input, not instructions** – you still decide what to accept
- **Citation verification still required** – if the reviewing AI suggests adding references, verify them independently

This cross-platform review step adds minimal time but can catch issues that would otherwise persist through to submission.

---

## Quality Checklist

Before considering the manuscript complete:

**Content:**
- [ ] All sections address their stated scope
- [ ] Key themes are adequately covered
- [ ] Gaps in the literature are identified
- [ ] Future directions are specific and actionable
- [ ] Conclusion synthesizes key points

**Citations:**
- [ ] Every factual claim has appropriate citation support
- [ ] All citations verified against primary sources
- [ ] Reference list matches in-text citations exactly
- [ ] Citation format matches journal requirements

**Structure:**
- [ ] Logical flow between sections
- [ ] No significant redundancy
- [ ] Appropriate depth for each topic
- [ ] Word count within target range

**Style:**
- [ ] Consistent terminology throughout
- [ ] Appropriate scholarly tone
- [ ] Clear, direct prose
- [ ] Author's voice preserved

**Compliance:**
- [ ] Meets journal formatting requirements
- [ ] Abstract within word limit
- [ ] Required sections present
- [ ] Figures/tables properly formatted (if applicable)

---

## Example: Effective Correction

**Problematic AI output:**
> "Sevengill sharks have been successfully identified using photo-ID methods in New Zealand waters (Dunkley et al. 2024)."

**Human correction:**
```
This citation appears to be fabricated – I cannot verify Dunkley et al. 2024
for sevengill sharks. There IS valid sevengill work from New Zealand by
Rayment and colleagues, but I need to verify the exact citation.

For now, remove this sentence. I'll add it back with the correct citation
once I've verified the reference.
```

**Lesson:** Don't try to "fix" uncertain citations by having AI guess – remove and replace with verified sources.

---

## Conclusion

AI-assisted scientific writing is a collaboration, not automation. The most successful outcomes result from:

1. **Strategic tool selection** – use Deep Research for broad literature synthesis, chat assistants for iterative refinement
2. **Clear human direction** – you set the scientific agenda and maintain quality control
3. **Structured workflow** – planning, drafting, refinement, verification in defined phases
4. **Rigorous verification** – especially for citations and factual claims
5. **Iterative refinement** – multiple passes with human review and course-correction
6. **Appropriate scope** – AI accelerates but doesn't replace expertise

The two-tool approach – Deep Research for initial compilation, followed by iterative refinement with a chat assistant like Claude – leverages the strengths of each:

- **Deep Research** excels at broad literature coverage, finding papers you don't know about, and generating comprehensive initial drafts
- **Chat assistants** excel at precise editing, following specific formatting requirements, and iterative refinement based on your expert feedback

Used well, this combination can dramatically accelerate the synthesis and writing process while maintaining scientific standards. A review that might take months of literature compilation and drafting can be substantially accelerated, with the time savings redirected to the verification and expert refinement that only you can provide.

The key is maintaining your role as the expert director of the process, using AI to handle the labour-intensive aspects of literature compilation, drafting, and revision while you ensure accuracy, coherence, and scientific integrity.

---

## Citation Quality Audit

Before submission, audit every cited paper for quality. Peer-reviewed publication is the initial bar, not the final one — work quality varies, and citing dubious methodology in an authoritative review implicitly endorses it.

### Process

1. **Compile the full citation list** from the manuscript (use a subagent to extract all unique citations).
2. **Dispatch parallel assessment agents** — split citations into batches by section. Each agent checks: journal quality/impact, methodology soundness, citation count, independent validation, and any red flags (retractions, published critiques, predatory journals).
3. **Rate each paper**: HIGH (solid, safe to cite), MEDIUM (acceptable with caveats), LOW (questionable, cite with caution or omit).
4. **Flag author concerns**: If the lead author has domain knowledge about specific researchers whose work is dubious, flag those for detailed examination. Expert judgment about research quality is a valid and important input.
5. **Detailed examination of LOW papers**: For any paper rated LOW, do a deep dive — check for published critiques, assess whether the conclusions are supported by the data, check whether the software/methods have been independently validated.
6. **Fact-check key claims**: Select the 3–5 most consequential verifiable claims in the manuscript and check them against primary sources via web search.
7. **Save the audit**: `CITATION QUALITY AUDIT — Summary.md` with per-paper ratings, plus detailed audit files by section.

### Primary Source Verification

When writing about a platform, tool, or organisation, don't rely solely on published papers or public documentation — both can be outdated. Check:

- **Organisation emails and newsletters** (e.g., Wild Me's donotreply@wildme.org emails for Wildbook/Sharkbook updates)
- **GitHub repositories** for actual configuration and recent commits
- **Community forums** for the most current operational status
- **HuggingFace model cards** for AI model specifications and performance metrics

These primary sources often contain more current and authoritative figures than the published literature, which may lag by 1–2 years.

---

## Incremental Paper Integration ("PR for Papers")

Review manuscripts accumulate new relevant literature between work sessions. Rather than doing a big catch-up each time, this workflow enables incremental updates with author review gates — like pull requests for a manuscript.

### How It Works (Designed for Photo-ID V3 Review, March 2026)

1. **Input:** Author drops a PDF, notes file, or reference into a `PAPERS/` subfolder alongside the manuscript
2. **Invoke:** A command (e.g., `/manuscript-update`, planned as a Claude Code skill) triggers processing
3. **Analysis:** Claude reads the paper, cross-references against the current manuscript sections
4. **Proposal:** A structured update proposal is saved to `PROPOSED UPDATES/` containing:
   - Which section(s) the paper is relevant to
   - Specific text additions or modifications (with before/after)
   - Rationale for each change
   - New references to add
5. **Review:** Author approves, modifies, or rejects each proposed change
6. **Apply:** Approved changes applied surgically to the manuscript

### When to Use This vs Direct Editing

- **PR model**: When the manuscript text is reasonably stable and unsupervised edits could disrupt coherence. The review gate prevents drift.
- **Direct editing**: During active drafting sessions where the author is present and reviewing in real time.

### Related Workflows

- `Literature Intake & Integration Workflow.md` — the general process for ingesting a new paper into the vault
- `Resolving Conflicts & TODOs in Synthesis Notes.md` — for handling uncertainty and conflicting evidence

### Status

Design spec complete (`02_MARINE MEGAFAUNA/MANUSCRIPTS/Shark Photo-ID V3/SPEC — V3 Review Design.md`). Skill implementation planned once the V3 manuscript reaches stable draft stage.

---

*Document created: January 2026. Updated March 2026 with voice reference workflow, three-source verification model, reference document comparison, and citation hallucination patterns from whale shark book chapter writing.*
*Based on: Collaborative development of "Photo-Identification of Sharks and Rays" review + whale shark book chapters 14 and 15.*
*Workflow: ChatGPT Deep Research → Obsidian → Claude (Desktop or Code) iterative refinement*
