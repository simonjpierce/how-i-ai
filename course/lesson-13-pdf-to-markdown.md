# Lesson 13 — `/pdf-to-markdown`

Get the content of a PDF into your vault without copy-paste hell or losing the structure.

The lesson reads on its own. A short screencast — me converting a journal article and a multi-page report, what each looks like in Obsidian afterwards — will pair with it when recorded.

## What it does

Converts a PDF into clean markdown for Obsidian. Handles the annoying bits that pure text extraction usually fluffs: paragraph joining, table reconstruction, header / footer removal, hyphenation repair (words split across line breaks), footnotes, reference list cleanup, and common OCR artefacts.

The output is a single `.md` file you can drop into your literature folder or paste into a project note.

## When to use it

- A new paper you want to annotate or reference.
- A report a colleague sent that you need to engage with substantively.
- A book chapter you want to highlight.
- Any PDF where the *content* matters more than the original layout.

## Try it

```
/pdf-to-markdown /path/to/paper.pdf
```

Or drag the PDF into the Code tab. The skill checks dependencies and tells you to install `marker_single` (preferred) or falls back to `pdftotext` + `pandoc` if you'd rather not bring in a new tool.

## Quality notes

- **Scanned PDFs** (image-only, no text layer) need OCR first. `marker_single` handles this.
- **Equations** often need manual cleanup. Mathematical content is the highest-friction part of any PDF conversion.
- **Tables** survive simple cases well; complex multi-column tables sometimes need a manual pass.

## What's next

[Lesson 14 — `/verify-citations`](./lesson-14-verify-citations.md). For when AI is helping you draft something with citations — catch fabricated references before submission.
