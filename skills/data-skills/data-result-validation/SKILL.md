---
name: data-result-validation
description: An honest read on whether a change, test or campaign actually worked, covering effect size, sample adequacy and the traps. Use for A/B tests, before and after comparisons or pilots.
---

# Did This Actually Work

Somebody is about to tell the leadership team that a change worked. This skill is the last check before that happens. Its job is not to confirm the result. Its job is to find every reason the result might be wrong, and then say plainly what can and cannot be concluded.

## When to use this

Trigger on: A/B test results, did the campaign work, is this statistically significant, before and after comparison, pilot results, "we changed X and Y went up", "can I present this".

## Before you start

Required: the numbers, and what you did.

Ask, briefly:
1. **Was there a control group, or is this a before and after?** This decides everything below, and it is the first section of this skill for that reason.
2. Group sizes, the metric for each group, and how long it ran. Without these nothing can be assessed.
3. **How many metrics were checked.** Testing twenty almost guarantees one looks significant by chance.
4. When and why the test was stopped, and against what rule.
5. Anything else that changed in the same window, and why the change was made in the first place.

Compute in code, never in prose. Every effect size, ratio, range and sample calculation runs as Python. A significance claim worked out inside a sentence is exactly the kind of confident wrong number this skill exists to catch.

## First question, and it decides everything

**Was there a control group, or is this a before and after?**

These are not the same and the difference is not a technicality.

- **Controlled test:** two groups running at the same time under the same conditions, split randomly. The comparison is meaningful because everything except the change is shared.
- **Before and after:** one group, two time periods. There is no counterfactual. You cannot know what would have happened anyway.

Establish which one this is before analysing anything, and set expectations accordingly. A before and after can be suggestive. It cannot be conclusive, and saying so is not pedantry. It is the difference between a finding and a coincidence.

## For a controlled test

### 1. Check the test before checking the result

A broken test produces a confident number, which is the worst possible output. Run these first.

**Sample ratio mismatch.** If the split was meant to be 50/50 and came out 53/47 on a large sample, something is wrong with the assignment or the tracking, and the result cannot be trusted no matter how good it looks. This single check catches more broken tests than any other and almost nobody runs it.

**Sample size.** Was the sample large enough to detect an effect of the size observed? If not, an apparently positive result may be noise. Compute what could have been detected reliably and compare it against what was claimed.

**Duration.** Did the test run at least one full weekly cycle? Weekday and weekend behaviour differ enough that a four-day test measures the days, not the change.

**Peeking.** Was the test stopped when it started looking good? Stopping at the moment a result crosses a threshold makes false positives far more likely. Ask when the stop decision was made and against what rule.

**Contamination.** Could the same person land in both groups, across devices or sessions? Could the two groups interact?

**Multiple comparisons.** How many metrics were checked? Testing twenty metrics almost guarantees one looks significant by chance. If several were checked, say so and adjust the interpretation.

### 2. Report the effect honestly

- Effect size in both absolute and relative terms. A 20 percent lift on a 0.5 percent base rate is a move to 0.6 percent, and stating only the relative number oversells it.
- **A range, never a point estimate.** The single most important rule here. "3.2 percent lift" invites a false sense of precision. "Somewhere between 0.4 percent and 6.1 percent, most likely around 3.2" is honest and just as usable.
- What the range implies for the decision. If the entire range is positive, the direction is safe even if the size is uncertain. If it crosses zero, the honest read is that this test did not settle it.
- Whether the effect is large enough to matter commercially, which is a separate question from whether it is real. A real but tiny effect is often not worth the implementation cost.

### 3. Say what would have to be true for this to be wrong

Write the two or three conditions that would overturn the conclusion. This is more useful than a confidence number, because it is actionable and a non-technical reader understands it.

## For a before and after

### 1. Name the confounders explicitly

Everything else that changed in the same window. Ask directly, since the user usually knows and has not thought to mention it:

- Seasonality, festivals, month-end and quarter-end effects
- Other changes shipped in the same period, which is very common
- A pricing, competitor or market change
- A trend that was already running before the change, which is the most frequent false positive of all
- Any change to tracking or measurement

### 2. Check whether the trend was already moving

Get the periods before the change. If the metric was already climbing at the same rate, the change explains nothing. This check alone overturns a large share of before and after conclusions.

### 3. Check for regression to the mean

If the change was made because the metric was unusually bad, some recovery would have happened anyway. This is one of the most common reasons an intervention appears to work.

### 4. State the ceiling on the conclusion

Say plainly what can be claimed. Usually it is something like: the metric improved after the change, no other obvious explanation was found, and a controlled test would be needed to attribute it. That is an honest and defensible position, and it is often enough to proceed on.

## The rules that apply to both

- **Never call something significant without stating what was tested, against what threshold, and on what sample size.** Significance without context means nothing and hides everything.
- **Statistically significant is not the same as worth doing.** Say both.
- **Not significant does not mean no effect.** It often means the sample was too small. Say which one it is, and state how much more data would settle it.
- **An inconclusive result is a valid finding.** "This test cannot tell us" is frequently the correct and most valuable answer, and it protects the person from presenting something that unravels in the room.

## Output format

**1. The verdict, in one paragraph, in plain English.** No statistics in this section. Somebody who does not know what a p-value is should understand what happened.

**2. What was measured.** Test type, groups, duration, sample sizes, the metric and its definition.

**3. The result.** Effect size in absolute and relative terms, with the range.

**4. Test health.** Every check run, and what it found. State the ones that passed as well as the ones that failed, so the reader knows what was examined.

**5. What would have to be true for this to be wrong.** Two or three conditions.

**6. What you can and cannot claim.** Written as sentences the person can use directly when presenting.

**7. What to do next.** Ship, do not ship, run longer, or run a proper test. One recommendation with the reason.

## Checks to run before delivering

- Test type identified and stated up front
- Sample ratio checked for any controlled test
- Effect reported as a range, never as a point estimate alone
- Absolute and relative effect both given
- Sample adequacy assessed, with the minimum detectable effect stated where the result is inconclusive
- No significance claim without its threshold and sample size
- Confounders listed for any before and after
- Where the answer is inconclusive, that is said in the first paragraph rather than buried at the end

## What this skill does not do

- It does not turn a before and after into a controlled test. It reports honestly on what it has.
- It does not decide whether an effect is commercially worth it. That needs your cost of implementation.
- It does not design your next test, though it will say what the next test would need to settle.
- It will not soften an inconclusive result to make it presentable. That protection is the point of the skill.
- It does not stop, extend or change a running test, and it does not ship anything. It gives you a read and a recommendation; the call is yours.
