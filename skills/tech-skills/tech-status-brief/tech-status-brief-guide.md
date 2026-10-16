# Engineering Brief for Non-Technical Readers

Turns technical facts into something a business reader can decide from: the consequence first, every fact costed in their currency, and what you know kept visibly apart from what you suspect.

---

## Who this is for

Anyone who has to explain engineering to people who do not do engineering: software engineers, tech leads and engineering managers, SREs writing incident updates, solution architects and pre-sales engineers, support leads handling escalations, and founders explaining technical risk to a board or a client.

## The problem it solves

Engineers explaining engineering to leadership have two failure modes and use both.

Either the explanation carries every detail, so the reader stops at paragraph two and decides from the last thing they understood. Or it gets simplified until it is no longer true, and the decision made from it is wrong in a way nobody catches for a month.

There is a third failure specific to incidents, and it is the expensive one. Somebody puts a suspected cause in a live update. It gets forwarded to a customer, it turns out to be wrong, and the correction costs more credibility than saying nothing would have. That single habit does more damage than any other thing in this document.

---

## What you give it

**Required:** what you want to communicate, and the technical detail behind it.

| Context | Why it matters |
|---|---|
| **Who reads it, and what they can do about it** | A reader who cannot act on something does not need it explained |
| **What decision is being asked for, if any** | A brief for a decision is a different document, and most are written as information when they should be the first |
| What they already believe, including anything wrong | Correcting a wrong belief is a different job from filling a gap |
| **For a live incident, confirmed against suspected** | These must not be mixed, and nothing suspected goes in |
| The forum and the length | Something read aloud in a meeting is not the same document as one read alone |

## What you get back

1. **The headline**: the consequence, in one or two lines, with no mechanism in it
2. What it means, in the reader's currency: money, time, customers, risk
3. **What we know and what we do not**, kept separate with hypotheses labelled
4. Options where a decision is needed, each with cost, time and risk, **including doing nothing**
5. Recommendation, and the reason
6. **What happens next, and when the next update comes**
7. Detail, at the end, for whoever wants it

---

## Translate into cost, not into simpler words

Explaining technical things to a business reader is usually taught as "avoid jargon". That is not the problem. The problem is that a technical fact with no consequence attached gives the reader nothing to decide with.

| What engineers write | What the reader can act on |
|---|---|
| The database is at 85 percent capacity | We have about six weeks before signups start failing, and the fix takes three |
| Significant technical debt in the payments module | Every change to payments takes three times longer than a year ago, and the next two features are both there |
| The service had a partial outage | For 40 minutes, about a fifth of customers could not complete checkout |

None of the right-hand column is dumbed down. It is the same fact with its consequence attached, which is the half engineers leave out.

## During an incident, silence beats a wrong cause

Confirmed facts and hypotheses go in different places, and the hypothesis is labelled as one.

**It will not put a suspected cause in a live incident update**, and it will not produce a version that does. "We do not yet know the cause. We know the impact is limited to X, and we will update at 4pm" is a strong update. A confident wrong cause is not, and it will be quoted back.

Every update also carries a next update time. It is the cheapest thing in incident communication and it stops a stream of questions from people who cannot help.

## The two arguments engineers lose by default

**Explaining a delay.** "It is more complex than expected" erodes trust in every future estimate you give. What works is saying what you now know that you did not, what it changes, and where that leaves you, as a range rather than a new single date.

**Justifying work with no visible output.** Debt, migration and infrastructure all share the problem that the benefit is an absence. It has to be framed as risk currently being carried or the cost of continuing: what is likely to happen and when, what it will cost then against now, and what else is blocked by it. Never on engineering aesthetics. "The code is messy" is not an argument to anybody outside engineering, and using it costs you the next request as well.

## What good output looks like

A strong brief could be read by somebody who leaves after the first two lines and they would still act correctly. That is the actual test, because that is what a lot of readers do.

The options section should include doing nothing with its cost. It is a real option, it is frequently the one chosen, and a brief that omits it reads as advocacy rather than analysis.

If it comes back shorter than you expected, check what was cut. The rule is that mechanism stays only where removing it would change what a reasonable reader decides, and most engineering briefs fail that test in three or four places.

---

## Installing it

1. Download this folder, or make a folder named `tech-status-brief` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill, so it works on a free plan.

## Using it

Give it the facts and say who is reading.

Examples that work:

- "Outage update for our biggest client. We know the impact. We do not know the cause yet."
- "I need three weeks for a migration nobody can see the value of. Write the case."
- "Feature is six weeks late. Explain it to the steering committee without losing the room."
- "Board asks why we cannot just add the feature. The answer is architectural. Two paragraphs."
- "Two options, one costs more and is safer. Present both with the tradeoff."

Saying what the reader can actually do about it is what stops the brief becoming an explanation nobody needed.

---

## Limits worth knowing

- It does not create the analysis. Give it the facts, and make sure they are confirmed before it writes them.
- **It does not speculate about the cause of a live incident**, and it will not produce a version that does.
- It does not commit a date, a fix or a recovery time on your behalf. Those come from whoever can deliver them.
- It does not minimise. A brief that flatters works exactly once, and the discount then applies to everything else you write.
- It does not decide whether to escalate, or to whom. It writes the document; that judgement stays yours.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It left out your cause theory | Live incident, cause not confirmed | Deliberate. Say it is confirmed and it will include it. |
| Shorter than you expected | Mechanism removed where it would not change a decision | Check what went. Most of it will not be missed. |
| It added "doing nothing" | It is a real option and usually the default | Its cost is what justifies the alternative. |
| Feels blunt about the delay | It explains by what changed, not by difficulty | "More complex than expected" is the sentence that costs you the next estimate. |
| No new delivery date | Uncertainty is not resolved | You get a range. A single date you cannot defend is worse. |
| Technical reader says it is oversimplified | It was written for the reader you named | Say who reads it. The engineering version is a different document. |

---

Part of the [Techies skills](../README.md) in the [Claude Skills Library](../../README.md).
