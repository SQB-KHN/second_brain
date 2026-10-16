# Past Paper and Weightage Analysis

Turns past papers into weightage measured in marks, reliability bands, the questions that repeat, and a strategy for what to finish first and what to leave.

---

## Who this is for

Anyone preparing for an exam with a history: class 9 to 12 students across boards, competitive exam aspirants for engineering, medical, civil services, management and banking, undergraduates and postgraduates facing university papers, working professionals taking certifications, and anybody self-studying without a coaching institute doing this for them.

## The problem it solves

The syllabus lists twelve chapters and implies they matter equally. The exam has disagreed for ten years, in the past papers nobody analysed.

So students work in syllabus order until time runs out. The last chapters get nothing, and nobody checked whether those were the ones carrying the marks. Meanwhile a chapter that appears every single year, worth eight marks reliably, sits unfinished because it happened to be chapter eleven.

Good coaching does this analysis. Self-studying students almost never do, because it means tagging several hundred questions by topic and by what they ask for, then counting marks rather than questions. That is two full days, and it feels like time not spent studying.

**It is the highest-return two days in any preparation**, because it decides where every remaining hour goes.

---

## What you give it

**Minimum:** past papers, or the question lists from them. Three years, five or more is better.

| Extra input | What it unlocks |
|---|---|
| **Marks per question** | Weightage in marks rather than counts, which is the only version that matters |
| **Whether the pattern changed, and when** | The analysis gets split there. Old papers stay useful for topics and become misleading for structure |
| Negative marking rules | The accuracy rate at which guessing becomes worthwhile, computed rather than asserted |
| Total marks, duration, question count | Time per mark, and which sections cost more time than their marks justify |
| Your syllabus | Coverage compared against what actually appears, including what never does |

**Handled automatically:** the same paper appearing twice under different names, which is common with shift-based exams; incomplete papers; inconsistent numbering; and questions that span two topics, which get counted in both with the overlap stated.

## What you get back

1. What share of marks the reliable topics carry, and the two highest-return topics
2. **A weightage table in marks**, per year and averaged
3. **Reliability bands**: every year, most years, occasional, and never appeared
4. What the paper asks for: recall, standard application, unfamiliar application, combined topics
5. **Repeats and variations**, with the years so you can check them
6. Paper shape: difficulty spread, where the easy marks sit, time per mark
7. Negative marking arithmetic where it applies
8. **A strategy**: what to finish first, what to leave, and what leaving it costs

---

## Marks, never counts

Ten one-mark questions and two five-mark questions carry identical weight and need completely different preparation. A count-based weightage table tells you the first topic is five times more important, which is wrong in a way that costs a month.

Everything here is computed in marks, with counts shown separately and labelled. And where you can estimate how long a topic takes to learn, it computes **marks per hour of study**, which ranks topics by return rather than by size.

## The four reliability bands

| Band | What to do with it |
|---|---|
| **Every year** | Guaranteed marks. Not optional, and they should be finished first |
| **Most years** | Reliable enough to plan around |
| **Occasional** | Worth knowing about, not worth equal effort |
| **Never appeared** | In the syllabus, absent from the papers |

That last band is the one students are never given permission to look at, and it is where their time comes from.

It comes with two warnings that are not softening. **Absence from past papers is not a guarantee of absence this year.** And anything foundational for other topics has to be studied regardless of whether it is examined directly, because you cannot skip the thing that three examined topics rest on.

## The pattern that turns twenty questions into one method

Beyond verbatim repeats, the useful finding is the set of standard variations on a single idea. The same concept, asked four ways across six years, with the numbers and the wording changed.

Recognising that turns what looks like twenty separate questions into one method with four faces, which is the difference between memorising solutions and being able to answer something you have not seen.

## What good output looks like

A strong analysis produces one sentence that changes how you study: "The eleven topics appearing every year are 68 percent of the paper."

It should also name at least one thing in your syllabus that has never appeared, and be honest about the risk of leaving it. If everything comes back as important, the sample was too small; three years is a minimum and five is where the bands become trustworthy.

If a topic you were confident about turns out to be occasional, check the years before acting. The analysis states them precisely so you can verify rather than trust it.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. It counts and computes rather than estimating.
2. Download this folder, or make a folder named `student-exam-analysis` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Paste the papers and say which exam.

Examples that work:

- "Six years of past papers, class 12 physics, CBSE. Where are the marks?"
- "I have two months and cannot finish the syllabus. What is safe to leave?"
- "Which questions repeat in this exam, and how much do they change?"
- "The pattern changed in 2023. Analyse before and after separately."
- "Negative marking is one quarter. At what accuracy is guessing worth it?"

Telling it whether the pattern changed, and when, is the input that most affects whether the analysis is trustworthy.

---

## How it protects accuracy

- Marks per topic are proved to sum to each paper's total
- Questions spanning two topics are counted in both, with the overlap stated rather than one topic silently chosen
- **Weightage is reported in marks**, with counts shown separately and labelled as counts
- Every reliability band states its years, so any claim can be checked against the papers
- Pattern changes are identified and the analysis is split at them
- Negative marking arithmetic is computed rather than asserted
- Anything named "never appeared" carries the warning that absence is not a guarantee
- Duplicate papers from shift-based exams are found and reported

## Limits worth knowing

- **It does not predict what will be asked this year.** It reports what has been asked and how reliably.
- It does not tell you to skip anything. It shows the return on each topic and what leaving it would cost.
- It does not know your syllabus, your board's current pattern, or a change announced this year. Supply them.
- Three years is a thin sample, and it will say when the sample cannot support a claim.
- It does not solve the questions or teach the topics.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Everything looks important | Sample too small | Three years is a minimum. Five is where the bands become trustworthy. |
| Weightage differs from your coaching notes | Yours may be count-based, not marks-based | Check which. Counts and marks give different answers. |
| A topic marked "never appeared" | It genuinely has not, in your papers | Check whether it is foundational for others before leaving it. |
| Two papers look identical | Shift-based exam, same paper under two names | It reports the duplicate rather than double-counting. |
| Bands disagree across years | The pattern changed in that period | Say when, and it splits the analysis there. |
| It will not tell you what will come | Nobody can, and it says so | You get reliability instead, which is what you can plan against. |

---

Part of the [Students skills](../README.md) in the [Claude Skills Library](../../README.md).
