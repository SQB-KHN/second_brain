# How These Skills Are Built

Every skill in this library has the same anatomy and the same refusals. Understand those and you understand all fifty-five.

---

## What counts as a skill

A prompt is something you retype every time. A skill is a standard that persists, carries the judgement a senior professional would apply, and knows what to verify before it hands you an answer.

A candidate has to pass all six tests:

1. **Recurring.** Done weekly or monthly. Something done once a year never becomes a habit.
2. **Produces an artifact.** A table, a document, a workbook, a brief. Not advice, not a conversation.
3. **Has a senior standard.** There is a right way a good professional does it, so there is something real to encode.
4. **Needs no system access.** The input is a file you export or text you paste.
5. **Time saved is visible in week one.** If you cannot feel it on first use, there is no second use.
6. **Safe.** Nothing makes a regulated, clinical, legal or tax decision. Skills compute, check, structure and flag.

Three things are excluded on principle: anything that is really just a prompt, anything Claude already does well unaided, and anything needing live data or an integration. That is why there is no code review skill for engineers and no "summarise my notes" for students.

## Every domain has the same five roles

| Slot | What it does |
|---|---|
| **Analyse** | Turns raw data into the standard output of the job |
| **Verify** | Proves something is correct, or finds where it is not |
| **Produce** | Builds the recurring deliverable the role is judged on |
| **Plan** | The forward-looking one |
| **Communicate** | Turns the work into a decision or a message |

The slot is the structure. The content is entirely domain-specific. Where a domain genuinely does not fit, the variant is named rather than forced: Healthcare's Communicate points outward to the patient, and Students replaces it with Review, because a student has no outward audience.

## Every skill has the same anatomy

`SKILL.md` is what you upload. It always contains, in this order: the problem in two to four sentences, the phrases that should trigger it, what it needs before starting and what to ask, a numbered workflow carrying the domain specifics, the output format, and an honest list of what it will not do.

It ends one of two ways, and the ending tells you what kind of skill it is:

| Shape | Output | Ends with |
|---|---|---|
| **A** | File in, analysis out. It either ties or it does not | `## Checks to run before delivering` |
| **B** | Brief in, crafted artifact out. Judged on quality | `## Quality bar`, every item answerable yes or no |

Beside it sits a guide: who it is for, what to give it, what good output looks like, its limits, and a troubleshooting table.

## Every skill refuses the same things

- **Computes in code, never in prose.** Arithmetic worked out inside a sentence is the largest single source of error in AI output.
- **Never loses data quietly.** Removed rows are quarantined visibly, exclusions are stated with their value.
- **Reports failed checks at the top**, never buried inside a file described as complete.
- **Labels assumptions next to the number they affect**, never as a benchmark or a finding.
- **Keeps evidence apart from interpretation.** What the data shows is fact; what might explain it is a labelled hypothesis.
- **Never invents to fill a gap.** Missing input becomes a stated assumption or an open question.
- **Says when the answer is inconclusive**, in the first paragraph rather than at the end.
- **Flags personal data once**, then works with whatever you decide. Healthcare and Educators go further: de-identified is the default, not an option.
- **Takes no action.** Nothing is posted, sent, filed, ordered or changed on your behalf.

## And each domain refuses one thing of its own

| Domain | Its hard line |
|---|---|
| Finance | No tax, GST, statutory or accounting-treatment advice |
| Data | No confident wrong answer |
| Marketing | No invented evidence |
| Operations | No unchecked commitment |
| Healthcare | No clinical content the clinician did not provide |
| Content | No unearned authority |
| Sales | No deal is more advanced than its evidence |
| Educators | Nothing labels the learner |
| Techies | No invented system behaviour |
| Business Owners | No advice that needs a licence |
| Students | Nothing you could submit |

Each line is built into all five skills of its domain, not stated once and forgotten.

## It is checked, not asserted

`.audit/audit.py` verifies the whole library in one command: every relative link resolves, no em dashes, every skill's name matches its folder, every description is under 200 characters, every required section is present, every domain is exactly eleven files, and no quality bar item is duplicated across domains.

Run it before believing any claim on this page.
