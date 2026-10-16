---
name: marketing-ad-diagnosis
description: Diagnose an underperforming Meta or Google ad account by funnel stage, separating creative fatigue from audience saturation. Use when ads stop working, CPA rises or ROAS drops.
---

# Ad Performance Diagnosis

When an ad account stops working, the usual response is to change the creative, because creative is the visible part. Often the creative is fine and the problem is three steps further down. This skill finds which layer is actually broken before anything gets changed.

## When to use this

Trigger on: ads not working, CPA went up, ROAS dropped, "should I change the creative", ad account audit, campaign performance review, "we are spending more for less".

## Before you start

Required: an export from the ad platform, at campaign, ad set or ad level.

Ask:
1. **The attribution window and model.** This is rarely stated and changes everything. A seven-day click and one-day view window reports very different numbers from one-day click, and a comparison across a window change is meaningless.
2. What the account looked like when it was working, and roughly when it changed. A step change on a date points to something that happened. A gradual drift points to something that is happening.
3. What has already been changed, since a recent edit is frequently the cause.
4. The target CPA or ROAS, so performance is judged against their goal rather than a general benchmark.

## Profile the export first

- Which level the data is at, and whether rows aggregate or overlap
- Date range and whether it is daily or summed
- Which columns are raw and which are derived. Recompute every rate from raw numbers **in code, never in prose**, rather than trusting a derived column, since exports often carry stale or differently-defined calculated fields.
- Whether conversion counts are platform-attributed or from the user's own analytics. These disagree, often substantially, and the output must say which it is using.

## Work down the funnel in order

Fixing the wrong layer is the most common waste in ad management. Diagnose in this sequence and stop at the first stage that is genuinely broken.

**1. Delivery.** Is it spending the budget at all? If not, the cause is bid, budget, audience size, ad approval or a rejected asset. Nothing downstream matters until this is resolved.

**2. Impressions to clicks.** A weak click-through rate is a creative or audience-match problem. This is the only stage where changing the creative is the right first move.

**3. Clicks to landing page views.** A large gap here is almost never a marketing problem. It is page speed, a broken link, a redirect, or tracking not firing. Twenty percent or more of clicks failing to register as page views should be flagged as a technical issue and not treated as a conversion problem.

**4. Landing page views to conversion.** A page problem, not an ad problem. Sending better traffic to a page that does not convert changes nothing, and this is where most budgets are actually lost.

**5. Conversion to revenue or qualified lead.** Volume is fine but value is not. That points to the offer, the pricing, or lead quality, which usually means the targeting is attracting the wrong people rather than too few.

State which stage is worst against the account's own history, and say plainly that the stages below it should not be touched until it is fixed.

## Separate creative fatigue from audience saturation

These look nearly identical in a dashboard and have opposite fixes, which is why so much budget goes into the wrong one.

**Creative fatigue**
- Frequency rising, click-through rate falling, cost per thousand impressions roughly stable, audience size unchanged
- The same people have seen it too often
- Fix: new creative. The audience is still available.

**Audience saturation**
- Reach plateauing, cost per thousand impressions rising, frequency rising, click-through rate possibly stable
- You are running out of people to reach, so the platform is paying more to find them
- Fix: new audience. New creative will not help, because the problem is not the message.

Both can be true at once. Say which dominates and on what evidence, and if the data cannot distinguish them, say that instead of guessing.

## Check the structural problems

- **Learning phase never exiting.** An ad set needs roughly fifty conversions a week to leave learning. Too many ad sets splitting one budget means none of them gets there, and the whole account underperforms while every individual campaign looks reasonable.
- **Audience overlap.** Ad sets targeting overlapping audiences bid against each other and raise their own costs.
- **Too many variants for the budget.** Splitting a small budget across many ads means nothing accumulates enough data to judge.
- **Budget changed recently**, which resets learning and makes any before-and-after comparison invalid for several days.

## Check whether there is enough data to conclude anything

Most ad decisions are made on samples far too small to support them.

Before recommending that anything be paused or scaled, check whether it has accumulated enough conversions for the difference to be real. An ad with four conversions against another with seven is not a finding.

Say explicitly which comparisons the data can support and which it cannot. Recommending a pause on noise is worse than recommending nothing, because it destroys ads that were working.

## Say what not to change

Include this section every time. List the things that look bad but sit within normal variation, and the things somebody is likely to change out of impatience.

Constant changes are themselves a common cause of poor performance, since every significant edit restarts learning.

## Output format

**1. Verdict.** Two lines. Which layer is broken and what it will take to fix.

**2. Funnel table.** Each stage, current rate, prior rate, and where the biggest deterioration is.

**3. Ranked diagnosis.** Each issue with the evidence behind it, ordered by impact on the objective.

**4. Fatigue or saturation.** The call, the evidence, and what it implies.

**5. Structural issues.** Learning phase, overlap, budget splitting.

**6. Data adequacy.** Which comparisons hold and which do not.

**7. What not to change.** With reasons.

**8. Next actions.** Ranked, each with what it addresses and how to tell whether it worked.

## Checks to run before delivering

- Spend in the export reconciles to the stated total
- Every rate recomputed from raw numbers, not taken from a derived column
- Attribution window stated in the output
- Conversion source stated as platform-attributed or analytics
- No recommendation to pause or scale anything without enough conversions to support it
- Any period containing a budget or structural change flagged as not comparable

## What this skill does not do

- It does not access your ad account. It works on the export you provide.
- It does not write or judge creative. It tells you whether creative is the problem.
- It cannot see your landing page unless you supply it, and page problems are frequently the real cause.
- It does not guarantee a fix. It ranks what is broken by evidence and says how you will know whether the fix worked.
