---
name: tech-status-brief
description: Turn technical facts into a brief a non-technical reader can decide from, with the consequence first, hypotheses separated from what is known. Use for exec updates or escalations.
---

# Engineering Brief for Non-Technical Readers

Engineers explaining engineering to leadership have two failure modes and use both. Either the explanation carries every detail, so the reader stops at paragraph two and decides from the last thing they understood. Or it is simplified until it is no longer true, and the decision made from it is wrong in a way nobody catches for a month.

## When to use this

Trigger on: status update, exec summary, escalation, outage update, customer update, steering committee, client update, "explain this to leadership", "why is it late", "justify the tech debt work", "how do I present this decision".

## Before you start

Required: what you want to communicate, and the technical detail behind it.

Ask, briefly:
1. **Who reads it, and what they can do about it.** A CEO, a client, a product manager and a steering committee need different documents, and the second half matters more: a reader who cannot act on something does not need it explained.
2. **What decision is being asked for, if any.** A brief for a decision is a different document from one for information, and most are written as the second when they should be the first.
3. What they already believe, including anything wrong. Correcting a wrong belief is a different job from filling a gap.
4. **For a live incident, what is confirmed against what is suspected.** These must not be mixed, and nothing suspected goes in.
5. The forum and the length. Something read aloud in a meeting is not the same document as something read alone.

## The rule that matters

**Lead with the consequence, not the cause.**

Engineers explain in the order things happened, because that is the order they were understood in. A business reader needs the impact first, and the mechanism only as far as it affects a decision.

If the first line is technical, the reader forms a conclusion from the first thing they recognise, and the rest of the page gets spent correcting it.

## Workflow

### 1. Translate into what it costs, not what it is

Every technical fact needs its consequence attached, in a currency the reader already tracks: money, time, customers, risk or capacity.

- "The database is at 85 percent capacity" becomes "we have about six weeks before signups start failing, and the fix takes three"
- "There is significant technical debt in the payments module" becomes "every change to payments now takes three times longer than a year ago, and the next two features are both in that module"
- "The service had a partial outage" becomes "for 40 minutes, about a fifth of customers could not complete checkout"

The consequence is the half engineers leave out, and the only half most readers can act on.

### 2. Keep the line between what you know and what you suspect visible

Confirmed facts and current hypotheses go in different places, and the hypothesis is labelled as one.

**Speculating about a cause during a live incident is the most damaging thing this document can do.** It gets repeated externally, it turns out to be wrong, and the correction costs more credibility than the original silence would have. "We do not yet know the cause. We know the impact is limited to X, and we will update at 4pm" is a strong update. A confident wrong cause is not.

### 3. Give a next update time, and meet it

An update with no next update generates a stream of questions from people who cannot help. A named time stops them, and it is the cheapest thing in incident communication.

### 4. Present options with their cost, not a recommendation alone

Where a decision is being asked for, give two or three options with the cost, the time and the risk of each, then your recommendation and why.

**Include doing nothing and what it costs.** It is a real option, it is frequently the one chosen, and a brief that omits it reads as advocacy rather than analysis.

### 5. Explain a delay by what changed, not by how hard it was

"This is taking longer because we found the export runs against the same database as checkout, so the fast approach would slow checkout during business hours" is an explanation. "It is more complex than expected" is not, and it is the sentence that erodes trust in every future estimate you give.

Say what you now know that you did not, what it changes, and where that leaves you. Give a range rather than a new single date, unless the uncertainty is genuinely gone.

### 6. For work with no visible output, argue in the reader's terms

Debt, migration and infrastructure work share a problem: the benefit is an absence. Frame it as risk currently being carried, or as the cost of continuing.

- What is likely to happen, and roughly when
- What it will cost then, against what it costs now
- What else is blocked by it

Never argue for it on engineering aesthetics. "The code is messy" is not an argument to anybody outside engineering, and using it costs you the next request too.

### 7. Cut the mechanism to what affects the decision

Some mechanism is necessary, because a reader who understands nothing about why cannot judge the recommendation. The test is whether removing a piece of detail would change what a reasonable reader decides. If not, it goes.

## Output format

**1. The headline.** The consequence, in one or two lines, with no technical mechanism in it.

**2. What this means.** Impact in the reader's currency: money, time, customers, risk.

**3. What we know, and what we do not.** Kept separate, hypotheses labelled as hypotheses.

**4. Options**, where a decision is needed. Each with cost, time and risk, including doing nothing.

**5. Recommendation**, and the reason.

**6. What happens next**, and when the next update comes.

**7. Detail**, at the end, for whoever wants it.

## Quality bar

- Does the first line carry the consequence rather than the mechanism
- Does every technical fact have a cost attached in the reader's own currency
- Are confirmed facts and hypotheses visibly separated, with nothing suspected presented as known
- For a live incident, is the cause left unstated where it is not established
- Is there a next update time
- Where a decision is asked for, are there options with costs, including doing nothing
- Is a delay explained by what changed rather than by difficulty
- Is technical work argued as risk carried or cost incurred, never as engineering aesthetics
- Would removing any remaining mechanism change what a reasonable reader decides
- Could the reader act on this without asking a follow-up question

## What this skill does not do

- It does not create the analysis. Give it the facts, and make sure they are confirmed before it writes them.
- It does not speculate about the cause of a live incident, and it will not produce a version that does.
- It does not commit a date, a fix or a recovery time on your behalf. Those come from whoever can deliver them.
- It does not minimise. A brief that flatters works exactly once, and the discount then applies to everything else you write.
- It does not decide whether to escalate, or to whom, and it does not send anything. It writes the document; the judgement and the sending stay yours.
