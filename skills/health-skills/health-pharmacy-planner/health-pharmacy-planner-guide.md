# Pharmacy and Consumables Planner

Turns a batch-level stock export into an expiry ladder built around supplier return windows, stockout risk weighted by clinical criticality, and a reorder list capped by shelf life.

---

## Who this is for

Anyone accountable for what is on the shelf: hospital and retail pharmacists, pharmacy managers, nursing store and theatre store in-charges, materials and purchase managers in healthcare, clinic managers, and owners of standalone pharmacies.

## The problem it solves

Pharmacy loss is quiet. Nothing breaks when a batch expires. The value simply leaves, a strip at a time, and surfaces as a write-off six months later with nobody's name attached to it.

Meanwhile the one item somebody actually needed was out of stock at two in the morning.

Both failures come from the same gap. Planning is done at item level on a problem that lives at batch level. An item with comfortable total stock can have most of it expiring next month, and no item-level report will show you that. And the item whose only remaining stock is a batch expiring inside the lead time is already a stockout, dressed up as healthy cover.

The third loss is ordering. A year of cover bought on a nine-month shelf life creates the next write-off at the moment of purchase, and nobody notices until the dates arrive. This works at batch level, orders the actions by what recovers most value, and caps every order at what can actually be consumed.

---

## What you give it

**Minimum:** a stock export at batch level, with item, batch, quantity, expiry date, and unit cost or value.

| Extra data | What it unlocks |
|---|---|
| Six to twelve months of consumption or issues | Turns expiry from a date list into a decision list, because it says what will actually get used |
| **Supplier return terms and the window** | The difference between a return and a write-off. The highest-value input here by a wide margin |
| **Your essential or emergency item list** | Criticality weighting, so a cheap vital item outranks an expensive optional one |
| Lead time by supplier, plus cold chain and controlled flags | Placeable recommendations, and both categories reported separately since handling and rules differ |

**Handled automatically:** expiry held as text or as month and year only, batches already expired still sitting on the file, the same molecule and strength under several codes as different pack forms, zero-cost items, negative stock from issue before receipt, header rows, brackets and Indian digit grouping.

Stock files usually carry no patient data. Prescription-linked issue files do, and it checks, saying once that planning needs item, batch and quantity rather than who received it.

## What you get back

1. Headline: total value, value expiring inside 90 and 180 days, value still returnable, and the vital-item shortfall count
2. **The expiry ladder**, with the value on each rung and the date each rung closes
3. **Return window closing**, dated, soonest first. The most time-critical section in the output
4. Already expired, separated from risk and sized as a write-off
5. **Stockout risk**, vital and essential first, with batch-expiry-inside-lead-time cases marked
6. ABC-VED matrix, count and value per cell
7. **Reorder list** with the constraint applied and the shelf-life cap shown per line
8. Stop stocking, with the reason per item
9. Controlled and cold chain items, reported separately
10. Data quality and exclusions

An Excel version with one sheet per section is offered at the end.

---

## Value is the wrong lens on its own

ABC sorts on consumption value and tells you where the money is. **VED sorts on criticality**, and in healthcare that matters more.

| | Vital | Essential | Desirable |
|---|---|---|---|
| **A, high value** | Tight control, high service level | Watch closely | Where you can accept risk |
| **B** | High service level | Standard rules | Standard rules |
| **C, low value** | **High service level anyway** | Standard rules | Candidate to stop stocking |

The bottom-left cell is the point. A cheap vital item deserves a buffer that makes no sense on value grounds at all, because the consequence of running out is clinical rather than financial, and every ABC-only plan gets this wrong. If you have no VED list it proposes one from your essential and emergency list plus item type, shows it, and waits. It will not assign criticality silently, because that classification decides what runs out.

## The expiry ladder, in the order that saves money

Most near-expiry handling jumps straight to discounting. That is the wrong rung.

| Rung | Action | Why the order matters |
|---|---|---|
| Will be consumed | None | Cover is shorter than shelf life remaining |
| **Returnable now** | Return to supplier | Recovers most of the value. Always the first action |
| **Return window closing** | Return before the date shown | The rung where doing nothing costs the entire value |
| Past return, transferable | Move to a location that will use it | Recovers full value if consumption exists there |
| Past return, discountable | Discount where item and setting allow | Recovers a fraction |
| Write-off | Size it and report it | Nothing left to do |

The "return window closing" section is the one to read first. Every other rung can wait a week. That one cannot.

## What good output looks like

A strong result gives you a dated action list, not a risk report: "4.2 lakh returnable now across 31 batches, and a further 1.8 lakh where the return window shuts before the 20th."

The stockout section should surprise you at least once, with an item showing healthy cover whose only stock is a batch expiring inside the lead time. That is the failure that catches experienced pharmacists, and it is invisible without batch-level analysis. If nothing shows as returnable, check whether you supplied the return terms; without them the skill cannot tell a returnable batch from a write-off, and the ladder collapses into a date list.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill runs Python on your export and will not work without it.
2. Download this folder, or make a folder named `health-pharmacy-planner` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the batch-level stock export and say what you are planning.

Examples that work:

- "What is expiring in the next six months, and what can still go back to the supplier?"
- "Here is the stock and six months of issues. Build the monthly indent."
- "Which of our crash cart and emergency items are short?"
- "Stock across the main pharmacy and two ward stores. What can I transfer instead of ordering?"

Supplying the supplier return terms is the single most valuable thing you can add.

---

## How it protects accuracy

- Expiry is computed at batch level before anything is aggregated to item, which is the whole point
- Every batch sits on exactly one rung, and rung values are proved to sum to total stock value
- Already-expired stock is excluded from risk and reported separately, so a write-off is never presented as an opportunity
- No reorder quantity exceeds what can be consumed inside that item's shelf life
- Vital and essential shortfalls are listed before higher-value optional ones
- Items already on order are netted off every recommendation, and where expiry carries only a month and year it assumes the last day and says so

## Limits worth knowing

- It does not substitute one drug for another, suggest a therapeutic alternative, or comment on interactions, dosing or clinical suitability. It plans stock, not therapy.
- It does not recommend a disposal or destruction route for expired or controlled items. Those are governed by regulation and by your institution's procedure.
- It does not decide your VED classification, and it does not place an order or raise an indent.
- It reads the export. It cannot check the physical shelf, and a file that disagrees with reality produces a confident plan for the wrong stock.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Nothing shows as returnable | Supplier return terms not supplied | Provide the window. Without it a returnable batch looks like a write-off. |
| Expiry risk looks low | File aggregated to item level, not batch | Re-export at batch level. Item level hides this entirely. |
| An item flagged short with good cover | Its only stock expires inside the lead time | That is the finding, and it is the one most often missed. |
| Reorder quantities smaller than expected | Capped by shelf life | Deliberate. The cap is shown per line with the reason. |
| Same medicine appears twice | Two codes for different pack forms | It proposes the merge and shows it. Confirm and rerun. |

---

Part of the [Healthcare skills](../README.md) in the [Claude Skills Library](../../README.md).
