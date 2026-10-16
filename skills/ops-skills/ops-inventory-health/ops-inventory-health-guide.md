# Inventory Health and Working Capital

Turns a stock export into ABC-XYZ classification, dead and excess stock, expiry risk, shortage, and the cash tied up in each.

---

## Who this is for

Anyone answerable for what is sitting in the warehouse: inventory and materials managers, stores and warehouse managers, supply chain and demand planners, procurement managers, retail and multi-store operations managers, and founders holding their own D2C stock.

If somebody senior asks how much stock you are carrying and why, this is built for that conversation.

## The problem it solves

Everybody knows the inventory total. Almost nobody can split it.

The split is the whole job. A crore of stock turning eleven times a year is a working business. A crore that includes forty lakh last issued in 2024 is a working business plus forty lakh of a decision nobody has made. From the balance sheet the two look identical, which is why the question keeps getting asked and never answered.

Doing it by hand means classifying a few thousand item codes on value, then again on variability, then ageing them, then reconciling the four overlapping definitions of "slow moving" that three departments each use differently. Two to three days, and stale the week after. This produces it in one pass, and the same way every month, so the numbers are comparable.

---

## What you give it

**Minimum:** a stock export with item code, quantity on hand, and either unit cost or stock value.

**Each of these changes the output materially:**

| Extra data | What it unlocks |
|---|---|
| Twelve months of sales or consumption history | ABC and XYZ classification, dead and excess, and the run rate everything else rests on |
| Lead time per item or supplier | Shortage detection, since cover means nothing except against lead time |
| Last movement or last receipt date | Ageing buckets, which is where dead stock actually surfaces |
| Shelf life or expiry dates | Expiry risk by month, and the value that will expire unsold |
| Stock status flags: free, blocked, QC hold, in transit | The available against not-available split, which is frequently the finding itself |
| Multiple locations | Excess in one warehouse against shortage in another, a transfer rather than a purchase |

**Handled automatically:** header rows that do not start on row 1, brackets for negatives, Indian digit grouping such as 12,34,567, batch and serial rows needing aggregation, negative stock from issue-before-receipt, zero-cost items, and the same item under two codes. The one thing it will stop and ask about is mixed units of measure in a single quantity column. Pieces and boxes and kilograms together with no conversion is the largest source of wrong inventory analysis there is, and it will not guess.

## What you get back

1. Total stock value, split into available and not available
2. **ABC-XYZ matrix**, count and value per cell, with the expensive cells called out
3. Ageing table by value, not by item count
4. **Dead, excess, shortage and expiry risk**, one table each, sorted by value with the largest items named
5. Working capital view: inventory days, turns by class, and the cash a reduction would release
6. The concentration, stated in one sentence
7. Data quality and exclusions, each with its value
8. The decisions this needs from you

An Excel version with one sheet per condition is offered at the end.

---

## Why it classifies twice

**ABC sorts on value**, so it tells you where the money is. **XYZ sorts on variability**, so it tells you how predictable demand is. Neither is useful alone, and most inventory reports stop at the first. The cross is where it earns its place:

| | X, stable | Y, variable | Z, erratic |
|---|---|---|---|
| **A, high value** | Tight control, low safety stock | Watch closely | **Where money is lost** |
| **B** | Standard rules | Standard rules | Review individually |
| **C, low value** | Simple min-max | Simple min-max | **Stop stocking, make to order** |

AZ items are expensive and unpredictable, and are almost always managed with the same rule as everything else. CZ items are cheap, erratic, and quietly consume more attention than their value justifies.

## The four conditions, and why they stay separate

Most reports produce one "slow moving" list. That list is useless, because it mixes four problems with four different owners.

| Condition | What it means | Who acts |
|---|---|---|
| **Dead** | No movement in the stated window | Management. A write-off or liquidation decision, not a calculation |
| **Excess** | Moving, but far more than the run rate needs | Planning. Stop buying, and decide what to do with the surplus |
| **Shortage** | Cover below reorder point or lead time | Procurement. The one that stops a line today |
| **Expiry risk** | Shelf life shorter than the time needed to consume it | Sales. Discount and move it, or lose the value entirely |

An item can be both excess and at expiry risk. It appears in both lists rather than being filed under one and lost.

## What good output looks like

A strong result names where the money is stuck in one sentence: "62 percent of dead stock value sits in 11 item codes, all in the electrical category, none issued since March." That sentence is what gets acted on. The four thousand row table under it is evidence, not the finding.

You should also see a gap between total stock and available stock that you did not expect. Blocked, in-transit and QC-hold stock counted as though it were sellable is one of the most common reasons a well-stocked business still misses orders.

If everything comes back healthy, check whether consumption history was supplied. Without it there is no run rate, so nothing can be called dead or excess, and the output collapses to an ageing table.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill runs Python on your file and will not work without it.
2. Download this folder, or make a folder named `ops-inventory-health` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the stock export and say what you are trying to find out.

Examples that work:

- "Here is our stock export and twelve months of sales. How much of this is dead?"
- "Finance wants inventory days down by 15. Where is the cash actually sitting?"
- "Stock across three warehouses. Show me what I can transfer instead of buying."
- "Run ABC-XYZ on this and tell me what we should stop stocking altogether."

Supplying your own dead stock definition and cover target saves a round trip and produces numbers your management already recognises.

---

## How it protects accuracy

- Available and not-available stock are separated before any metric is computed, so restricted stock is never counted as sellable
- Every classification, day count and ratio runs in code, never worked out inside a sentence
- Ageing buckets are proved to sum to total stock value
- Excluded rows are reported with their quantity and value. Negative stock, zero-cost items and unit conflicts are quarantined visibly, not dropped
- Duplicate item codes are proposed and shown, never merged on its own judgement, and carrying cost and cover targets are labelled as assumptions rather than benchmarks

## Limits worth knowing

- It does not write off or provision anything. It sizes the exposure and names the items; the decision stays with management and finance.
- It does not set reorder quantities or place orders. Pair it with the replenishment skill for that.
- It has no industry data, so it will not tell you whether your inventory days are good. It tells you what they are and where they come from.
- It reads the export. It cannot check the physical count, so a file that disagrees with the shelf produces a confident analysis of the wrong quantity.
- It does not value stock for statutory, audit or tax purposes.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It refuses to compute quantities | Mixed units of measure in one column | Supply the conversion, or re-export with a UOM column. It will not guess. |
| Nothing shows as dead or excess | No consumption history supplied | Add twelve months of sales or issues. Without a run rate neither can be calculated. |
| Values do not match your system | Quantity and value columns disagree, meaning stale unit cost | It reports which it used. Re-export with current costs. |
| Too much stock shows as unavailable | Blocked, QC and in-transit stock sitting in the file | That is usually the finding. Check why it is being held. |
| One item appears twice | Two codes for one item, common after a migration | It proposes the merge and shows it. Confirm and rerun. |

---

Part of the [Operations and Supply Chain skills](../README.md) in the [Claude Skills Library](../../README.md).
