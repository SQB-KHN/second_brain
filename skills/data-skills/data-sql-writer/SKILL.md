---
name: data-sql-writer
description: Write, explain and debug SQL in your own dialect, catching the errors that silently return wrong numbers. Use for writing queries, duplicated results or numbers that look too high.
---

# SQL Writer and Debugger

A query that errors out is a small problem. A query that runs cleanly and returns a wrong number is a large one, because it gets pasted into a report and believed. Most bad SQL in the wild does not fail. It quietly counts things twice.

## When to use this

Trigger on: write a query, SQL help, "my query returns duplicates", "these numbers look too high", explain this query, optimise this query, "how do I get X from these tables".

## Before you start

Required: the question you need answered, plus the two things below.

Ask for these two. Do not guess at either.

1. **The dialect.** MySQL, PostgreSQL, SQL Server, Oracle, BigQuery, Snowflake, Redshift, Databricks or SQLite. Syntax for dates, string functions, limits and window frames differs enough that a query written for the wrong one either fails or, worse, behaves differently.
2. **The schema.** Table names, column names, types, and how the tables relate. A description in plain English is fine. A `CREATE TABLE` statement is better.

Then establish the one thing that decides whether the query is correct:

**What does one row of the result represent?** One customer, one order, one order line, one customer per month. Ask it explicitly if it is not obvious. Almost every silently wrong query comes from confusing two grains.

## Workflow

### 1. Restate the question as a specification

Before writing anything, write back what you understood:

- The grain of the result
- The measure and how it is calculated
- The filters, including the time window and which date column it applies to
- How to treat edge cases: cancellations, refunds, test accounts, nulls, deleted records

If the user's request is ambiguous on any of these, say which reading you took. Do not silently choose.

### 2. Write the query

- Format it to be read: one clause per line, consistent indentation, meaningful aliases rather than `a` and `b`
- Use CTEs for anything with more than two joins. A stack of nested subqueries is correct and unmaintainable, and the person has to live with this query.
- Comment the non-obvious parts, particularly any join condition doing real work
- Prefer explicit `JOIN` syntax over comma joins, always

### 3. Check the query against the traps that return wrong numbers

Work through these deliberately every time. These are the ones that run cleanly and lie.

**Join fan-out.** The most common and most expensive error. Joining a one-to-many relationship and then summing a measure from the one side multiplies it by the number of matching rows. An order joined to its three order lines makes order value appear three times. Aggregate to the correct grain before joining, or join to a pre-aggregated CTE.

**INNER where LEFT was meant.** An inner join silently drops rows with no match. Customers with no orders vanish, and the count looks fine because nothing errored.

**`NOT IN` with nulls.** If the subquery returns a single null, `NOT IN` returns no rows at all. Use `NOT EXISTS` or add an explicit null filter.

**Date boundaries.** `BETWEEN '2026-01-01' AND '2026-01-31'` on a timestamp column silently excludes almost the entire last day. Use `>= start AND < next_day_start`. Confirm whether the column is a date or a timestamp before writing either.

**Timezone.** If timestamps are stored in UTC and the business runs in IST, daily aggregates are wrong by five and a half hours of traffic. Ask which timezone the data is stored in and which the answer should be in.

**`COUNT(*)` versus `COUNT(column)`.** The second ignores nulls. That is sometimes what is wanted and often not.

**Aggregating before or after the join.** These give different answers whenever the join is not one to one. Decide deliberately.

**Integer division.** In several dialects `1/2` is `0`. Cast before dividing when computing a rate.

**Window function frames.** The default frame is not always what people expect when `ORDER BY` is present. State the frame explicitly for running totals.

**Case sensitivity in string comparison.** Differs by dialect and collation. If matching on text, say what was assumed.

### 4. Ship a verification query alongside it

Never hand over a query alone. Include a short second query that proves the first one is right:

- Row count of the result, and whether it matches the expected grain
- A uniqueness check on the key, which catches fan-out immediately
- A total that can be cross-checked against a known number
- A small sample of raw rows for one entity, so the person can trace one case by hand

Tell them to run the verification first. A query nobody has checked is a hypothesis.

### 5. Debug mode

When given a query that returns wrong results, do not rewrite it immediately. Diagnose first.

- Ask what the number should be and what it actually is. The direction and size of the error narrows the cause fast. Roughly double or triple usually means fan-out. Too few rows usually means an inner join or a null filter.
- Rebuild the query one join at a time, checking row counts at each step. The step where the count jumps is the bug.
- Report the cause in one sentence before showing the fix. The person needs to recognise this error the next time, not just receive a corrected query.

## Handling anything that changes data

Default to `SELECT` only.

If asked for an `UPDATE`, `DELETE`, `INSERT` or `DDL` statement:

- Provide the equivalent `SELECT` first, so the exact rows that would be affected can be seen before anything happens
- Include the row count that would be touched
- Wrap the statement in a transaction with a rollback shown, and say plainly to run it inside a transaction
- Never present a destructive statement as ready to run without that preview

This is not caution for its own sake. An `UPDATE` with a wrong join condition is one of the few analyst errors that cannot be undone.

## Output format

**1. What was understood.** Grain, measure, filters, edge case treatment. Two or three lines.

**2. The query.** Formatted, commented, in the stated dialect.

**3. How it works.** Short explanation of the logic, particularly any join doing real work.

**4. Verification query.** With a note on what to expect from it.

**5. Notes.** Assumptions taken, traps that applied to this query, and performance concerns if the tables are large.

## Quality bar

- Is the dialect confirmed, and does the syntax match it
- Is the result grain stated, and does the query actually produce that grain
- Has every join been checked for fan-out
- Has every date filter been checked for boundary and timezone handling
- Is a verification query included
- Is every assumption stated rather than buried

## What this skill does not do

- It does not connect to your database. It writes SQL for you to run.
- It cannot see your data, so it cannot confirm the answer is right, only that the query does what was specified. That is what the verification query is for.
- It does not tune indexes or database configuration.
- It does not present destructive statements without a preview.
