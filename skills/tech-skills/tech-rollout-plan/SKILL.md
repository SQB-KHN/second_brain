---
name: tech-rollout-plan
description: Classify a change by reversibility, phase it by blast radius, and set abort criteria and a tested rollback before it starts. Use for rollouts, migrations or cutovers.
---

# Rollout and Migration Plan

The plan is usually "deploy it and watch". That holds until the thing being watched is a metric that lags by an hour, or until the rollback everybody assumed exists turns out to need a schema change that has already run. Most bad deploys are not bad code. They are a change nobody could undo quickly enough.

## When to use this

Trigger on: rollout plan, migration plan, deployment plan, cutover, phased rollout, canary, feature flag plan, data migration, go live plan, zero downtime, "how do we ship this safely".

## Before you start

Required: what is changing, and what it touches.

Ask, briefly:
1. **Whether this is reversible, and how fast.** A change behind a flag reverses in seconds. A schema migration with a backfill may not reverse at all. This single answer determines the shape of the whole plan.
2. **Whether data is being changed, moved or reinterpreted.** Data migrations are the ones that go wrong, and the ones people plan least.
3. What is downstream: who consumes this, including the internal team you forgot and the report that runs on Monday.
4. **What the signal is.** What number tells you within minutes, not hours, that this is going badly.
5. Traffic pattern and timing constraints: peak hours, month end, a freeze, a festival, a customer event.

## Workflow

### 1. Classify the change, because the plan follows from it

- **Reversible in place.** Flag off, revert the deploy. Short plan, low risk.
- **Reversible with effort.** Rollback needs a deploy or a config change, and minutes to hours.
- **One way.** A destructive migration, a deletion, an external commitment, a schema change already written against. The plan is different in kind: emphasis moves from rollback to verification before the irreversible step.

State which this is, at the top. Teams routinely run one-way changes with a plan written for a reversible one, and find out the difference at the worst possible moment.

### 2. Where data is involved, expand the plan and slow it down

The sequence that works, and the one that gets shortened under time pressure:

1. Write to both old and new, read from old
2. Backfill in batches, with progress visible and the ability to stop
3. Verify the two agree, on a sample and then on totals, with a stated tolerance
4. Read from new, keep writing to both
5. Stop writing to old, after a stated period during which rollback is still possible
6. Only then remove the old path

**State how long each step should soak.** The failure is running all six in one evening because the change looked small, which removes every point at which the problem would have been caught cheaply.

### 3. Phase by blast radius, and make each phase capable of showing a problem

Internal, then one percent, then ten, then fifty, then everyone, is a shape rather than a rule. What matters:

- **Each phase is large enough for the signal to be visible.** One percent of low traffic tells you nothing, and a phase that cannot show a problem is a delay pretending to be a safeguard.
- Each phase has a stated soak time covering a full daily cycle, since load varies by hour
- Each phase names what has to be true before the next one starts

### 4. Set the abort criteria before starting, in numbers

What signal, at what threshold, over what window, means stop.

Written **before** the rollout, because during one every number is arguable and the person arguing is the person who wants it to work. Also name who can call the abort, and whether they need permission. A criterion requiring somebody to be woken up before it can be invoked will not be invoked.

### 5. Write the verification, not just the deploy steps

For each phase: what to check, where to look, and what the healthy value looks like. "Monitor the dashboard" is not verification.

Include the thing that is easy to forget: **check that the old path still works**, for as long as it still exists. Most rollout incidents are discovered on the new path and caused on the old one.

### 6. Write the rollback as a procedure, not as a sentence

Steps in order, with who runs them and how long it takes. Then the questions nobody asks until it is three in the morning:

- What happens to data written while the new path was live
- **Does rolling back the deploy roll back the schema**, and if not, does the old code work against the new schema
- Is the rollback itself risky, and has it ever been tested

An untested rollback is a hypothesis, and it should be labelled as one in the plan.

### 7. Name the people and the timing

Who runs it, who watches, who decides, and who is reachable. Then when: avoid end of day, end of week, the day before a holiday, and the peak hour. A rollout starting at 6pm on a Friday has already made one bad decision.

### 8. Say what is not covered

The dependency you cannot test, the client you cannot coordinate with, the thing that only fails at production scale. Naming it beats discovering it.

## Output format

**1. Change classification.** Reversible in place, reversible with effort, or one way, and what follows from that.

**2. Blast radius per phase.** Who is affected at each step.

**3. Phases.** Each with entry conditions, soak time, verification, and what must be true to proceed.

**4. Data plan**, where data is involved. Dual write, backfill, verify, cutover, cleanup, with soak times.

**5. Abort criteria.** Signal, threshold, window, and who can call it without asking.

**6. Verification per phase.** What to check, where, and the healthy value. Including the old path.

**7. Rollback procedure.** Steps, owner, duration, and what happens to data written in the meantime.

**8. Timing and people.** Who, when, and what is being avoided.

**9. What is not covered.**

## Quality bar

- Is the change classified as reversible in place, reversible with effort, or one way, at the top
- Does the shape of the plan match that classification
- Where data changes, is there a dual-write, backfill, verify, cutover, cleanup sequence with soak times
- Is each phase large enough for the signal to be visible
- Does every phase have a soak covering a full daily cycle
- Are abort criteria written as a signal, a threshold and a window, before the rollout starts
- Is it stated who can call the abort without needing permission
- Is verification specific about where to look and what healthy looks like
- Does the rollback state what happens to data written while the new path was live
- Is it stated whether the rollback has been tested, or is an assumption
- Is the old path verified for as long as it still exists

## What this skill does not do

- It does not deploy, migrate, execute or run anything. It produces a plan for people to follow.
- **It does not hand over commands to run against production.** Anything that has to be run is described as a step for an engineer to write and review.
- It has no access to your systems, so it cannot tell you whether your rollback works. It tells you to test it.
- It does not know your traffic, data volumes or dependencies unless you say. Figures you do not supply become open questions, never estimates.
- It does not decide whether to proceed. It sets the criteria, and the decision stays with the people accountable for it.
