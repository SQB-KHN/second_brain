# Design Doc and ADR

Writes or reviews a design document with alternatives that could genuinely win, the tradeoff stated as something given up, and the conditions that would change the decision.

---

## Who this is for

Anyone who proposes or reviews technical direction: software engineers writing their first design doc, senior and staff engineers, tech leads and engineering managers, solution and enterprise architects, platform teams publishing RFCs, and anyone reviewing somebody else's proposal.

## The problem it solves

Most design documents describe the chosen solution, then add two alternatives afterwards so the section is not empty.

Both alternatives are obviously worse, because they were written to lose. Experienced reviewers recognise this in about ten seconds and stop trusting the rest of the document. So the review adds nothing, the real tradeoff is never examined, and the decision gets relitigated in six months by somebody who cannot tell what was actually considered and what was theatre.

Asking any AI to write one unaided produces exactly this shape, and produces it fluently. A plausible design doc with strawmanned alternatives and a consequences section listing only benefits is the default output, and it is indistinguishable at a glance from a good one.

---

## What you give it

**Required:** the problem, and what you are considering doing about it.

| Context | Why it matters |
|---|---|
| **The problem stated without a solution in it** | "We need a queue" is a solution. "Order confirmations are lost when payments is slow" is a problem. If you cannot state it without naming the technology, the design is already decided |
| Real constraints | Deadline, team size and skills, systems that cannot change, compliance, budget, **who will operate it** |
| **What you have already decided and will not reconsider** | Say it. A document pretending everything is open wastes reviewers' time and their goodwill |
| Scale now, and scale in a year | Both. Designing for the second without stating the first is the commonest source of over-engineering |
| Who reviews it and what they will object to | The objection you can answer in the document is one you do not answer in a meeting |

## What you get back

1. The problem, non-goals and constraints, before any solution
2. **Options considered**, each with what it does well, what it costs, and **the conditions under which it wins**
3. The decision, and why it beat the others under your constraints
4. **The tradeoff**, stated as something given up
5. What breaks it: the load-bearing assumption, the scale limit, the failure modes handled and accepted
6. **Reversibility**, and whether the depth of analysis matches it
7. What would change this decision, as two or three specific conditions
8. Open questions with owners
9. In review mode: what is missing, ranked, and which alternatives are not real

---

## The test that kills fake alternatives

For every option, it asks one thing: **under what conditions would this be the right choice?**

If you cannot describe a world in which an alternative wins, either you have not understood it or it should not be in the document. That single question is what separates a real comparison from a justification with decoration.

It also insists on the two options that always get left out:

- **Doing nothing.** It has a cost, and stating that cost is what justifies the project at all. A document that omits it has not established that the work is worth doing.
- **The simplest thing that could work.** The baseline every other option has to beat. Skipping it is how teams end up with a distributed system where a cron job would have held for two more years.

## Non-goals, and why they save the most time

The section most often missing, and the one that prevents the largest number of review comments.

Without non-goals, every reviewer proposes the thing you already decided against, and you answer the same objection four times in four threads. With them, the review moves to the part you actually wanted looked at.

## Reversibility sets how much analysis it deserves

| Kind of decision | What it deserves |
|---|---|
| Undone in a week | A paragraph and a decision |
| Load-bearing for five years | The full argument, and the assumption named |

Most design documents give both the same treatment, which wastes time on one and under-thinks the other. So it states the cost of reversing, and matches the depth to it.

## What good output looks like

A strong design doc contains something the author would rather not have written. Usually that is in the tradeoff section: the thing being given up, stated plainly, with no attempt to argue it is not really a cost.

The alternatives should be uncomfortable to read, because at least one of them should look genuinely defensible. If they all read as obviously worse, the section is still decoration and it will say so.

In review mode, the findings are usually omissions rather than errors. Design documents fail by leaving things out, not by being wrong, and the most common omissions are the non-goals, the load-bearing assumption, and any honest statement of what the choice costs.

---

## Installing it

1. Download this folder, or make a folder named `tech-design-doc` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill, so it works on a free plan.

## Using it

State the problem, and be honest about what is already decided.

Examples that work:

- "We keep losing order confirmations when payments is slow. I think we need a queue but I want the alternatives tested."
- "Review this RFC before it goes to the architecture group. What will they push back on?"
- "Short ADR. We picked Postgres over DynamoDB. Capture why, properly."
- "My design doc got approved and I do not trust that. Find what the reviewers missed."
- "Build versus buy for our notification service. Include the operational cost of buying."

Telling it what is already decided and not up for discussion makes the document shorter and the review sharper.

---

## Limits worth knowing

- It does not know your systems, constraints or team unless you tell it. Everything it reasons about comes from what you supply.
- It does not decide for you. It makes the tradeoff visible and says what each option costs.
- **It does not invent benchmarks, latency figures or capacity numbers.** Where a number is needed and you do not have one, it becomes an open question rather than an estimate.
- It does not produce diagrams. It says what each one has to show.
- It does not review your code. It reviews the design you describe.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It rejected your problem statement | The solution was inside it | "We need X" is a solution. State what goes wrong today instead. |
| An alternative you dismissed came back | It can win under some condition | Read the condition. If it cannot happen, say so and it drops it. |
| It insists on "doing nothing" | It is a real option and often the chosen one | Its cost is what justifies the project. Omitting it reads as advocacy. |
| No performance numbers | It will not invent them | They come back as open questions. Supply yours and it uses them. |
| Review found only omissions | Design docs fail by leaving things out | That is the normal result and usually the useful one. |
| Document feels shorter than expected | Reversible decision, so the depth was scaled | Check the reversibility section. If it is wrong, say so. |

---

Part of the [Techies skills](../README.md) in the [Claude Skills Library](../../README.md).
