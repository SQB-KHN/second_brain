# Finance Skills for Claude

Five skills that do the mechanical half of a finance month, so you keep the half that needs judgement.

They run inside your own Claude account, on files you export from your own systems. Nothing to install on your computer, nothing to connect, no coding.

---

## Who these are for

Finance professionals who do this work every month: FP&A analysts, management accountants, finance business partners, controllers, accountants in practice, and finance leads at startups and SMEs who run the whole function themselves.

If you close books, explain variances, reconcile anything, build an MIS pack, forecast cash, or present numbers to someone above you, these are built for your calendar.

---

## The five skills

| Skill | Give it | Get back |
|---|---|---|
| **[Variance Commentary](finance-variance-commentary/finance-variance-commentary-guide.md)** | A P&L, TB or cost centre report with actual and comparative columns | A ranked variance table plus written commentary explaining the driver behind every movement that matters |
| **[Reconciliation Exceptions](finance-reconciliation/finance-reconciliation-guide.md)** | Any two files that should agree | A classified, aged exception list plus a reconciliation statement that ties |
| **[MIS Pack Builder](finance-mis-pack/finance-mis-pack-guide.md)** | A trial balance or ledger export | A formatted Excel management pack: grouped P&L, balance sheet, KPIs, mapping sheet and a visible checks sheet |
| **[Cash Flow and Scenario Planning](finance-cash-flow-forecast/finance-cash-flow-forecast-guide.md)** | Receivables and payables ageing, fixed costs, opening balance | A 13-week rolling forecast, three scenarios, dated shortfall warnings and ranked actions naming your own accounts |
| **[Finance Leadership Brief](finance-leadership-brief/finance-leadership-brief-guide.md)** | Any finance analysis you have finished | A one-page brief or short deck a CEO or board will read and act on |

Each skill has its own guide with the exact inputs it needs, the phrasings that trigger it, its limits, and a troubleshooting table.

## What is in the folder

```
finance-skills/
├── README.md                                 ← this file
├── finance-variance-commentary/
│   ├── SKILL.md                              ← the skill
│   └── finance-variance-commentary-guide.md  ← how to use it
├── finance-reconciliation/
│   ├── SKILL.md
│   └── finance-reconciliation-guide.md
├── finance-mis-pack/
│   ├── SKILL.md
│   └── finance-mis-pack-guide.md
├── finance-cash-flow-forecast/
│   ├── SKILL.md
│   └── finance-cash-flow-forecast-guide.md
└── finance-leadership-brief/
    ├── SKILL.md
    └── finance-leadership-brief-guide.md
```

Every skill sits in its own folder. Inside, the file is always called `SKILL.md`, because that is the filename Claude looks for. Do not rename it. The guide beside it is named after the skill, so it stays identifiable once you have several downloaded.

---

## Why these five

Because these are the five things that eat a finance month.

**Variance commentary.** The numbers take minutes. Explaining them takes days, because finding the driver behind each movement means opening account after account. This does that pass and writes it up in language a non-finance reader can act on.

**Reconciliation.** The largest block of manual hours in any finance calendar, and almost all of it is mechanical matching done by eye. The useful part, a short list of what does not match and why, arrives late and tired. This produces that list first.

**MIS pack.** The same trial balance gets reshaped into the same pack every month, with the mapping rebuilt from memory each time. Build it once here and the mapping travels with the workbook, so next month is a rerun.

**Cash flow.** Most forecasts are rebuilt from scratch and carry one optimistic assumption: that invoices collect on their due date. They do not, which is why forecasts fail in exactly the week they were meant to warn about. This one derives collection behaviour from what actually happened and gives you a dated answer.

**Leadership brief.** Finance professionals are judged on analysis and promoted on communication. The gap between a correct pack and a decision made because of it is one page of writing that nobody was ever taught to produce.

Each of these is recurring, produces something you can hand over, and saves time you will feel the first time you use it.

## They work together

Each skill stands alone. Used in sequence they cover a month end from raw export to the decision made because of it.

```
Trial balance      →  MIS Pack Builder            →  a formatted pack
Two files          →  Reconciliation Exceptions   →  numbers you can trust
Pack plus budget   →  Variance Commentary         →  movements explained
Ageing files       →  Cash Flow Scenarios         →  the forward view
Any of the above   →  Finance Leadership Brief    →  the page leadership reads
```

---

## What makes these different from just asking

**They expect messy exports, not clean data.** Every skill looks at your file before parsing it, and handles what accounting exports actually contain: group and subtotal rows that double count if you sum them, debit and credit split across two columns, brackets for negatives, digit grouping like 12,34,567, headers that start on row 6, dates that read two ways, and invoice references formatted differently in every system. This is where generic AI output usually falls over on the first real file.

**They calculate in code, never in a sentence.** Every number is computed by running Python on your file. Nothing is worked out inside a paragraph, because that is the single largest source of error in AI finance output.

**They prove the numbers tie, and show you.** Variances must sum to the total variance. Matched plus unmatched must equal total rows. The trial balance must balance before a pack gets built. Each forecast week must open where the last one closed. Every check is reported whether it passes or fails, and a failure is stated at the top, never buried.

**They never lose anything quietly.** Accounts that cannot be mapped appear in a visible Unmapped section with their balance. Excluded receivables are stated with their value. Dropped rows are counted and explained. A pack that quietly loses two accounts looks finished and is wrong, and nobody notices until a board meeting.

**They say when they do not know.** Where your data does not explain a movement, you get a specific question to put to the business rather than an invented reason. Where an assumption had to be made, that assumption appears in the output next to the number it affects.

**The judgement stays yours.** Mapping decisions are proposed and wait for your confirmation. Fuzzy matches are labelled as fuzzy so you can check them. Nothing is ever posted, filed or sent.

---

## Getting started

1. Open Settings in Claude, go to **Capabilities**, and turn on **code execution and file creation**. Four of the five skills run Python and will not work without it.
2. Take one skill's folder and compress it to a `.zip`. The file inside must stay named `SKILL.md`, because that is what Claude looks for. The guide beside it is not needed and can be left out.
3. Go to **Customize**, then **Skills**, then add a skill and upload the zip.
4. Repeat for each skill you want.

Skills you upload stay private to your account. Once installed they work in both Chat and Cowork, and Claude picks the right one from what you ask. You do not have to name it.

**Where to start.** Try Variance Commentary or Reconciliation Exceptions first on a file you have already finished by hand. Comparing the output against work you know is correct is the fastest way to build trust in it, and to learn what it needs from you.

## Using them

Upload your file and describe the task the way you would to a colleague.

- "Explain the variances in this month's P&L against budget"
- "Reconcile this bank statement against the ledger for March"
- "Build the monthly MIS pack from this trial balance"
- "Can we make payroll on the 30th if collections stay as they are"
- "Turn this pack into a one-page brief for the CEO"

Saying which file is which and what period it covers saves a round trip.

---

## What these will not do

These boundaries are firm, and they are what makes the skills safe to use on real work.

- **No tax, GST or statutory advice.** A skill will flag input credit at risk, report a tax head difference, or place a payment on a cash flow grid. It will not tell you what to claim, when to pay, or how to treat something. Law changes and facts differ, so that stays with you and your advisor.
- **No accounting treatment or provisioning decisions.**
- **No statutory financial statements, and nothing intended for filing.**
- **No system access.** These work on files you export. They never connect to your accounting system, your bank, or any government portal.
- **No invented data.** Missing inputs become stated assumptions or open questions, never estimates dressed up as findings.
- **Nothing is posted or sent.** Every output is for you to review and act on.

You will also not find a valuation model or a compliance advisor here. Those either serve a much narrower group or carry risk that does not belong in an automated output.

## What you need

- A Claude account with code execution and file creation turned on
- Your files in Excel or CSV
- Nothing else. No installation, no terminal, no coding, nothing to connect

---

Part of the [Claude Skills Library](../README.md).
