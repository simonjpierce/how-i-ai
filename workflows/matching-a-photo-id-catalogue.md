# Matching a photo-ID catalogue

Check a whole batch of new animal sightings against everything already catalogued (at your site, then the neighbouring region, then the ocean basin) and get back a short, ranked list that a person confirms by eye. The AI finds the candidates and records every decision; it never names an animal on its own.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

*What you'll need: an account on a photo-ID platform that lets you read its data through an API (a programming interface) — the maintainer uses Sharkbook — and some Python on your machine. You also need someone who knows the animals, because every identity decision is theirs.*

## The core idea

Photo-identification recognises individual animals from their natural markings, such as the spot pattern behind a whale shark's gills. Platforms like **Sharkbook** (built on the open-source **Wildbook** software) run an AI matcher called **MiewID** over each uploaded photo. It turns the marked-up part of the photo into a numerical "fingerprint" and scores it against every other fingerprint. On the website you check a sighting's candidates one at a time, usually against a single site. That leaves three gaps. Whole seasons rarely get re-checked at once, and cross-region checks are easy to skip, so a shark that swam from Madagascar to the Seychelles can go unnoticed. And a sighting whose photo was never marked up has no fingerprint, so no matcher has ever compared it with anything.

There's also a trap in the scores. In a catalogue of tens of thousands of photos, the best *wrong* animal already scores about as high as a typical true match, so a simple "anything above 0.5 is a match" rule flags nearly half the animals that aren't in the catalogue at all. What works is looking at the **margin**: how far the top animal is ahead of the next-best *different* animal. A clear winner is a likely match; a close race is a maybe, whatever the raw score.

So the fix has two halves. The AI does the bulk comparison and the bookkeeping: it pulls the fingerprints through the platform's API, runs the comparisons on your own computer, applies a rule tested on thousands of known animals, and writes a report. The person does what only a person can: looks at the photos side by side and decides. **The machine ranks; a person decides every name.**

## How it runs

**Audit what can be matched at all.** Before any matching, the AI counts, for every sighting at the site, whether it has a usable fingerprint. It sorts out the ones that don't and says why: a video with no still frame, a photo with no box drawn round the animal, a box marked with an unusual view angle, or no photos at all. Those sightings are invisible to every matcher, and fixing them often changes the results more than any clever matching does.

**Widen the search one ring at a time.** A batch of sightings is checked against its own site first, then the neighbouring region, then the whole ocean basin. A sighting stops at the first ring where it finds a clear match. That way a shark re-sighted at home isn't compared against the whole world, and a shark that turns up somewhere new still gets a basin-wide look. Photos are grouped by which side of the animal they show and by matcher version, so like is only ever compared with like.

**Apply a tested rule, and say how good it is.** The maintainer's rule for whale sharks: "likely" means the top animal scores at least 0.45 *and* leads the next-best animal by at least 0.10. On 35,000 known sightings, the top animal was the right one 98% of the time when that rule fired. It also fired for about 3 in 100 animals that were genuinely absent from the catalogue. "Possible" is a narrower lead. The flip side matters as much: the rule catches only about half of true re-sightings. So "no match found" is not evidence that an animal is new. That's why naming a new animal is a person's call.

**Put the photos side by side.** For each candidate, the AI builds a simple web page. The new sighting's cropped photo sits on the left, and every photo of the candidate animal, from the same side, sits on the right, with the score and margin shown. The reviewer clicks through and gives a verdict for each: same animal, different, or can't tell.

**The reviewer decides, then acts.** The reviewer makes the name assignment in the platform, not the AI. For whale sharks, a new individual gets a name only if there's a good photo of its left side. Right-side-only sightings stay unnamed until a left-side photo turns up.

**Keep the decisions as the record.** Every verdict goes into a plain decision file, and every count in a summary, email or paper is printed from those files by a small script, never typed from memory. Before anything is shared, a second AI model (the maintainer uses the Codex CLI) reads the summary against the files and flags any number that has drifted.

## What this does *not* do

It doesn't identify animals. It shortlists candidates and records what a trained person decided. It won't turn a "possible" into a match because the story would be good. An 18-year return of an old shark has to pass the same side-by-side look as anything else. It won't report a movement between sites without checking the field records. A photo filed under the wrong site looks exactly like a long-distance movement, and the tell is often that the recorded sighting date equals the upload date. It changes nothing in the shared catalogue on its own: reading and scoring happen on your computer, and every change in the catalogue is a person's decision.

## Why this works

The fingerprints already exist; the platform computes them for every marked-up photo. What was missing was a way to compare a whole season, across the whole basin, at once, plus a rule that states how often it's wrong. Moving the comparison off the website and onto your own computer makes a basin-wide check take minutes instead of days. And because the output is a short list of photos to look at, not a verdict, the expert's time goes where it counts.

## Note

This is a pattern, not a fixed pipeline. Your platform, your species, which side of the animal counts, the thresholds, and how far out you search are all yours to set. Re-test the rule on your own catalogue before trusting it, and again whenever the matcher's version changes. The durable idea is: *let the AI compare everything with everything and keep the books; keep the naming with the person who knows the animals.* Paste this to your AI and build the version that fits how you work.

For the concrete method (the audit, the ring-by-ring search, the rule, the review pages, and the mistakes that caught the maintainer out), see [the reference companion](../reference/matching-a-photo-id-catalogue.md).
