# Patient Instruction Writer

Turns clinician-supplied content into plain-language patient instructions, with a medication grid organised by time of day, red flags that name a threshold and an action, and a script for the verbal explanation.

---

## Who this is for

Anyone who has to make a patient understand what to do next: consultants and hospital doctors, staff nurses and ward in-charges, patient educators and counsellors, physiotherapists and dietitians, discharge coordinators, and clinic staff who field the calls afterwards.

## The problem it solves

Instructions get given at the moment the patient is least able to absorb them, by somebody who has said the same thing four hundred times, in a register the patient does not use. Then they are handed a printed sheet written for a different reader entirely.

Most non-adherence is not defiance. It is a comprehension failure nobody checked for. The patient nods, goes home, and takes the tablet twice at two random times because "twice daily" reasonably means that. Or stops the antibiotic on day three because nobody said how many days. Or does not come back when they should, because "watch for complications" is not an instruction anybody can follow.

Writing this properly means dropping every abbreviation, restructuring the medication list by time rather than by drug, and turning each warning into a sign plus a threshold plus a place to go. It takes twenty minutes per sheet by hand, so it does not get done, and the same generic printout goes out for the fortieth time.

---

## What you give it

**Required:** the clinical content from the treating clinician. What the patient is to do, take, avoid and watch for.

| Context | Why it matters |
|---|---|
| Which set: pre-procedure, post-procedure, discharge, medication, self-management | Each has a different shape and a different urgency |
| **Language, and whether a verbal script is wanted too** | Most of this is delivered by speaking, not by handing over paper |
| **Who actually reads it**: patient, attendant, or home carer | These are not the same document |
| Reading level, and whether literacy may be limited | Changes the structure, and shifts weight onto the verbal script |
| Anything that must be said, or must not | Your clinical call, applied without argument |

**It handles:** content in clinical shorthand, content out of order, and content for several drugs and several instruction types at once. Where a sheet is being built as a reusable template rather than for one patient, say so and it keeps identifiers out entirely.

## What you get back

1. **Queries first**, if anything is missing. What the clinician must supply before this goes to a patient
2. The patient sheet, in the target language at the target reading level
3. **Medication grid organised by time of day**, with a duration for every drug
4. **Red flags**: sign, threshold, action, destination, and a placeholder for the number to call
5. Common questions, answered where the clinician covered them and listed as queries where not
6. **Verbal script**, in order, with teach-back questions at the end
7. A clinician sign-off block, unfilled
8. A translation note, where another language was produced

---

## The rule it will not bend

**It translates and structures what the clinician gave it. It never adds an instruction.**

No medication you did not name. No dose or timing you did not specify. No dietary restriction, activity limit or duration you did not set. No warning sign you did not list.

The reason is specific. A patient follows a printed instruction as though a doctor wrote it, because as far as they know one did. An added instruction is not a draft error, it is an unsupervised clinical instruction, and it carries your signature.

So if something the patient obviously needs is missing, it comes back as a query. That includes the questions patients ring back about most: what to do about a missed dose, whether to continue their existing regular medication, and when they can bathe, drive, lift, work, travel or fast. Every one of those is a clinical judgement specific to that patient, and it will list them rather than answer them.

## The three changes that do most of the work

**Medication by time of day, not by drug.** A patient does not take drugs, they take a morning handful and a night handful. A list organised by drug leaves them to do the scheduling; a grid organised by time does it for them.

| Medicine | What it is for | Morning | Afternoon | Night | With food | For how many days |

**Clock times or meal anchors, never intervals.** "8 am and 8 pm" or "after breakfast and after dinner" beats "twice daily", which a patient reads as any two times, because that is what it says.

**No clinical abbreviations at all.** Not BD, not OD, not TDS, not SOS, not PRN. These are among the commonest causes of patient medication error. OD means once daily to a prescriber and overdose to everyone else.

## Red flags need four parts

"Watch for complications" is not an instruction. Every warning gets:

- **The sign**, described as the patient would notice it, not in clinical terms
- **The threshold**, where one applies, in something they can actually measure
- **What to do**
- **Where to go**, and a number to call

Kept short and placed where it can be found in a hurry. A list of twenty warning signs does not get read, so only the ones the clinician named go in.

## What good output looks like

A strong sheet reads as though it were written for one person who is worried and slightly rushed. Every line is one instruction. The medication grid can be followed without reading anything else on the page. The red flags fit in the space someone glances at.

The verbal script should end with questions like "tell me when you will take the white tablet", not "do you understand?". Everyone says yes to the second one, which is why it is worthless.

If the query list is empty on a complex discharge, check it. Complete content is possible but uncommon, and an empty query list more often means something was helpfully filled in.

---

## Installing it

1. Download this folder, or make a folder named `health-patient-instructions` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill, so it works on a free plan.

## Using it

Give it the clinical content and say who is reading it.

Examples that work:

- "Discharge instructions from these notes. Patient is 68, limited literacy, attendant will read it."
- "Post-op instructions after gallbladder surgery, in Hindi and English."
- "Medication schedule for these six drugs. Grid by time of day."
- "Pre-op preparation sheet, and a script for what the nurse should say."
- "Rewrite this printed sheet in plain language. It is written for doctors."

Saying whether the reader is the patient, an attendant or a carer changes the document more than anything else you can tell it.

---

## Limits worth knowing

- It does not add an instruction, a medication, a dose, a restriction or a warning the clinician did not give.
- It does not answer clinical questions for you, including missed doses or when to resume an activity.
- It does not draft informed consent. Consent is a legal instrument, and even simplifying its language is a decision for whoever owns consent in your organisation.
- It does not produce a validated translation. It produces a draft for a speaker to check before it reaches a patient.
- It does not replace the conversation. The sheet supports what was said, which is why the verbal script and teach-back questions exist.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Query list is long | Durations, follow-up or red flags were not in the content | Each is a specific question. Answer and rerun. |
| It refuses to answer a common question | Missed doses, driving, bathing are clinical judgements | Deliberate. Tell it your answer and it will include it. |
| Sheet reads too simple | Working to the reading level you asked for | Say the reader is health-literate and it will lift the register. |
| Translation feels stiff | Word-for-word rendering was unavoidable for a clinical term | It keeps the English term and explains it. Have a speaker check it. |
| No consent wording produced | Out of scope by design | Consent stays with whoever owns it in your organisation. |

---

Part of the [Healthcare skills](../README.md) in the [Claude Skills Library](../../README.md).
