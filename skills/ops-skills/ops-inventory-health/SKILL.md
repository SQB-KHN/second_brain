---
name: ops-inventory-health
description: Turn a stock export into ABC-XYZ classification, dead and excess stock, expiry risk, shortage and the cash tied up. Use for inventory review, dead stock, stock ageing or working capital.
---

# Inventory Health and Working Capital

Inventory is usually the largest number on the balance sheet and the least understood line in the business. Everybody knows the total. Almost nobody can say which part of it is working and which part is money that stopped moving eighteen months ago. This skill splits the total into things you can act on.

## When to use this

Trigger on: inventory analysis, dead stock, slow moving, stock review, ABC analysis, inventory days, working capital tied up in stock, excess and obsolete, E&O, stock ageing, "how much stock are we sitting on", inventory reduction target.

## Before you start

Required: a stock export with item code, quantity on hand, and either unit cost or stock value.

Ask, briefly, only what you cannot infer:
1. Sales or consumption history, and how much of it. Twelve months separates seasonal from dead. Three months cannot.
2. Lead time, per item or per supplier. Coverage means nothing except against lead time.
3. Whether stock sits across several locations, and whether transfers between them are practical. Excess in Bhiwandi and a stockout in Hosur is a different problem from a real shortage.
4. Shelf life or expiry dates, where the product has them.
5. Their own definition of dead stock, if they have one. Companies differ, and their number is the one their management already uses.

If only the stock file exists, produce the ageing and concentration view, and say what consumption history would add. Do not stall.

## Workflow

### 1. Profile the export before touching it

Inventory exports carry traps that are specific to them, and each one produces a confidently wrong answer:

- **Mixed units of measure in one quantity column.** Pieces, boxes, kilograms and cartons in the same column with no conversion. This is the single largest source of wrong inventory analysis. Ask for the conversion, or quarantine the affected rows and say so.
- **The same item under two codes**, from a system migration or two people creating masters. It splits one item's history into two thin ones and hides both excess and shortage.
- **Quantity and value columns that do not agree.** Usually means the unit cost is stale. Say which you trusted and why.
- **Negative stock.** A system artefact of issuing before receipting, never a real quantity. Quarantine it and report the count.
- **Zero-cost or blank-cost items**, which silently vanish from every value calculation while still occupying the count.
- **Batch or serial rows** that must be aggregated to item level before anything else.
- Header row position, brackets for negatives, Indian digit grouping such as 12,34,567.

State row count, total quantity, total value, and the value you had to exclude, before showing any analysis.

### 2. Compute in code, never in prose

Every classification, every day count, every ratio runs as Python. Nothing arithmetic is worked out inside a sentence.

### 3. Establish what is actually available, first

Free stock is not total stock, and conflating them is why a company with plenty of inventory still misses orders. Separate and report both:

- **Available:** free, unrestricted, sellable or issuable
- **Not available:** in transit, quality hold, blocked, damaged, reserved against a confirmed order, or consignment stock the supplier still owns

Every metric below uses available stock. The gap between the two totals is frequently the finding on its own.

### 4. Classify twice, on value and on movement

**ABC on annual consumption value.** A is the top 80 percent of value, B the next 15, C the last 5. State the cut you used.

**XYZ on demand variability**, using the coefficient of variation of period demand. X is stable, Y is variable, Z is erratic or intermittent.

The cross is what makes this useful rather than decorative:

- **AX** items justify tight control and can run on low safety stock
- **AZ** items are where money is lost. High value, unpredictable, and usually managed with the same rule as everything else
- **CZ** items are candidates for making or buying to order rather than stocking at all

### 5. Age the stock and report value, not count

Buckets: 0 to 30, 31 to 60, 61 to 90, 91 to 180, 181 to 365, and over 365 days. Age from last receipt where lot data exists, otherwise from last movement, and say which.

Report value per bucket. A thousand old C items matter less than four old A items, and a count-based ageing table hides exactly that.

### 6. Separate the four conditions, because the remedies differ

- **Dead.** No issue or sale in the stated window, default 365 days. The remedy is liquidation, disposal or write-off, and every one of those is a decision, not a calculation.
- **Excess.** Moving, but on-hand quantity exceeds what the observed run rate consumes in a stated horizon. Report the excess quantity, its value, and the months of cover it represents.
- **Shortage.** Cover below reorder point, or below lead time. This is the one that stops a line or loses an order.
- **At expiry risk.** Shelf life remaining is shorter than the time the run rate needs to consume the quantity held. Report what will expire unsold, by value, by month.

An item can be both excess and at expiry risk. Report it in both and say so, rather than choosing one and losing the other.

### 7. Build the working capital view

- **Inventory days**, and state the cost of goods sold basis used
- **Turns overall and turns by ABC class.** A blended turns figure conceals everything worth knowing
- **Value of stock above the stated cover target**, which is the cash a reduction would actually release
- **Carrying cost of dead and excess**, at a stated rate, labelled as an assumption the user should replace with their own

Never present a carrying-cost percentage or a turns figure as an industry benchmark. You do not have industry data.

### 8. Find the concentration and say it in one sentence

"62 percent of dead stock value sits in 11 item codes, all in the electrical category, none issued since March" is worth more than a four thousand row table. Lead with that sentence.

## Output format

**1. Headline.** Total stock value, available against not available, and the value that is dead or excess.

**2. Availability split.** With the reason each restricted category is held.

**3. ABC-XYZ matrix.** Count and value per cell, with the AZ and CZ cells called out.

**4. Ageing table.**

| Bucket | Items | Quantity | Value | % of total value |

**5. The four conditions.** Dead, excess, shortage, expiry risk. One table each, sorted by value, with the largest items named.

**6. Working capital view.** Days, turns by class, releasable cash, carrying cost with its assumed rate.

**7. Concentration.** Where the money is stuck, and what it points at.

**8. Data quality and exclusions.** Unit of measure conflicts, zero-cost items, duplicate codes, negative stock, each with its quantity and value.

**9. Decisions this needs from you.** The write-off calls, the transfer calls, the items where only the business knows whether demand is coming back.

Offer the Excel version with one sheet per condition. Build it only if asked.

## Checks to run before delivering

- Available plus not available equals the total, and matches the file's own total where it states one
- Every item falls in exactly one ABC class and exactly one XYZ class
- Ageing buckets sum to total stock value
- No item appears in two mutually exclusive conditions, and items that are legitimately both excess and at expiry risk are flagged as such
- Excluded rows are stated with their quantity and value, never dropped silently
- Inventory days states its cost of goods sold basis
- Every day count and ratio was computed in code

## What this skill does not do

- It does not write off, provision or dispose of anything. It sizes the exposure and names the items; the write-off is an accounting and management decision.
- It does not set reorder quantities or place orders. That is the replenishment skill.
- It does not choose your carrying cost, cover target or service level. It uses what you give it and labels every default.
- It does not value inventory for statutory, audit or tax purposes.
- It reads the export it is given. A file that mixes units of measure will produce wrong answers unless the conversion is supplied, and it will say so rather than guessing.
