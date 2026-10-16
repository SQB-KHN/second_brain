---
name: health-pharmacy-planner
description: Turn a batch-level stock export into expiry risk, supplier return windows, stockout risk weighted by criticality, and a reorder list. Use for pharmacy or consumables planning.
---

# Pharmacy and Consumables Planner

Pharmacy loss is quiet. Nothing breaks when a batch expires. The value simply leaves, a strip at a time, and surfaces as a write-off six months later with nobody's name on it. Meanwhile the one item somebody actually needed was out of stock at two in the morning. Both failures come from the same gap: planning done at item level on a problem that lives at batch level.

## When to use this

Trigger on: pharmacy stock, expiry, near expiry, batch expiry, dead stock, drug reorder, indent, consumables planning, return to supplier, stock write-off, VED analysis, crash cart stock, "what is expiring", "what do we need to order".

## Before you start

Required: a stock export at batch level, with item, batch, quantity, expiry date, and unit cost or value.

Ask, briefly:
1. Consumption or issue history, and how much. Six to twelve months turns expiry from a date list into a decision list, because it says what will actually get used.
2. **Supplier return terms.** Most suppliers accept near-expiry returns inside a contractual window, commonly some months before expiry. That window is the whole difference between a return and a write-off, and it is the highest-value input here.
3. Their essential or emergency item list, however informal. Crash cart, emergency drugs, theatre must-stock. A stockout here is a different class of problem from a stockout anywhere else.
4. Whether controlled or scheduled substances are in the file, and whether they should be reported separately. They usually should.
5. Cold chain items, where the file flags them.
6. Lead time by supplier, and the indent or order day.

## Check for patient identifiers first

Stock files usually carry none. Prescription-linked issue files do. Check, and if any are present say once that planning needs item, batch and quantity rather than who received it, then continue with whatever they choose.

## Workflow

### 1. Profile at batch level, and do not aggregate yet

- **Compute expiry at batch level before aggregating anything to item.** An item with comfortable total stock can still have most of it expiring next month, and item-level aggregation hides precisely that.
- **The same molecule and strength under several codes**, as different pack forms. A strip of ten and a box of a hundred held as separate items splits one consumption history into two thin ones.
- **Expiry held as text**, or as month and year only. Where only a month is given, treat it as the last day of that month and say so.
- **Batches already expired** and still on the file. Those are a write-off, not a risk, and belong on their own line.
- Zero-cost items, negative stock from issue before receipt, header rows, brackets, Indian digit grouping.

State item count, batch count, total value, and the value excluded.

### 2. Compute in code, never in prose

### 3. Classify on VED alongside ABC, because value alone is the wrong lens here

**ABC sorts on consumption value** and tells you where the money is. **VED sorts on criticality:** Vital, where a stockout has an immediate clinical consequence; Essential, where it disrupts care; Desirable, where it is an inconvenience.

The cross is what makes the plan defensible. A cheap vital item deserves a service level and a buffer that make no sense on value grounds at all, and that is exactly the point. A high-value desirable item is where you accept the risk instead.

If no VED list exists, propose one from the essential and emergency list plus item type, show it, and wait for confirmation. Never assign criticality silently. That classification decides what runs out.

### 4. Work the expiry ladder, and put the return window before the discount

This ordering is what saves the money, and it is usually done in the wrong sequence. For every batch, compute months to expiry and months of cover at the current run rate, then place it on a rung:

- **Will be consumed.** Cover shorter than shelf life remaining. No action.
- **Returnable now.** Inside the supplier's return window. This is always the first action, because a return recovers most of the value and a discount recovers a fraction of it.
- **Return window closing.** Approaching the window, with the date it shuts. **This is the most valuable single section in the output**, because it is the one where doing nothing costs the entire value.
- **Past return, transferable.** Another location can consume it inside its remaining shelf life.
- **Past return, discountable.** Where the item and the setting allow it.
- **Write-off.** Nothing left to do. Size it and report it rather than leaving it in the risk column.

Report the value on each rung, and the date each rung closes.

### 5. Find stockout risk, weighted by criticality rather than value

- Cover below lead time, which is a stockout already in motion
- **Vital and Essential items with any shortfall, listed first regardless of value**
- Items at zero with recorded consumption
- **Items whose only stock is a batch expiring inside the lead time.** This is a stockout in disguise, and it is invisible in every item-level report. It is the one that catches experienced pharmacists.

### 6. Build the reorder list with constraints applied visibly

- Reorder point from consumption over lead time, plus a buffer set by VED class
- **Cap every order at what can be consumed inside the item's shelf life.** Ordering a year of cover on a nine-month shelf life creates the next write-off, and this is the commonest self-inflicted loss in pharmacy.
- Apply minimum order quantity and pack size, and show where each changed the number and what excess it created
- Net off what is already on order
- Respect the supplier's indent day, so the recommendation can actually be placed
- Flag cold chain items separately, since handling and loss risk both differ

### 7. Report controlled substances separately

Where scheduled or controlled items are present, report them in their own section with quantities and batches. State that their movement, register and disposal are governed by regulation and by the institution's own procedure.

Do not recommend a disposal route, a destruction method or a register entry. Those are not planning decisions.

### 8. Say what to stop stocking

Items with no consumption in the period, items whose pack size guarantees expiry at the current run rate, and duplicate formulations of the same molecule and strength held under different codes.

Pharmacy grows by accretion. Things get added and nothing gets removed, so this section is usually longer than anyone expects.

## Output format

**1. Headline.** Total stock value, value expiring inside 90 and 180 days, value still returnable, and the vital-item shortfall count.

**2. Expiry ladder.**

| Rung | Items | Batches | Value | Action | Date this closes |

**3. Return window closing.** Dated, soonest first. The most time-critical section in the output.

**4. Already expired.** Separated from risk and sized as a write-off.

**5. Stockout risk.** Vital and Essential first, then by value, with batch-expiry-inside-lead-time cases marked.

**6. ABC-VED matrix.** Count and value per cell.

**7. Reorder list.**

| Item | VED | Cover | On order | Suggested | Constraint applied | Shelf-life cap | Value |

**8. Stop stocking.** With the reason per item.

**9. Controlled and cold chain.** Reported separately.

**10. Data quality and exclusions.** Each with its quantity and value.

Offer the Excel version with one sheet per section. Build it only if asked.

## Checks to run before delivering

- Expiry is computed at batch level before any aggregation to item
- Every batch sits on exactly one rung of the expiry ladder
- Ladder values sum to total stock value, with will-be-consumed as the balancing rung
- Already-expired stock is excluded from risk and reported separately with its value
- No reorder quantity exceeds what can be consumed inside that item's shelf life
- Vital and Essential shortfalls appear before higher-value Desirable ones
- Return windows are computed from the terms supplied, and the output says so where no terms were given
- Items already on order are netted off every recommendation
- Excluded rows are stated with their quantity and value

## What this skill does not do

- It does not substitute one drug for another, suggest a therapeutic alternative, or comment on interactions, dosing or clinical suitability. It plans stock, not therapy.
- It does not recommend a disposal or destruction route for expired or controlled items. Those are governed by regulation and by your institution's procedure.
- It does not decide your VED classification. It proposes one and waits for a pharmacist to confirm it.
- It does not place an order or raise an indent.
- It reads the export. Where expiry carries only a month and year it assumes the last day of that month, and says so.
