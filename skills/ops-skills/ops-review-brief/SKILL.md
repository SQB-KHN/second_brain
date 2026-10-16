---
name: ops-review-brief
description: Turn operations numbers into a one-page review brief or escalation: committed against delivered, what it cost, and actions with owners. Use for ops reviews, S&OP or escalations.
---

# Operations Review Brief

Operations gets judged once a month by people who were not there when it went wrong. The instinct is to explain everything that happened, in the order it happened. What the room actually needs is what was committed, what was delivered, what the gap cost, and what changes next month. The distance between a team that fixed the problem and a team that gets credit for fixing it is one page.

## When to use this

Trigger on: ops review, monthly operations review, S&OP meeting, management review, escalation, customer escalation, "explain why we missed", service failure report, RCA summary, supplier QBR prep, "prepare the ops update".

## Before you start

Required: the numbers already worked out. Service level, fill rate, inventory, cost, exceptions, whatever this review runs on.

Ask, briefly:
1. **Who reads it, and whether they sit inside or outside the company.** An internal review and a customer-facing explanation are different documents with different rules, and the second one carries commercial risk.
2. **What was committed, and by whom.** A miss can only be stated against a commitment. Without one there is no story, only a number.
3. Whether a decision or approval is being sought, or this is information.
4. What they already know, so the brief does not open on last month's news.
5. **For an escalation, whether a recovery date has already been given to the customer.** If one has, this brief must not contradict it. If one has not, this brief does not invent one.

## The one rule that matters

Lead with what was committed against what was delivered.

Operations reporting defaults to chronology, because chronology is how the month was experienced. A leader reads for exposure. If the first line does not say whether the commitment was met, the reader builds their own conclusion from whatever number they see first, and the rest of the page gets spent correcting it.

Every section opens with its conclusion. The narrative, where it is needed at all, comes after.

## Workflow

### 1. State the commitment, then the delivery

One line each. "Committed 96 percent fill rate, delivered 91.4. Committed the Nashik launch stock by 15 September, delivered 12 of 18 items."

If there was no explicit commitment, say so plainly rather than inventing one after the fact. An implied target is worth naming as implied.

### 2. Separate what you controlled from what you did not, rigorously

This section decides whether the brief is trusted, and it is the section most often abused.

- **Controllable:** a planning error, a late indent, a wrong forecast, a picking failure, an unplanned changeover, a decision taken too slowly
- **Not controllable:** a supplier's plant shutdown, a port closure, a transporter strike, a regulatory change, a customer changing the order after cut-off

Two rules make this credible. Every not-controllable item needs evidence attached, or it moves to controllable. And every one needs its mitigation stated, because a genuinely external cause with no mitigation attempted becomes controllable the second time it happens.

A brief in which nothing was controllable is not believed, and it should not be.

### 3. Price the miss

A service failure with no number attached does not get resourced. Convert it into money, or into a consequence the reader already tracks:

- Revenue lost or deferred, and say which of the two it was
- Expedite and air freight premium paid to recover
- Penalty or chargeback incurred, where a contract provides for one
- Production hours lost, and what those represent
- Working capital tied up in the wrong stock

Use only figures that exist in the source. Where the cost is genuinely unknown, say it is unknown and name who could size it. Never estimate a penalty or a lost-revenue figure, because an invented number gets quoted back as though it were measured.

### 4. Translate operations into business language

The reader thinks in customers, orders, cash and risk, not in operations metrics. Translate every time, and add the consequence:

- "Fill rate fell to 91 percent" becomes "38 customer orders shipped short, of which 11 went to the three accounts up for renewal this quarter"
- "Inventory days rose to 74" becomes "we are holding 18 days more stock than plan, which is 2.1 crore of cash, most of it in the slow-moving electrical range"
- "OTIF from the Coimbatore supplier is 62 percent" becomes "the Coimbatore supplier missed a third of its commitments, and it is the only source for four of our top ten items"

The consequence is the half operations leaves out, and the half the room needs to act.

### 5. Name the corrective actions properly

Each one carries what is being changed, what it prevents, who owns it, by when, and how anyone will know it worked.

An action without an owner and a date is a wish. An action without a verification measure returns next month as the same problem with a new explanation.

Then separate the two kinds, and label them:

- **Containment**, which stops the bleeding now
- **Fix**, which stops it recurring

Reporting containment as a fix is the most common failure in this document, and the reason one item appears in three consecutive reviews.

### 6. Carry the risks forward

Two to four items that need no decision now but would if they continue. One line each, with the trigger that would escalate them.

This section buys more credibility than any other, because it proves the last problem was seen before it landed.

## Output format

One page, roughly 400 to 500 words. If it runs longer, cut something. Do not shrink the type.

```
# [Period] Operations Review

## Committed against delivered
[Two or three lines. The commitment, the actual, the gap. Nothing else.]

## What drove the gap
[Three to five items. Cause first, number attached, marked controllable or not, with evidence.]

## What it cost
[Money, or a consequence the reader already tracks. Stated as unknown where it is unknown.]

## What changes
[Each action with owner, date and verification measure. Containment separated from fix.]

## Risks carried forward
[Two to four lines, each with its escalation trigger.]
```

For a deck, the same content across five to eight slides, one message per slide, each title written as a sentence. "Fill rate fell on a single supplier's delay" is a title. "Service Level Performance" is not.

For a customer-facing escalation the structure holds, but three things change: no internal blame, no naming of individuals, and no recovery date that has not been confirmed by whoever has to deliver it.

## Quality bar

- Does the first line state the commitment against the delivery
- Does every number trace to the source, with nothing introduced or estimated
- Does every not-controllable cause carry evidence and a stated mitigation
- Is containment separated from the permanent fix
- Does every action have an owner, a date and a way to tell whether it worked
- Is the cost of the miss stated, or explicitly stated as unknown with someone named to size it
- Would a reader outside operations understand every sentence on one pass
- Does it fit on one page without dropping the corrective actions or the risks carried forward
- For anything customer-facing, is every date in it one that a person has actually committed to

## What this skill does not do

- It does not create the analysis. It presents work already done, so the numbers must be final before they arrive here.
- It does not commit a recovery date, a delivery date or a service level on your behalf. Dates come from whoever can deliver them.
- It does not accept, assign or deny liability, and it does not interpret a penalty clause. Those are contract and legal questions.
- It does not make a miss look smaller than it is. A brief that flatters works exactly once.
- It does not attribute a cause to a supplier, a team or a person without the evidence sitting in the source.
