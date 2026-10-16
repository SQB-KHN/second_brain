# Supplier Performance Scorecard

Turns purchase order and receipt data into a supplier scorecard covering OTIF, lead time variability, quality, price behaviour and dependency risk, plus the agenda for the review meeting.

---

## Who this is for

Anyone who has to sit across from a supplier and be specific: procurement and sourcing managers, purchase executives, vendor development engineers, supply chain managers, category managers, and founders managing their own supplier base.

## The problem it solves

Most supplier reviews run on two inputs: the buyer's memory, and the loudest recent failure.

That produces the wrong ranking every time. The supplier who quietly delivered late nine times looks better than the one who missed badly once, because only the second one caused a meeting. Meanwhile the supplier who is genuinely expensive to deal with, not because they are slow but because they are unpredictable, does not show up in any metric anyone tracks.

Building one by hand means pulling every PO line, matching receipts to promised dates, deciding what counts as late, and discovering the same supplier exists under three codes. Most teams do it once, for a presentation, and never again. This produces it from data you already have, the same way each quarter, so the trend means something.

---

## What you give it

**Minimum:** purchase order and receipt data for at least one full quarter, with item, supplier, order date, promised date, receipt date, quantity ordered and quantity received.

**Each of these changes the scorecard materially:**

| Extra data | What it unlocks |
|---|---|
| The **original** promised date, not just the latest revised one | Delivery metrics that mean anything at all. This is the single most important input |
| Incoming inspection or rejection data | A real quality score instead of none |
| Line value or item cost | OTIF by value alongside OTIF by line count, which often tell opposite stories |
| Category or criticality per supplier | Suppliers judged on the right scale, so stationery is not ranked against single-source components |
| Quoted lead time, and what the review is for | Quoted against actual, and weighting aimed at consolidation, a negotiation or a performance conversation |

**Handled automatically:** the same supplier appearing under several codes after a system migration, cancelled and closed-short lines, service POs with no meaningful receipt date, free-issue and intercompany lines, partial deliveries against one PO line, header rows, brackets for negatives and Indian digit grouping.

## What you get back

1. The two or three findings that need action, before the table
2. **Scorecard** with every component visible, sorted by the weighting chosen
3. Component detail per metric, so any number can be traced back
4. **Failure mode per underperformer**, naming specifically whether they are late, short, variable or rejecting
5. Lead time variability, called out separately with what it costs you in safety stock
6. **Dependency and single-source exposure**, counted and valued
7. Suppliers excluded for insufficient data, with their order counts
8. **Review agenda**: for each supplier, the evidence, the question to ask, and the outcome to ask for
9. The weights used, and any supplier codes merged

An Excel workbook with one sheet per supplier is offered at the end.

---

## The question that decides whether this works

**Is the promised date in your file the original commitment, or the latest revised one?**

If a supplier can call, move the date, and your system overwrites the old one, then every supplier scores near perfect and the scorecard is worse than useless, because it launders poor performance into good numbers.

It asks this first, every time. If only revised dates exist it still produces the scorecard, but states at the top what the number does and does not measure, so nobody carries it into a negotiation believing otherwise.

## Why variability matters more than the average

This is the finding most existing scorecards miss, and it usually changes a decision.

| Supplier | Mean lead time | Spread | Looks | Actually costs |
|---|---|---|---|---|
| A | 20 days | 2 days | Slower | Less. You can plan around 20 days |
| B | 14 days | 12 days | Faster | More. You have to hold stock for the bad case |

Safety stock is driven far more by the spread of lead time than by its average. Supplier B looks better on every dashboard and is more expensive to buy from, because the inventory you carry to absorb their unpredictability never appears on their scorecard.

Every mean in the output is reported with its spread beside it, and the implication is stated in words rather than left for you to infer.

## It will refuse to score some suppliers

A supplier with three orders has no performance record, only three anecdotes. Anyone below the minimum, default ten order lines in the period, goes into an **insufficient data** section with their counts rather than getting a score.

This matters commercially. Ranking a supplier on three orders is how a good supplier gets dropped and a bad one gets more business.

## What good output looks like

A strong scorecard names the failure rather than the supplier. "62 percent OTIF, and every miss is short quantity rather than late delivery, on four of our top ten items where this supplier is our only source." That is a conversation. "Poor performer" is not.

You should also find at least one supplier whose score is fine and whose dependency exposure is not. A well-performing single source is still a risk, and a scorecard that buries it under a good number has failed. If almost everyone scores above 95 percent, your file almost certainly holds revised promised dates, and that is the first thing to check.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill runs Python on your data and will not work without it.
2. Download this folder, or make a folder named `ops-supplier-scorecard` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the PO and receipt data and say what the review is for.

Examples that work:

- "Build the supplier scorecard from this. Quarterly vendor review next week."
- "Which of these suppliers are actually costing us money, not just delivering late?"
- "We want to consolidate from 40 vendors to 15. Score them and show me the single-source risk."
- "This supplier says their OTIF is 94 percent. Here is our data. Check it."

Saying whether the promised date is original or revised saves the first question and changes the whole output.

---

## How it protects accuracy

- Order lines per supplier are proved to sum to the total lines in the file
- OTIF is computed against the original promised date, or the output states plainly that only revised dates were available
- On time and in full are computed separately before being combined, because they are different failures with different fixes
- No supplier is scored below the stated minimum order count
- Every mean lead time is reported with its spread, never a mean alone
- Every composite score displays its components and weights so the number can be argued with, and merged supplier codes are listed rather than combined silently

## Limits worth knowing

- It does not blacklist, approve, terminate or select a supplier. It produces the evidence for that decision.
- It has no market data, so it will not tell you whether your prices are competitive. It tells you how they moved and whether the PO rate was honoured.
- It does not make claims about contractual breach or penalty entitlement. Those are contract and legal questions.
- It will not build a quality score where no quality data exists, however much a number is wanted.
- It reads your records. If receipts are booked late as a matter of habit, every supplier looks later than they were.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Everyone scores above 95 percent | File holds revised promised dates | Export the original commitment date. It states the limitation until you do. |
| A supplier appears two or three times | Multiple supplier codes after a migration | It proposes the merges and shows them. Confirm and rerun. |
| OTIF by line and by value disagree sharply | Misses are concentrated on high-value lines | That is the finding. The value figure is the one to take into the meeting. |
| Half your suppliers have no score | Below the minimum order count | Widen the period, or accept that they have no record yet. |
| No quality metrics | No inspection data supplied | It will not infer quality from delivery data. Supply rejection records. |

---

Part of the [Operations and Supply Chain skills](../README.md) in the [Claude Skills Library](../../README.md).
