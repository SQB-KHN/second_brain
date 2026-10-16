# Assessment and Item Analysis

Turns a question-wise mark sheet into item statistics, topic and cognitive-level gaps, students grouped by what they missed, and a reteach plan triaged against the time you actually have.

---

## Who this is for

Anyone who sets tests and has to act on the results: school teachers across all subjects, coaching and test-prep faculty, college lecturers, heads of department and academic coordinators, exam cells, and tutors tracking a handful of students.

## The problem it solves

The marks get entered, the average gets announced, and the class moves on.

Buried in that mark sheet is the only thing worth knowing. Which ideas the class did not learn. Which questions failed to measure anything at all. Which students need something different next week, and which ones can be taught together because they missed the same thing.

By hand this means a difficulty and discrimination index for every question, a question-to-topic map, then students cross-tabulated against gaps. An evening per test, so it does not happen; what happens instead is an average, a list of toppers, and a sense that the class found it hard. This does it in one pass, and does the one thing that changes a teacher's week: it separates "the class did not learn this" from "that question was broken".

---

## What you give it

**Minimum:** marks at question level, per student. Roll numbers or initials are enough.

| Extra data | What it unlocks |
|---|---|
| **Topic and cognitive level per question** | Turns arithmetic into a diagnosis. Without it there is no topic or level analysis at all |
| Maximum marks per question | Weighted analysis, so a two-mark gap is not treated like a ten-mark one |
| **An earlier test on overlapping topics** | Movement rather than a snapshot |
| **A second section on the same paper** | The strongest comparison available, because it separates the teaching from the paper |
| The blueprint, and what the assessment was for | Blueprint compliance and paper soundness, and a low score read diagnostically rather than summatively |

**Handled automatically:** marks above a question maximum, blanks distinguished from zeros, absent students excluded from item statistics, choice questions computed on attempters only, bonus and moderation marks kept separate from raw scores, totals that do not equal the sum of their parts, header rows and Indian digit grouping.

**It names the identifying columns first** and offers to run de-identified. Roll numbers work throughout; it needs an identifier, not a name.

## What you get back

1. Class mean and spread, the two topics with most marks lost, and any question that did not work
2. **Item statistics per question**: difficulty, discrimination, attempt rate, mean, verdict
3. **Questions that did not work**, separated out, with the instruction not to reteach on their evidence
4. Topic performance, ranked by marks lost and weighted by marks available
5. **Cognitive level performance**, and what the pattern implies for teaching
6. **Students grouped by what they missed**, described by the gap
7. Attempt patterns, where low attempt rate rather than wrong answers drove the loss
8. Whether the paper itself was sound
9. **A reteach plan triaged against the time you have**, with what is being dropped
10. Data quality and exclusions

An Excel version with one sheet per view is offered at the end.

---

## The distinction that changes your week

Two situations produce an identical low score and need opposite responses.

| | The class did not learn it | The question did not work |
|---|---|---|
| **Difficulty index** | Low | Low |
| **Discrimination** | Positive | Low or negative |
| **What it means** | The question worked, the learning did not | Strong students got it wrong at the same rate as weak ones |
| **Usual cause** | Teaching, practice or prerequisites | Ambiguous wording, a mis-keyed answer, or something never taught |
| **What to do** | Reteach it | Fix the paper. Reteaching here is wasted time |

**A negative discrimination index is the single most useful number on the page**, and almost nobody computes it. It is the mark sheet telling you the problem is the paper's, not the class's. One note on naming: the difficulty index reads backwards to most people, because a *high* index means an *easy* question, so the output spells out the direction every time.

## It groups by gap, not by rank

A mark sheet already gives you a rank order. What it cannot give you is who can be taught together.

So students come back grouped by what they missed: the fourteen who lost marks on the same topic, the ones whose profile is uneven rather than uniformly low, and the ones whose loss came from not attempting rather than answering wrongly. That last group needs a different response entirely, usually about time or confidence rather than knowledge. **Every group is described by the gap, never by a label.** "Fourteen students lost most of their marks on questions requiring equations to be balanced" is a finding. "Fourteen weak students" does not appear anywhere in the output, in any form.

## What good output looks like

A strong result names a broken question. Most papers have at least one, and finding it is worth more than the rest of the analysis, because it stops you reteaching something the class may well already know.

The reteach plan should be uncomfortable. It ranks by marks at stake against how foundational a topic is, states the teaching time needed against what exists, and names what is being dropped. Nine reteach topics for a term with two spare periods is not a plan, and it will say so. If the analysis comes back thin, the question-to-topic map was missing. Without it there is no topic view and no cognitive-level view, and what remains is a well-computed set of question statistics.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill computes item statistics and will not do it in prose.
2. Download this folder, or make a folder named `edu-assessment-analysis` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the mark sheet and say what each question tested.

Examples that work:

- "Unit test marks, question-wise, 38 students. Question topics attached. What do I reteach?"
- "Class average dropped 11 marks from the last test. Same topics. What happened?"
- "Two sections wrote this paper and the results are very different. Is that the paper or the teaching?"
- "I have two spare periods before the term exam. What is worth reteaching?"

Supplying the topic and cognitive level per question roughly triples what it can tell you.

---

## How it protects accuracy

- Question marks are proved to sum to each student's total and to the paper maximum
- Any mark above its question maximum is reported as a data entry error rather than analysed
- **Blanks are classified as unattempted, absent or unmarked**, and never silently treated as zero
- Choice-question statistics are computed on attempters only, with the attempt count stated
- Raw and moderated scores are kept separate, and every difficulty index states its direction since the name reads backwards
- Discrimination is computed for every question, and negative values are surfaced rather than buried
- No student is described by anything other than the specific gap in their work

## Limits worth knowing

- It does not assign, change or moderate marks. The mark is yours.
- It does not predict a future score, a rank or a board result, and it will not say what a student is capable of. It describes one paper on one day.
- It does not identify, suggest or rule out a learning difficulty. Where a pattern is unusual it describes the pattern and names who in your school is qualified to look.
- It does not rank students for streaming, section or placement decisions.
- It cannot see the scripts, so it reports what the marks show, not why one student wrote what they wrote.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| No topic or level analysis | Question-to-topic map not supplied | Add it. It is the input that changes the output most. |
| A question flagged as not working | Negative or near-zero discrimination | Usually genuine. Reread the wording before reteaching anything. |
| Fewer students than you expected | Absentees excluded from item statistics | The count is stated. Item statistics on absentees would be wrong. |
| Statistics look odd on one question | It was a choice question | Computed on attempters only, with the attempt count shown. |
| Difficulty index seems inverted | The name genuinely reads backwards | High index means easy. The output spells this out each time. |
| It will not name weak students | Deliberate, and not negotiable | You get groups by gap, which is what you can actually teach to. |

---

Part of the [Educators skills](../README.md) in the [Claude Skills Library](../../README.md).
