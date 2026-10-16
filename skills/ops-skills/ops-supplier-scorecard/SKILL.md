---
name: ops-supplier-scorecard
description: Turn PO and receipt data into a supplier scorecard on OTIF, lead time variability, quality, price and dependency risk. Use for vendor reviews, supplier performance or consolidation.
---

# Supplier Performance Scorecard

Most supplier reviews run on two inputs: the buyer's memory, and the loudest recent failure. So the supplier who quietly delivered late nine times looks better than the one who missed badly once. A scorecard fixes that, but only if it measures against what was originally committed rather than what was later renegotiated.

## When to use this

Trigger on: supplier scorecard, vendor performance, vendor review, OTIF, on time in full, supplier rating, vendor evaluation, supplier QBR, supplier consolidation, "which vendors are letting us down", single source risk.

## Before you start

Required: purchase order and receipt data covering at least one full quarter, with item, supplier, order date, promised date, receipt date, quantity ordered and quantity received.

Ask, briefly:
1. **Whether the promised date in the file is the original commitment or the latest revised one.** This is the most important question in this skill. If a supplier can move the date and the system keeps only the newest, every supplier scores near perfect and the scorecard is worthless. Ask explicitly. If only revised dates exist, say clearly what the number does and does not measure.
2. Quality data, if it exists. Incoming inspection results, rejections, returns, complaints.
3. Their tolerance for early delivery. Early is not free; it consumes cash and space, and many companies treat significantly early as a miss.
4. What the scorecard is for: a review meeting, a consolidation decision, or a rate negotiation. Each needs different weighting.
5. Category or criticality per supplier, if they have it. A stationery supplier and a single-source component supplier should not be judged on one scale.

## Workflow

### 1. Profile the data and establish the population

- **One row per PO line, or per receipt?** Partial deliveries mean one line has several receipts, and this decides how on-time-in-full can be computed at all.
- **Goods mixed with services.** Service POs rarely carry meaningful receipt dates and will distort every delivery metric. Separate them out.
- **The same supplier under several codes.** Extremely common after a system migration, and it splits one supplier's record into two mediocre ones. Propose the merges, show them, and wait.
- **Cancelled and closed-short lines.** A cancelled line is not a late delivery.
- **Free-issue, intercompany and consignment lines**, which follow different rules and should not be scored alongside bought-out supply.

State order count, line count and value per supplier before scoring anything.

### 2. Compute in code, never in prose

Every percentage, every day count, every mean and every standard deviation runs as Python. Lead time variability in particular cannot be eyeballed, and a scorecard that reaches a supplier review with a wrong number in it does not get a second hearing.

### 3. Set a minimum before you score anyone

A supplier with three orders has no performance record, only three anecdotes. State a minimum, default ten order lines in the period, and put everyone below it into an **insufficient data** section with their counts rather than a score.

Ranking a supplier on three orders is how a good supplier gets dropped and a bad one gets more business.

### 4. Measure delivery against the original commitment

- **On time.** Received within the agreed window against the original promised date. State the window used.
- **In full.** Quantity received against quantity ordered on that line, within the receipt tolerance.
- **OTIF.** Both, on the same line. Report it as a percentage of lines **and** as a percentage of value, because a supplier can be 90 percent on lines and 40 percent on value if the misses are all on the big ones.
- **Late by how much.** Average and worst case, in days. A supplier averaging two days late needs a scheduling adjustment. One averaging two days with a worst case of forty has an entirely different problem, and the average conceals it.
- **Early deliveries**, counted and stated rather than silently treated as good news.

Report the split between on-time-but-short and in-full-but-late. They are different failures with different fixes, and a blended OTIF number hides which one you have.

### 5. Measure lead time variability, and say why it matters more than the mean

- Quoted lead time against actual
- Mean actual lead time
- Standard deviation of actual lead time, and the 90th percentile

The spread is the number that costs money. Safety stock is driven far more by the variability of lead time than by its average, so a supplier at 20 days with a 2 day spread is cheaper to hold stock against than one at 14 days with a 12 day spread, even though the second looks faster on every dashboard.

Say this explicitly in the output. It is usually the finding that changes a decision, and it is almost never on the scorecard people already have.

### 6. Measure quality only where the data supports it

- Rejection rate at incoming inspection, by lines and by quantity
- Returns after acceptance, which cost more and are frequently not attributed back to the supplier
- Repeat rejections of the same item, which distinguish a bad batch from a bad process

If no quality data exists, say so plainly. Do not construct a quality score out of delivery data.

### 7. Measure price and commercial behaviour

- Price paid against PO rate. This should be zero, and it is a finding when it is not.
- Price movement over the period, per item, against the previous rate
- Whether agreed slab or volume pricing was actually honoured

Do not benchmark against market rates. You have no market data, and an invented benchmark is worse than none because it gets quoted in a negotiation.

### 8. Name the dependency risk separately

This is not a performance measure, and it usually matters more than one:

- Share of category spend per supplier
- **Single-source items, counted and valued.** This is the number every management team asks for and few procurement teams have ready.
- Suppliers who are both high spend and poor performing, which is the quadrant that needs action this quarter

A well-performing single source is still a risk. Say so, rather than letting a good score bury it.

### 9. Score last, and show the weights

Combine into an overall score only after every component is visible. State the weights used, and state that they are a choice rather than a standard. If the user named a purpose in step 4, weight toward it and say you did.

Never present a composite score without its components beside it. A single number invites an argument nobody can settle, because nobody can see what produced it.

## Output format

**1. Headline.** Suppliers scored, suppliers excluded for insufficient data, and the two or three findings that need action.

**2. Scorecard.**

| Supplier | Lines | Value | OTIF % lines | OTIF % value | Avg days late | Worst case | Lead time mean | Lead time spread | Rejection % | Price variance | Score |

**3. Component detail.** Each metric in its own short table, so any number can be traced back.

**4. Failure mode per underperformer.** One line each: specifically whether they are late, short, variable or rejecting. "Poor performance" is not a finding.

**5. Lead time variability.** Called out separately, with what it implies for the safety stock you have to carry.

**6. Dependency and single-source exposure.** Counted and valued.

**7. Insufficient data.** Suppliers listed with their order counts.

**8. Review agenda.** For each supplier needing a conversation: the evidence, the specific question to ask, and the outcome to ask for.

**9. Weights used, and data quality notes.** Including any supplier codes merged.

Offer the Excel workbook with one sheet per supplier. Build it only if asked.

## Checks to run before delivering

- Order lines per supplier sum to the total lines in the file
- OTIF is computed against the original promised date, or the output states plainly that only revised dates were available
- No supplier is scored below the stated minimum order count
- On time and in full are computed separately before being combined
- Lead time spread is reported alongside every mean, never a mean alone
- Every composite score displays its components and its weights
- Merged supplier codes are listed, and nothing was merged without being shown first

## What this skill does not do

- It does not blacklist, approve, terminate or select a supplier. It produces the evidence for that decision.
- It does not benchmark your suppliers against the market or against other companies. It has no market data and will not invent any.
- It does not make a claim about contractual breach or penalty entitlement. That is a contract and legal question.
- It does not score a supplier on too few orders, however much a number is wanted.
- It does not build a quality score where no quality data exists.
