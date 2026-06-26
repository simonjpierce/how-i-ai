# Automated photo-ID image upload

Turn a folder of edited field photos into properly-formatted records in a shared research database — tagged, de-duplicated, and uploaded in the background — with the AI building the whole pipeline, including the part the platform never gave you an easy door for.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Photo-identification — recognising individual animals from natural markings, like the spot patterns on a shark's flank — runs on shared online catalogues where researchers pool their sightings so a matching engine can recognise the same animal across people and years. The platform the maintainer uses is **Sharkbook**, which runs on the open-source **Wildbook** software. The friction is the same everywhere: you come home with hundreds of photos and the only ways in are death-by-clicking — a web form per animal, or a bulk-upload wizard that ties up your browser for the whole upload.

And it's needless friction, because the information the database wants is *already in your photos*. The capture date sits in the file. Which individual, its sex, life-stage, a distinctive scar — those live in your judgement, and a minute of tagging in your photo editor pins them to the right frame. The job is just to reshape all that into the platform's expected format and move it. So the principle the whole thing rests on: **the human supplies the judgement — which frame, which animal, is she pregnant — and the AI supplies the plumbing.**

## How it runs

- **Tag where you can see the animal.** In the photo editor (the maintainer uses Adobe Lightroom), tick a few keywords on the photos you actually know something about — sex, maturity, which flank you're looking at — and type freehand notes like a distinctive scar into the caption field. Most photos get nothing, and blank is fine. The point is that this judgement happens where the animal is on screen, not in a chat window where you'd be guessing from filenames.

- **Export with the metadata baked in.** A normal export — for spot-pattern matching the animal should fill the frame, sized to the platform's sweet spot — carries those keywords and captions *inside* each image file.

- **The AI reshapes.** It reads each file's embedded data (capture date, GPS if present, keywords, caption — using a tool like exiftool), fills in the facts shared across the batch that you'd otherwise retype (species, site, photographer), and writes the database's import spreadsheet. The fiddly part it absorbs: mapping your natural words to the platform's exact field names and permitted values — so a "pregnant" tag becomes the platform's `adult-pregnant` life-stage, and "right side" becomes its viewpoint code.

- **It refuses to upload the same photo twice.** A running ledger — just a plain spreadsheet — records every photo ever sent, keyed by both filename and a content fingerprint. Re-process a folder months later, or leave a stray duplicate in the export, and it's skipped. Note the unit: it de-duplicates *photos*, not *animals*. The same individual resighted on a later dive is a different file and uploads normally — that resighting is the whole point of the catalogue.

- **It builds the door the platform didn't give you.** This is the part worth lingering on. The official bulk upload was a browser wizard that monopolises the machine while it runs — no good when you want to keep working. Because Wildbook is open source, the agent read its actual code, worked out the exact sequence of web requests the wizard makes under the hood, and rebuilt that as a small background uploader: it signs in with the maintainer's own login (kept in the operating system's keychain, never written to a file), sends the images, then the spreadsheet, then asks the platform to run its matching — all untended, so the maintainer keeps working while it goes.

- **It self-corrects against the live system.** The first attempts bounced. The platform's own validator rejected field names the documentation had implied were fine, and a username that was subtly wrong — and each rejection came back as a precise error message. The AI read the error, corrected the mapping, and retried until the record landed cleanly. The platform's validation became the test suite.

## What this does *not* do

It doesn't decide which animal is which, whether a shark is pregnant, or which frame is the keeper — those are the human's calls, made in the editor before anything is exported. Uploading a photo doesn't *assign* an identity; it places the image in front of the platform's matching engine, which ranks candidate matches for a human to confirm or reject. The AI never invents an identification, and it won't send the same photo twice. It removes the clerical work, not the expertise — and it's done with the maintainer's own account and own data, on a platform he advises, not by hammering someone else's service.

## Why this works

The metadata chore and the upload chore look like two separate problems; they're really one. Everything the database needs is already latent in a well-tended photo library — the export just has to carry it out and something has to reshape it on the way in. And the "build the door" part generalises well beyond photo-ID: a platform without a friendly programming interface isn't necessarily a dead end for automation. If its workings are visible — open-source code, or even just the network requests a browser makes — an agent can often replicate them, build the integration the platform never published, and then harden it against the live system's own error messages until it's reliable.

## Note

This is a pattern, not a fixed pipeline. The photo editor, the database, how far you take the background uploader versus just using the official route — all yours to shape. The durable idea is: *your edited library already holds the data the database wants; let the AI reshape and move it — and when the official route is painful, the agent can often build a better one out of how the platform already works.* Paste this to your AI and build the version that fits how you work.
