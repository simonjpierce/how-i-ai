# PDF to markdown

Get the papers, reports, and books that matter to you *out* of PDF and into your notes as clean, readable text the AI can actually work with — not as files sitting in a folder that neither you nor the AI ever opens again.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (which converter, where files land) in collaboration with you. (It has to be an agent that can run command-line tools and write files on your machine — a plain chat assistant can't set this up.)

*What you'll need: a few command-line PDF tools, which your AI can install for you. Most are light; the heavy one is the layout-aware extractor (an ML model with a sizeable download), so let your AI flag whether your machine can run it. The OCR and chapter-splitting tools you only need if you actually hit scanned pages or whole books — skip them until then.*

## The core idea

A PDF is where knowledge goes to be inaccessible. The AI can't read most of them reliably, you can't link to a paragraph inside one, you can't search across a shelf of them, and they connect to nothing else you know. The move here is simple: when a document earns a place in your notes, **convert it to clean markdown** and bring it in, where it becomes readable, linkable, quotable, and part of the same memory as everything else.

"Clean" is the whole game, and it's the part naive conversion gets wrong. Dump a PDF to text and you get a mess: lines wrapped mid-sentence, page numbers and running headers spliced into paragraphs, words hyphenated at line-ends left as two half-words, tables collapsed into rubble, footnote markers scattered through the prose, figure captions floating free of their figures, and — on scanned documents — stray characters from imperfect text recognition. The pattern here is a conversion that *repairs* all of that, so what lands is something you'd actually read and something the AI can reason over without tripping on the artefacts.

The principle the whole thing rests on: **extraction is the easy part; the clean-up is the work.** Pulling the words out is nearly free. Turning them back into a faithful document is where the value is.

## How it runs

You point the agent at a PDF; it pulls the text out, runs a structured clean-up so the output reads properly, and writes the result into your notes alongside everything else.

A good build handles each of these clean-up problems explicitly rather than hoping the extractor got them right:

- **Headers and footers** — the running title, page numbers, and journal furniture that repeat on every page are detected and stripped, not woven into the sentences around them.
- **Paragraph joining** — lines wrapped for the page are rejoined into real paragraphs, while genuine breaks (new paragraphs, headings, list items) are preserved.
- **Hyphenation repair** — words split across a line-end ("mega-\nfauna") are healed back into one word. These are pervasive — often dozens per chapter — so it's worth doing as a deliberate pass.
- **Tables** — reconstructed into proper markdown tables rather than left as scrambled columns. Tables are the single biggest source of conversion errors, so they deserve the most scrutiny.
- **Footnotes and references** — markers tidied, footnote text collected where it belongs, and reference lists cleaned into something consistent.
- **Figure captions** — kept attached to a sensible place rather than stranded mid-paragraph.
- **Text-recognition artefacts** — on scanned documents, the stray characters and mangled words that optical character recognition leaves behind are cleaned up.

**Two extractions, not one.** The most useful trick here is to run *two* extractors and use one to check the other. A layout-aware extractor (tools like *marker* or *nougat*, or a cloud extraction service) does the smart reconstruction of tables, columns, and structure. Alongside it, run a plain, dumb text dump that preserves the raw layout (the `pdftotext` utility from the *poppler* toolkit, in its layout-preserving mode, does this well). The plain dump is ugly but faithful — it becomes the ground truth you check the polished version against, especially for tables, where the smart extractor is most likely to invent or drop a cell.

The division of labour is sharpest on tables, and it isn't "tables are hard, use the smart tool". On **structured** tables — a few columns of prose, like a plan's action matrix — the layout-aware extractor is far better than the plain dump and worth the wait. On **dense reference** tables — long species lists, numeric data grids — it is the *less* trustworthy of the two: it duplicates rows, scrambles columns, and occasionally invents entries that read plausibly. Rebuild those from the plain layout-preserving dump instead. Knowing which kind of table you're looking at before you choose is most of the battle.

**Scanned PDFs need a text layer first.** If a PDF is just images of pages with no underlying text (old papers, photographed book pages), there's nothing to extract until you add a text layer with an OCR step (a tool like *ocrmypdf*). The agent can detect this case and run that step before converting.

**Whole books, chapter by chapter.** A 400-page book is too much to convert in one pass and easy to lose your place in. The cleaner approach is to split it into chapters by page range first (the `qpdf` utility does this), convert and clean each chapter on its own, then verify each — work that can run in parallel if your setup allows, or one chapter at a time if not. Same result either way.

**A quick check before it's done.** Because the plain text dump is faithful, the agent can compare the cleaned markdown back against it to catch anything dropped, duplicated, or mangled — and it flags the hard spots (dense tables, equations, multi-column scans) for your eye rather than pretending they came out perfect. This is a fidelity check, not a fact-check: the concern is that the markdown faithfully matches the source, not whether the source is correct.

**Checking a conversion you already have.** Worth building as its own mode: the markdown exists, and the question is simply *did anything get lost?* Having the AI read the two versions side by side is slow, expensive, and — on a long document — not even reliable. A ladder of cheap mechanical checks, run first, is faster and catches more:

- **Pin the page mapping** between the printed page numbers and the PDF's own page numbers, and verify it at the front *and* the back — unnumbered plates shift it mid-book.
- **Compare word counts**, whole-document first and then per chapter against that chapter's page range. Per-chapter is the highest-value check, because it localises the loss. Expect the markdown to land slightly *below* the raw dump — the clean-up strips running headers and page numbers — so a count coming in *above* the raw dump is a duplication signal.
- **Scan for leftover artefacts**: stray page numbers on their own line, invisible soft hyphens, dangling line-end hyphens, running headers that survived the strip.
- **Diff the figure and table numbers** found on each side. One trap: a caption set in small capitals can extract from the PDF as a single stray character, so a chapter with four tables can audit as having none — which looks exactly like the AI invented them. Confirm by searching for a distinctive value *inside* the table before concluding anything is missing or fabricated.
- **Sample sentences** from the source and search the markdown for a distinctive ten-word window from the *middle* of each — not the whole sentence, which won't survive legitimate hyphen and caption repairs. Expect a handful of apparent misses and chase every one individually; in practice nearly all turn out to be artefacts of the test rather than real loss, and reporting them unchecked destroys trust in the check itself.
- **Check the end of each chapter**, where truncation hides — losing the last few paragraphs barely moves a word count.
- **Do one cell-by-cell check** on the hardest table in the document. If that one is right, spot-checking the easy ones has little yield.

Only where a check flags something is close reading worth it, and then only on the flagged part. Write the verdict to a short dated note that records the page mapping, so the next check starts from it instead of re-deriving it.

## What this does *not* do

It's not flawless on hard layouts — multi-column scans, heavy tables, and equations still want a human glance, and a good build surfaces those rather than burying them. It doesn't read the document *for* you; it makes the document *available* to you and the AI. It doesn't fact-check the contents — its job is faithfulness to the source, not judgement about it. And it's for documents worth keeping: you don't convert everything, just what earns a place in your notes.

## Why this works

The reason a naive copy-paste produces garbage is that a PDF describes where ink goes on a page, not what the text *means* — so the structure you read effortlessly (this is a heading, that's a footnote, these cells form a row) has to be reconstructed, and a single tool guessing alone gets it wrong in ways you won't notice until you quote a broken table back to a colleague. Running a smart extractor against a faithful plain dump turns "trust the conversion" into "check the conversion," cheaply and every time. The clean-up is tedious, repetitive work — exactly the kind a person skips under time pressure and an AI does the same way on the thousandth page as the first. And the checks that catch real loss are counting exercises, not reading exercises, which is why they're worth running before anyone opens the document at all.

## Note

This is a pattern, not a fixed tool. Which extractor you use, how much of the clean-up you automate versus eyeball, whether you ever need OCR or chapter-splitting, what you bother to convert at all — all yours to shape, and all modular: the dual-extraction check is the load-bearing idea, the rest you add as your material demands. Once a document is clean markdown in your notes, the rest of your system can use it — a source for research, a reference for a manuscript, or just a note you link to. The durable idea is: *the documents that matter belong in your notes as clean text, not stranded as PDFs — and the way you trust the conversion is to check the smart version against a faithful dump.* Paste this to your AI and build the version that fits your reading.
