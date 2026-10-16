---
name: data-change-analysis
description: Explain why a metric moved by decomposing it across segments, separating mix from rate, and stating what the data cannot explain. Use when someone asks why a number went up or down.
---

# Why Did This Change

This is the most common request an analyst receives and the one most often answered with a guess. The guess sounds reasonable, gets repeated upward, and becomes the accepted reason. This skill answers it with decomposition, and is explicit about the difference between what moved and what caused it.

## When to use this

Trigger on: why did X drop, what is driving this change, why are sales down, explain this movement, "the number looks off this month", root cause of a metric change.

## Before you start

Required: the metric with its dimensions, covering both periods being compared.

Ask, briefly:
1. Which two periods are being compared, and whether the comparison should be against the prior period, the same period last year, or a target
2. Which dimensions are available: region, channel, product, segment, salesperson, store, campaign
3. Whether anything changed operationally in the window, such as a price change, a campaign, a tracking change or a definition change. Ask this early. It frequently is the answer, and it saves an hour of decomposition.

## Step zero, and do not skip it

**Is this even a real change?**

Most metric movements are normal variation, and explaining noise is the most common waste of analyst time. Before decomposing anything:

- Look at the metric's history if it is available. How much does it move month to month in a normal period?
- If the current movement sits inside that normal range, say so first and clearly. "This is a 4 percent drop, and this metric has moved between 6 percent up and 7 percent down in each of the last twelve months" is a complete and valuable answer.
- Check for mechanical explanations before behavioural ones. A month with fewer working days, a period with one fewer weekend, a festival shifting between months, or a comparison against an unusual base period all move a number without anything having changed.

If the movement is inside normal variation, still show the decomposition if asked, but lead with the fact that it may be noise. Letting somebody act on noise is a real cost.

## Workflow

### 1. Establish the size and shape of the change

- Absolute change and percentage change, both, since either alone misleads
- Where it sits against the metric's own recent range
- Whether it appeared suddenly on a specific date or built gradually. A step change points to something that happened. A drift points to something that is happening.

If daily or weekly data exists, plot the shape before decomposing. A step on a single date usually means a technical or tracking cause, not a market one.

### 2. Compute in code, never in prose

Every contribution, every percentage and every mix and rate split runs as Python. The decomposition has to sum to the total change, and that is a property you can only prove by computing it. A number worked out inside a sentence cannot be proved and is the largest single source of error in analysis output.

### 3. Decompose by segment

For each dimension available, compute each segment's contribution to the total change, in absolute terms, and rank them.

The key output is not which segment is largest. It is which segment moved most. A segment that is 40 percent of the business and moved 1 percent contributes less than a segment that is 5 percent and collapsed.

State the concentration plainly. "Two of nineteen regions account for 78 percent of the decline" is far more actionable than a list of nineteen numbers.

### 4. Separate mix from rate

This is the distinction that most analysis misses, and it changes what someone should do.

- **Rate effect:** performance changed within segments. Each segment is converting or selling differently than before.
- **Mix effect:** performance within segments is unchanged, but the composition shifted. More volume moved to a lower-value segment, so the average fell without anything getting worse.

These call for completely different responses. A mix shift is often a channel or campaign change, while a rate change is usually a real performance issue.

Compute both and state which dominates. Where quantity and value both exist, decompose into volume and price as well.

### 5. Decompose by entity movement where the data allows

If the data is at the level of customers, products, stores or accounts, the more useful cut is often movement rather than segment:

- New: entities present this period, absent last
- Lost: present last period, absent this
- Grown: present in both, up
- Shrunk: present in both, down

A drop caused by losing twelve accounts is a fundamentally different problem from the same drop caused by every account buying slightly less, and the segment view cannot tell them apart.

### 6. Rule out data causes before accepting business ones

Check these before writing any business explanation:

- A new segment or category appearing mid-period, which can mean a reclassification rather than a change
- A segment disappearing, which often means renaming, not loss
- A definition or tracking change
- Duplicate or missing records in one period only
- Unequal period lengths
- A late-arriving data problem, where the current period is simply incomplete

A tracking change that looks like a 20 percent drop has ended more than one campaign that was working perfectly.

### 7. Separate what moved from what caused it, in the output itself

This is the discipline that makes the skill trustworthy.

**What the data shows** is fact. The decomposition, the concentrations, the mix and rate split. State these plainly.

**What might have caused it** is a hypothesis. Label it as such. Attach the check that would confirm or kill it, and who could answer it. Never write a cause as though the data proved it, because the data almost never does. Correlation inside a dataset is not evidence of a mechanism.

If the data does not explain the movement, say so directly. "The decline is concentrated in two regions and no available dimension explains it further, so the next step is asking those two regional managers what changed" is an honest and useful answer. Manufacturing a plausible story is the failure mode here, and it is worse than admitting a limit because it stops the real investigation.

## Output format

**1. The answer in two lines.** What moved, by how much, and where it is concentrated.

**2. Is this unusual.** How this movement compares against the metric's normal range, and any mechanical explanation.

**3. Decomposition.** Contribution by segment, ranked, with the concentration stated.

**4. Mix versus rate.** Which dominates and what that implies.

**5. Entity movement.** New, lost, grown, shrunk, where the data supports it.

**6. Data causes ruled out.** What was checked and cleared, so nobody has to ask.

**7. Hypotheses.** Labelled as hypotheses, each with the check that would confirm it and the person who could answer.

**8. What the data cannot explain.** Stated plainly, with the amount attached.

## Checks to run before delivering

- Segment contributions sum to the total change. If they do not, something is being double counted or missed.
- Both absolute and percentage change shown for every material segment
- Mix and rate effects sum to the total change
- The movement has been compared against normal variation before being explained
- Every hypothesis is labelled as one, and no causal claim is made from the data alone
- The unexplained portion is stated rather than absorbed into a story

## What this skill does not do

- It does not prove causation. It shows where a change is concentrated and what is consistent with the pattern.
- It does not invent business reasons. Unexplained movement becomes a question with an owner.
- It cannot see anything outside the data provided, including the campaign, the competitor or the process change that may be the real answer.
- It does not tell you whether the change is good or bad. That is a judgement about your goals.
