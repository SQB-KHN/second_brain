---
name: tech-postmortem
description: Turn incident evidence into a timeline that reconciles, contributing factors in the plural, and action items that will actually happen. Use for postmortems, RCAs or incident reviews.
---

# Incident Postmortem

The postmortem gets written by the person who was up all night, three days later, for an audience that includes their manager. So it names one root cause, the timeline has holes where nobody was taking notes, and the actions are the five things somebody thought of in the meeting. Eight months later the same incident happens and nobody connects them.

## When to use this

Trigger on: postmortem, post-mortem, RCA, root cause analysis, incident review, incident report, blameless postmortem, five whys, problem record, "write up the incident", "what actually happened".

## Before you start

Required: the raw material. Alert timestamps, chat or bridge logs, deploy records, tickets, graphs described in words, and whatever people remember.

Ask, briefly:
1. **The timezone of every timestamp, and whether they are all in one.** Logs are UTC, chat is local, the pager is something else. This is the commonest defect in a postmortem and it invalidates every duration in the document.
2. Who was involved, by role. Roles go in the document. Names do not.
3. **What the user actually experienced, and for how long**, which is usually different from what the system did and is the number leadership cares about.
4. Whether this has happened before, and the earlier postmortem if so. A recurrence is a far more serious finding than a novel failure.
5. The audience: an internal review, a customer summary, or a client or regulator deliverable.

## Roles, not names

Say once that this document will use roles rather than names, and that the analysis is about the system and the process rather than about who was on call. If the input names individuals, offer to replace them with roles. Then continue.

## Workflow

### 1. Build the timeline before forming any theory

Every entry carries a timestamp, what happened, how it was known, and the source. Distinguish four things:

- What the system did
- What the monitoring showed
- What a human did
- **What a human believed at the time**

That fourth category is what makes a postmortem useful and it is the one most often left out. "At 02:14 the on-call believed the deploy had rolled back" explains the next forty minutes. Without it the response reads as incompetent instead of reasonable.

### 2. Compute the durations in code, in one timezone

Convert every timestamp to a single stated timezone in code, never by eye. Then compute and report four separate numbers:

- **Time to detect**, from first user impact to first alert or report
- **Time to acknowledge**
- **Time to mitigate**, when impact stops
- **Time to resolve**, when the underlying issue is fixed

These point at different problems. A long detect time is a monitoring problem. Fast detection with a long mitigate time is a runbook or access problem. Collapsing them into one duration hides which one you have.

### 3. Mark what is unknown, and do not fill it

Timelines have gaps. Where nobody was taking notes, write "no record between 02:20 and 02:47" rather than constructing a plausible sequence.

A reconstructed gap becomes fact the moment it is written down, and the next reader will have no way to tell which parts were reconstructed.

### 4. Find contributing factors, plural, and refuse to name one root cause

This is the discipline that matters most, and the one that gets abandoned first. Any incident worth a postmortem is several conditions holding at once:

- What changed
- What was already true and made the change dangerous
- What was supposed to catch it and did not
- What made it hard to diagnose
- What made it hard to fix

Removing any one of these might have prevented the incident or shortened it, and that is the point. **A postmortem with a single root cause stopped looking as soon as it found something.**

### 5. Separate the failure from the response

Two distinct sets of findings, and conflating them produces the wrong actions:

- **What broke, and why it was possible.** Design, dependency, capacity, configuration, an assumption that no longer held.
- **How the response went.** Detection, escalation, diagnosis, access, tooling, communication.

A team can respond flawlessly to an unavoidable failure, or badly to a trivial one. The actions differ completely.

### 6. Keep it blameless, which is a technical requirement rather than a courtesy

No person appears as a cause. Where a human action contributed, the finding is about the system that made that action possible or reasonable:

- Not "the engineer deployed without running the tests", but "the pipeline allowed a deploy with failing tests, and the failure was not visible in the deploy output"
- Not "the on-call did not check the dashboard", but "the alert did not link to a dashboard, and the relevant panel was on a different board"

This is not softening. A postmortem that names a person produces exactly one outcome, which is that person being more careful, and that fixes nothing for the next person.

### 7. Ask what would have made it shorter, not only what would have prevented it

Prevention is one lever and often the expensive one. Also ask what would have detected it in one minute rather than twenty, what would have made the cause obvious, and what would have let anyone on the team mitigate it rather than only the person who knew.

Most of the recoverable time in a long incident is diagnosis, and almost no postmortem produces an action against it.

### 8. Write action items that will actually happen

Each one: what specifically changes, who owns it, by when, and how anyone will know it is done. Then mark each as prevention, detection, mitigation or documentation. **A list containing only prevention items means the response findings were ignored.**

Be honest about volume. Twelve actions from one incident means none will be done. Rank them, name the two that matter, and say plainly that the rest are a backlog.

Where this incident recurred, check the earlier postmortem's actions and report which were never completed. That is usually the most important finding in the document.

### 9. Never speculate beyond the evidence

Where the cause is not established, say so and say what would establish it. "The connection pool exhausted and we do not yet know what held the connections; the next step is X" is a better postmortem than a confident narrative that turns out to be wrong.

## Output format

**1. Summary.** What happened, who was affected, for how long, and the state now. Four lines, for someone who was not there.

**2. Impact.** Users affected, duration, what they experienced, and anything unrecoverable.

**3. Timeline.** Timestamp, event, source, and what was believed at the time. Gaps marked as gaps.

**4. The four durations.** Detect, acknowledge, mitigate, resolve, with what each points at.

**5. Contributing factors.** Plural, each with its evidence.

**6. Response findings.** Kept separate from the failure findings.

**7. What would have made it shorter.** Detection, diagnosis, mitigation.

**8. Action items.** Ranked, each with owner, date, verification and category.

**9. Recurrence check.** Earlier incidents, and which of their actions were never done.

**10. What we still do not know**, and what would settle it.

## Checks to run before delivering

- Every timestamp is converted to one stated timezone, in code rather than by eye
- The four durations are consistent with the total impact window, and any discrepancy is reported
- Every timeline entry carries a source
- Gaps are marked as gaps and never filled with a reconstruction
- More than one contributing factor is named, or the output states explicitly why only one applies
- No person is named as a cause anywhere in the document
- Every action item has an owner, a date and a verification
- Actions are categorised, and a list containing only prevention items is flagged
- Where this is a recurrence, the earlier postmortem's incomplete actions are listed

## What this skill does not do

- It has no access to your systems, logs, metrics or code. Everything it says about your system comes from what you gave it.
- It does not name a single root cause, and it will explain why when asked to.
- It does not name individuals as causes, and it will not produce a version that does.
- It does not run, suggest or hand over any command. Nothing here is meant to be executed, least of all at three in the morning.
- It does not judge whether an incident should have been avoided. It reports what the evidence shows.
