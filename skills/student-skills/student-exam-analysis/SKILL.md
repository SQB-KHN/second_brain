---
name: student-exam-analysis
description: Turn past papers into weightage by marks, reliability bands, repeated question patterns and a strategy for what to finish first. Use for past papers, weightage or exam pattern.
---

# Past Paper and Weightage Analysis

The syllabus lists twelve chapters and implies they matter equally. The exam does not agree, and it has been saying so for ten years in the past papers nobody analysed. Most students work in syllabus order until time runs out, so the last chapters get nothing, and nobody checked whether those were the ones carrying the marks.

## When to use this

Trigger on: past papers, previous year questions, PYQ, weightage, exam pattern, important chapters, marks distribution, question trends, blueprint, "what comes in the exam", "which topics matter", "what should I study first".

## Before you start

Required: past papers, or the question lists from them. Three years is a minimum, five or more is better.

Ask, briefly:
1. **Which exam exactly, and which paper.** Patterns differ between boards, streams and sessions, and one exam's pattern tells you nothing about a different level of the same exam.
2. Marks per question, and whether there is negative marking. Negative marking changes what attempting everything is worth, and it changes the whole strategy.
3. **Whether the pattern changed in this period.** A syllabus revision or a format change makes older papers useful for topics and misleading for structure. Split the analysis at that point.
4. Total marks, duration and question count, so time per mark can be computed.
5. Whether they have the syllabus, so coverage can be compared against what actually appears.

## Check for personal data first

Past papers carry none. If a marksheet or a rank card is uploaded alongside, say once that this analysis works on the papers rather than on their scores, and that mistake analysis is the skill for their own results.

## Workflow

### 1. Profile what you were given

- Which years and sessions, and whether any paper is incomplete
- **The same paper appearing twice under different names**, which is common with shift-based exams
- Whether questions are numbered consistently, so any claim can be traced back
- Whether the pattern changed within the period, and exactly where

State paper count, question count, total marks covered, and anything excluded.

### 2. Compute in code, never in prose

Every count, share and marks-per-topic figure runs as Python. A weightage table worked out by eye is exactly how a student ends up trusting the wrong chapters for six months.

### 3. Tag every question twice

- **By topic**, at the level a student actually studies. Not "Physics" but "rotational motion", and the sub-topic where possible.
- **By what it asks for:** recall a fact, apply a standard method, apply in an unfamiliar situation, or combine two topics. This second tag tells a student *how* to study, not just what.

Where a question spans two topics, count it in both and state that totals will exceed 100 percent for that reason. Do not silently pick one.

### 4. Build the weightage table in marks, not in counts

Report marks per topic per year, and the average. **Counts mislead.** Ten one-mark questions and two five-mark questions carry the same marks and need completely different preparation.

Then compute what almost nobody has: **marks per topic against the time that topic takes to learn.** That ranks topics by return rather than by size, which is the ranking that should drive a study plan.

### 5. Separate the reliable from the occasional

- **Every year.** Guaranteed marks. Not optional, and they should be finished first.
- **Most years.** Reliable enough to plan around.
- **Occasional.** Appeared once or twice. Worth knowing, not worth equal effort.
- **Never appeared.** In the syllabus, absent from the papers. **Name these explicitly**, because deciding not to study something is a decision students are never given permission to make, and it is where their time comes from.

Be careful with the last band. Say plainly that absence from past papers is not a guarantee of absence this year, and that anything foundational for other topics has to be studied regardless of whether it is examined directly.

### 6. Find what repeats, and how

- Questions repeating almost verbatim
- Questions repeating in structure with the numbers changed
- **The standard variations of a single idea**, which is the most useful pattern of all, because it turns twenty questions into one method

State the specific years for anything claimed as a repeat, so it can be checked.

### 7. Analyse the shape of the paper, not only its content

Marks by difficulty where it can be inferred. Where the easy marks sit, and whether they are spread or clustered. Time per mark, and which sections take longer than their marks justify. For negative marking, the accuracy rate at which a guess becomes worthwhile, computed rather than asserted.

### 8. Turn it into a strategy

What to finish first and why. What to leave, and what leaving it costs if it appears. Where marks per hour are highest. Anything recently changed in the pattern.

State plainly what share of the paper the reliable topics carry. "The eleven topics appearing every year are 68 percent of the paper" is the sentence that changes how somebody studies.

## Output format

**1. Headline.** What share of marks the reliable topics carry, and the two highest-return topics.

**2. Weightage table.**

| Topic | Marks per year | Average | Share | Appears in |

**3. Reliability bands.** Every year, most years, occasional, never appeared.

**4. What it asks for.** Share of marks by recall, standard application, unfamiliar application, combined topics.

**5. Repeats and variations.** With years, so they can be checked.

**6. Paper shape.** Difficulty spread, where the easy marks are, time per mark.

**7. Negative marking arithmetic**, where it applies.

**8. Strategy.** What to finish first, what to leave, and what leaving it costs.

**9. Data notes.** Papers used, pattern changes, questions counted in two topics.

## Checks to run before delivering

- Marks per topic sum to each paper's total, and questions counted in two topics are stated as such
- Weightage is reported in marks, with counts shown separately and labelled
- Every reliability band states its years, so a student can verify it
- Pattern changes within the period are identified, and the analysis is split at them
- Negative marking arithmetic is computed rather than asserted
- Anything named "never appeared" carries the warning that absence is not a guarantee
- Foundational topics are flagged as required regardless of direct weightage
- Papers excluded or found duplicated are stated

## What this skill does not do

- It does not predict what will be asked this year. It reports what has been asked, and how reliably.
- It does not tell you to skip anything. It shows the return on each topic and what leaving it would cost. The decision is yours.
- It does not know your syllabus, your board's current pattern, or a change announced this year. Supply them.
- It cannot see papers you do not give it, and three years is a thin sample. It will say when the sample cannot support a claim.
- It does not solve the questions or teach the topics.
