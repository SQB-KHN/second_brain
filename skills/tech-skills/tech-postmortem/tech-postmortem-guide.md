# Incident Postmortem

Turns incident evidence into a timeline that reconciles, contributing factors in the plural, and a short list of action items somebody will actually do.

---

## Who this is for

Anyone who has to write up an incident: software engineers, SREs and platform engineers, DevOps, support and L2 or L3 engineers, engineering managers and tech leads, and anyone who ran an incident bridge and now has to explain it to people who were asleep.

## The problem it solves

The postmortem gets written by the person who was up all night, three days later, for an audience that includes their manager.

So three things happen. It names one root cause, because a single cause reads as competence and a list reads as confusion. The timeline has holes where nobody was taking notes, filled with a plausible sequence nobody can later distinguish from evidence. And the actions are the five things somebody thought of in the meeting, half of which will never be done. Eight months later the same incident happens and nobody connects them, because the earlier document never checked whether it was a recurrence.

Asking any AI for this unaided has a specific failure too. It will happily write "Root Cause: the connection pool was exhausted", which is fluent, confident, and stops the investigation exactly where it should have started.

---

## What you give it

**Required:** the raw material. Alert timestamps, chat or bridge logs, deploy records, tickets, and what people remember.

| Context | Why it matters |
|---|---|
| **The timezone of every timestamp** | Logs are UTC, chat is local, the pager is something else. This is the commonest defect in a postmortem and it invalidates every duration in it |
| **What the user actually experienced** | Usually different from what the system did, and it is the number leadership cares about |
| **Whether this has happened before** | A recurrence is a far more serious finding than a novel failure, and it changes the whole document |
| Who was involved by role, and the audience | Roles go in the document, names do not, and an internal review differs from a customer or client deliverable |
| What people believed at the time | The most valuable category in any timeline, and the one most often omitted |

It says once that the document will use roles rather than names, and offers to replace any individuals in your input with roles.

## What you get back

1. A summary written for somebody who was not there
2. Impact: who, how long, what they experienced, what is unrecoverable
3. **The timeline**, with sources, and gaps marked as gaps
4. **Four separate durations**: detect, acknowledge, mitigate, resolve, with what each points at
5. **Contributing factors, plural**, each with its evidence
6. Response findings, kept separate from the failure findings
7. What would have made it shorter, not only what would have prevented it
8. **Action items**, ranked, each with owner, date, verification and category
9. Recurrence check, including which earlier actions were never done
10. What is still unknown, and what would settle it

---

## Why it will not give you a root cause

Any incident worth writing up is several conditions holding at once. What changed, what was already true that made the change dangerous, what should have caught it, what made it hard to diagnose, and what made it hard to fix.

Removing any one of those might have prevented the incident or shortened it, and that is the point. **A postmortem with a single root cause stopped looking as soon as it found something**, and the conditions it did not name are all still in place. If you ask for one anyway, it will say which factor was most proximate and note plainly that the others remain.

## Four durations, not one

| Duration | What a long one points at |
|---|---|
| **Detect** | A monitoring problem. Nothing was watching the thing users care about |
| **Acknowledge** | An alerting or escalation problem. It fired and nobody saw it |
| **Mitigate** | A runbook or access problem. You knew and could not stop it quickly |
| **Resolve** | A different question entirely, and often not urgent once impact has stopped |

Collapsing these into one number hides which one you have. Fast detection with a long mitigate time is a completely different finding from the reverse. Every timestamp is converted to one timezone in code before any of this is computed, because incident timelines are routinely wrong by hours and nobody notices.

## Blameless is a technical requirement, not a courtesy

No person appears as a cause. Where a human action contributed, the finding is about the system that made that action possible or reasonable.

| Not this | This |
|---|---|
| The engineer deployed without running the tests | The pipeline allowed a deploy with failing tests, and the failure was not visible in the deploy output |
| The on-call did not check the dashboard | The alert did not link to a dashboard, and the relevant panel was on a different board |

This is not softening. A postmortem naming a person produces exactly one outcome, that person being more careful, and that fixes nothing for whoever is on call next month.

## What good output looks like

A strong postmortem is uncomfortable in the response section rather than the failure section. Most teams find the failure easier to write about, because it is about the system; the response is about them.

The action list should be short. Twelve actions from one incident means none will be done, so it ranks them and calls the rest a backlog, and it flags a list containing only prevention items because that means the response findings were ignored. If your timeline comes back with visible gaps, that is correct: a reconstructed gap becomes fact the moment it is written down.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. It converts timezones and computes durations in code rather than by eye.
2. Download this folder, or make a folder named `tech-postmortem` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Paste the evidence and say what the user experienced.

Examples that work:

- "Bridge log, alert times and the deploy record. Checkout was down 40 minutes. Write it up."
- "This is the third time this has happened. Here is the old postmortem and the new incident."
- "Customer-facing summary of this incident, for their account team."
- "The timeline does not add up. Alerts are UTC and the chat is IST."

Saying which timestamps are in which timezone is the single most useful thing you can add.

---

## How it protects accuracy

- Every timestamp is converted to one stated timezone in code, never compared by eye
- The four durations are checked against the total impact window, and any discrepancy is reported
- Every timeline entry carries a source, so a claim can be traced back
- **Gaps are marked as gaps and never filled with a plausible reconstruction**
- More than one contributing factor is named, or it states explicitly why only one applies
- No person is named as a cause anywhere in the document
- Every action item carries an owner, a date and a verification, and where this is a recurrence the earlier postmortem's incomplete actions are listed

## Limits worth knowing

- It has no access to your systems, logs, metrics or code. Everything it says about your system comes from what you gave it.
- It does not name a single root cause, and it will explain why when asked to.
- It does not name individuals as causes, and it will not produce a version that does.
- **It does not run, suggest or hand over any command.** Nothing here is meant to be executed, least of all at three in the morning.
- It does not judge whether an incident should have been avoided. It reports what the evidence shows.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It refuses to name one root cause | Deliberate, and not negotiable | Ask which factor was most proximate. It will say, and note the others remain. |
| Durations do not match your memory | Timezone mismatch in the source | State which timestamps are in which zone. This is the commonest defect. |
| Timeline has visible holes | No record existed for that window | Correct. A filled gap becomes indistinguishable from evidence. |
| Findings feel critical of the response | Response and failure are assessed separately | That split is the point. Flawless response to an unavoidable failure is a good outcome. |
| Too few action items | It ranked them and called the rest a backlog | Twelve actions from one incident means none get done. |
| No cause stated at all | The evidence does not establish one | It says what would establish it. Better than a confident wrong narrative. |

---

Part of the [Techies skills](../README.md) in the [Claude Skills Library](../../README.md).
