# Searching your vault

Give the AI a way to find anything in your notes by *meaning*, not just by the exact words you happen to remember — so a vault of thousands of notes stays as findable on day 900 as it was on day 9, and the AI's first move on "what do I know about X?" is to search *your* accumulated knowledge rather than start cold.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics (which search tool, where the index lives) in collaboration with you. (It has to be an agent that can run tools on your machine.)

*What you'll need: a local search tool your AI installs once and points at your notes folder — the maintainer uses [QMD](https://www.npmjs.com/package/@tobilu/qmd), a local markdown search engine. The keyword part works immediately; the search-by-meaning part needs a small embedding model that runs on your own machine to do the indexing (QMD uses Google's [EmbeddingGemma-300M](https://huggingface.co/ggml-org/embeddinggemma-300M-GGUF), a few hundred MB) — a one-time setup your AI can handle, and everything stays local, nothing uploaded.*

## The core idea

A growing vault has a quiet failure mode: the more you put in it, the harder it is to find. You half-remember writing something about donor retention, or a paper's method, or a decision from four months ago — but not *where*, and not the exact words you used. Ordinary keyword search only finds the literal words, so a note that made the same point in different language stays invisible. And the AI, left to itself, doesn't know your notes exist at all — it answers from its general training, not from the body of work you've built.

The fix is a **search layer**: a local index over every note in your vault that the AI can query before it does anything else. Two things make it more than a glorified file-finder. First, it searches by *meaning* — ask about "keeping supporters engaged" and it surfaces the note you filed under "donor retention," because it matches the idea, not the spelling. (The technique is usually called *semantic search*: the indexer reads each note and stores a mathematical fingerprint of what it's *about*, so notes about the same thing land near each other even when the words differ.) Second, it's the AI's **default first step** — a standing instruction that on any "what have I written about…" question, it searches your vault first and works from what it finds, so its recall is *yours* and not generic.

## How it runs

**One index over all your notes, kept current.** Your AI sets up a search tool pointed at your vault and builds an index — a compact, searchable summary of every note. When notes change, a quick re-index brings it up to date (a few seconds for new files; it leaves unchanged notes alone). You can keep separate **collections** — say, your whole vault versus just your mirrored reference library — so a search can be scoped to "only the literature" or "everything."

**Three ways to ask, for three kinds of question.** Keep all three; they catch different things. *By keyword* — fast and literal, for when you know the exact term (a species name, a project code). *By meaning* — for when you remember the idea but not the words; this is the one that finds what keyword search misses. *By describing the ideal answer* — you (or the AI) write a sentence or two of what a good answer would look like, and it finds the notes most like that description; counter-intuitively, searching with a sketch of the answer often beats searching with the question. A good search runs more than one of these and merges the results.

**The AI uses it as a reflex, not a special request.** The payoff only lands if searching the vault is automatic. A standing instruction in your setup tells the AI to reach for this on any recall question — so it pulls the three most relevant notes and grounds its answer in them, instead of answering from memory and quietly missing the work you'd already done.

**It deepens exactly where you work.** The search is only as good as what's indexed — abstracts let you *find* a paper; full text lets you find the sentence buried in its methods. As you pull full text into the vault (see [the reference library](./the-reference-library.md)), those become searchable too, so the layer gets sharper in the corners you actually use.

## What this does *not* do

It isn't a chatbot that answers *from* your notes — it's the retrieval step that hands the AI the right notes to read and reason over. The judgement still happens after the search. It doesn't reach the open web; for that, point the AI at a question with [deep research](./deep-research.md). And it doesn't replace curation or filing — a search layer over a junk drawer just finds junk faster. It surfaces candidates by relevance; you and the AI still decide what's actually useful.

## Why this works

Externalising your knowledge into a vault only pays off if you can get it back out. As the pile grows, your own memory of *where things are* fails long before the notes stop being valuable — so the vault's worth comes to depend entirely on how well it can be searched. Meaning-based retrieval over your own curated notes is what closes that loop: it turns a folder you can no longer hold in your head into a knowledge base the AI can draw on instantly, and the bigger the vault gets, the more this earns its keep. It's also the quiet engine under the showier capabilities — the [reference library](./the-reference-library.md) and [deep research](./deep-research.md) both lean on it to find the right material before they do anything with it.

## Note

This is a pattern, not a fixed tool. The parts that are yours to shape: which search tool you use (the maintainer runs QMD), whether you run the search-by-meaning layer at all or start with plain keyword search and add it later, how you split your notes into collections, and how aggressively you tell the AI to reach for it. The durable idea is: *a vault you can't search by meaning is a vault you'll outgrow — give the AI a retrieval layer over your own knowledge and make using it the default.* Paste this to your AI and build the version that fits how you keep your notes.
