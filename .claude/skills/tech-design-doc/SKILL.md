---
name: tech-design-doc
description: Write or review a design doc, RFC or ADR with alternatives that could actually win, the tradeoff stated, and what would change the decision. Use for design docs or ADRs.
---

# Design Doc and ADR

Most design documents describe the chosen solution, then add two alternatives afterwards so the section is not empty. Both are obviously worse, because they were written to lose. So the review adds nothing, the real tradeoff is never examined, and the decision gets relitigated in six months by somebody who cannot tell what was actually considered.

## When to use this

Trigger on: design doc, RFC, ADR, architecture decision record, technical proposal, tech spec, solution document, design review, "write up the design", "which approach should we take".

## Before you start

Required: the problem, and what you are considering doing about it.

Ask, briefly:
1. **The problem, stated without a solution inside it.** "We need a queue" is a solution. "Order confirmations are lost when the payment service is slow" is a problem. If it cannot be stated without naming the technology, the design is already decided and this document is a justification.
2. Constraints that are real: deadline, team size and skills, systems that cannot change, compliance, budget, who will operate it. A design that ignores who runs it is not a design.
3. **What you have already decided and will not reconsider.** Say it explicitly. A document pretending everything is open when it is not wastes the reviewers' time and their goodwill.
4. Scale now, and scale in a year. Both. Designing for the second without stating the first is the commonest source of over-engineering.
5. Who reviews this, and what they will object to.

## Two modes

**Write** a design doc, or **review** one. The same standard runs in both, because a document's failures are usually omissions rather than errors.

## Workflow

### 1. State the problem, the non-goals and the constraints before any solution

**Non-goals save the most review time and are the section most often missing.** What this explicitly does not solve, and what it is not trying to be. Without them, every reviewer proposes the thing you already decided against.

### 2. Consider alternatives that could actually win

This is the discipline the whole document rests on.

An option that was never viable is not an alternative, it is a rhetorical device, and experienced reviewers recognise it immediately and stop trusting the rest of the document.

For each option state what it does well, what it costs, and **under what conditions it would be the right choice.** That last clause is the test. If you cannot describe a world in which an alternative wins, either you have not understood it or it should not be in the document.

Always include the two that get left out: **doing nothing**, and **the simplest thing that could work.** Doing nothing has a cost, and stating it is what justifies the project at all. The simplest thing is the baseline every other option has to beat.

### 3. Make the tradeoff explicit rather than implicit

Every design gives something up. Name it:

- Complexity now against flexibility later, which is usually paid at the wrong time
- Consistency against availability
- Build against buy, including the operational cost of the thing you bought
- Performance against operability
- Speed of delivery against cost of change

A document with no stated downside has not been thought about, and reviewers will assume the downside exists and is being hidden.

### 4. Say what breaks it

- The assumption the whole design rests on, and what happens if it is wrong
- The scale at which it stops working, roughly
- The failure modes, and which are handled against which are accepted
- What happens when each dependency is unavailable

State these yourself. Being the person who names the design's weakness is the difference between a review that improves it and a review that discovers it.

### 5. Say whether the decision is reversible, because it sets how much analysis it deserves

A choice that can be undone in a week deserves a paragraph. A choice that will be load-bearing for five years deserves the argument. Most design documents give both the same treatment, wasting time on one and under-thinking the other.

State the cost of reversing it, and what would make the team want to.

### 6. Write down what would change the decision

Two or three specific conditions. This is what makes the document useful in a year, because a reader can check whether those conditions have arrived instead of guessing whether the reasoning still holds.

### 7. For an ADR, keep it short and keep the alternatives

Context, decision, status, consequences. The consequences section carries the bad as well as the good, and **a consequences section with only benefits is an advertisement.**

### 8. In review mode, review against the same standard

Are the alternatives real. Is the tradeoff stated. Are non-goals present. Is the load-bearing assumption named. Is reversibility assessed and does the depth match it. Look for what is missing rather than what is wrong.

## Output format

**1. Problem**, stated without a solution in it.

**2. Non-goals, and constraints.**

**3. Options considered.** Each with what it does well, what it costs, and the conditions under which it wins. Including doing nothing and the simplest thing that could work.

**4. The decision**, and why it beat the others under the stated constraints.

**5. The tradeoff.** What is being given up, explicitly.

**6. What breaks it.** The load-bearing assumption, the scale limit, the failure modes handled and accepted.

**7. Reversibility.** Cost of undoing it, and what would prompt that.

**8. What would change this decision.** Two or three specific conditions.

**9. Open questions**, with owners.

**10. In review mode:** what is missing, ranked, and which alternatives are not real.

## Quality bar

- Is the problem stated without naming the solution
- Are non-goals present and specific
- Could each alternative win under some stated condition, or is it there to lose
- Are doing nothing and the simplest thing that could work both considered
- Is the tradeoff stated as something given up, rather than only as benefits
- Is the load-bearing assumption named, with what happens if it is wrong
- Is reversibility assessed, and does the depth of analysis match it
- Are the conditions that would change the decision written down
- Would a reader in a year be able to tell what was actually considered
- Does the tradeoff or consequences section contain something the author would rather not write

## What this skill does not do

- It does not know your systems, constraints or team unless you tell it. Everything it reasons about comes from what you supply.
- It does not decide for you. It makes the tradeoff visible and says what each option costs.
- It does not invent benchmarks, latency figures or capacity numbers. Where a number is needed and you do not have one, it becomes an open question rather than an estimate.
- It does not produce diagrams. It says what each one has to show.
- It does not review your code. It reviews the design you describe.
- It does not hand over anything to be run. Where a design implies a migration or a command, it is described as a step for an engineer to write and review.
