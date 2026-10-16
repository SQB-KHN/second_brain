# Mistake Analysis

Classifies every wrong answer as concept, application, execution or time, finds the pattern across several tests, and gives you three fixes ranked by the marks they recover.

---

## Who this is for

Anyone who takes practice tests and wants the score to move: competitive exam aspirants across engineering, medical, civil services, management and banking, class 11 and 12 students taking regular mocks, undergraduates in continuous assessment, and anybody whose scores have plateaued despite practising more.

## The problem it solves

You review a test by looking at what you got wrong, feeling bad about it, and moving on.

Nothing changes. The same mistakes appear in the next test, and the pattern that would have been obvious across four tests stays invisible because nobody wrote it down. So the response to a flat score is to practise more, which repeats the same errors at higher volume.

The single biggest reason this fails is one word. **"Silly mistake" is not a category.** It is what students call execution errors, and calling them silly implies they are random and unfixable, which is precisely why they never get fixed; they are usually a repeatable process failure with a specific cause and a specific habit that removes it. Doing this properly means classifying every error by what actually went wrong and tracking it across tests, which is the habit separating people who improve from people who practise a lot.

---

## What you give it

**Required:** your wrong answers, and enough of each question to know what was asked.

| Context | Why it matters |
|---|---|
| **What you were thinking when you did it** | The whole input, and the one students skip. Only you have it |
| Whether the test was timed and whether you finished | Untimed tells you about knowledge; timed tells you about knowledge and speed |
| **Earlier test data** | One test is a description. Several tests are a pattern, which is where the value is |
| Negative marking rules, and which ones you guessed correctly | Changes what a wrong attempt cost against a skipped one, and guessed-correct data predicts the next mistake |

A list of wrong question numbers produces a topic list, not an analysis. The reasoning is the input.

## What you get back

1. Marks lost by error type, and the biggest recoverable group
2. **The four-way breakdown**: concept, application, execution, time, and **where your own classification was changed**, with the reason
4. Patterns by topic, by type, by position in the paper, and by repetition across tests
5. **Execution errors grouped, with the process fix for each group**
6. Guessed-correct answers counted as gaps, with the negative marking arithmetic
7. Skipped analysis: right calls, wrong calls, and what they cost
8. **Three or four actions**, ranked by marks recoverable, and what is not being fixed this cycle
9. A log format so it accumulates

---

## Four categories, and each needs a different fix

| Category | What happened | The fix |
|---|---|---|
| **Concept** | You did not know it, or knew it wrong | Study |
| **Application** | You knew the concept and did not see this question needed it | Practice on varied question forms, **not re-reading the concept** |
| **Execution** | You knew what to do and erred doing it | A process change, not more study |
| **Time** | You could have got it and did not have the minutes | Strategy, not knowledge |

Getting the category wrong wastes the cycle. Studying harder does nothing for an application problem, and no amount of practice fixes a sign convention you never write down.

## It will argue with your classification

Students over-classify as execution and under-classify as application, consistently and in one direction. Calling something a silly mistake is more comfortable than admitting the method was not solid, and the same question type then keeps failing.

So there is a test, and it gets applied: **if you had unlimited time and could redo it now, without looking anything up, would you get it right?** If not, it was not execution. Any reclassification comes with its reason attached, so you can disagree with the specific case rather than with the finding.

## Execution errors are the cheapest marks you will ever recover

They get grouped, because each group has a different habit that removes it:

| Error group | The habit |
|---|---|
| Sign errors | Write the sign convention at the top of the page |
| Unit errors, and transcription between lines | Box the final answer and check units, and re-read the line you copied from |
| Misreading the question, or answering the wrong part | Underline what is actually being asked, and read the question twice before starting |

**Recovering these requires no new knowledge**, which makes them the fastest score improvement available and the one students spend least time on.

## The data students throw away

**Right but guessed.** A correct guess is a wrong answer that has not happened yet. It gets counted as a gap and filed with your concept errors, and where negative marking applies the arithmetic usually disagrees with your impression of how well you guess.

**Skipped questions.** Skipped and would have got it is a time or confidence problem; skipped and would not have is a correct decision worth confirming; attempted and lost marks where skipping was better is a strategy error. Almost no student reviews any of this.

## What good output looks like

A strong analysis reclassifies at least one of your "silly mistakes" and shows you why. That is uncomfortable and it is the finding, because the same question type will fail again unless the method gets fixed. The action list should be three or four items, not eleven, with a clear statement of what is deliberately not being fixed this cycle. And if the patterns section labels something as a single instance rather than a pattern, that is correct: **one instance is noise**, and treating it as a trend is how students restudy a topic they already knew.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. It counts marks by category and computes the negative marking arithmetic.
2. Download this folder, or make a folder named `student-mistake-log` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Give it the wrong answers and, crucially, what you were thinking.

Examples that work:

- "18 wrong in this mock. For each one, here is what I thought at the time."
- "My score has been flat for four tests. Here are all four. What is the pattern?"
- "I keep making silly mistakes. Are they actually silly?"
- "Negative marking is one quarter. Has my guessing helped or hurt?"

Saying what you were thinking is the difference between an analysis and a list of topics.

---

## How it protects accuracy

- Every mistake is classified into exactly one of four categories, and marks by category are proved to sum to total marks lost
- Any reclassification of your own label is stated with its reason, so you can disagree with the case
- **Patterns are claimed only where something appears more than once**, and single instances are labelled as single instances
- Guessed-correct answers are counted as gaps rather than successes, and negative marking arithmetic is computed rather than asserted
- Actions are limited to three or four, with what is not being fixed stated explicitly
- **The word "silly" does not appear as a category anywhere in the output**

## Limits worth knowing

- It does not predict your next score or your rank.
- **It cannot classify a mistake without knowing what you were thinking.** Question numbers alone produce a topic list.
- It does not teach the topics behind your concept errors. It tells you which ones they are.
- It does not accept "silly mistake" as an explanation, and it will ask the question that tests whether it was one.
- It does not judge you on a score, and a rank is not an input it needs.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It reclassified your silly mistakes | The redo test said otherwise | Uncomfortable and usually right. The reason is stated per case. |
| Only a topic list came back | You gave question numbers, not reasoning | Say what you were thinking on each. That is the input. |
| No pattern found | One test only | Patterns need several. Add earlier tests. |
| It counted a correct answer as a gap | You marked it as guessed | A correct guess is a wrong answer that has not happened yet. |
| Only three actions, and it ignored your rank | Both deliberate | Eleven actions is a list nobody works on, and it works on errors rather than placement. |

---

Part of the [Students skills](../README.md) in the [Claude Skills Library](../../README.md).
