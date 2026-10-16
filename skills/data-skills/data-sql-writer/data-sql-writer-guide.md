# SQL Writer and Debugger

Writes, explains and debugs SQL in your own dialect, and catches the errors that run cleanly and return the wrong number.

---

## Who this is for

Anyone who queries a database as part of the job: business and reporting analysts, MIS executives, BI developers, ops and marketing analysts, and anyone who writes enough SQL to be dangerous but not enough to have been burned by every trap yet.

## The problem it solves

A query that throws an error is a small problem. You see it and you fix it.

A query that runs cleanly and returns a wrong number is a large one. It gets pasted into a report, presented, and believed. Most bad SQL in the wild does not fail. It quietly counts things twice, drops rows nobody notices, or misses most of the last day in a date range.

This skill writes the query and then checks it against the specific errors that lie rather than fail. It saves twenty minutes on a routine query and several hours on the debugging sessions that would otherwise start with "the numbers look too high".

---

## What you give it

**Two things it will always ask for, so leading with them saves a round trip:**

| Input | Why it matters |
|---|---|
| Your dialect | MySQL, PostgreSQL, SQL Server, Oracle, BigQuery, Snowflake, Redshift, Databricks or SQLite. Date handling, string functions, limits and window frames differ enough that the wrong dialect either fails or behaves differently. |
| Your schema | Table names, columns, types, and how tables relate. Plain English is fine. A `CREATE TABLE` statement is better. |

**Then the question that decides whether the query is correct:** what should one row of the result represent? One customer, one order, one order line, one customer per month. Almost every silently wrong query comes from confusing two grains.

**Also useful:** how to treat cancellations, refunds, test accounts and deleted records. If you do not say, it will state which reading it took rather than choosing silently.

## What you get back

1. What it understood: grain, measure, filters, edge case treatment
2. The query, formatted to be read, commented, in your dialect
3. A short explanation of the logic, particularly any join doing real work
4. **A verification query**, which is the part most people have never been given
5. Notes on assumptions, traps that applied, and performance if your tables are large

---

## The traps it checks every time

These all run cleanly. That is what makes them expensive.

| Trap | What happens |
|---|---|
| **Join fan-out** | Joining one-to-many and then summing from the one side multiplies the measure. An order joined to three order lines makes order value appear three times. The most common and most expensive error there is. |
| **INNER where LEFT was meant** | Rows with no match silently disappear. Customers with no orders vanish and nothing errors. |
| **`NOT IN` with nulls** | One null in the subquery and the whole thing returns zero rows. |
| **Date boundaries** | `BETWEEN '2026-01-01' AND '2026-01-31'` on a timestamp column excludes almost the entire last day. |
| **Timezone** | Timestamps in UTC and a business running in IST makes every daily aggregate wrong by five and a half hours of traffic. |
| **`COUNT(*)` vs `COUNT(column)`** | The second ignores nulls. Sometimes intended, often not. |
| **Aggregating before vs after a join** | Different answers whenever the join is not one to one. |
| **Integer division** | `1/2` is `0` in several dialects, which quietly zeroes out a rate. |
| **Window frame defaults** | Not always what people expect once `ORDER BY` is present. |

## The verification query

Every query comes with a second one that proves the first is right: a row count against the expected grain, a uniqueness check on the key that catches fan-out immediately, a total you can cross-check, and a small sample of raw rows so you can trace one case by hand.

Run the verification first. A query nobody has checked is a hypothesis, not an answer.

## Debugging an existing query

Paste the query and say what the number should be and what it actually is. The direction and size of the error narrows the cause quickly. Roughly double or triple usually means fan-out. Too few rows usually means an inner join or a null filter.

It rebuilds your query one join at a time and checks the row count at each step. The step where the count jumps is the bug. It tells you the cause in one sentence before showing the fix, so you recognise it next time rather than just receiving a corrected query.

---

## Anything that changes data

It defaults to `SELECT` only.

If you ask for an `UPDATE`, `DELETE` or `INSERT`, you get the equivalent `SELECT` first, so you can see exactly which rows would be affected, plus the count, plus the statement wrapped in a transaction with the rollback shown.

An `UPDATE` with a wrong join condition is one of the few analyst errors that cannot be undone, so it will not hand you one without the preview.

## What good output looks like

A strong answer includes a query you did not ask for. Run the verification query first: a uniqueness check returning zero duplicate keys is what tells you the join did not fan out, and it takes seconds.

If the reply keeps coming back with questions attached, the grain was never stated. Saying what one row should represent resolves most of them at once. If the query errors on your database, the dialect was assumed rather than given.

---

## Installing it

1. Download this folder, or make a folder named `data-sql-writer` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill, since it writes SQL rather than running it.

## Using it

Describe your tables and what you need.

Examples that work:

- "Postgres. I have orders, order_lines and customers. Give me revenue by customer for last quarter, one row per customer"
- "This query returns about triple what it should, find the problem" (paste the query)
- "Explain what this query is actually doing" (paste the query)
- "Same query but in BigQuery syntax"
- "I need monthly active users, timestamps are UTC, we report in IST"

---

## Limits worth knowing

- It does not connect to your database. It writes SQL for you to run.
- It cannot see your data, so it cannot confirm the answer is right, only that the query does what was specified. That is exactly what the verification query is for.
- It does not tune indexes or database configuration. Performance notes are advisory.
- If your schema description is wrong or incomplete, the query will be too. It is worth pasting the real `CREATE TABLE` when you have it.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Numbers roughly double or triple | Join fan-out | Say what the number should be. It rebuilds join by join to find where the count jumps. |
| Query errors on your database | Wrong dialect assumed | State your dialect. Same query, different syntax. |
| Fewer rows than expected | Inner join, or a null filter excluding more than intended | Paste the query and the expected count. |
| Last day of the month missing | Timestamp column with a `BETWEEN` filter | It rewrites to a half-open range. |
| Daily numbers shifted | Timezone mismatch between storage and reporting | Tell it both timezones. |
| It keeps asking questions | Grain or edge cases unstated | Say what one row should represent. That resolves most of them at once. |

---

Part of the [Data skills](../README.md) in the [Claude Skills Library](../../README.md).
