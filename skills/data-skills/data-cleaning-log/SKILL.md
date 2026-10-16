---
name: data-cleaning-log
description: Clean a messy dataset and produce a documented log of every change and why. Use for raw exports, CRM dumps, survey files, duplicates, or preparing a file for analysis.
---

# Data Cleaning and Prep Log

Cleaning a file is easy. Defending it three weeks later is not. When somebody asks why this month's number does not match last month's, the answer is almost always an undocumented cleaning decision that nobody wrote down. This skill cleans the file and writes the log that survives the question.

## When to use this

Trigger on: clean this data, fix this file, remove duplicates, standardise these values, prepare this for analysis, "this export is a mess", "why are there two versions of the same customer".

Also run this first whenever another analysis is requested on an obviously raw file. Analysis on dirty data produces a confident wrong answer, which is worse than no answer.

## Before you start

Required: the file.

Ask, briefly, only what you cannot infer:
1. What one row is supposed to represent. This is the single most useful question, and getting it wrong makes everything downstream wrong.
2. What the file will be used for. Cleaning for a headline count is different from cleaning for a customer-level join.
3. Whether any column is a key that must stay unique.

## Check for personal data before anything else

Scan the columns for anything that identifies a person: names, email addresses, phone numbers, addresses, PIN codes, customer IDs tied to individuals, government identifiers, dates of birth.

If any are present, say so plainly before proceeding and ask whether the user is permitted to share this file. Many analysts work under policies that forbid it and have not thought about it. Offer to work on a version with those columns removed or masked, and note that most cleaning and analysis works perfectly well without them.

Do not lecture. State it once, offer the alternative, and continue with whatever they choose.

## Workflow

### 1. Profile before touching anything

Never transform a file you have not looked at. Report:

- Row and column counts, and the real header row position, which is often not row 1
- Data type actually present in each column, against what it should be
- Missing value count per column, and how missing is represented, since blank, `NA`, `-`, `null`, `0` and `#N/A` can all appear in one file and do not mean the same thing
- Distinct value counts for categorical columns, which immediately exposes inconsistent labelling
- Min, max and a few sample values per column, which exposes format chaos faster than any summary statistic

### 2. Find what is actually wrong

Work through these deliberately. Each is common enough to expect.

**Structure**
- Multi-row or merged headers
- Blank rows and columns used as visual separators
- Subtotal and total rows sitting inside the data
- Multiple tables stacked in one sheet
- Data starting several rows down

**Excel damage**, which is silent and very common
- Leading zeros stripped from PIN codes, phone numbers and account codes
- Long numbers converted to scientific notation
- Text that looked like a date converted into one
- Numbers stored as text, which breaks every aggregation

**Values**
- Inconsistent categorical labels: `Mumbai`, `mumbai`, `MUMBAI`, `Bombay ` are four values and one city
- Leading and trailing whitespace, which creates invisible duplicates
- Mixed units in one column, such as some rows in units and some in thousands
- Mixed currencies with no currency column
- Dates in several formats in the same column, including the ambiguous ones. `03-04-2026` reads two ways. Resolve it explicitly rather than letting a parser guess, and if both readings are possible, ask.

**Rows**
- Exact duplicates
- Near duplicates, which is the harder and more valuable case: the same entity recorded twice with a small difference in spelling, spacing or punctuation
- Rows that are impossible rather than merely odd, such as a negative quantity or a date in the future

### 3. Follow three rules while fixing

These are what make the output defensible.

**Never delete silently.** Rows removed go to a quarantine table that is handed back with the clean file. Deleted data that nobody can see is how a wrong number survives for months.

**Never fill a gap without saying so.** If a missing value is filled, the method is stated and the affected rows are flagged. Preferably leave it missing and let the analysis handle it, because an imputed value that travels downstream stops looking imputed very quickly.

**Never deduplicate without a stated key.** Say which columns define a duplicate, and show the merged groups so a human can check. For near duplicates, propose the matches and get them confirmed rather than merging on your own judgement.

### 4. Standardise

- Trim whitespace, unify case for categorical columns while preserving the original in a separate column where the display form matters
- Map variant labels to a single value, and show the mapping table rather than burying it
- Convert dates to one ISO format after the ambiguity question is settled
- Strip currency symbols and separators from numeric columns, handling Indian digit grouping such as `12,34,567` and brackets for negatives
- Normalise phone numbers to a consistent form, keeping the original
- Split or combine columns only where asked, since guessing at structure creates work rather than saving it

### 5. Produce the log

The log is the deliverable, not a by-product. For each change:

| Step | Column | What changed | Rows affected | Why | Reversible |

Anyone reading it should be able to reproduce the cleaning by hand, or challenge any single decision without re-examining the whole file.

## Output format

**1. Summary.** Rows in, rows out, rows quarantined, columns changed, and the three biggest issues found.

**2. The cleaning log.** As above, one line per change.

**3. Data quality notes.** What is still wrong and was left alone, and why. A file is rarely perfectly clean, and pretending otherwise is the problem.

**4. Open questions.** Decisions that need a human: ambiguous dates, near-duplicate groups, columns whose meaning is unclear, values that look impossible.

**5. The clean file.** Written out, with the quarantine table and the mapping tables included as separate sheets so nothing is lost.

## Checks to run before delivering

Run in code and report the result.

- Rows in equals rows kept plus rows quarantined plus rows merged. This must reconcile exactly.
- No column dropped without being listed
- Numeric column totals before and after, with any change explained by a logged step
- Key columns are unique if they were declared unique, and the breaches are listed if not
- No new missing values introduced by a transformation, which is a common side effect of type conversion

## What this skill does not do

- It does not decide what your data means. Ambiguous columns become questions.
- It does not merge near duplicates on its own judgement. It proposes and waits.
- It does not invent values to fill gaps.
- It does not silently improve anything. If it is not in the log, it did not happen.
- It does not overwrite your source file, and it does not touch the system the export came from. You get a clean file, a quarantine table and a log, all for you to review.
