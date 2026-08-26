# Reference — The reference library (Paperpile → on-device, as actually built)

> **What this is.** The actual method behind [the *Reference library* workflow](../workflows/the-reference-library.md), concretely enough that you can paste this page to your AI and have it walk you through building the same thing. The maintainer's system mirrors **Paperpile**; if you use Zotero or Mendeley the shape is identical and only the export step changes. Nothing here needs programming from you — your AI writes and runs the build step; your job is the three decisions called out in **bold questions** below.

## The architecture in one paragraph

Paperpile keeps your PDFs in Google Drive and can export your whole library's metadata as one JSON file. Sync that Drive folder to your laptop (so the PDFs exist as real local files), export the metadata, and have your AI build **one markdown note per paper** — title, authors, year, journal, abstract, DOI, and the local path to the PDF — into a folder your search tools can reach. Then, per paper (or in one cheap batch), extract the PDF's text into a **sidecar file** next to the note so the full body is searchable too. Result: your AI can search *your* curated literature by meaning, on your own machine, before it ever touches the web — and each piece is a plain file you can open and read yourself.

## Step by step

**1. Get the PDFs onto the laptop.** Paperpile already syncs its PDF folder to Google Drive. Install Google Drive for desktop, and make the Paperpile folder available offline (mirrored, not streaming-only) — you want real files on disk, because the text-extraction step reads them directly. Scale check from the working system: ~8,000 PDFs ≈ 14 GB. (Zotero users: your storage folder is already local; skip this step.)

**2. Export the metadata.** In Paperpile: *Export → JSON*, whole library. One file, and it completes in a single shot even at ~9,000 references (an older warning about export timeouts near 8,000 turned out to be wrong). Save it somewhere your AI can read. Re-export whenever you've added a batch of papers — the build step below is additive, so refreshing is cheap.

**3. Have your AI build the notes.** Give it the JSON export and the Drive folder path and ask for: one markdown note per reference, filename slug `lastname-year-shorttitle`, frontmatter carrying title / authors / year / journal / DOI / any labels or folders you use in Paperpile / `local_pdf:` path, abstract in the body. Three hard-won rules to state up front:

- **Join metadata to PDFs on Paperpile's internal ID (`gdrive_id` in the export), never on filename.** Real libraries are full of `Unknown - Unknown.pdf` and truncated titles; filename matching is the last-resort fallback, not the method.
- **Make the build additive (merge mode).** A re-run processes only new or changed records and never touches existing notes. A "rebuild everything" mode can exist, but it's the exception you invoke deliberately — a refresh must never be able to destroy what's there.
- **Quote the `local_pdf:` value** (paths contain spaces), and expect some references to have *no* PDF — that's normal (see step 6).

**4. Extract full text into sidecars.** The note's abstract is enough to *find* a paper; full text is what lets a search hit the sentence buried in a methods section. A plain-text extractor (`pdftotext` class — your AI can install one) takes seconds per paper and produces a few hundred kilobytes per paper of searchable text — cheap enough that batch-extracting the whole library is realistic. Write each as `<slug>.fulltext.md` next to the note, marked in frontmatter as a sidecar of the canonical note, with the extraction date. Keep the source PDF as the authority for exact quotes and table values. **Decision for you: batch-extract everything now, or extract on demand the first time a paper is read deeply?** (The working system started on-demand and regretted nothing, but with a cheap extractor the batch is defensible — measure yours first.)

**5. Keep the library out of your notes app's index, but inside your search tool's reach.** ~9,000 papers means ~15,000–35,000 files. Dropped inside an Obsidian vault, that many files makes the app grind — the working system originally had the mirror in-vault and had to relocate it. Put the library in a **sibling folder next to the vault**, and point your semantic-search tool at it as its own named collection, searched only when you ask a literature question (so everyday vault searches don't wade through papers). If your search tool is ever down, the fallback that works at this scale: filter by *filename* first (`ls | grep -i ningaloo` — the slug carries the topic), and only content-grep the shortlisted files. A content-first grep over 600 MB times out.

**6. Handle the no-PDF tail without letting it stall anything.** Some references are metadata-only. Two moves: (a) a legal open-access top-up — for each PDF-less DOI, ask Unpaywall (free API) for a downloadable OA copy, OpenAlex as fallback; expect a low hit rate (~5% in a marine-science library — most is paywalled) and tag anything fetched with its OA source. (b) the **wanted list** — when your AI hits a relevant paper mid-task that it can't read, it notes title + DOI on a running list and keeps working; you get the list at the end, pull the worthwhile ones through your own library access, drop them into Paperpile, and the next mirror refresh folds them in. It never pretends to have read a metadata-only paper, and it never interrupts a run to ask for one.

**7. Tell your AI to use it.** One standing instruction in your AI's memory or project instructions: *literature questions search the library collection first, before the web.* This is the point of the whole build — without the instruction, the mirror is furniture.

## Gotchas from the working system

- **Google Drive desktop sync silently fails to materialise some files.** ~15% of the working library's PDFs existed in Drive's cloud but never appeared on disk. A missing local PDF is therefore *not* proof the paper is unavailable — check the cloud copy (Drive API or the web UI) before writing it off. When fetching those by API, match on the paper *title appearing in the Drive filename*, then verify the downloaded text actually contains the note's title or DOI — full-text search also matches papers that merely *cite* yours.
- **Paperpile's "Starred" folder syncs as symlinks, not files** — enumerate it with link-aware tools if you want starred status mirrored, or skip it.
- **Verify citations at the door.** New references get checked against Semantic Scholar / CrossRef / OpenAlex on import — mechanical lookups, never the model's own opinion. Method: [citation verification](./citation-verification.md).
- **Refreshing is a habit, not a project.** The working system watches for new Paperpile JSON exports and merges them in automatically; starting out, "re-export and re-run the build after each batch of saves" by hand is fine. What matters is that the run is additive, so there is never a reason to put it off.

## What stays yours

Which reference manager, where the library folder lives, abstracts-only vs full text, batch vs on-demand extraction, how much of the automation you bother with. The transferable spine: *one plain-file note per paper you chose, full text where you work deeply, searched by meaning before the web, joined on IDs not filenames, refreshed additively, verified at the door.*
