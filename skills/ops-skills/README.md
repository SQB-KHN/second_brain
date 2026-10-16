# Operations and Supply Chain Skills for Claude

Five skills for the questions operations actually gets asked: what are we sitting on, did we pay what we agreed, who is letting us down, what should we buy, and why did we miss.

They run inside your own Claude account, on exports you already pull from your own systems. Nothing to install on your machine, nothing to connect, no coding.

---

## Who these are for

People who answer for physical movement and the money tied up in it: inventory and materials managers, demand and supply planners, procurement and purchase managers, warehouse and stores managers, logistics and dispatch managers, PPC executives, plant and operations managers, retail and multi-store ops, and founders running their own supply chain.

If your week involves an export, a spreadsheet, and a meeting where somebody senior asks why, these are built for it.

## The five skills

| Skill | Give it | Get back |
|---|---|---|
| **[Inventory Health and Working Capital](ops-inventory-health/ops-inventory-health-guide.md)** | A stock export, plus sales history | ABC-XYZ classification, dead and excess stock, expiry risk, shortage, and the cash tied up in each |
| **[Purchase and Freight Bill Audit](ops-bill-audit/ops-bill-audit-guide.md)** | Invoices, plus the PO and GRN or the rate card | A valued exception list, with recoverable separated from unverifiable |
| **[Supplier Performance Scorecard](ops-supplier-scorecard/ops-supplier-scorecard-guide.md)** | PO and receipt data, plus rejections if you have them | OTIF, lead time variability, quality, price behaviour, single-source risk, and the review agenda |
| **[Demand Forecast and Replenishment Plan](ops-demand-replenishment/ops-demand-replenishment-guide.md)** | Sales history, current stock, lead times | A reorder list with safety stock, reorder points, and every constraint applied visibly |
| **[Operations Review Brief](ops-review-brief/ops-review-brief-guide.md)** | Numbers you have already worked out | A one-page brief or escalation: committed against delivered, what it cost, actions with owners |

Each skill has its own guide with the exact inputs it needs, the phrasings that trigger it, what good output looks like, its limits, and a troubleshooting table.

## What is in the folder

```
ops-skills/
├── README.md                              ← this file
├── ops-inventory-health/
│   ├── SKILL.md                           ← the skill
│   └── ops-inventory-health-guide.md      ← how to use it
├── ops-bill-audit/
│   ├── SKILL.md
│   └── ops-bill-audit-guide.md
├── ops-supplier-scorecard/
│   ├── SKILL.md
│   └── ops-supplier-scorecard-guide.md
├── ops-demand-replenishment/
│   ├── SKILL.md
│   └── ops-demand-replenishment-guide.md
└── ops-review-brief/
    ├── SKILL.md
    └── ops-review-brief-guide.md
```

Every skill sits in its own folder. Inside, the file is always called `SKILL.md`, because that is the filename Claude looks for. Do not rename it. The guide beside it is named after the skill, so it stays identifiable once you have several downloaded.

---

## Why these five

Because these are the five things that fill an operations month, and each of them is done badly by default rather than by choice.

**Inventory health.** Everybody knows the stock total. Almost nobody can split it. A crore that turns eleven times a year and a crore holding forty lakh of 2024 stock look identical on the balance sheet, which is why the question keeps getting asked and never answered.

**Bill audit.** Bill passing is a signature at the end of a queue, done by somebody who has thirty invoices and an afternoon. The rate was agreed months ago by somebody else. Overcharges survive for years because nothing about them looks wrong, and freight is worse, since chargeable weight and slab boundaries and detention clocks are all contractual and almost never checked.

**Supplier scorecard.** Reviews run on the buyer's memory and the loudest recent failure, so the supplier who quietly delivered late nine times outranks the one who missed badly once. And the supplier who is genuinely expensive to buy from, because they are unpredictable rather than slow, appears on nobody's dashboard.

**Replenishment.** The most consequential document in operations and the one most often written from memory. Most of it runs on last month's sales, which is the one number guaranteed to understate demand for exactly the items that ran out.

**Review brief.** Operations is judged once a month by people who only saw the outcome. The instinct is to explain everything in the order it happened. The distance between a team that fixed the problem and a team that gets credit for fixing it is one page.

## They work together

Each stands alone. In sequence they cover an operations cycle:

```
Stock export        →  Inventory Health          →  what is working and what is stuck
Invoices plus PO    →  Purchase and Freight Audit →  what you overpaid, with the evidence
PO and receipts     →  Supplier Scorecard        →  who to talk to, and about what
History plus stock  →  Demand and Replenishment  →  what to buy, and what to stop buying
Any of the above    →  Operations Review Brief   →  the page the review actually reads
```

Three pairings worth knowing. Run inventory health before replenishment, so you stop buying what you already have too much of. Take the supplier scorecard's lead time variability straight into replenishment, because that spread is what sets your safety stock. And when the bill audit finds a pattern rather than a one-off, that belongs in the supplier scorecard as commercial behaviour, not filed as an accounts query.

---

## What makes these different from asking directly

**Nothing commits on your behalf.** No skill here places an order, confirms a delivery date, raises a debit note, or decides a safety, hazmat or customs classification. Every quantity, date and vendor call is a recommendation with its assumptions beside it, for a person to approve. Operations output spends real money and moves real stock, so the approval step is the point.

**They expect real exports.** Mixed units of measure in one quantity column. The same item under two codes after a migration. Negative stock from issuing before receipting. Zero-cost items that vanish from every value calculation. Batch rows needing aggregation. Blocked and in-transit stock counted as though it were sellable. This is where generic AI output falls over on the first real file.

**They will not guess at a unit of measure.** Pieces and boxes and kilograms in one column with no conversion is the largest source of wrong inventory analysis there is. The skill stops and asks rather than producing a confident answer that is wrong by a factor of twelve.

**They correct for what your history cannot show.** Sales records show what you sold, not what customers wanted. Every period an item was out of stock, demand was capped by supply, so a forecast built on it under-orders exactly the items that matter. That correction is made, stated, and its effect on each quantity is shown.

**Constraints are shown, never absorbed.** If you need 180 units and the minimum order quantity is 500, the answer is 500, and the output says so, states the cover that creates, and values the excess. A constraint that silently triples an order is how dead stock is born.

**Variability is reported alongside every average.** A supplier at 20 days with a 2 day spread is cheaper to hold stock against than one at 14 days with a 12 day spread. The second looks faster on every dashboard. Safety stock is driven by the spread, so the spread is never dropped.

**Nothing is lost quietly.** Excluded rows are stated with their quantity and value. Unmatched invoice lines appear as exceptions. Suppliers with too few orders go into an insufficient-data section rather than getting a made-up score. Silent loss looks finished and is wrong.

**Evidence is separated from what cannot be proved.** A recoverable overcharge has a rate card line behind it. An invoice with no goods receipt is a question for your stores team. They are totalled separately, because a combined number looks better than it is and collapses in the first vendor meeting.

**They refuse to score on noise.** A supplier with three orders has no performance record. Ranking one on three orders is how a good supplier gets dropped and a bad one gets more business.

---

## Getting started

1. Open Settings in Claude, go to **Capabilities**, and turn on **code execution and file creation**. Four of the five run Python on your files and will not work without it. The Operations Review Brief works without it.
2. Take one skill's folder and compress it to a `.zip`. The file inside must stay named `SKILL.md`, because that is what Claude looks for. The guide beside it is not needed and can be left out.
3. Go to **Customize**, then **Skills**, then add a skill and upload the zip.
4. Repeat for each skill you want.

Skills you upload stay private to your account. Once installed they work in Chat and Cowork, and Claude picks the right one from what you ask.

**Where to start.** Run the bill audit on three months of invoices you have already passed and paid. It is the fastest way to see whether this is worth your time, because it either finds money or it does not, and you will know within one run.

## Using them

Upload the export and describe the task the way you would to a colleague.

- "Here is our stock export and 12 months of sales. How much of this is dead?"
- "Three-way match these. PO file, GRN file, last month's vendor invoices."
- "Score these suppliers, quarterly review next week. Which ones are actually costing us money?"
- "Build this month's reorder list. 18 lakh budget, and here is what is already on order."
- "We committed 96 percent fill rate and hit 91. Write the review page."

Saying which file is which, and what period it covers, saves a round trip.

---

## What these will not do

- **Nothing orders, confirms or commits.** No purchase order is raised, no delivery date is confirmed, no debit note is issued, no vendor is contacted. You get the recommendation and the evidence.
- **No safety, hazmat or customs decisions.** HS codes, e-way bills, hazardous goods classification and food safety categorisation are flagged and handed to whoever owns them. They are never decided here.
- **No tax positions.** A bill audit reports what the invoice shows against what the PO says. It does not decide a rate, a head, or whether input credit can be claimed.
- **No write-offs.** Inventory health sizes the dead stock exposure and names the items. The write-off is an accounting and management decision.
- **No market benchmarks.** These skills have no industry data. They will not tell you whether your inventory days or your prices are competitive, and they will not invent a benchmark to fill the gap.
- **No contractual or legal claims.** Poor supplier performance is reported as evidence, not as breach. Penalty clauses are quoted, never interpreted.
- **No system access.** They work on exports you provide. They never connect to your ERP, WMS, TMS or any portal.

## What you need

- A Claude account, with code execution and file creation turned on for four of the five
- Your exports in Excel or CSV
- Nothing else. No installation, no terminal, no coding, nothing to connect

---

Part of the [Claude Skills Library](../README.md).
