# Why Did This Change

Explains a metric movement by decomposing it across segments, separating mix from rate, and being explicit about what the data cannot explain.

---

## Who this is for

Any analyst who gets asked "why did this drop" and has an hour to answer: business and reporting analysts, MIS executives, marketing and sales analysts, ops analysts, and anyone who has to explain a number to someone more senior than them.

## The problem it solves

This is the most common request an analyst receives and the one most often answered with a guess.

The guess sounds reasonable. It gets repeated upward. Within a week it is the accepted reason, and the actual cause is still out there. Worse, half the time the movement was normal variation and there was nothing to explain at all.

This skill decomposes the change properly, checks whether it is even unusual before explaining it, and keeps a hard line between what the data shows and what somebody might guess from it. Saves one to three hours per request, and prevents the more expensive failure of acting on a wrong reason.

---

## What you give it

The metric with its dimensions, covering both periods you are comparing.

**Minimum:** the metric value broken down by at least one dimension, for two periods.

**Each of these makes the answer materially better:**

| Extra data | What it unlocks |
|---|---|
| More dimensions (region, channel, product, segment, rep, store) | Finds where the change is actually concentrated |
| Twelve months of history | Lets it say whether this movement is even unusual, which is often the whole answer |
| Daily or weekly granularity | Distinguishes a step change on one date from a gradual drift, which point to completely different causes |
| Quantity and value separately | Volume versus price decomposition |
| Entity-level rows (customer, product, store) | New, lost, grown and shrunk analysis, which segment views cannot show |
| A note on what changed operationally | Often turns out to be the answer, and saves an hour of decomposition |

## What you get back

1. The answer in two lines: what moved, by how much, where it is concentrated
2. **Whether this is even unusual**, compared against the metric's normal range
3. Decomposition by segment, ranked by contribution, with the concentration stated
4. Mix versus rate, and what each implies
5. New, lost, grown and shrunk, where the data supports it
6. Data causes checked and ruled out
7. Hypotheses, clearly labelled as hypotheses, each with the check that would confirm it and who can answer
8. What the data cannot explain, stated plainly with the amount attached

---

## What it does differently

**It asks whether the change is real first.** Most movements are normal variation, and explaining noise is the most common waste of analyst time. If your metric has moved between 6 percent up and 7 percent down every month for a year, a 4 percent drop is not a story. It says that first, and clearly.

**It checks the boring explanations before the interesting ones.** Fewer working days, one fewer weekend, a festival shifting between months, an unusual base period. These move numbers without anything having changed.

**It ranks by movement, not by size.** A segment that is 40 percent of your business and moved 1 percent matters less than one that is 5 percent and collapsed. Most analysis gets this backwards.

**It separates mix from rate**, which is the distinction most analysis misses and the one that changes what you should do:

- **Rate effect:** performance changed within segments. Something is genuinely worse.
- **Mix effect:** performance is unchanged, but volume shifted toward a lower-value segment, so the average fell without anything getting worse.

These call for completely different responses, and confusing them sends teams to fix a problem that does not exist.

**It splits new, lost, grown and shrunk** for entity-level data. A drop caused by losing twelve accounts is a fundamentally different problem from every account buying slightly less, and no segment breakdown will tell you which one you have.

**It rules out data causes before accepting business ones.** A tracking change that looks like a 20 percent drop has killed more than one campaign that was working perfectly.

## The line it will not cross

The output keeps two things strictly apart.

**What the data shows** is fact: the decomposition, the concentration, the mix and rate split.

**What might have caused it** is a hypothesis, labelled as one, with the check that would confirm or kill it and the person who could answer.

It will not write a cause as though the data proved it, because data almost never proves a cause. And if the data does not explain the movement, it says so directly rather than assembling a plausible story. Manufacturing a reason is worse than admitting a limit, because it stops the real investigation.

## What good output looks like

A strong answer often opens by telling you there is nothing to explain: "This is a 4 percent drop, and this metric has moved between 6 percent up and 7 percent down every month for a year." Where there is something, it names the concentration rather than listing everything: "Two of nineteen regions account for 78 percent of the decline." Hypotheses are labelled, each with the person who could confirm it.

If the answer feels thin, you supplied one dimension and two periods. More dimensions, more history, or entity-level rows change the quality substantially.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities.
2. Download this folder, or make a folder named `data-change-analysis` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the data and ask the question the way it was asked of you.

Examples that work:

- "Sales dropped 12 percent last month, my boss wants to know why by tomorrow"
- "Conversion rate fell from 3.1 to 2.6 percent. Here is the data by channel and device."
- "Why is our average order value down when volume is up"
- "Revenue is flat but it feels like something changed underneath. Here are twelve months by segment."

Mentioning anything that changed operationally in the window, a price change, a campaign, a tracking update, saves real time. It is often the answer.

---

## How it protects accuracy

- Segment contributions are proved to sum to the total change, so nothing is double counted or missed
- Mix and rate effects also sum to the total change
- Both absolute and percentage change are shown, since either alone misleads
- The movement is compared against normal variation before any explanation is offered
- Every hypothesis is labelled, and no causal claim is made from the data alone
- The unexplained portion is stated with its amount rather than absorbed into a narrative

## Limits worth knowing

- It does not prove causation. Nothing that works from a single dataset can.
- It cannot see the campaign, the competitor, the process change or the market event that may be the real answer.
- It does not tell you whether the change is good or bad. That depends on your goals.
- With one dimension and two periods, the answer will be thin. More dimensions and more history change the quality significantly.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It says the change may be noise | The movement sits inside normal variation | That is the finding. Acting on noise is a real cost. |
| Answer is thin | Only one dimension supplied | Add more dimensions, or entity-level rows. |
| Contributions do not sum | Overlapping segments or double counted rows | It reports this rather than hiding it. Usually a data structure issue. |
| No cause identified | The data genuinely does not contain one | You get the specific question and who to ask, which is the honest next step. |
| Nothing happens on upload | Code execution is off | Turn it on in Settings, under Capabilities. |

---

Part of the [Data skills](../README.md) in the [Claude Skills Library](../../README.md).
