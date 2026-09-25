# Reference — Matching a photo-ID catalogue

> **What this is.** The actual method behind [the *Matching a photo-ID catalogue* workflow](../workflows/matching-a-photo-id-catalogue.md), cleaned of the maintainer's personal specifics. It's a **starting point to adapt, not a drop-in command**: your platform, species and catalogue are shaped differently, so read it *with* your AI and build the version that fits. It was written for a team call on the Seychelles whale shark catalogue (September 2026) and is kept current as the work moves.
>
> Throughout, "the platform" is the shared photo-ID catalogue (the maintainer uses **Sharkbook**, built on **Wildbook**, with the **MiewID** matcher). A "fingerprint" is the list of numbers MiewID computes from the boxed part of a photo. An "encounter" is one sighting record; an "individual" is a named animal that encounters are linked to. "The reviewer" is the person who decides identities.

## The rule that governs everything

The AI reads, compares, builds review pages and keeps records. **Only the reviewer assigns identities**, one item at a time, after looking at the photos. Nothing the AI finds is a match until the reviewer says so.

## 1. Get read access

Sharkbook issues a personal API token (Account → API access) that expires after about eight hours. The AI keeps it in a private file outside any shared folder, never in notes or code, and checks the expiry before starting. When it runs out, the AI asks the reviewer for a fresh one; it doesn't find another way in. The token is read-only, and that's the point: the whole workflow runs without write access.

Two API habits that save grief: searches take full dates (`2025-01-01`, not `2025`; a bare year silently drops records), and one search returns at most 10,000 records, so big regions are pulled in date slices and the AI checks none came back truncated.

## 2. Audit coverage before matching

For every encounter at the site, record: date, linked individual (if any), approval state, number and type of media (image or video), and each box's view angle and whether it has a current-version fingerprint. Then summarise by era. The audit answers the questions a team always asks first:

- **Are the old animals matchable?** Count the named individuals with at least one fingerprinted photo of the side you name them from. List any without one.
- **What can't be matched, and why?** Video-only encounters (the detector skips video; someone must pull a still frame and upload it). Encounters with no box (run detection). Boxes with a blank or unusual view angle such as "downleft" or "up" (re-draw with the right angle; the new box gets a fingerprint automatically). Encounters with no media at all.
- **What's unlinked?** Old encounters that were never attached to an individual are common in catalogues imported from earlier systems. They are a clean-up job in their own right (see section 6).
- **What's the next free name?** The highest number in the site's naming series, so new names continue it.

## 3. Search one ring at a time

A small spec file names the query encounters (a site plus a date range, or a list of IDs) and the rings: **site → region → ocean**. Each ring's gallery includes the rings before it. For each fingerprinted photo:

1. Score it against every gallery photo **of the same side and the same matcher version** (cosine similarity between fingerprints). Leave out photos from the same encounter.
2. **Rank by animal, not by photo:** each animal's score is its single best photo.
3. Take the top animal's score (`s1`) and the next-best *different* animal's (`s2`). The margin is `s1 − s2`.
4. Classify with the rule below. If the sighting is "likely" at this ring, stop; if not, go out to the next ring.

Galleries are cached on disk with a record of when and what was pulled, so a re-run takes seconds and the platform is hit once per location. The first pull of the whole western Indian Ocean took about 40 minutes.

## 4. The decision rule (whale sharks, MiewID `msv4_v3`)

| Class | Rule | What it means |
|---|---|---|
| Likely | `s1 ≥ 0.45` and margin `≥ 0.10` | Top animal right 98% of the time; fires for about 3% of animals absent from the gallery |
| Possible | not likely, and either (`s1 ≥ 0.45` and margin `≥ 0.05`) or `s1 ≥ 0.55` | Worth a visual review (see the note below the table) |
| Too few animals | only one animal in the gallery | No margin exists, so never called a match |
| Nothing | anything else | **Not** evidence of a new animal: the likely rule catches only about half of true re-sightings |

These numbers were measured on about 35,000 sightings of known animals from 27 Indian Ocean sites. The left and right sides agree within a couple of points. Treat them as descriptive, not held-out, because the thresholds were chosen on the same data. The "possible" row has no separate measurement: the roughly 95% precision and 11% absent-animal flag rate were measured for the broader rule `s1 ≥ 0.45` and margin `≥ 0.05` *including* likely matches, so don't read them as the accuracy of the leftover possible cases. Re-test on your own catalogue, and re-test whenever the matcher version changes. The platform shows its own score on a different scale: its on-screen score is `(cosine + 1) / 2`, so 0.75 on screen is 0.50 here.

Two extra flags travel with each result:

- **Possible duplicate:** a score of 0.97 or more (the same photo uploaded twice, often under different dates).
- **Hub count:** how many different query animals a candidate photo scored highly against. A few photos in every catalogue score well against everything.

## 5. Review pages and the reviewer's pass

For each candidate pair, the AI builds a page: the query's cropped photo (the platform's own detection box, so exactly what MiewID saw) on the left, and every same-side crop of the candidate animal on the right, with dates, score and margin. Click a crop for the full photo; the encounter ID opens the record on the platform. The reviewer works through the pages one item at a time and gives a verdict: *same animal*, *different*, *duplicate photo*, *can't tell*.

Naming conventions the maintainer follows for whale sharks:

- A new individual needs a good **left**-side photo. Right-side-only sightings stay unnamed.
- New names continue the site's series. In the Seychelles that's S-465 onwards as of September 2026.
- An encounter is **approved** only once reviewed; "unidentifiable" is also a reviewed, final state.
- The reviewer makes the assignment and approval in the platform after the decision, never before.
- **Note scars in the same pass.** While each animal is on screen, the reviewer also records its scars: *none seen*, with the body regions the photos actually show (usually one flank), or each scar in plain words. The words are kept verbatim and coded into the scar-classification categories later (cause, severity, body region), so the naming pass also feeds a scarring dataset at almost no extra cost. A "none seen" row matters as much as a scar, because it's the denominator.

## 6. Keep the books

Every verdict goes into a plain decision file, one per review pass (JSON rows with the pair, the scores and a free-text decision starting with the verdict word). A small tally script prints the counts, and **every number in a summary, email or paper is pasted from that output**, never typed from memory. Before anything leaves the building, a second model (the maintainer uses the Codex CLI) reads the write-up against the decision files and the reports and flags drift. It once caught "16 of 16" that should have read "15 of 15" after one pair turned out to be a mis-dated duplicate.

## Mistakes that caught the maintainer out

- **A mis-filed photo looks like a movement.** A "Tofo → Mafia" shark was a Mafia photo uploaded under the wrong site. The tell: its sighting date equalled its upload date, and the field logbook showed no trips then. Check the field record before calling any cross-site match a movement.
- **Duplicates arrive with different dates.** The same photo re-entered weeks or a year apart. A near-1.0 score is a better duplicate flag than a same-date check.
- **Blank view angles hide animals.** 31 of one season's boxes had a blank or non-flank side recorded and were invisible to every matcher until fixed.
- **Far-flung "likely" hits are usually noise.** Run 200 queries across two rings and several false flags are expected at a 3% rate. A Seychelles shark "likely" matching one in the Andaman Sea is a review item, not a finding.
- **Head-on crops and collapsed boxes** (a sliver of a box) produce confident-looking false leads. Check the crop before the score.
- **The platform's search index lags edits by ten minutes or more**, so re-run an audit after changes settle, not straight away.

## Worked example: Seychelles, September 2026

Kept current during the work. Counts come from the audit and run reports, not from memory.

- **Catalogue (25 Sep):** 924 encounters, 469 named individuals. 861 of the 875 sightings from before 2020 (or with no date) have a fingerprint; one named animal has none.
- **Since 2020 (49 encounters):** 12 named, and up to 23 unnamed sharks with a good left photo (19 from October 2025, 4 from 2021–22; one of the 2021–22 sharks was uploaded twice). Also 4 right-side only, 7 video only, and 2 with no usable photo. One Madagascar shark seen in 2019 was re-found in the Seychelles in 2025 without being pointed at it, and confirmed by eye. Two October 2025 sightings came up as "possible" returns of sharks last seen in 2007 and 2015; on the side-by-side look both were different animals, a reminder that a good story is not a match.
- **Old, never-linked sightings:** 216 historical encounters had no individual; 205 were matchable. The run flagged 62 as near-identical to photos already in the catalogue, 20 as likely re-sightings of named Seychelles sharks and 11 as possible ones. 8 matched another unlinked sighting, 19 had a likely or possible hit outside the Seychelles (to be treated as review items), and 85 matched nothing.
- **Next:** a naming pass for the 23 candidates with the team, then approval, then the historical clean-up.
