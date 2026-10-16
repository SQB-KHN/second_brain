# Data Skills for Claude

Five skills for the analyst who gets handed someone else's messy data and asked a question about it.

They run inside your own Claude account, on files you export yourself. Nothing to install on your machine, nothing to connect, no coding required.

---

## Who these are for

Analysts who live in Excel and SQL rather than in notebooks: MIS executives, reporting and business analysts, BI developers, marketing, sales and ops analysts, and anyone who inherited a report they did not build.

If your week involves cleaning a file someone sent you, writing a query, explaining why a number moved, or being asked whether something worked, these are built for your job.

---

## The five skills

| Skill | Give it | Get back |
|---|---|---|
| **[Data Cleaning and Prep Log](data-cleaning-log/data-cleaning-log-guide.md)** | Any messy export | A clean file plus a documented log of every change and why |
| **[SQL Writer and Debugger](data-sql-writer/data-sql-writer-guide.md)** | Your schema and your question | Working SQL in your dialect, explained, with a verification query |
| **[Metric Definition and Dashboard Spec](data-metric-definition/data-metric-definition-guide.md)** | A vague stakeholder request | An unambiguous metric definition and build spec, before anything gets built |
| **[Why Did This Change](data-change-analysis/data-change-analysis-guide.md)** | A metric with its dimensions | Contribution by segment, mix versus rate, and what the data cannot explain |
| **[Did This Actually Work](data-result-validation/data-result-validation-guide.md)** | A test or a before-and-after | An honest read on effect size, sample adequacy and the traps |

Each has its own guide with the exact inputs it needs, the phrasings that trigger it, its limits, and a troubleshooting table.

## What is in the folder

```
data-skills/
├── README.md                            ← this file
├── data-cleaning-log/
│   ├── SKILL.md                         ← the skill
│   └── data-cleaning-log-guide.md       ← how to use it
├── data-sql-writer/
│   ├── SKILL.md
│   └── data-sql-writer-guide.md
├── data-metric-definition/
│   ├── SKILL.md
│   └── data-metric-definition-guide.md
├── data-change-analysis/
│   ├── SKILL.md
│   └── data-change-analysis-guide.md
└── data-result-validation/
    ├── SKILL.md
    └── data-result-validation-guide.md
```

Every skill sits in its own folder. Inside, the file is always called `SKILL.md`, because that is the filename Claude looks for. Do not rename it. The guide beside it is named after the skill, so it stays identifiable once you have several downloaded.

**Start with cleaning.** The other four assume reasonably clean input. Analysis on dirty data produces a confident wrong answer, which is worse than no answer.

---

## Why these five

Because these are the five things that actually fill an analyst's week.

**Cleaning.** Not the hard part. Defending it three weeks later is. When somebody asks why this month's number does not match last month's, the answer is almost always a cleaning decision nobody wrote down. The log is the deliverable here.

**SQL.** A query that errors is a small problem. A query that runs cleanly and returns the wrong number is a large one, because it gets pasted into a report and believed. Most bad SQL does not fail. It quietly counts things twice.

**Metric definitions.** Every analytics team ends up with three dashboards showing three different revenue numbers, each correct under its own definition, and nobody able to say which belongs in the board meeting. That happens because building started before defining finished.

**Why did this change.** The most common request you will ever receive, and the one most often answered with a guess. The guess sounds reasonable, gets repeated upward, and becomes the accepted reason while the real cause goes unfound.

**Did this actually work.** The last check before someone tells the leadership team that a change worked. The usual failure is not dishonesty, it is a genuine result sitting on a broken test.

---

## What makes these different from asking directly

**They expect real exports, not clean data.** Multi-row headers, subtotal rows sitting inside the data, leading zeros stripped by Excel, numbers stored as text, four spellings of the same city, dates that read two ways. This is where generic AI output falls over on the first real file.

**They calculate in code.** Every number is computed by running Python on your file. Nothing is worked out inside a paragraph, which is the largest single source of error in AI analysis.

**They keep facts and guesses apart.** What the data shows is stated as fact. What might have caused it is labelled a hypothesis, with the check that would confirm it and the person who could answer. No causal claim is made from a single dataset, because a single dataset cannot support one.

**They tell you when a change is not a change.** Most metric movements are normal variation, and explaining noise is the most common waste of analyst time. Before decomposing anything, you get told whether this movement is even unusual.

**They never lose data quietly.** Removed rows go to a quarantine table you receive. Filled gaps are flagged. Merged duplicates are shown for approval. If it is not in the log, it did not happen.

**They give you the check, not just the answer.** Every SQL query comes with a verification query. Every decomposition is proved to sum to the total. Every test result is a range rather than a falsely precise point.

**They will tell you the answer is inconclusive.** "This data cannot settle that" is often the correct finding, and it protects you from presenting something that unravels in the room.

## They work together

Each stands alone. In sequence they cover the shape of an analyst's week:

```
Raw export        →  Data Cleaning and Prep Log       →  a file you can defend
A question        →  SQL Writer and Debugger          →  a query plus its verification
A vague request   →  Metric Definition and Spec       →  a definition everyone agrees on
A number moved    →  Why Did This Change              →  where it is concentrated, and what is still unexplained
A change shipped  →  Did This Actually Work           →  what you can honestly claim
```

---

## A note on personal data

Analyst files frequently contain customer names, emails, phone numbers and addresses.

The cleaning skill scans for these and will tell you once if it finds them, then ask whether you are permitted to share the file. Many analysts work under policies that forbid it and have simply never thought about it. Most cleaning and analysis works perfectly well on a version with those columns removed or masked, and it will offer that.

It states this once and then proceeds with whatever you decide.

---

## Getting started

1. Open Settings in Claude, go to **Capabilities**, and turn on **code execution and file creation**. Three of the five run Python and will not work without it. SQL Writer and Metric Definition work without it.
2. Take one skill's folder and compress it to a `.zip`. The file inside must stay named `SKILL.md`, because that is what Claude looks for. The guide beside it is not needed and can be left out.
3. Go to **Customize**, then **Skills**, then add a skill and upload the zip.
4. Repeat for each skill you want.

Skills you upload stay private to your account. Once installed they work in Chat and Cowork, and Claude picks the right one from what you ask. You do not have to name it.

**Where to start.** Run the cleaning skill on a file you have already cleaned by hand. Comparing its log against the decisions you made yourself is the fastest way to see what it catches and what it needs from you.

## Using them

Upload your file and describe the task the way you would to a colleague.

- "Clean this CRM export, one row should be one customer"
- "Postgres, here are my tables, give me revenue by customer for last quarter"
- "Marketing wants a campaign dashboard and that is all I have been told"
- "Sales dropped 12 percent, my boss wants to know why by tomorrow"
- "I present this pilot on Friday, tear it apart first"

---

## What these will not do

- **No causal claims from data alone.** They show where a change is concentrated and what is consistent with the pattern. They will not tell you what caused it.
- **No invented values.** Missing data stays missing, or is filled with the method stated and the rows flagged.
- **No silent changes.** Every transformation is logged. Every quarantined row is handed back.
- **No system access.** They work on files you export and SQL you run. They never connect to your database, warehouse or BI tool.
- **No false precision.** Effect sizes come as ranges. Significance claims come with their threshold and sample size, or not at all.
- **No decision about whether a result is good.** That depends on your goals, and they will not guess at them.

## What you need

- A Claude account with code execution and file creation turned on for three of the five
- Your files in Excel or CSV
- Nothing else. No installation, no terminal, nothing to connect

---

Part of the [Claude Skills Library](../README.md).
