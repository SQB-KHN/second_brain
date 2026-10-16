# Metric Definition and Dashboard Spec

Turns a vague dashboard request into an unambiguous metric definition and build spec, before anything gets built.

---

## Who this is for

Analysts and BI people who receive requests like "I need a dashboard for sales performance" and are expected to build something from it: reporting and business analysts, BI developers, MIS leads, analytics managers, and anyone who owns the numbers other teams argue about.

## The problem it solves

Every analytics team eventually ends up with three dashboards showing three different revenue numbers. All three are correct under their own definition. Nobody can say which one belongs in the board meeting.

The cause is always the same. Building started before defining finished, and the definition lived in someone's head rather than on paper.

This skill produces the definition first, forces the edge case decisions into the open while they are still cheap to settle, and then writes the build spec. It saves a few hours upfront and considerably more later, because rebuilding a dashboard after a definitional argument costs far more than specifying it once.

It is the least glamorous skill in this set and usually the highest return.

---

## What you give it

A request, however vague. "We need a sales dashboard" is enough to start.

**It will ask you four things, and the first two matter most:**

| Question | Why |
|---|---|
| Who uses this and what decision do they make with it | A metric nobody acts on does not need to exist. This kills more unnecessary dashboards than anything else. |
| What action follows a bad number | If the answer is none, the metric is decoration |
| How often they look, and how fresh it must be | Daily refresh for a monthly decision is wasted engineering |
| Whether a definition already exists | If finance and sales each have one, the job is reconciliation, not invention |

**Helpful if you have it:** your schema, existing definitions from other teams, and a screenshot of whatever people use today.

## What you get back

1. **Purpose.** Who, what decision, what action follows
2. **Metric definitions.** One complete block per metric, every field filled
3. **Edge case decisions.** A table of every question asked, the answer, and who decided
4. **Reconciliation**, if other definitions already exist
5. **Build spec.** Layout, each element, filters, deliberate exclusions, refresh
6. **Open decisions**, each with an owner and the numeric implication of each option

---

## The edge cases it forces into the open

A metric is not a formula. It is a formula plus a grain plus a time basis plus a set of edge case decisions. Two teams using the same formula and different edge case decisions will disagree forever, and both will be able to defend their number.

So this is where most of the work goes:

| Area | Questions it makes you answer |
|---|---|
| **Inclusion** | Internal and test accounts, cancellations, refunds, deleted records, free and trial transactions, intercompany activity, bot traffic |
| **Timing** | Which date drives it: order, ship, invoice, payment or event date. Which timezone. How incomplete current periods are shown. How restatements are handled. |
| **Measurement** | Gross or net, and net of what. Tax in or out. Currency and the conversion date. How nulls are treated, which alone can move a rate by several points. |
| **Grain and attribution** | What one row represents. First touch, last touch or split credit, and what happens when both apply. |

Each unanswered question here is a future argument. Answering them takes twenty minutes now.

## Two fields that do the heavy lifting

**Owner.** The person who resolves disputes about this metric. Without one, disagreements become a standing argument rather than a decision.

**Do not confuse with.** The similar-sounding metric people will reach for by mistake. This single line prevents most of the wrong-number-in-a-meeting incidents six months later.

## What good output looks like

A strong spec is mostly definitions and edge cases, and the build section is the short part. Every metric block has its owner filled in and a "do not confuse with" line. The edge case table records who decided each answer, and that record is what ends the argument six months later.

If the spec feels smaller than you expected, check the excluded list. Metrics with no decision attached were cut, each with its reason. A long list of open decisions is not a fault; those questions were always open, they were just invisible before.

---

## Installing it

1. Download this folder, or make a folder named `data-metric-definition` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill.

## Using it

Bring the request as you received it. Vague is fine, and is in fact the point.

Examples that work:

- "Marketing wants a dashboard for campaign performance, that is all I have been told"
- "Finance and sales report different revenue every month, help me pin down the definitions"
- "Define active user for us, three teams count it differently"
- "Write the spec for a weekly ops report before I build it"
- "Here is the dashboard we have. It has forty tiles and nobody uses it. Rebuild the spec."

---

## What it will push back on

- **Too many tiles.** A dashboard with forty numbers gets used for none of them. It pushes for the five that drive the decision.
- **No comparison.** A number alone means nothing. Every metric gets a target, prior period or trend specified alongside it.
- **Definitions hidden in a document.** They belong on the dashboard surface, in a tooltip or notes panel.
- **Chart types that mislead.** Pie charts past three slices, dual axes and 3D anything. It says so and proposes the alternative.
- **Metrics with no decision attached.** They move to the excluded list with a reason, which stops the same request arriving again next month.

## Limits worth knowing

- It does not build the dashboard. It produces the spec that makes building it possible and correct.
- It does not settle a real disagreement between two teams. It names the disagreement, shows what each option implies numerically where it can, and routes it to the owner. That call is a business one.
- It does not pick your BI tool.
- It will not invent answers to edge case questions. Anything you cannot answer stays visible as an open decision rather than being quietly decided for you.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It keeps asking instead of producing | Purpose and decision not stated | Answer who uses it and what they do differently because of it. Most other questions resolve from there. |
| Spec feels too small | It cut metrics with no decision attached | Check the excluded list. Each has a reason. Push back if one is genuinely needed. |
| Definitions conflict with another team's | Expected, and the point | The reconciliation table shows where and by how much. Take it to the owner. |
| Too many open decisions | Genuinely unresolved questions | These were always open. They were just invisible before. |
| No owner named on a metric | Nobody has been asked to own it | It leaves the field visible and empty rather than filling it. That gap is the finding. |

---

Part of the [Data skills](../README.md) in the [Claude Skills Library](../../README.md).
