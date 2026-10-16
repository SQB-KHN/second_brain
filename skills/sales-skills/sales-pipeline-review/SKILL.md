---
name: sales-pipeline-review
description: Turn a CRM export into stage integrity, aged and parked deals, slippage, real coverage and an evidence-based forecast. Use for pipeline review, coverage or forecast checks.
---

# Pipeline Review and Forecast Reality Check

Every pipeline is too big and every forecast is too optimistic, and everybody in the room already knows both. So the Monday review spends an hour on whichever deal the loudest voice wants to discuss, and the four deals that will actually decide the quarter get three minutes each. This produces the agenda that meeting should have had.

## When to use this

Trigger on: pipeline review, forecast, pipeline health, coverage, deal review, stage conversion, aged deals, quota attainment, pipeline hygiene, "will we make the number", "is this pipeline real".

## Before you start

Required: a pipeline or CRM export with deal identifier, account, stage, value, close date, owner and created date.

Ask, briefly:
1. Quota or target for the period, and the period boundaries. Without a target there is nothing to assess coverage against.
2. **What each stage means, and what has to be true to leave it.** Most CRMs have stages with names and no exit criteria, which is exactly why stage means nothing and every conversion rate built on it is noise.
3. Whether stage probability is set by the system per stage, or entered per deal by the rep. These give very different answers and only one of them is a forecast.
4. Last period's closed-won and closed-lost, so conversion can be measured rather than assumed.
5. Whether close date history exists, so slippage can be counted.

## Check for personal data first

CRM exports carry contact names, email addresses and phone numbers. Say so once, note that this analysis needs account, stage, value, dates and owner rather than contacts, and offer to run on a file with the contact columns removed. Then continue with whatever they choose.

## Workflow

### 1. Profile the export

- **One row per deal against one row per stage-history entry.** Summing a history-level file multiplies your pipeline by the number of stage changes.
- **Duplicate deals**, the same opportunity entered twice, which is common where marketing and sales both create records
- **Deals with zero or blank value**, which drop silently out of coverage while still inflating the deal count
- **Mixed currency in one column** with no currency field
- **Closed deals still sitting in the open pipeline**, and **open deals with a close date already in the past.** The second is the most common and the most revealing thing in most exports.
- Test and internal deals, header rows, brackets, Indian digit grouping

State deal count, total value, and everything excluded with its value.

### 2. Compute in code, never in prose

### 3. Test whether stage means anything, before using it

If stages have no exit criteria, say so first, because every conversion rate below rests on them. Then look for the signature of stage inflation:

- Deals sitting in a late stage with a created date only days old
- Deals in a late stage with no recorded activity
- A stage where almost nothing is ever lost, which usually means deals are being pushed forward rather than qualified

Report the pattern rather than only the number. "Nothing has been lost from proposal stage in six months" tells a manager more than a conversion percentage.

### 4. Age the pipeline and find the rot

- Days in current stage per deal, against the median for that stage. A deal at three times the median is not progressing, it is parked.
- Total age since creation
- **Deals with no activity in 30, 60 and 90 days.** Silence is the strongest single predictor available in an export.
- **Deals with no scheduled next step.** A deal with no next step is not a deal, it is a hope.

Report value at each threshold, not just count. Twelve parked deals worth 3 lakh is housekeeping. Two worth 80 lakh is the review.

### 5. Count slippage honestly

Where close date history exists, count how many times each deal's date has moved, and by how long in total.

A deal that has slipped three quarters is not a deal for this quarter. It is either not real or it is blocked by something nobody has named, and naming it is the point. Report slipped value separately from the rest of the pipeline, because it behaves differently and should not be averaged in with deals that have never moved.

### 6. Compute conversion by stage, and state what it cannot tell you

Stage to stage, and stage to won, using the prior period's actuals wherever available.

**State the sample size for every rate.** A conversion rate computed on nine deals is not a rate, and presenting it as one is how bad forecasts get built. Where the sample is thin, say so and give a range instead of a point.

### 7. Compute coverage twice

Coverage is pipeline value over the gap to target. Report it on the whole pipeline, then again after removing what the checks above flagged: the parked deals, the repeatedly slipped ones, the ones with no next step.

**The second number is the real one, and the difference between them is the finding.** Coverage on a pipeline full of parked deals is a number that reassures and misleads, which is the worst combination available.

### 8. Build the forecast in three tiers, from evidence

- **Commit.** Evidence supports the date. Name the criteria and apply them consistently.
- **Best case.** Would close if a specific named thing happens. Name the thing per deal.
- **Upside.** Everything else, stated as not forecast.

Never apply a stage probability and call the result a forecast. A weighted pipeline is arithmetic performed on a set of guesses. Show it if asked, lead with the evidence tiers, and say why.

### 9. Name the deals that decide the period

State the concentration plainly. "Four deals carry 61 percent of commit, and two of them are single-threaded" is the review agenda, and it is the sentence nobody produces.

## Output format

**1. Verdict.** Coverage on the real pipeline, whether the target is reachable, and the single biggest risk. Two lines.

**2. Pipeline summary.** Count and value by stage, with exclusions stated.

**3. Stage integrity.** Whether stages have exit criteria, and the inflation signals found.

**4. Ageing and inactivity.** Value at each threshold, with the parked deals named.

**5. Slippage.** Deals by number of times slipped, with value.

**6. Conversion by stage.** Every rate with its sample size, and a range where the sample is thin.

**7. Coverage, twice.** Whole pipeline, and after exclusions, with the difference stated.

**8. Forecast tiers.** Commit, best case, upside, with criteria and the named condition per best-case deal.

**9. The deals that decide the period.** Concentration and single-threading flagged.

**10. Review agenda.** What to spend the meeting on, ranked, with the question to ask on each deal.

**11. Data quality and exclusions.**

Offer the Excel version with one sheet per view. Build it only if asked.

## Checks to run before delivering

- Open plus closed equals total deals, and the values reconcile
- No deal counted twice through a duplicate record or a history-level export
- Excluded deals are stated with their count and value
- Coverage is reported on the whole pipeline and after exclusions, with the difference stated
- Commit plus best case plus upside equals the open pipeline exactly
- Every conversion rate carries its sample size
- No stage probability is presented as a forecast
- Deals with a close date already in the past are flagged, not silently counted in the period

## What this skill does not do

- It does not change your CRM or update a deal. It reads the export.
- It does not decide whether a deal will close. It says what the evidence supports and what is missing.
- It does not set your stage definitions or exit criteria. It tells you when their absence makes the numbers meaningless.
- It does not judge a rep. It assesses deals, and where a pattern concentrates in one owner or territory it reports the pattern and leaves the conversation to a manager.
- It does not advise on discount or terms to pull a deal in.
