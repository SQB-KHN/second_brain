---
name: edu-assessment-analysis
description: Turn a question-wise mark sheet into item statistics, topic and cognitive-level gaps, groups by what students missed, and a triaged reteach plan. Use for test analysis.
---

# Assessment and Item Analysis

The marks get entered, the average gets announced, and the class moves on. Buried in that mark sheet is the only thing worth knowing: which ideas the class did not learn, which questions failed to measure anything at all, and which students need something different next week. Almost nobody extracts it, because by hand it costs an evening per test.

## When to use this

Trigger on: item analysis, question-wise analysis, test analysis, marks analysis, class performance, difficulty index, discrimination index, what to reteach, weak areas, remedial list, "why did the class do badly", "who is struggling".

## Before you start

Required: marks at question level, per student. Roll numbers or initials are enough.

Ask, briefly:
1. **Maximum marks per question, and the topic and cognitive level each question tested.** Without the topic map this becomes arithmetic rather than a diagnosis.
2. Whether an earlier test on overlapping topics exists, so movement can be measured rather than one snapshot described.
3. Class size, and whether more than one section sat the same paper. Two sections on one paper is the strongest comparison available, because it separates the teaching from the paper.
4. What the assessment was for: diagnostic before teaching, formative during, or summative at the end. It changes what a low score means.
5. Whether any student had an accommodation, so their marks are read correctly rather than flagged as an outlier.

## Check for student data first

Name which columns identify a student: name, admission number, parent contact, date of birth.

Say once that **this analysis needs an identifier, not a name.** Roll numbers or initials work throughout. Offer to run on a de-identified file. Say also that the output is written for the teacher and will not produce a characterisation of any student. Then continue with whatever they choose, without repeating it.

## Workflow

### 1. Profile the mark sheet

- **Marks above the maximum** for a question. That is a data entry error, not a finding.
- **Blank against zero.** A blank may be unattempted, absent or unmarked, and the three mean different things. Ask which, and never treat a blank as zero silently.
- **Choice questions**, where not every student attempted the same items. Item statistics there are computed only on attempters, and the attempt count is stated.
- **Bonus, grace and moderation marks**, which distort every statistic. Keep the raw score separate from the awarded score and say which was used.
- Students absent for the test, and a total column that does not equal the sum of its parts

State student count, question count, paper maximum, and everything excluded with its count.

### 2. Compute in code, never in prose

Every index, mean, percentage and correlation runs as Python. Item statistics done by eye are the reason most mark sheets get summarised as an average and nothing else.

### 3. Compute item statistics, then separate the two findings they distinguish

For each question: **difficulty index** (the proportion who got it right, reported as a percentage, with the direction spelled out because the name reads backwards to almost everybody), **discrimination index**, mean marks, spread, and attempt rate kept separate from success rate.

Then make the distinction that carries this whole skill:

- **The class did not learn it.** Low difficulty, positive discrimination. The question worked. The teaching or the learning did not.
- **The question did not work.** Low or negative discrimination. Strong students got it wrong at a similar rate to weaker ones, which usually means it was ambiguous, mis-keyed, or tested something never taught. **That is a paper problem, not a class problem**, and reteaching on its evidence is wasted time.

A negative discrimination index is the single most useful number on the page, and almost nobody computes it.

### 4. Roll up to topic and cognitive level

- Performance by topic, ranked, weighted by the marks available
- Performance by cognitive level: recall, understanding, application, higher order. **A class that scores well on recall and collapses on application has a specific, addressable problem**, and the marks total hides it entirely.
- Where a topic is measured by one question only, say so. One question is not a measurement of a topic.

### 5. Group students by what they missed, not by rank

Rank orders are what a mark sheet already gives. What a teacher cannot get is grouping by gap:

- Students who missed the same topic, listed together, because they can be taught together
- Students whose profile is uneven, strong on some topics and weak on others, which points at content rather than capability
- Students whose attempt rate was low, which is a time, confidence or reading-speed issue rather than a knowledge one and needs a completely different response

**Describe the gap, never the student.** "Fourteen students lost most of their marks on the questions requiring equations to be balanced" is a finding. "Fourteen weak students" is a label and does not appear anywhere in the output.

### 6. Check whether the paper itself was sound

Total marks against the blueprint where one exists. Whether the difficulty spread was reasonable or the paper was uniformly easy or hard. Whether total scores spread out at all. Ceiling and floor effects, since everybody near full marks measures nothing and so does everybody near zero. Time feasibility, where length and duration are known.

### 7. Say what to reteach, and be honest about the cost

Rank by marks at stake and by how foundational the topic is for what comes next. Then state how much teaching time that would take against what actually exists.

A list of nine reteach topics in a term with two spare periods is not a plan. Name what will not be retaught and what that means, rather than listing everything and leaving the triage to somebody at ten at night.

### 8. Never predict

No projected board score, no predicted rank, no statement about what a student is capable of. This data describes one paper on one day.

## Output format

**1. Headline.** Class mean and spread, the two topics with most marks lost, and any question that did not work.

**2. Item statistics.**

| Q | Max | Topic | Level | Attempted | Mean | Difficulty | Discrimination | Verdict |

**3. Questions that did not work.** Separated out, with what is likely wrong and the instruction not to reteach on their evidence.

**4. Topic performance.** Ranked by marks lost, weighted by marks available.

**5. Cognitive level performance.** With what the pattern implies for teaching.

**6. Groups by gap.** Students grouped by what they missed, described by the gap.

**7. Attempt patterns.** Where low attempt rate rather than wrong answers drove the loss.

**8. Was the paper sound.** Blueprint, spread, discrimination, ceiling and floor effects, timing.

**9. Reteach plan, triaged.** Against the time actually available, with what is being dropped.

**10. Data quality and exclusions.**

Offer the Excel version with one sheet per view. Build it only if asked.

## Checks to run before delivering

- Question marks sum to each student's total, and to the paper maximum
- No mark exceeds its question maximum, and any that does is reported as a data error
- Blanks are classified as unattempted, absent or unmarked, never silently treated as zero
- Choice-question statistics are computed on attempters only, with the attempt count stated
- Raw and moderated scores are kept separate, and the output states which was used
- Every difficulty index states its direction, since the name reads backwards
- Discrimination is computed for every question, and negative values are surfaced rather than buried
- Absent students are excluded from item statistics with the count stated
- No student is described by anything other than the specific gap in their work

## What this skill does not do

- It does not assign, change or moderate marks. The mark is the teacher's.
- It does not predict a future score, a rank or a board result, and it does not say what a student is capable of. It describes one paper on one day.
- It does not identify, suggest or rule out a learning difficulty. Where a pattern is unusual it describes the pattern and names who in the school is qualified to look at it.
- It does not rank students for streaming, section or placement decisions.
- It cannot see the answer scripts, so it reports what the marks show, not why one student wrote what they wrote.
