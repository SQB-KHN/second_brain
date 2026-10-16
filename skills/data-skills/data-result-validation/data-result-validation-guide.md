# Did This Actually Work

An honest read on whether a change, test or campaign really worked, before you present it to anyone.

---

## Who this is for

Anyone who has to say whether something worked: marketing and growth analysts, product analysts, business analysts, ops analysts running pilots, and anyone whose result is about to be shown to a leadership team.

## The problem it solves

Somebody is about to tell the leadership team that a change worked. This is the last check before that happens.

The usual failure is not fraud. It is a genuine result with a broken test underneath it, or a before-and-after where the trend was already moving, or a metric that looked good because it was checked twenty times. All of these produce a confident number, which is the most dangerous output there is.

This skill's job is not to confirm your result. It is to find every reason the result might be wrong, and then say plainly what you can and cannot claim. It takes minutes, and it prevents the meeting where your conclusion falls apart in front of the people you were trying to convince.

---

## The first question, which decides everything

**Was there a control group, or is this a before and after?**

| Type | What it is | What you can conclude |
|---|---|---|
| **Controlled test** | Two groups, same time, same conditions, split randomly | The comparison is meaningful, because everything except the change is shared |
| **Before and after** | One group, two time periods | Suggestive, never conclusive. There is no counterfactual, so you cannot know what would have happened anyway. |

This is not a technicality. It is the difference between a finding and a coincidence, and the skill sets expectations from it before analysing anything.

## What you give it

**For a controlled test:** group sizes, the metric for each group, test duration, and how many metrics you checked.

**For a before and after:** the metric across both periods, and ideally several periods before the change so it can see whether the trend was already moving.

**Always worth mentioning:**

| Context | Why it matters |
|---|---|
| Anything else that changed in the same window | The most common cause of a false conclusion |
| Why the change was made | If the metric was unusually bad, some recovery would have happened anyway |
| When and why you stopped the test | Stopping the moment it looked good makes false positives far more likely |
| Your cost of implementation | Lets it say whether a real effect is worth doing |

## What you get back

1. **The verdict in one paragraph, in plain English**, with no statistics in it. Someone who does not know what a p-value is should understand what happened.
2. What was measured: test type, groups, duration, sample sizes, metric definition
3. The result: effect size in absolute and relative terms, with a range
4. **Test health**, every check run and what it found, including the ones that passed
5. What would have to be true for this to be wrong, in two or three conditions
6. What you can and cannot claim, written as sentences you can use directly when presenting
7. What to do next: ship, do not ship, run longer, or run a proper test

---

## The checks it runs on a controlled test

| Check | What it catches |
|---|---|
| **Sample ratio mismatch** | A 50/50 split that came out 53/47 means assignment or tracking is broken and the result cannot be trusted, however good it looks. Catches more broken tests than anything else, and almost nobody runs it. |
| **Sample size** | Whether the sample could reliably detect an effect the size of the one observed |
| **Duration** | A four-day test measures the days of the week, not your change |
| **Peeking** | Stopping when it started looking good makes a false positive much more likely |
| **Contamination** | The same person landing in both groups across devices, or the groups influencing each other |
| **Multiple comparisons** | Check twenty metrics and one will look significant by chance |

## The checks it runs on a before and after

- **Was the trend already moving?** If the metric was climbing at the same rate before the change, the change explains nothing. This overturns a large share of before-and-after conclusions on its own.
- **Regression to the mean.** If you made the change because the number was unusually bad, some recovery was coming anyway.
- **Confounders.** Seasonality, festivals, month and quarter end, other things shipped in the same window, competitor and market moves, tracking changes.

---

## Rules it will not bend

- **A range, never a single number.** "3.2 percent lift" invites false precision. "Between 0.4 and 6.1 percent, most likely around 3.2" is honest and just as usable.
- **Absolute and relative, both.** A 20 percent lift on a 0.5 percent base is a move to 0.6 percent. Reporting only the relative figure oversells it.
- **No significance claim without its threshold and sample size.** Significance without context means nothing and hides everything.
- **Statistically significant is not the same as worth doing.** You get both answers.
- **Not significant does not mean no effect.** Usually it means the sample was too small, and it will say which, plus how much more data would settle it.
- **Inconclusive is a valid finding**, said in the first paragraph rather than buried. It will not soften a weak result to make it presentable. That protection is the whole point.

## What good output looks like

A strong verdict is a paragraph with no statistics in it that a non-technical reader follows on one pass, and it frequently disappoints: "The lift is somewhere between 0.4 and 6.1 percent, most likely around 3.2, so the direction is safe but the size is not settled." Test health lists what passed as well as what failed, so you know what was examined.

If the verdict is weaker than you hoped, that is usually the sample rather than the skill, and it states how much more data would settle it. If it flags a sample ratio mismatch, investigate that before trusting anything else in the result.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities.
2. Download this folder, or make a folder named `data-result-validation` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Bring the numbers and say what you did.

Examples that work:

- "We tested a new checkout flow. Control 12,400 users at 2.9 percent, variant 12,100 at 3.4 percent, ran nine days. Is this real?"
- "We changed our pricing in June and revenue is up 8 percent. Can I say the pricing worked?"
- "The campaign got 340 leads against 280 last month. Is that a result or noise?"
- "I present this pilot on Friday. Tear it apart first."

That last one is the best use of this skill.

---

## How it protects accuracy

- Test type is identified and stated before anything is analysed, because it caps what can be concluded
- Sample ratio is checked on every controlled test, which catches more broken tests than any other single check
- Every effect is reported as a range, never as a bare point estimate
- Absolute and relative effect are both given, since either alone misleads
- No significance claim appears without its threshold and its sample size
- Every calculation runs in code, never in prose, so a confident wrong number cannot come from arithmetic done in a sentence

## Limits worth knowing

- It cannot turn a before and after into a controlled test. It reports honestly on what you have.
- It does not decide whether an effect is commercially worth it without your implementation cost.
- It does not design your next test, though it will tell you what that test would need to settle the question.
- It works on the numbers you provide. If the underlying tracking is wrong, no analysis can find that.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It says your win is inconclusive | Sample too small, or the range crosses zero | It states how much more data would settle it. That is the honest position. |
| It flags sample ratio mismatch | Assignment or tracking issue | Worth investigating before trusting any result from this test. |
| Verdict weaker than expected | Before and after, no control group | Expected. It will say what can still be claimed defensibly. |
| It asks what else changed | Confounders are the main risk in before-and-after work | Answering honestly makes the conclusion stronger, not weaker. |
| Nothing happens on upload | Code execution is off | Turn it on in Settings, under Capabilities. |

---

Part of the [Data skills](../README.md) in the [Claude Skills Library](../../README.md).
