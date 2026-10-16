# Rollout and Migration Plan

Classifies a change by how reversible it is, phases it by blast radius, and sets the abort criteria and the rollback procedure before anything starts.

---

## Who this is for

Anyone who has to get a change into production without breaking it: software engineers, SREs and platform engineers, DevOps and release engineers, data engineers running migrations, tech leads, and anyone who has been handed a cutover date.

## The problem it solves

The plan is usually "deploy it and watch".

That holds until the thing being watched is a metric that lags by an hour, or until the rollback everybody assumed exists turns out to need a schema change that has already run. Most bad deploys are not bad code. They are a change nobody could undo quickly enough, discovered at the point where undoing it was the only option left.

The other reliable failure is the data migration compressed into one evening. The dual-write, backfill, verify, cutover, cleanup sequence exists because each step is a cheap place to catch a problem. Running them all in one sitting because the change looked small removes every one of those places, and the problem surfaces later, in the data, where it is expensive.

---

## What you give it

**Required:** what is changing, and what it touches.

| Context | Why it matters |
|---|---|
| **Whether it is reversible, and how fast** | A flag reverses in seconds; a migration with a backfill may not reverse at all. This one answer determines the entire shape of the plan |
| **Whether data is changed, moved or reinterpreted** | Data migrations are the ones that go wrong and the ones people plan least |
| What is downstream | Including the internal team you forgot and the report that runs on Monday |
| **What the signal is** | The number that tells you within minutes, not hours, that this is going badly |
| Traffic pattern and timing constraints | Peak hours, month end, a freeze, a festival, a customer event |

## What you get back

1. **Change classification**: reversible in place, reversible with effort, or one way, and what follows from it
2. Blast radius per phase
3. **Phases**, each with entry conditions, soak time, verification, and what must be true to proceed
4. **The data plan**, where data is involved, with soak times per step
5. **Abort criteria**: signal, threshold, window, and who can call it without asking
6. Verification per phase, including the old path
7. **Rollback as a procedure**, with what happens to data written in the meantime
8. Timing and people, and what is being avoided
9. What is not covered

---

## Classification first, because the plan follows from it

| Class | What it means | What the plan emphasises |
|---|---|---|
| **Reversible in place** | Flag off, revert the deploy | Short plan, low ceremony |
| **Reversible with effort** | Rollback needs a deploy or config change, minutes to hours | Phasing and a tested rollback |
| **One way** | Destructive migration, deletion, external commitment, schema already written against | Verification **before** the irreversible step, because there is no after |

Teams routinely run one-way changes with a plan written for a reversible one, and discover the difference at the worst possible moment. So this goes at the top of the document.

## Abort criteria get written before you start

What signal, at what threshold, over what window, means stop.

This has to be decided in advance, because during a rollout every number is arguable and **the person arguing is the person who wants it to work.** A threshold agreed while nobody is under pressure is a different threshold from one negotiated at 40 percent traffic.

It also names who can call the abort and whether they need permission. A criterion that requires waking somebody up before it can be invoked will not be invoked, which makes it decoration.

## Phases that can actually show a problem

A phase is only useful if the signal is visible in it. **One percent of low traffic tells you nothing**, and a phase that cannot surface a problem is a delay pretending to be a safeguard.

So each phase gets a soak time covering a full daily cycle, because load varies by hour and the failure that only appears at peak will not appear at 3pm on a Tuesday. And each names what has to be true before the next one starts, rather than leaving that to whoever is watching.

## The rollback questions nobody asks until 3am

- What happens to data written while the new path was live
- **Does rolling back the deploy roll back the schema**, and if not, does the old code work against the new schema
- Is the rollback itself risky, and has it ever been tested

An untested rollback is a hypothesis, and the plan labels it as one rather than listing it as a step. The verification section also includes the thing most people drop: **check that the old path still works**, for as long as it exists. Most rollout incidents are found on the new path and caused on the old one.

## What good output looks like

A strong plan is longer than you wanted for a one-way change and shorter than you expected for a reversible one. That asymmetry is the classification doing its job.

The abort criteria should be numbers you would actually act on. If reading them makes you want to soften one, that is the one to keep, because it is the one you will be tempted to argue with at the time.

And the rollback should have at least one uncomfortable line in it, usually about data written during the window. If rollback is described in a single sentence, it has not been thought about.

---

## Installing it

1. Download this folder, or make a folder named `tech-rollout-plan` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill, so it works on a free plan.

## Using it

Say what is changing and whether it can be undone.

Examples that work:

- "Moving user sessions from one store to another. Zero downtime, two million rows. Plan it."
- "Schema change with a backfill. It cannot be rolled back once the old column is dropped."
- "We are behind a feature flag at 5 percent and nothing is happening. Is the phase too small to tell?"
- "Cutover is Saturday night. What are we going to wish we had written down?"
- "Review this rollout plan. It says rollback is 'revert the deploy' and I do not believe it."

Saying whether data is involved changes the plan more than anything else you can tell it.

---

## Limits worth knowing

- It does not deploy, migrate, execute or run anything. It produces a plan for people to follow.
- **It does not hand over commands to run against production.** Anything that has to be run is described as a step for an engineer to write and review.
- It has no access to your systems, so it cannot tell you whether your rollback works. It tells you to test it.
- It does not know your traffic, data volumes or dependencies unless you say. Figures you do not supply become open questions, never estimates.
- It does not decide whether to proceed. It sets the criteria, and the decision stays with the people accountable.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Plan longer than expected | Classified as one way, or data is involved | Correct. One-way changes need verification before, not rollback after. |
| Plan shorter than expected | Reversible in place | Also correct. A flag change does not need six phases. |
| It will not give you commands | Deliberate, and not negotiable | You get the step described. An engineer writes and reviews the command. |
| Soak times feel long | Each covers a full daily cycle | Load varies by hour. A peak-only failure will not appear at 3pm Tuesday. |
| It flags your rollback as untested | You said it was assumed | Test it once. An untested rollback is a hypothesis. |
| Abort thresholds feel harsh | Set before anyone is under pressure | That is why they are set then. They are easier to agree now than to enforce at 40 percent. |

---

Part of the [Techies skills](../README.md) in the [Claude Skills Library](../../README.md).
