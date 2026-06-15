# The replication audit

Check whether your finished study is actually *set up to be re-run by someone else* — that the code, the data, and the steps behind every figure and number are really present and traceable — and get back a plain checklist of the gaps, before a reviewer, a co-author, or a stranger with your repository link finds them.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (where your code lives, how it's run) in collaboration with you. It's the back half of the science arc — the test you apply once [the analysis](./lab-notebook-analysis.md) is done and [the manuscript](./the-science-workflow.md) is drafting — and the thing that lets an independent review actually mean something.

*What you'll need: somewhere your analysis code and data live under version control (a Git repository, public or private). The audit reads that repository and tries to follow it the way an outsider would; nothing exotic beyond your AI and the repo.*

## The core idea

Reproducibility is the part of science that everyone agrees matters and almost nobody checks until it's too late. The quiet truth is that a study can be completely correct *and* impossible for anyone else to re-run: the figure was made by a script that isn't in the repository, the analysis depends on a data file that only exists on your laptop, a number in the abstract came from a calculation nobody wrote down, the code runs only because of a package version you happen to have installed. None of that is visible from the manuscript. It surfaces when a reviewer asks for the code, or a collaborator tries to build on the work, or — worst — someone fails to reproduce a result and you can't reconstruct why either.

The fix is to make reproducibility something you *test*, on purpose, rather than assume. The standing habit underneath it is simple and strict: **push everything needed to re-run each result — the code, the input data, and the saved outputs — to the project's repository, not just the code.** The test it works toward is concrete: *could someone handed only the repository link rerun it and land on the same numbers?* The audit doesn't *prove* that re-run succeeds — it checks how close you are to passing it: whether everything needed is present and every number is traceable to a runnable source, and hands you the remaining gaps as a checklist.

This is what makes the rest of the science arc honest. A [hostile review of the analysis](./lab-notebook-analysis.md), or [an independent review of your own manuscript](./reviewing-your-own-manuscript.md), can only mean something if the work is reproducible — otherwise the reviewer (human or AI) is critiquing a description, not the thing itself.

## How it runs

**Check the repository exists and holds what it should.** The AI looks at whether there *is* a repository for the analysis, and whether the things needed to reproduce the study are actually in it: the analysis code, the input data (or a clear, honest account of where it is and why it's held back), and the saved outputs each result is drawn from. A study with the code but not the data, or the data but not the script that made Figure 3, fails this — and the audit says exactly what's absent.

**Trace every figure and headline number back to a runnable source.** For each figure, table, and number that matters, the AI tries to find the line of code and the input that produced it. A number in the manuscript that traces to nothing runnable is the highest-value thing this catches — it's both a reproducibility gap and, often, a sign the number drifted somewhere along the way.

**Check the code would actually run for someone else.** Beyond presence, a light cleanliness pass: are the dependencies stated, so someone could recreate the environment? Are there absolute paths hard-wired to your own machine that would break for anyone else? Is the order things must be run in clear? It isn't trying to re-execute everything (often it can't), but it flags the things that would obviously stop an outsider cold.

**Handle sensitive data honestly.** Some data genuinely can't be public — the precise locations of a threatened species, human-subject data, a partner's unpublished records. The answer is not to skip reproducibility but to be explicit about the carve-out: keep the repository private, or coarsen and hold back the risky detail, and *note what was held back and why*. A documented, deliberate gap is reproducible science; an undocumented one is just a hole.

**Hand back a replication-gaps checklist.** The output is a short, plain list: what's reproducible, what isn't, and the specific fix for each gap ("Figure 2's script isn't in the repo"; "the abstract's 34% isn't traceable to any output"; "`/Users/you/data.csv` is a local path that will break"). It's a to-do list for making the study genuinely re-runnable — not a grade, a punch-list.

## What this does *not* do

It doesn't *re-run* your whole analysis and confirm the science is correct — that's beyond what it can usually do, and it's a different question (the [analysis checks](./lab-notebook-analysis.md) handle correctness *during* the work). This audits whether the work *could* be re-run, which is the prerequisite for anyone — including you, later — to confirm it. It won't decide what's safe to make public; it flags sensitive data and you make the call. And it isn't a substitute for someone actually reproducing the study — it's how you make sure that when they try, they can.

## Why this works

The gaps that break reproducibility are individually small and collectively fatal, and every one of them is invisible from the manuscript — which is exactly why they survive to publication. An outside reader following the repository link is the only thing that finds them, and the audit is an AI playing that reader before a real one shows up. Doing it as a standing habit — everything pushed, every number traceable — rather than a scramble at submission is what keeps it cheap: the work was reproducible all along, and the audit just proves it.

## Note

This is a pattern, not a fixed tool. The parts that are yours to shape: where your repositories live, how strict you are about full re-runnability versus presence, how you handle data you can't share. The load-bearing habit is the strict one — *push everything needed to rerun each result, not just the code* — because the audit can only check what's there. The durable idea is: *a study you can't re-run isn't finished — so test, before anyone else does, that the repository link alone would land a stranger on the same numbers.* Paste this to your AI and build the version that fits how your field shares its work.
