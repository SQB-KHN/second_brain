# Clinical Documentation Builder

Turns dictation or rough notes into a structured discharge summary, referral letter, consultation note or operative note, and raises every gap as a query instead of filling it.

---

## Who this is for

Anyone who writes up clinical encounters: consultants in private practice, hospital doctors, residents and registrars, staff nurses writing handover and discharge notes, medical scribes, and medical records staff who chase incomplete files for a living.

## The problem it solves

The note gets written at the end of a twelve hour day, or three days later from memory.

It is also the most consequential thing a clinician writes. It is the record that gets audited, the document a payer claims against, and the only thing the next doctor treating that patient will actually read. And it is produced at the moment its author has least left.

The work in it is structure, not content. The clinician already knows what happened. What goes missing is the medication duration, the follow-up date, the implant identifier, the specific question in a referral, the instruction on when to come back early. Every one of those is a known audit finding and a known safety gap, and every one is the sort of thing a tired person drops.

This does the structuring, and it will not quietly fill a gap to make the document look finished. Saves ten to twenty minutes per document and considerably more when a file comes back incomplete.

---

## What you give it

**Required:** the clinical content. Dictation, rough notes, point form, or a transcript. Whatever you actually said or wrote.

**Tell it these and the output changes materially:**

| Context | Why it matters |
|---|---|
| Which document you need | Each has a different required structure and a different reader |
| Who reads it | A patient, the next treating doctor, a referring doctor, a payer or medical records need different things spelled out |
| Your institution's format | It follows yours exactly rather than proposing its own |
| Whether you are signing it | If you are drafting for someone else, gaps go back to them rather than being filled by you |

**It handles:** messy dictation, point form, content out of order, mixed shorthand, and content that jumps between sections. It sorts what it was given into the target structure without moving content into a section it does not belong to.

**Before anything else** it names which fields identify the patient and offers to work with those as placeholders you reinstate in your own system. The structuring work needs the clinical content, not the identity.

## What you get back

1. A readiness line: whether this can be signed as it stands, and how many blocking queries there are
2. The document, in its required structure, in your institution's format if you supplied one
3. **Queries**, grouped by whether they block the document, affect an audit, or just help the next reader
4. **Internal inconsistencies**, where one section contradicts another
5. Abbreviations expanded, and any left as queries because they were genuinely ambiguous
6. A clinician sign-off block, unfilled

---

## The rule it will not bend

**It structures what you gave it. It never generates clinical content.**

No diagnosis you did not state. No severity you did not state. No medication or dose you did not give. No finding inferred from another finding. No "likely" or "presumed" you did not say. And no normal finding filled in because a section looked empty.

A missing element comes back as a query. That is safe, because you answer it. An invented one is not, and it becomes invisible the second the note is signed.

This is also why the document-type question turned out not to matter. A discharge summary carries diagnosis and plan just as a consultation note does, so restricting which documents it will build buys no safety at all. The safety is in the operation, and the operation is the same for all of them.

## What it checks that you would catch if you were not tired

| Check | What it finds |
|---|---|
| **Medication reconciliation** | A drug in the treatment narrative but missing from the discharge list, or the reverse |
| **Diagnosis consistency** | Stated one way in one section, differently in another |
| **Date sequencing** | An investigation dated before admission, a summary dated before the last recorded service |
| **Procedure completeness** | A procedure mentioned with no date, or an operative note with no implant identifier or specimen disposition |
| **Discharge essentials** | Medication without a duration, follow-up without a date, no stated reason to return early |
| **Referral essentials** | A referral letter with no specific question in it |

Each becomes a query. It reports these; it does not resolve them.

## What good output looks like

A strong result gives you a document you would sign and a short list of specific questions. The queries are the useful part: "Duration not stated for the antibiotic on discharge, please specify" is answerable in four seconds. "Medication section incomplete" is not.

It should also read like you. If the register has been upgraded, the sentences lengthened, or formality added that you did not use, that is a failure, because a note that sounds like somebody else wrote it will not get signed and should not be.

If it comes back with almost no queries on a rushed dictation, be suspicious. That usually means content was inferred rather than raised, which is the one thing this is built to prevent.

---

## Installing it

1. Download this folder, or make a folder named `health-clinical-documentation` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill, so it works on a free plan.

## Using it

Paste or dictate the content and say which document you need.

Examples that work:

- "Discharge summary from these notes. Four day admission, here is what happened."
- "Turn this dictation into a referral letter to a cardiologist."
- "Structure this as an operative note. Our format attached."
- "This case sheet is going for audit. Tell me what is missing before it goes."

Saying who reads it changes what gets spelled out, and it is the cheapest sentence you can add.

---

## Limits worth knowing

- It does not diagnose, stage, grade or assess severity. It records what you stated.
- It does not add a medication, a dose, a finding or a normal result you did not supply.
- It does not assign a clinical code.
- It does not judge the care given. Where the record looks clinically incomplete it raises a query and offers no opinion on the treatment.
- It does not sign anything. The sign-off block stays empty, because the clinical content is yours.
- It works on what you give it. It cannot see the chart, the imaging or the previous admission.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Long query list | The dictation genuinely did not cover those elements | That is the finding. Each query is a specific question and most take seconds to answer. |
| It sounds nothing like you | Register upgraded from terse notes | Tell it to keep your phrasing. Shorter input tends to invite more rewriting. |
| A section reads thin | Content for it was absent, and it will not move other content in | Correct. Check the query list for that section. |
| Abbreviation left unexpanded | It was ambiguous between two meanings | It queries rather than choosing. Tell it which you meant. |
| Wrong structure | Document type or institutional format not stated | Say which document, and attach your format. It follows yours exactly. |

---

Part of the [Healthcare skills](../README.md) in the [Claude Skills Library](../../README.md).
