# Question Paper and Blueprint

Builds a paper to a blueprint you confirm first, or reviews an existing one against it, applying the item quality rules and checking whether it can actually be finished in the time given.

---

## Who this is for

Anyone who sets assessments: school teachers across subjects, coaching and test-prep faculty, college lecturers, heads of department reviewing other people's papers, exam cells and academic coordinators, and corporate trainers writing module assessments.

## The problem it solves

A question paper gets written the week it is needed, from memory. Then the blueprint is reverse-engineered afterwards to match whatever got written.

Three things follow, reliably. The paper over-tests whatever the writer finds interesting. The marks do not line up with the teaching time spent, which students notice immediately and resent. And two ambiguous questions are discovered simultaneously by two hundred candidates, which is the worst possible moment and the least recoverable.

The discipline that prevents all of it is thirty years old and well documented: blueprint first, questions written to cells, item rules applied to each, time tested before it goes out. It gets skipped because doing it properly costs longer than writing the paper.

---

## What you give it

**Minimum:** the topics to be tested, the total marks, and the duration.

| Extra input | What it unlocks |
|---|---|
| **The prescribed blueprint or format** | It follows yours exactly rather than proposing a better one. Board and institutional formats are not up for improvement |
| The class, board or curriculum | Command words, expected answer length and mark conventions all differ |
| **Teaching time actually spent per topic** | The honest basis for weightage, and almost never used. Six periods taught and two marks tested is a mismatch students feel |
| What the paper is for | Practice, unit test, term exam or diagnostic all need different difficulty spreads |
| Question types to include or avoid | Stops it producing a format your students have never seen |
| An existing paper | Switches it into review mode |

## What you get back

1. **The blueprint grid**, topics against cognitive levels, with the margins checked
2. The paper, formatted as students will receive it
3. **Question map**: topic, level, marks, expected creditable points, estimated time
4. **The marking scheme**, written with the paper, including the alternative answers a real class produces
5. Time analysis, per section and total, against the duration
6. Item quality notes, including anything that needed a compromise
7. In review mode: a verdict, blueprint compliance as found, per-question findings, mark arithmetic, coverage and timing

---

## The blueprint comes first, and that is the whole point

Rows are topics. Columns are cognitive levels. Cells carry the marks. Then the margins get checked:

- **Topic totals** against teaching time or prescribed weightage
- **Cognitive level totals.** A paper that is 80 percent recall tests memory and predicts nothing about understanding, and it is exactly what a paper written from memory produces
- **Question type totals** against the prescribed format

The grid is shown and confirmed before a single question is written. Writing first and reverse-engineering the blueprint is the failure this prevents, and it is what almost every paper does.

Then each question is written **to a cell**, with the cognitive level as a design constraint rather than a label added afterwards. The command word has to match: "explain" on a question answerable by naming three things is a recall question wearing an understanding label, and the blueprint it fills is fiction.

## The item rules, each one checkable

| Rule | The failure it prevents |
|---|---|
| **One thing at a time** | A question testing two ideas cannot be part-marked fairly, so a student with one and not the other gets an arbitrary score |
| **No ambiguity** | Read it as a student who knows less than you. If two readings exist, one gets defended in the staff room afterwards |
| **No unintended cues** | Option length, grammatical agreement, "all of the above", and a correct option more detailed than the rest |
| **Plausible distractors** | Options nobody picks turn a four-option question into a two-option one |
| **No dependency chains** | Getting (a) wrong should not make (b) and (c) unanswerable. One error, one loss |
| **Nothing outside syllabus** | Including in the stem and the context |
| **Fair context** | A word problem set in a context only some students recognise tests the context |

Marks then get allocated to match the work rather than habit: a three-mark question needs three creditable points or three steps, and where the mark and the work disagree, one of them is wrong.

## The time check almost nobody runs

Each question gets a time estimate, summed, plus reading and checking time, compared against the duration.

Papers are routinely set that cannot be finished, and the result measures writing speed rather than learning. Where the estimate exceeds the duration it says so, and says what to cut.

## What good output looks like

In build mode, a strong result is uncomfortable at the blueprint stage rather than at the end. It usually shows that the intended paper is heavier on recall than you thought, or that a topic taught for two weeks is carrying four marks.

In review mode, a strong result finds a dependency chain or an ambiguous stem you had read past. Writers cannot see their own ambiguity, because they know what they meant, which is exactly why review mode exists.

The marking scheme should contain answers you did not expect. A scheme written before the scripts arrive is a scheme that holds; one written afterwards gets bent to fit them.

---

## Installing it

1. Download this folder, or make a folder named `edu-question-paper` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required, though having it on lets it produce the paper as a document if you ask.

## Using it

Say the topics, the marks, the duration, and the format if one is prescribed.

Examples that work:

- "Unit test, 40 marks, 90 minutes, classes 9 chapters 3 to 5. Our blueprint is attached."
- "Build the blueprint first. I want to see the recall to application split before you write anything."
- "Check this paper before it goes out tomorrow. 200 students are writing it."
- "This paper takes my class 25 minutes longer than the time given. Where do I cut?"
- "I taught differentiation for eight periods. Does my weightage match that?"

Supplying the teaching time per topic changes the weightage more than anything else, and it is the input nobody thinks to give.

---

## Limits worth knowing

- It does not know your board's current syllabus, prescribed format or mark conventions. Supply them and it follows them; it will not assume them.
- It does not set the difficulty for you. It builds to the spread you ask for and says what that spread implies.
- **It does not guarantee a paper is error free.** It applies the item rules and flags what it could not resolve. A subject expert still reads it before it goes out.
- It does not produce diagrams, graphs or figures. It specifies what each has to show.
- It does not predict how a class will score on it.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It will not write questions yet | The blueprint is not confirmed | Deliberate. Confirm the grid and it writes to it. |
| Blueprint looks recall-heavy | It reflects the topics and marks you gave it | That is the finding. Change the cell allocation and rerun. |
| Time estimate exceeds your duration | Usually genuine | It says what to cut. Papers that cannot be finished measure writing speed. |
| Questions feel simpler than yours | Written to one idea each, per the item rules | Two-idea questions cannot be part-marked fairly. Ask for higher-order cells instead. |
| Format does not match your board | It was not supplied | Paste your prescribed format. It follows yours exactly. |
| Review flags questions you like | It reads them as a student who knows less would | Check the specific problem named. Ambiguity is invisible to whoever wrote it. |

---

Part of the [Educators skills](../README.md) in the [Claude Skills Library](../../README.md).
