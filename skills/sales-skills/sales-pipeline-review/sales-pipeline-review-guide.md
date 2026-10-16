# Pipeline Review and Forecast Reality Check

Turns a CRM export into stage integrity, parked deals, slippage, coverage computed twice, and a forecast built from evidence instead of stage probability.

---

## Who this is for

Anyone who owns a number or reviews one: sales managers and team leads, regional and area sales managers, account executives, inside sales leads, sales operations analysts, channel and distributor managers, and founders running their own pipeline.

## The problem it solves

Every pipeline is too big and every forecast is too optimistic, and everybody in the room already knows both.

So the Monday review becomes a negotiation. An hour goes on whichever deal the loudest voice wants to discuss, and the four deals that will actually decide the quarter get three minutes each. Nobody asks the boring questions, because the boring questions have uncomfortable answers.

The information needed to run that meeting properly is already in the export. Which deals have not moved in sixty days, which have slipped three times, which have no scheduled next step, and what coverage looks like once you remove those. Nobody computes it, because it takes two hours in a spreadsheet every week and the meeting is in ten minutes. This produces that agenda in one pass.

---

## What you give it

**Minimum:** a pipeline export with deal identifier, account, stage, value, close date, owner and created date.

| Extra data | What it unlocks |
|---|---|
| **Quota or target for the period** | Coverage. Without a target there is nothing to assess against |
| **What each stage means, and its exit criteria** | Whether stage means anything at all, which every conversion rate rests on |
| **Close date history, last activity, and next step with its date** | Slippage counting, parked deals at 30, 60 and 90 days, and the most predictive field in any CRM, usually the emptiest |
| Prior period closed-won and closed-lost | Conversion measured rather than assumed |

**Handled automatically:** history-level exports where the deal total repeats on every stage change, duplicate opportunities created by two teams, zero and blank values, mixed currency in one column, closed deals still in the open pipeline, **open deals with a close date already in the past**, test records, header rows, brackets and Indian digit grouping.

**Before anything else** it names which columns carry contact names, emails and phone numbers, and offers to run without them. The analysis needs account, stage, value, dates and owner, not contacts.

## What you get back

1. Verdict: coverage on the real pipeline, whether the target is reachable, and the biggest risk
2. Pipeline by stage, with exclusions stated
3. **Stage integrity**: whether stages have exit criteria, and the inflation signals found
4. Ageing and inactivity, valued at each threshold, with parked deals named
5. **Slippage**: deals by how many times they have moved, with value
6. Conversion by stage, **every rate with its sample size**
7. **Coverage twice**: whole pipeline, and after removing what was flagged
8. Forecast tiers: commit, best case, upside, with criteria and per-deal conditions
9. The deals that decide the period, with concentration and single-threading
10. A ranked review agenda, with the question to ask on each deal

An Excel version with one sheet per view is offered at the end.

---

## Coverage gets computed twice, and the second number is the real one

Coverage on the whole pipeline is the number that reassures and misleads, which is the worst combination available in a forecast.

So it reports coverage twice: once on everything, and once after removing the deals that failed the checks above, meaning the parked ones, the repeatedly slipped ones and the ones with no next step.

**The gap between them is the finding.** A pipeline at 3.2x coverage that drops to 1.4x once you remove what has not moved in two months is not healthy, and no single coverage figure will ever tell you that.

## Why it will not weight your pipeline and call it a forecast

Applying a stage probability to a stage value is arithmetic performed on a set of guesses, and it produces a number that looks calculated and is not. So the forecast comes in three tiers built from evidence instead:

| Tier | What it means |
|---|---|
| **Commit** | Evidence supports the date. Named criteria, applied consistently |
| **Best case** | Would close if one specific named thing happens, stated per deal |
| **Upside** | Everything else, and labelled as not forecast |

It will show you the weighted number if you ask. It will not lead with it.

## The signals that actually predict

| Signal | Why it matters |
|---|---|
| **No scheduled next step, or no activity in 60 days** | A deal with no next step is a hope, and silence is the strongest single predictor available in an export |
| **Slipped three times** | Not a deal for this quarter. Either not real, or blocked by something nobody has named |
| **Days in stage above 3x the median** | Not progressing. Parked |
| **Late stage, created last week, or a stage nothing is ever lost from** | Stage inflation. Deals are being pushed forward rather than qualified |

## What good output looks like

A strong result is a review agenda, not a report. It says which four deals to spend the meeting on and what to ask about each, and it usually names a deal everyone was comfortable with.

The most useful sentence is normally about concentration: "Four deals carry 61 percent of commit, and two of them are single-threaded." That is the whole review in one line.

If coverage barely changes between the two computations, your pipeline is genuinely clean, which is rare and worth knowing. If almost nothing has a next step, that is a CRM discipline finding rather than a pipeline finding, and it will say so.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill runs Python on your export and will not work without it.
2. Download this folder, or make a folder named `sales-pipeline-review` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the export and say what the target is.

Examples that work:

- "Q3 pipeline, target is 4.2 crore. Is this real?"
- "Forecast call tomorrow. Which deals will I get asked about and what will they ask?"
- "We hit coverage every quarter and miss the number. Work out why."
- "Build the review agenda. I have an hour and 90 open deals."

Supplying close date history and last activity date roughly doubles what it can find.

---

## How it protects accuracy

- Open plus closed is proved to equal total deals, and the values reconcile
- History-level exports are detected, because summing one multiplies your pipeline by the number of stage changes
- Duplicate opportunities are found and reported rather than counted twice, and coverage is always reported both before and after exclusions with the difference stated
- Commit plus best case plus upside is proved to equal the open pipeline exactly
- Every conversion rate carries its sample size, because a rate on nine deals is not a rate
- Deals with a close date already in the past are flagged, never silently counted in the period

## Limits worth knowing

- It does not change your CRM or update a deal. It reads the export.
- It does not decide whether a deal will close. It says what the evidence supports and what is missing.
- It does not set your stage definitions. It tells you when their absence makes the numbers meaningless.
- It does not judge a rep, and it does not advise on discount or terms to pull a deal in. Where a pattern concentrates in one owner it reports the pattern and leaves the conversation to you.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Pipeline far larger than you expect | History-level export, totals repeating per stage change | It detects and states the level. Re-export at deal level. |
| Coverage collapses after exclusions | Large share of the pipeline is parked or slipped | That is the finding, and it is the honest number. |
| Conversion rates look implausible | Small samples per stage | Every rate shows its sample size. Thin ones come back as a range. |
| Most deals flagged with no next step | The field is genuinely empty | A CRM discipline finding rather than a pipeline one. It says which. |
| It refuses to weight the pipeline | Deliberate | Ask and it will show the weighted number. It will not lead with it. |

---

Part of the [Sales skills](../README.md) in the [Claude Skills Library](../../README.md).
