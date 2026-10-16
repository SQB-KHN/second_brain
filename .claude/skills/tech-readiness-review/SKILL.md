---
name: tech-readiness-review
description: Review a service against blast radius, observability, failure handling, rollback and ownership, and separate real blockers from debt. Use for production or launch readiness.
---

# Production Readiness Review

A service ships because it works, and works is the lowest bar available. Six weeks later somebody discovers it has no alerts, no runbook, no tested rollback and exactly one person who understands it. They discover this during an incident, at a bad hour, and none of it is fixable then.

## When to use this

Trigger on: production readiness, launch readiness, go live checklist, PRR, operational readiness, pre-launch review, GA checklist, handover to on-call, "are we ready to ship", "what are we missing before launch".

## Before you start

Required: a description of what is shipping and what it depends on.

Ask, briefly:
1. **What breaks for a user if this is completely down, and separately if it is only slow.** These differ, and they set how much of the rest matters. A batch job and a login path do not need the same review.
2. **Who owns it after launch, and whether they know that.** An unowned service is the finding, not a footnote.
3. What it depends on, including the ones people forget: auth, config, DNS, a third-party API, a shared database, a cron job somewhere.
4. What the launch actually is: internal, a percentage of traffic, one customer, or everyone.
5. Whether an existing checklist or standard applies. Follow theirs rather than proposing your own.

## Workflow

### 1. Establish the blast radius first, because it scales everything else

Ask in order: who is affected if this fails, how would they notice, is there a workaround, and **is anything lost permanently.**

That last one changes the review. A failure that loses data or money permanently justifies work a recoverable failure does not, and a review that treats every failure alike will over-engineer a batch job and under-protect a payment path.

### 2. Work the areas, marking each present, partial, absent or not applicable

"Not applicable" is a real answer and it needs a reason, not a blank.

**Observability**
- Does it emit anything at all when it fails, and where does that go
- Is there a dashboard, and could somebody who did not build it find it
- Do alerts fire on user impact rather than on machine state. CPU is not an alert; failed logins are.
- **Does every alert have a runbook that exists**, rather than one that is planned
- Can you tell the difference between this being broken and its dependency being broken

**Failure handling**
- What happens when each dependency is **slow** rather than down. Slow is the harder case and the one nobody tests.
- Timeouts set deliberately, or inherited from a library nobody has read
- Retries, and whether they are safe to repeat. A retry on a non-idempotent write is a data corruption path.
- What happens under a burst, and whether anything sheds load or everything degrades together

**Rollback**
- Can this be turned off, by whom, and how long does it take
- Is the rollback path tested, or assumed
- **Does the rollback still work after a schema or data change**, which is where most rollbacks actually fail
- Is there a flag, and does turning it off genuinely stop the behaviour

**Data**
- What is written, where, and what happens if it is written twice
- Migration and backfill state, and whether the old path still works
- What is retained and for how long, and whether that was a decision or a default

**Operability**
- Who is on call, and have they seen this before launch
- Is there anything only one person can do
- Configuration, secrets and access: how are they changed, and by whom

**Capacity and cost**
- Expected load and the headroom above it, what happens at ten times that, and whether anybody will notice if it becomes expensive

### 3. Separate blockers from debt, strictly

- **Blocker.** Shipping without this creates a failure that is undetectable, unrecoverable, or unfixable by the person who will be paged.
- **Should have.** Real risk, acceptable for a defined window, with an owner and a date.
- **Accept.** A known gap, deliberately accepted, written down so it is not rediscovered later as a surprise.

The third category is what makes this usable. Most readiness reviews produce a list that gets ignored because everything is on it. **A short blocker list gets acted on.**

### 4. Test every blocker against one question

For each: what happens at three in the morning if this is missing and the service fails?

If the honest answer is that the person paged can still see the problem, understand it and stop it, then it is not a blocker. That question settles arguments about severity faster than any scoring matrix.

### 5. Give a verdict, and make it a decision

Ready, ready with named conditions, or not ready. Where not ready, the blockers come first and nothing else is discussed until they are addressed.

Where the team intends to ship anyway, say so plainly, record the accepted risks, and **name who accepted them.** A documented decision to accept risk is a legitimate outcome. An undocumented one is how the next incident starts.

## Output format

**1. Verdict.** Ready, ready with conditions, or not ready, and the blocker count.

**2. Blast radius.** Who is affected, how they notice, whether there is a workaround, and what is unrecoverable.

**3. Readiness table.**

| Area | Item | Present / partial / absent / N-A | Evidence | Owner |

**4. Blockers.** Each with its three-in-the-morning consequence and what would close it.

**5. Should have.** Each with an owner and a date.

**6. Accepted gaps.** Written down, with who accepted them.

**7. What could not be assessed.** Anything needing access to the running system, stated plainly.

**8. Questions for the team.** What the review could not answer from the description given.

## Quality bar

- Is the blast radius established before anything else is assessed
- Does every item carry present, partial, absent or not applicable, with none left blank
- Is every "not applicable" justified rather than asserted
- Does every alert named have a runbook that exists rather than one that is planned
- Is the slow-dependency case assessed, not only the down case
- Is the rollback checked against a schema or data change, not only a code change
- Is every blocker justified by what happens at three in the morning to the person paged
- Are blockers, should-haves and accepted gaps genuinely separated, with a short blocker list
- Where the team will ship anyway, is the accepted risk recorded with who accepted it
- Is everything that could not be assessed stated rather than passed over

## What this skill does not do

- It has no access to your service, monitoring, infrastructure or code. It reviews what you describe, and it states what it could not see.
- It does not certify anything as safe. It produces an assessment for the people who own the decision.
- It does not run checks, execute commands or test anything.
- It does not know your organisation's standards unless you supply them. Where you do, it applies yours instead of a general list.
- It does not decide whether to ship. It gives you the blockers and the accepted risks, and the call stays with the team.
