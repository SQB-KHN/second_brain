---
name: data-metric-definition
description: Turn a vague dashboard request into an unambiguous metric definition and build spec before anything gets built. Use for dashboard requests, defining a metric, or mismatched numbers.
---

# Metric Definition and Dashboard Spec

Every analytics team eventually has three dashboards showing three different revenue numbers, all correct under their own definition, and nobody able to say which one to use in the board meeting. The cause is always the same: building started before defining finished. This skill produces the definition first.

## When to use this

Trigger on: build me a dashboard, I need a report on X, define this metric, "our numbers do not match", "what counts as an active user", dashboard requirements, reporting spec.

Also use this when someone asks for a dashboard and has given only a topic. A topic is not a requirement.

## The one idea behind this skill

A metric is not a formula. It is a formula plus a grain plus a time basis plus a set of decisions about edge cases. Two teams using the same formula and different edge case decisions will produce different numbers forever, and each will be able to defend theirs.

The edge cases are where the disagreement lives, so that is where most of this skill's attention goes.

## Before you start

Required: the request, however vague. A topic is enough to start from.

Ask these four. Keep it short, and do not proceed on guesses for the first two.

1. **Who uses this, and what decision do they make with it?** A metric nobody acts on does not need to exist. This question kills more unnecessary dashboards than any other.
2. **What action follows a bad number?** If the answer is none, the metric is decoration. Say so gently and ask what would actually prompt action.
3. **How often do they look, and how fresh does it need to be?** Daily refresh for a monthly decision is wasted engineering.
4. **Does a definition already exist somewhere?** If finance, sales and product each have one, the job is reconciliation, not invention, and that changes the whole exercise.

## Workflow

### 1. Force the edge case decisions

This is the core of the skill. Walk through every one that applies and get an explicit answer. Do not let any of these stay unstated, because each one is a future argument.

**Inclusion and exclusion**
- Internal, test and staff accounts: in or out
- Cancelled and refunded transactions: excluded, or included and netted, and in which period
- Deleted or archived records
- Free, trial and zero-value transactions
- Related-party or intercompany activity
- Bots and non-human traffic, for anything web-based

**Timing**
- Which date drives the metric: order date, ship date, invoice date, payment date, event date, or record creation date. These give visibly different answers.
- Timezone the metric is reported in, and the timezone the data is stored in
- How a partial period is treated at the edges: does an incomplete current month show, and is it labelled
- How restatements are handled when a past record changes after the report was published

**Measurement**
- Gross or net, and net of exactly what
- Tax inclusive or exclusive
- Currency, and if multiple, the conversion rate and the date it is taken on
- How nulls are treated: excluded from the denominator, treated as zero, or shown separately. This choice alone can move a rate by several points.
- Deduplication rule, if one entity can appear more than once

**Grain and attribution**
- What one row represents
- For anything with attribution, such as a sale credited to a channel or a rep: first touch, last touch, or split, and what happens when both apply

### 2. Write the definition

One block per metric. Every field filled. A blank field is an unresolved argument.

```
Metric name:
Plain-English definition:      [one sentence a non-analyst understands]
Formula:                       [exact, including the denominator]
Grain:                         [what one row represents]
Source tables and columns:
Date basis:                    [which date, which timezone]
Included:
Excluded:
Null handling:
Currency and conversion:
Refresh cadence:
Owner:                         [the person who resolves disputes about it]
Known caveats:                 [what this metric does not capture]
Do not confuse with:           [the similar metric people will mistake it for]
```

Two fields carry more weight than the rest. **Owner** means disagreements have somewhere to go instead of becoming a standing argument. **Do not confuse with** is what stops a similar-sounding metric being used in its place six months later.

### 3. Reconcile against existing definitions

If other definitions exist, produce a comparison rather than declaring a winner:

| Aspect | Finance version | Sales version | Proposed |

Then state plainly which differences are real disagreements needing a decision, and which are just wording. Most turn out to be wording, and saying so defuses the meeting.

Do not resolve a genuine disagreement yourself. Name it, show what each choice implies numerically where possible, and route it to the owner.

### 4. Write the build spec

Only after the definitions are settled.

- **Audience and decision.** One line. This governs everything below it.
- **Layout.** What sits at the top, because that is what gets looked at. Order by decision importance, not by ease of building.
- **Each element.** Chart type, metric, dimensions, default filters, default time range, and the reason it earns its place.
- **Filters.** Which are exposed to the user, and their default values.
- **Deliberately excluded.** The metrics someone asked for that were left out, with the reason. This section prevents the request arriving again in a month.
- **Refresh and dependencies.** What must land before this is valid, and what the user sees if it has not.

### 5. Design against the common failures

- **Too many tiles.** A dashboard with forty numbers gets used for none of them. Push for the five that drive the decision, and put the rest in a detail view.
- **No comparison.** A number alone is meaningless. Every metric needs a comparison against target, prior period or trend, and it should be specified.
- **No definition on the surface.** Definitions belong on the dashboard, in a tooltip or a notes panel, not in a document nobody opens.
- **Chart type chosen for looks.** Pie charts beyond three slices, dual axes, and 3D anything all mislead. Say so and propose the alternative.

## Output format

**1. Purpose.** Who, what decision, what action follows.

**2. Metric definitions.** One full block per metric.

**3. Edge case decisions.** A table of every question asked, the answer given, and who decided. This is the record that ends future arguments.

**4. Reconciliation.** Only if other definitions exist.

**5. Build spec.** Layout, elements, filters, exclusions, refresh.

**6. Open decisions.** Anything the requester could not answer, named with its owner and the numeric implication of each option where it can be shown.

## Quality bar

- Does every metric have a filled owner field
- Does every definition state its date basis and timezone
- Is null handling stated for every rate or average
- Does the build spec avoid every metric not defined above it
- Does every element tie back to the stated decision, with anything that does not moved to the excluded list
- Does every open decision carry an owner rather than just a question mark

## What this skill does not do

- It does not build the dashboard. It produces the specification that makes building it possible.
- It does not settle a genuine definitional disagreement between teams. It names it, shows what each option implies, and routes it to the owner.
- It does not pick your BI tool.
- It does not invent an answer to an edge case question. Unanswered questions stay visible as open decisions.
- It does not build, deploy or change anything in your BI tool. The spec is a document for a human to build from.
