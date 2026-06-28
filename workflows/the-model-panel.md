# The model panel — several AIs on one problem

Put a few different AI models on the same question at once — independently — then have one of them reconcile the answers, so you get a cross-checked result instead of one model's confident guess.

This is an idea file. Paste it into Claude Code or Codex to build a version for your own work; it'll wire in the specifics (which models, where the results go) with you. It has to be an agent that can run command-line tools and create files on your machine — a plain chat assistant can't dispatch the other models.

*What you'll need: the extra panel members are other AI models reachable from the command line — OpenAI's Codex and Google's Gemini are the two used here. Each is a separate install and account. With only your main model you can still get value (run it twice in fresh, independent passes and merge), but a panel of different model *families* is the real point, so flag the setup cost up front.*

## The core idea

One model is one opinion — fluent, fast, and unchecked. And different model families fail in different ways: each has its own blind spots, its own things it over-confidently gets wrong. So the reliable move on anything that matters is not to ask one model harder, but to ask *several* — independently, without letting them see each other's answers — and then reconcile what comes back. Where they agree, you have a strong signal. Where they differ, you have something worth a closer look. And a final reading-over of all of them together catches things no single one raised.

This isn't a new idea — it's one this system was already leaning on (the independent passes in [reviewing someone else's work](./reviewing-others-work.md) and in [drafting and review](./writing-and-review.md) are exactly this shape). What's new is naming it as *one reusable engine* and pinning down when to use it. The push to do that came from a published result: a tool called Fusion (from OpenRouter) showed that a **panel of models, merged by a judge model, beat any single top-tier model** on a hard research benchmark — and, strikingly, that even running *one* model twice and reconciling the two passes did better than running it once. Most of the gain came from the reconciling step itself, not just from having fancier models. That matched what this setup was already finding in practice, so it was worth making deliberate.

The one distinction that decides everything is **what job you're doing:**

- **Answering once (fresh assessment).** A question, a decision, a "what do the models, taken together, think about X?" Here you want maximum independence: all the models hit the *same* input in parallel, then one reconciles. There's no second round — you asked, they answered, you merge.
- **Improving a document over rounds (iterative refinement).** Reviewing a plan, hardening a draft. Here the panel runs once to find the problems, the fixes get folded into the document, and then the *edited* document goes back through a model again — because a fix can introduce a new problem, and only a reader looking at the current version can catch that. This half is deliberately sequential, not another parallel panel: each pass needs to see what the last fix did. It loops until the model stops finding real problems.

Getting those two the wrong way round is the classic mistake — running a parallel panel on a document you're iterating loses the catch-the-regression benefit; looping a one-shot question wastes effort. The panel is for breadth; the loop is for settling.

## How it runs

- **The panel — different families, in parallel, blind to each other.** Three independent reviewers read the same frozen input at once: your main model (Claude), plus two others reached from the command line (Codex and Gemini). "Command line" just means the text terminal the agent already drives; the extra models are run **read-only** there — they can read everything and comment, but can't change a file. They also run on their *own* accounts and quotas, so leaning on them doesn't eat into your main model's budget. Keeping them blind to one another is the whole point — three genuinely independent reads, not an echo.
- **The reconcile.** One model (your main one) reads all the responses and writes a structured merge: what they agree on, where they contradict each other, what only one of them raised, and what *none* of them caught. Then a deliberate filter: only act on a point if two of the three agree, or if it's been checked against the actual source. That filter matters — three models surface a lot, much of it low-value, and without the bar you'd churn a working document chasing noise.
- **The loop (document mode only).** Fold the agreed fixes into the document, then send the edited version back through one model to check whether the fixes broke anything. Repeat until it comes back clean. There's no fixed number of rounds — it runs until the work genuinely settles, which can be several passes — with a simple guard that stops and asks for a human if it starts going in circles (the same issue reappearing, fixes fighting each other).

In practice this is wired as one shared capability that the more specific workflows call, so the panel logic lives in exactly one place and a fix to it improves everything that uses it.

## What this does *not* do

- **It doesn't make the call for you.** It hands you a reconciled, cross-checked view; the judgement — which fix to take, whether the decision is right — stays yours.
- **It's the wrong tool for some jobs.** Voice-driven writing (an email, an essay, anything in your own voice) should *not* go through a panel — merging several drafts sands off the voice that made it yours; keep that single-author. And pure fact-lookups (does this citation exist? what's this exact figure?) want a definite source, not a panel — a model asked to "verify" a fact can invent a confident wrong answer, which is the opposite of what you need.
- **More models is not always better.** The benefit comes from *diversity* of perspective, and it has diminishing returns — two or three different families is the sweet spot; a fourth mostly adds cost.
- **It costs time, money, and setup.** A three-model panel is slower and pricier than one quick answer, and the extra models each need their own account. So it's reserved for things that warrant it — a high-stakes review, a foundational decision — not routine edits. The everyday work stays single-model; the panel is the move you reach for when being *right* matters more than being fast.

## Why this works

Two independent things stack. First, different model families genuinely catch different errors, so a panel covers more of the failure space than any one model run harder. Second — and this is the surprising part — the *reconciling* step adds value on its own: forcing the disagreements into the open and weighing them is where a lot of the gain comes from, which is why even one model run twice and merged beats one run once. You're not just buying more horsepower; you're buying a structured second look.

## Note

This is a pattern, not a fixed tool. What's yours to shape: which second and third models you add (or whether you start with just your main model run twice), whether you bother with the convergence loop or only ever use the one-shot panel, and where you set the bar for "this is high-stakes enough to convene the panel." It pairs naturally with [reviewing someone else's work](./reviewing-others-work.md), [drafting and review](./writing-and-review.md), and [surfacing conflicts](./surfacing-conflicts.md) — all of which are really this engine pointed at a specific job. The durable idea is: *on anything that matters, ask several independent models, reconcile them deliberately, and — for a document you're improving — keep looping until it stops finding real problems.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/the-model-panel.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
