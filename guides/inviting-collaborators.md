---
audience: simon
---

# Inviting collaborators

The repo is private. New users who click the GitHub link without access get a 404 with no signal about what to do next — they assume the link is broken and bounce. Resolve access before sending the link.

## The flow

1. **Ask for their GitHub username first.** Use the template below.
2. **When they reply with the username**, add them to the `marinemegafauna` org or the repo directly:

   ```bash
   gh api -X PUT "/repos/marinemegafauna/mmf-claude-code/collaborators/<username>" \
     -f permission=read
   ```

   Read access is enough — they can clone the repo and the bootstrap script handles everything else. They don't need write access until they're contributing back, and even then PRs from forks work fine.

3. **Send the README link** along with the three-step prompt. Once they've accepted the invite (GitHub emails them) the link works.

## The template

Slack / email / DM, in roughly this shape:

> Hey <name> — want to set you up on the Claude system I've been using. It's a private repo so I need to add you first.
>
> What's your GitHub username? (or the email on your GitHub account, if you don't know off-hand)
>
> Once you reply I'll add you, then I'll send a link with a short prompt. Setup is ~30 minutes (~10 min downloading apps, ~15 min answering questions). You'll need a Claude Pro plan ($20/month) — let me know if you're not on one yet, MMF has an org plan I can add you to.

Adjust the Pro-plan paragraph based on context:

- **MMF science team:** *"You'll be added to the MMF org Pro plan — no personal subscription needed."*
- **External collaborators:** as written above (Pro is the right plan; higher tiers not required).
- **Already-paying-Pro users:** drop the plan paragraph entirely.

## After they're added

Send the README link with the three-step prompt:

> You should have a GitHub invite by email. Once you accept, the README is at:
>
> https://github.com/marinemegafauna/mmf-claude-code
>
> The whole setup is the three steps in the README — install Claude Desktop, click the Code tab, paste the prompt. Ping me if anything's unclear.

That's it. The rest is on the README + `/onboard`.

## If they bounced before you saw this guide

If a collaborator already hit the 404, message them: *"Sorry — that repo's private and I forgot to add you first. What's your GitHub username and I'll fix it now."* No setup is wasted; they haven't done anything yet.
