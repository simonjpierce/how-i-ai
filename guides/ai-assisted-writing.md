# AI-Assisted Writing — Reports, Manuscripts & Analysis

> **Adapting this for your work.** Examples are drawn from MMF's conservation reports, marine megafauna manuscripts, and field-data analyses. The principles — interview-style information capture, AI structuring/drafting, human edit-and-refine — apply to any kind of long-form professional writing. The MMF-specific shortcuts (donor reports, board memos, funder narratives) translate naturally to any organisation's equivalent comms. Substitute your own document types and stakeholders for the MMF examples.

Status: active
Owner: shared (MMF team)
Last reviewed: 2026-03-26
Consolidates: AI Workflow for Report Writing, AI Workflow for Scientific Writing and Analysis

> Practical workflows for using AI to write conservation reports, scientific manuscripts, and data analyses. For the detailed scientific writing process (manuscript structure, literature audits, citation quality, multi-platform research sweeps), see [AI-Assisted Scientific Writing – Process Guide](./ai-assisted-scientific-writing.md).

---

## Core Philosophy

The goal is to **bypass the blank page problem**. Rather than staring at an empty document, you:
1. Capture information through conversation (interviews, voice notes)
2. Let AI structure and draft
3. Edit and refine human-generated content

This approach is faster because **people find it easier to edit mostly-right text than to produce a document from scratch**.

Think of AI as **spell check on steroids** — it's your ideas, but AI helps you get them down on paper and structures them better. You take absolute responsibility for what comes out because you have reviewed and refined it.

### For Scientific Analysis

The focus has shifted from **learning to code** to **learning to use AI effectively**. For the analyses we typically do, AI can handle much of the coding. Your job is to:
1. Understand **what** you want to do (the method)
2. Understand **why** it works (the theory, where needed)
3. Direct AI to implement it
4. Verify the output makes sense

**Time investment:** Read papers and methods so you understand what the code is doing. Don't invest time in learning programming syntax — that's what AI is for now.

> "It's an amazing tool for productivity — seriously, why waste your time doing things that would have taken you three weeks when you can do them in half a day. But you have to actually read through it, because it does misinterpret things when it doesn't have the context."

---

## Recommended Tools

| Purpose | Tool | Notes |
|---------|------|-------|
| Voice input & transcription | **ChatGPT Desktop** | Superior transcription; built-in recording function |
| Writing & structuring | **Claude** | Better at long-form writing and maintaining document structure |
| Coding & analysis | **Claude Co-work** (Desktop) or **Claude Code** (Terminal) | Can read/write files directly; runs code autonomously |
| Cross-checking | Both | Use one to review the other's output for quality control |

### Model Selection in Claude

For complex writing tasks (strategic plans, reports, papers):
1. Click on the model name (e.g., "Sonnet 4.6") in Claude
2. For early iterations, **Sonnet** is fine (faster, cheaper)
3. **Switch to Opus** for the final polish — it's slower but better at nuanced writing
4. Enable **extended thinking** (clock icon next to the text input) for deeper reasoning on complex documents

For coding and analysis, use **Opus** in Co-work for complex work — Sonnet is the default but less capable.

### Dual-Tool Workflow

Keep a ChatGPT window next to Claude. Voice dump into ChatGPT, copy the transcript into Claude for writing. This combines ChatGPT's superior voice handling with Claude's stronger writing capabilities.

### Tool Setup
- Use the MMF team plan for Claude (check bottom-left of interface — switch from personal to team plan)
- Download both desktop apps for full functionality
- ChatGPT web vs desktop can have different features

---

## Voice Input Workflow

Voice input is faster than typing for complex prompts:

> "The key thing is that voice input is just tell it your hopes and dreams."

### Using ChatGPT for Transcription
1. Open ChatGPT alongside Claude
2. Click the microphone button in ChatGPT
3. Speak your prompt naturally — include context, goals, constraints
4. Copy the transcribed text into Claude

### When to Use Voice
- Explaining complex context or background
- Describing what you want when you're not sure of exact terminology
- Quick interviews with collaborators to capture their input
- Iterating on results: "That's not quite right, what I actually meant was..."

### Recording Length Limits
- **ChatGPT gets "funky" after ~1 hour** of continuous recording — quality degrades
- For longer interviews/conversations, use your **phone's voice memo app as backup**
- Consider breaking long sessions into 45-minute chunks with natural pause points
- Always have a backup recording running for important conversations

---

## Claude Projects & Context Management

### Using Claude Projects for Complex Documents

For larger pieces of work, use **Claude Projects** to maintain context across sessions.

**This approach works well for:**
- Multi-year strategic plans (regional or programmatic)
- Grant proposals requiring narrative strategy sections
- Conservation blueprints and roadmaps
- Major reports with multiple sections
- Scientific manuscripts with data analysis

### Setting Up a Project
1. Open Claude Desktop and click **Projects** (top left)
2. Click **New Project** (top right)
3. Name it descriptively (e.g., "Americas Strategic Plan")
4. In the "What are you trying to achieve?" box, provide a brief description

### Adding Project Files
Use the files panel (right side) to upload relevant context. More context = better output.

**Essential:**
- Any draft notes you've already written
- Previous strategic plans or reports (as templates for structure)
- Relevant grant applications (shows what's funded/planned)

**Helpful:**
- The MMF global strategic plan (for alignment)
- Conservation blueprint documents
- Species-specific plans or IUCN assessments
- Previous related papers from your group (for style/context)
- Raw data files (Excel, CSV) for analysis projects

**Tip:** Don't be shy about uploading 5–10 documents if they're relevant. Files persist across conversations within the project.

### The Canonical Markdown File

**Problem:** AI loses context in long sessions. When Claude "compacts itself," it's not relying on exactly what you told it — it's relying on what it *remembers* you told it, which are two different things.

**Solution:** Maintain a canonical markdown file as the AI's external memory.

1. Create a master `.md` file (e.g., `manuscript_draft.md` or `project_notes.md`)
2. Tell AI: "The document you are maintaining is the one in [location]. Keep this updated as we work."
3. At the top of the file, maintain a **running to-do list** of outstanding tasks
4. Include all key definitions, decisions, and results

> "The good thing about having it continually referring to a markdown file is that that is its external memory. It's referring to exactly what happened."

**Useful prompts:**
```
Please fully update the manuscript_draft.md file at this stage with everything that's been done so far. We want this document to be in sufficient detail that we can pick up this chat in another session and be able to start from exactly where we are now.
```

```
Before continuing, please read the project file and recap where we are.
```

---

## Workflow 1: Interview-to-Report

For reports requiring input from colleagues (e.g., community work, education activities, field observations).

### Step 1: Interview Your Sources
1. **Schedule a short conversation** with the person who has the information
2. **Record the conversation** using ChatGPT Desktop's recording function
3. **Ask open questions** and let them talk — you're capturing raw information, not structuring it yet

### Step 2: Extract the Transcript
After recording in ChatGPT:
1. Ask for the **full transcript** (it will initially give you a summary — ask specifically for the full transcript)
2. Copy the raw transcript text

### Step 3: Feed into Claude with Context
Provide Claude with:
- The transcript
- A previous report in the same format (if available), as a template
- Any other relevant material (the original grant, field reports, press releases)
- Clear instructions on structure and length
- End with: "Ask any clarifying questions that are potentially useful for improving the initial output."

### Step 4: Interview Yourself (Brain Dump)
For sections where *you* have the information:
1. Open ChatGPT Desktop
2. Start recording and **talk through your plan** — don't worry about structure, just get the ideas out
3. For strategic plans, try to cover: current situation, threats, research needed, conservation actions, 3–5 year vision
4. Transcribe and feed into Claude as above

### Step 5: Voice-Based Iteration
Rather than typing detailed feedback:
1. Read through Claude's draft
2. Open ChatGPT Desktop and start recording
3. **Verbalise your feedback** as you skim — be specific:
   - "This section is too technical for donors"
   - "We need to add more about the boat strike threat"
   - "The conservation actions section is good but needs more on fisheries"
4. Get the transcript from ChatGPT
5. Paste it into Claude: "Here's my feedback on the draft. Please incorporate these changes."

### The 80–90% Rule
- Each iteration typically gets about **10% better**
- Stop using AI at **80–90%** and do the final polish yourself
- Going too many iterations causes diminishing returns — it starts to get worse, not better
- If you're getting something 60% right, aim for 2–3 voice feedback rounds to hit ~80%
- The final 10–20% requires your human judgement and expertise

---

## Workflow 2: Scientific Manuscript Preparation

### When to Trust AI vs. When You Need Theory

| Analysis Type | Theory Required? | AI Reliability | Notes |
|---|---|---|---|
| **Passive acoustic telemetry** | Low | High | Detection patterns: day/night, seasonal, tidal. Specify "passive acoustic telemetry" — AI confuses with soundscape analysis. |
| **Telemetry / Satellite tags** | Low | High | Finding where the animal is going. Relatively straightforward spatial analysis. |
| **Population modelling** | **High** | Moderate | People make mistakes if they just ask AI without understanding the underlying theory. |
| **Manuscript writing** | Moderate | High | Needs specific guidance on scientific conventions and journal requirements. |

**Rule of thumb:** The more complex the statistical assumptions, the more you need to understand the theory before trusting AI output.

### Phase 1: Project Setup
1. **Create a Claude Project** or Co-work session for the manuscript
2. **Upload all source materials:** thesis/dissertation, raw data, previous related papers, relevant literature
3. **Initial assessment:**
```
Please read, access, and understand these files. Give me a breakdown of what each file contains. This is a [student project/draft manuscript] that we need to prepare for publication. Please suggest any additional analysis needed, improvements, or gaps you identify.
```

### Phase 2: Data Cleaning
AI excels at converting messy data into analysis-ready formats:
```
I have an Excel spreadsheet with [X] tabs containing [describe data].
Please create R code to:
1. Import and tidy this data
2. Convert it to a clean CSV format
3. Handle any date formatting issues
4. Flag any inconsistencies or missing data

Annotate the code well so we can rerun it later with updated data.
```

### Phase 3: Analysis and Results
1. **Define your season/time periods clearly**
2. **Request preliminary results with sanity checks:** "For each result, explain how you calculated it so I can verify the approach."
3. **Flag issues for manual review:** "If you encounter ambiguous data entries, create a list of items that need manual verification rather than guessing."

### Phase 4: Writing
**Structure the output explicitly:**
```
The introduction should have five paragraphs:
1. Broader introduction to [topic] and why it's important
2. [Specific context]
3. [Knowledge gap]
4. [Study system]
5. [Objectives]
```

**Use existing papers as templates:**
```
I'm uploading two papers from the same study site and author group.
Please use these as references for writing style, study site description,
standard methods language, and citation formatting.
```

---

## Cross-Checking & Quality Control

### Cross-Validate with Multiple AIs
For important analyses or documents, use two AI models:
1. Generate analysis/code in Claude
2. Give ChatGPT the clean data and a thorough methods description
3. Ask ChatGPT to replicate the analysis independently
4. Compare results

> "If they come up with exactly the same numbers, then I can be pretty confident that's accurate. If they come up with different numbers, then I'll start asking very specific questions — break that down by years, etc. — and I can pinpoint exactly where the errors have come from."

### The Red-Team Approach
For mission-critical content, use the second AI as a **constructive critic** once you've hit diminishing returns:
1. Download the document from Claude
2. Upload to ChatGPT with context and a specific reviewer role:
   > "Act as a critical reviewer and potential donor. I've drafted this strategic plan for [context]. What's missing? What could be clearer? What would make you more likely to fund this work?"

For a more thorough automated review, use `/red-team` in Claude Code — it runs a structured three-model critical review (Claude + Codex + Gemini) and, for documents with associated code, an ecosystem review of related files.

### Managing AI "Emotions" When Cross-Checking
When feeding ChatGPT's suggestions back to Claude, **don't say they came from ChatGPT**. Claude can get "defensive" about competing AI suggestions. Instead, frame as:
- "A colleague who is an expert in X reviewed this and suggested..."
- "An expert reviewer recommended these improvements..."

### Verify Definitions and Assumptions
AI can confidently produce wrong results if its definitions differ from yours. Always check:
```
How exactly are you obtaining this number? Please break down the calculation.
```
```
How are you defining [term]? Please work that up into a clear definition
so we can check we're on the same page.
```

**Example from practice:** An AI calculated "scar accrual rate" by counting every observation of a scar as a new scar — when in reality, the same scar persisting across years shouldn't be counted multiple times. The numbers looked plausible but were completely wrong.

---

## De-AI Your Writing

Before finalising, run `/polish` on the document. This combines three automated passes:
1. **LanguageTool** — grammar, spelling, punctuation (`--language en-GB` by default; use `en-US` for US-audience documents)
2. **Vale** — prose style checks via write-good and proselint
3. **AI writing detection** — scans for vocabulary clusters, structural patterns, and stylistic tells

The skill triages findings into Fix / Consider / Skip categories and asks for approval before applying changes. For scientific writing it's tolerant of passive voice and formal phrasing; for reports and web content it flags these more aggressively.

This replaces the manual prompt approach — `/polish` covers the same AI writing tells (and more) with automated tooling. See Polish Skill — Setup and Usage for setup details on new machines.

Reference: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

---

## Quick Reference: AI Reliability by Task

| Task | Trust Level | Notes |
|------|-------------|-------|
| Data cleaning/formatting | High | AI excels at this |
| Excel → tidy data conversion | High | Common task, well-handled |
| Visualisation | High | Quick iteration on plots |
| Basic statistics | High | t-tests, ANOVA, etc. |
| Spatial analysis | Moderate-High | Check coordinate systems |
| Time series | Moderate | Verify handling of gaps |
| Report drafting | Moderate-High | Voice → structure → iterate |
| Manuscript drafting | Moderate-High | Needs specific guidance on structure |
| Complex models | Moderate | Understand theory first |
| Novel methods | Low | Cross-check thoroughly |

---

## Specific Tips

### For Short Reports (Newsletter-Style)
- Interview approach works well
- One interview can provide most content
- Feed previous report as template for format matching

### For Scientific Notes or Short Papers
Quick papers (e.g., first international movements, new sighting records) can be drafted rapidly:
1. Brain dump into ChatGPT what you want to accomplish
2. Feed it your data/observations
3. Include an example paper from the target journal as a template
4. Prompt: "Get me as close as you can and point out what's missing"
5. Iterate once or twice, then do your final polish

### For Longer Technical Reports
- Break into sections
- Interview different people for different sections
- Build iteratively rather than all at once

### For Strategic Plans and Grant Applications
- Use Claude Projects to maintain context
- Include previous strategic plans as templates for structure
- Be explicit about audience: "This is primarily a donor-facing document" vs. "This is a technical document for collaborators"
- Request specific output formats: "Please provide the output as a .docx file"

### Vibe-Coding Workflow
1. Describe what you want in plain language
2. Let AI generate code
3. Test on full dataset (only sub-sample if code takes 30+ minutes)
4. Iterate: "This isn't quite right — I need X instead"
5. Once working, ask AI to add comments explaining each section
6. Cross-validate with a second AI

### When Stuck
- Paste error messages directly
- Show AI your data structure (`str(data)` in R)
- Ask: "What's the most common reason this fails?"

### For Analysis You've Never Done
1. Find a paper that did similar analysis
2. Feed AI the methods section: "Explain what they did here"
3. Ask: "How would I implement this with my data?"

### Creating Presentations
Claude can generate PowerPoint files:
- Once you have an 80–90% text document, ask Claude to convert it to a presentation
- Give constraints: "If I'm giving this as a presentation, I want it to be a 15-minute presentation"
- Claude will structure the content appropriately for slides
- PowerPoints can be uploaded to Canva if you prefer that interface

---

## Use Cases: Scientific Analysis

### Acoustic Telemetry
**What it is:** Receivers in the water detect tagged animals as they swim past. This is *not* soundscape analysis — we're listening for tag pings, not animal sounds.

**Typical goals:** Analyse detection patterns across time periods, locations, or conditions (day/night, seasonal, tidal).

**Theory level:** Low — primarily descriptive statistics and comparisons.

**Getting started:** Code likely already exists from Mafia project. Upload existing code, and the resulting paper, to Claude: "This is what we did before — walk me through it, then help me adapt it."

> **Terminology matters:** If you just say "acoustic analysis," AI assumes soundscape recording. Always specify "passive acoustic telemetry" or "acoustic receiver data."

### Satellite Tag Analysis
**Typical goals:** Map movement patterns, identify habitat use, analyse behaviour from track data.

**Theory level:** Low to moderate — spatial analysis is relatively intuitive, but some methods have assumptions.

**Getting started:** Kenya marlin satellite tag code exists on Dropbox. Time zone handling and data formatting are common pain points — AI handles these well.

### Population Modelling
**Theory level:** HIGH — you must understand the model assumptions before using AI.

> "Population modelling: people make mistakes if they just ask AI — you need theory."

**AI can write the code, but you need to:**
1. Understand what model is appropriate for your data
2. Know the assumptions and whether your data meets them
3. Interpret output correctly
4. Recognise when results don't make biological sense

**Recommended approach:** Read the methods literature first — understand mark-recapture, POPAN, Jolly-Seber, etc. Use AI to implement models you understand. Sanity-check all outputs against biological knowledge.

### Converting Student Work to Publication
1. Upload everything: thesis, data files, any existing code
2. Initial assessment: Ask AI to identify gaps between current state and publication-ready
3. Prioritise: Focus on methods and results first — writing polish comes last
4. Update data: If possible, add recent years to make the paper current
5. Clean once: Get all data cleaned before deep analysis to avoid redoing work
6. Cross-validate: Use multiple AIs to verify results before finalising

---

## Quick Reference: The Report Workflow

```
1. CAPTURE
   └── Interview colleagues (record in ChatGPT)
   └── Monologue your own sections (record in ChatGPT)
   └── Insist on ChatGPT providing a verbatim transcript
   └── For complex projects: set up a Claude Project with background files

2. STRUCTURE
   └── Feed transcripts to Claude (use Opus + extended thinking for complex docs)
   └── Include previous report as template
   └── Specify format, length, audience
   └── Request output as .docx if needed

3. ITERATE (aim for 80–90%)
   └── Review draft
   └── Voice-record your feedback into ChatGPT
   └── Paste transcript back into Claude
   └── Repeat 2–3 times max (diminishing returns after that)

4. CROSS-CHECK (if critical)
   └── Upload to ChatGPT for constructive criticism
   └── Incorporate useful suggestions, ignore others
   └── Catches errors either AI might miss alone

5. FINALISE
   └── Switch to Opus for final AI polish
   └── Run /polish (grammar + style + AI writing detection)
   └── Human editing pass (the final 10–20%)
   └── Verify any facts/figures AI may have confused
   └── Format for final output
```

---

## Related Notes
- [AI-Assisted Scientific Writing – Process Guide](./ai-assisted-scientific-writing.md) — detailed scientific manuscript workflow (structure, citations, multi-platform research, voice reference)
- AI-Assisted Scientific Review Writing – Best Practices Guide — detailed review paper workflow
- Guide to Effective AI Prompting
- [Research Workflow](./research-workflow.md) — vault + web research for topic briefs (not writing)
- Transcript to Article Pipeline — article pipeline from transcripts
- Polish Skill — Setup and Usage — `/polish` setup and configuration

---

*Consolidated from: AI Workflow for Report Writing + AI Workflow for Scientific Writing and Analysis*
*Sources: Team catch-up discussions on AI workflows (Jan–Feb 2026), Chris Rohner (population ecology), Simon Pierce (workflow development)*
