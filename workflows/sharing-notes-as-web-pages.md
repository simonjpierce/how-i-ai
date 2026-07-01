# Sharing a note as a web page

Turn any note in your vault into a clean, shareable web page — a real link you can send someone — for free, in a single step, without it leaving your control or landing in anyone's Drive.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

You finish something worth sharing — a review of a collaborator's grant, an explainer of a process, a short briefing — and now you want to *hand it to one person*. The usual routes all have friction. A file attachment is clunky and unversioned. A Google Doc drags the thing into someone's Drive, invites permission faff, and signals "please edit me." Pasting into an email loses the formatting. What you actually want is a plain link: they click, they read, done.

Your notes are already markdown, which is already the web's native format — so the gap between "a note on your machine" and "a web page with a URL" is tiny. A **static-site host** closes it for free: it takes plain files and serves them as web pages at a public address, with no server to run or pay for. The maintainer uses **Cloudflare Pages** (GitHub Pages and Netlify are equivalent free options); the page is built with **Astro**, a lightweight static-site generator, so each note comes out styled to match the maintainer's other sites instead of looking like a raw text dump.

The principle the whole thing rests on: **the note is the artifact, and publishing it should be one instruction, not a chore.** You say "publish this note"; the AI does the packaging, hosting, and bookkeeping, and hands you back a link.

## How it runs

- **One instruction to publish.** You point the AI at a note and say publish it. It picks a short, readable address from the title (a "slug" — the last part of the URL), builds the page, deploys it to the host, and reports the live link. What was a note a moment ago is now a URL you can paste into a message.

- **These pages are openly AI-assisted, and that's the point.** The maintainer uses them mostly to share work that was *done with AI* — a review, an analysis, a briefing — transparently, as assistant-written output rather than something dressed up as hand-crafted prose. So the design stays plain and the pages are set to **`noindex`** (a small instruction that tells search engines to ignore them): they're for sending to a specific person, not for being found by strangers. Anyone with the link can read it, but it won't surface in a search.

- **It keeps a record of what's live.** Publishing tags the source note as published and files it in a "published" folder, so you always know what's out in the world. Ask for a status check and the AI lists every published note and flags any whose source you've edited since — so you can re-publish the ones that have drifted. Updating is just re-publishing (same link); unpublishing removes the page.

- **It checks before it ships, because the page is public.** The body goes live *verbatim* — so the AI glances over it first for anything that shouldn't be public (someone else's private information, unpublished data, financials) and stops to confirm with you if it's unsure. Publishing is deliberate and on-request only; nothing goes live automatically.

- **Images and long pages work with a little extra handling.** A picture hosted somewhere public drops straight in; local images need copying alongside the page so they travel with it. For a long document, the AI can wire up a clickable contents list and "back to top" links. These are the rough edges worth knowing about up front rather than discovering live.

## What this does *not* do

It's not a blog or a public website, and it's not a discovery channel — the pages are deliberately unlisted and unsearchable, meant for one-to-one sharing by link. It doesn't manage access: there's no password, so anyone you give the link to can read it (and could pass it on) — which is exactly why the pre-publish sensitive-content check matters, and why anything genuinely private shouldn't go here at all. And it doesn't decide *what's* worth sharing or write it for you; it packages and ships a note you've already decided to hand over.

## Why this works

The friction in sharing was never the hosting — free static hosts have existed for years. It was the packaging: converting, styling, deploying, and remembering what you'd put where. Each step is small, but together they're enough that most people fall back to attachments and Google Docs. Handing that whole chain to the AI collapses it to a single instruction, and because the page is built from a plain file you already own, you stay in control of it — it lives on your host, under your account, and comes down when you say so.

## Note

This is a pattern, not a fixed implementation. The host (Cloudflare Pages, GitHub Pages, Netlify), the generator (Astro or any static-site tool), whether you style the pages to match a brand or keep them bare, how far you take the bookkeeping — all yours to shape. The durable idea is: *your notes are already web-ready, so sharing one should cost you a single instruction and keep the thing on your own turf.* Paste this to your AI and build the version that fits how you work.
