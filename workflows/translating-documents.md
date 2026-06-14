# Translating a long document

Turn a long document in another language into a faithful, readable English version you can quote and act on — not a rough gist, but a translation careful enough to trust on the details that matter.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics (languages, tools, where the file lives) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Ask an AI to "translate this 100-page document" in one go and it will hand you something that reads beautifully and is quietly wrong in three predictable ways. **It drops things** — whole sentences or sections vanish, and because what remains is fluent, you never notice. **Its terms drift** — the same source word becomes "enforcement" on page 4 and "surveillance" on page 40, so a reader can't tell whether one thing is meant or two. And **it mistranslates the bits that matter most** — a legal clause, a number, a date, a species name — with the same confident tone as the rest.

The fix is to stop treating translation as one big act and treat it as a disciplined process with a verification layer. Three moves do most of the work. **Translate section by section**, never in a single pass — chunking is what kills silent omission, because a missing section is obvious when you're checking one at a time. **Lock a glossary before you start** — fix one agreed English rendering for every recurring term, every acronym (keep institutional acronyms as-is and gloss them once), every proper noun, and never translate things that shouldn't be (Latin species names, legal instrument titles). Feed that glossary to every translator and every checker so nothing drifts. And **cross-check with a second and third independent model** — not re-translating, just reviewing the translation against the source for omissions, wrong numbers, and mistranslations.

## How it runs

**Prep.** Start from clean text, not a raw scan — if it's a PDF, extract it first (see [PDF to markdown](./pdf-to-markdown.md)) so you're translating words, not image noise. Map the document's sections, then build the locked glossary up front. This single step is the biggest lever on consistency.

**Translate.** Work through the document section by section, preserving every heading, table, list, number and date exactly, keeping the glossary terms fixed. A long document can be split across several translator passes running in parallel — that's fine, *because* the shared glossary keeps them consistent. Anything genuinely ambiguous gets flagged in place rather than silently guessed.

**Cross-check.** Hand the source and the draft translation to two different AI models and ask each to flag mistranslations, omissions, wrong numbers, and inconsistent terms — a review, not a rewrite. Give the high-stakes passages (anything legal, any table of figures) a line-by-line check. When the two reviewers disagree, the source document is the arbiter — go back and read it. This is the same instinct as [surfacing conflicts](./surfacing-conflicts.md): two independent perspectives catch what one confident pass misses.

**A caution about tables.** Dense tables are where automated extraction fails worst — rows duplicate, columns scramble. Before trusting any table, check it against the most faithful extraction you have of the original, and rebuild it from there if needed. On one real run, the single most important table in the document (which species were legally protected) was garbled by the converter; only re-reading the original settled it. And the cross-check earned its keep elsewhere too: the first translator and one reviewer both proposed a *wrong* common name for a species, and only opening the source resolved it.

## What this does *not* do

It does not produce a legally authoritative text. A careful AI translation is a working reference — excellent for understanding, briefing colleagues, and deciding what matters — but for anything binding, the original-language document remains the authority, and the translation should say so plainly. It also doesn't remove the need for a human who knows the subject: the process catches dropped sections and drifting terms, but judging whether a subtle rendering is *right* in context is still yours. The verification layer raises your confidence; it doesn't hand you certainty.

## Why this works

Each move attacks one specific failure. Section-by-section kills omission. The locked glossary kills drift. The independent cross-check, plus treating the source as the final word, catches the confident-but-wrong mistranslations that a single pass — however good — produces and cannot see in itself.
