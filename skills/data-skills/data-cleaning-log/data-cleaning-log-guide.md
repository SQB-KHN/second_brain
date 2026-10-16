# Data Cleaning and Prep Log

Cleans a messy dataset and hands back a documented log of every change made and why.

---

## Who this is for

Anyone who gets handed someone else's data and has to make it usable: MIS executives, reporting and business analysts, BI developers, ops and sales analysts, and anyone who has inherited a report they did not build.

## The problem it solves

Cleaning is not the hard part. Defending it is.

Three weeks after you fix a file, someone asks why this month's number does not match last month's. The answer is almost always a cleaning decision that was made in a hurry and never written down. By then you cannot reconstruct it, so you either redo the work or lose the argument.

This skill does the cleaning and produces the log that survives that question. It typically saves one to three hours per file, and it saves considerably more the first time somebody challenges a number.

---

## What you give it

One file. Excel or CSV.

**Tell it these and the output gets sharply better:**

| Context | Why it matters |
|---|---|
| What one row is supposed to represent | The single most useful thing you can say. Getting this wrong makes everything downstream wrong. |
| What the file is for | Cleaning for a headline count is different from cleaning for a customer-level join |
| Which column should be unique | Lets it check the key and report breaches rather than guessing |
| Which date format your source uses | Removes the ambiguity on dates like 03-04-2026, which read two ways |

**Problems it finds and handles:**

| Category | Examples |
|---|---|
| Structure | Multi-row and merged headers, blank separator rows, subtotal rows inside the data, several tables in one sheet, data starting on row 6 |
| Excel damage | Leading zeros stripped from PIN codes and phone numbers, long numbers in scientific notation, text converted to dates, numbers stored as text |
| Values | Mumbai, mumbai, MUMBAI and Bombay treated as four values, trailing whitespace creating invisible duplicates, mixed units, mixed currencies, several date formats in one column |
| Rows | Exact duplicates, near duplicates where the same entity is recorded twice with a small spelling difference, impossible values like negative quantities or future dates |

## What you get back

1. A summary: rows in, rows out, rows quarantined, and the three biggest issues found
2. **The cleaning log**, one line per change, with column, rows affected, reason and whether it is reversible
3. Data quality notes covering what is still wrong and was deliberately left alone
4. Open questions: the decisions that need a human, such as ambiguous dates and near-duplicate groups
5. The clean file, with the quarantine table and mapping tables as separate sheets

The log is the deliverable, not a by-product. Anyone reading it can reproduce your cleaning by hand or challenge one decision without re-examining the whole file.

---

## Before it starts: a check on personal data

It scans your columns for anything identifying a person: names, emails, phone numbers, addresses, dates of birth, government identifiers.

If it finds any, it says so once and asks whether you are allowed to share the file. Many analysts work under policies that forbid it and have simply not thought about it. It offers to work on a version with those columns removed or masked, and most cleaning and analysis works perfectly well without them.

It states this once and then continues with whatever you decide.

## The three rules it follows

**Nothing is deleted silently.** Removed rows go to a quarantine table handed back with the clean file. Deleted data nobody can see is how a wrong number survives for months.

**No gap is filled without saying so.** If a missing value is filled, the method is stated and the rows are flagged. Its preference is to leave it missing, because an imputed value stops looking imputed very quickly once it travels downstream.

**No deduplication without a stated key.** It says which columns define a duplicate and shows the merged groups. For near duplicates it proposes the matches and waits for you rather than merging on its own judgement.

## What good output looks like

A strong result is judged by the log, not the file. Every line is specific enough to redo by hand: "Merged 14 city spellings into 4 values, mapping on sheet 3, reversible." Rows in reconciles exactly against rows kept plus quarantined plus merged, and the open questions name real decisions rather than listing worries.

If the log is short but the file changed a lot, something was cleaned silently, which is the one failure this skill exists to prevent. If the row count fell further than you expected, open the quarantine table. Nothing is deleted.

---

## Installing it

1. On claude.ai, open Settings, go to Capabilities, and turn on code execution and file creation. This skill runs Python and will not work without it.
2. Download this folder, or make a folder named `data-cleaning-log` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the file and say what it is.

Examples that work:

- "Clean this CRM export, one row should be one customer"
- "This sales file has duplicates, sort it out and tell me what you changed"
- "Standardise the city and category columns in this, they are a mess"
- "Prepare this for analysis and flag anything you are unsure about"

Run this first when a file is obviously raw. Analysis on dirty data produces a confident wrong answer, which is worse than no answer.

---

## How it protects accuracy

- Rows in must equal rows kept plus quarantined plus merged, checked in code and reported
- Numeric column totals before and after are compared, and any difference must be explained by a logged step
- No column is dropped without appearing in the log
- Declared key columns are tested for uniqueness, with breaches listed
- It checks that type conversions have not introduced new missing values, which is a common silent side effect

## Limits worth knowing

- It does not decide what your data means. Columns whose meaning is unclear become questions, not assumptions.
- It does not merge near duplicates on its own. It proposes and waits for you.
- It never invents values to fill gaps.
- It cleans the file it is given. It cannot go back to the source system to check something.
- If it is not in the log, it did not happen. That is the point.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Row count dropped more than expected | Rows quarantined as impossible or duplicate | Open the quarantine table. Nothing is deleted, so you can see exactly what went and why. |
| Dates read wrong | Ambiguous format such as 03-04-2026 | It asks when both readings are possible. Answer, or state the format upfront. |
| Real distinct values merged together | Standardisation mapping too aggressive | The mapping table is included. Correct it and rerun. |
| Duplicates not caught | Duplicate key not stated | Tell it which columns define a duplicate. |
| Leading zeros still missing | Lost before you got the file, in the source export | Re-export as CSV rather than XLSX, or as text. It flags this when it detects it. |
| Nothing happens on upload | Code execution is off | Turn it on in Settings, under Capabilities. |

---

Part of the [Data skills](../README.md) in the [Claude Skills Library](../../README.md).
