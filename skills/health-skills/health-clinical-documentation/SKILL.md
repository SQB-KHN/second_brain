---
name: health-clinical-documentation
description: Turn dictation or rough notes into a structured discharge summary, referral letter, consultation note or operative note, raising every gap as a query. Use for clinical write-ups.
---

# Clinical Documentation Builder

The note gets written at the end of a twelve hour day, or three days later from memory. It is the record that gets audited, claimed against, and read by the next doctor treating that patient. So it is the most consequential thing a clinician writes, produced at the moment they have least left. The work in it is structure, and structure is the first thing a tired writer drops.

## When to use this

Trigger on: discharge summary, referral letter, consultation note, operative note, procedure note, case sheet, handover note, "write this up", "structure these notes", "turn my dictation into a summary", "format this properly".

## Before you start

Required: the clinical content. Dictation, rough notes, point form, or a transcript. Whatever the clinician actually said or wrote.

Ask, briefly:
1. Which document is being produced. Each has a different required structure and a different reader.
2. Who reads it: the patient, the next treating doctor, a referring doctor, a payer, or medical records. This changes what leads and what has to be spelled out.
3. Their institution's format, if they have one. Follow it exactly. Their format is not up for improvement unless they ask.
4. Whether the person supplying the content is the person signing. If someone is drafting on a clinician's behalf, every gap goes back to that clinician rather than being filled by the drafter.

## Check for patient identifiers first

Name which fields identify the patient: name, hospital or UHID number tied to an individual, phone, address, scheme or policy number, date of birth.

Say once that the document can be built with those held as placeholders, which the clinician reinstates in their own system, and that the structuring work needs the clinical content rather than the identity. Then continue with whatever they choose. Do not lecture and do not repeat it.

## The rule this skill exists to enforce

**Structure what you were given. Never generate clinical content.**

No diagnosis you were not told. No severity you were not told. No medication or dose you were not given. No finding inferred from another finding. No "likely" or "presumed" the clinician did not say. And no normal finding filled in because a section looked empty.

If a required element is missing, it appears as an explicit query in the draft. A missing element is safe and gets answered. An invented one is not, and it becomes invisible the moment the note is signed.

## Workflow

### 1. Extract what is there, and mark what is not

Sort the supplied content into the target structure. For every required section, record it as present, partial or absent. Do not smooth over an absent section by moving adjacent content into it, which is the most common way invented content enters a note.

### 2. Build the document to its own structure

**Discharge summary.** Admission and discharge dates, presenting complaint, relevant past history, examination findings as recorded, investigations with results, diagnosis at discharge, treatment given, procedures with dates, condition at discharge, medication on discharge with dose, route, frequency and duration, follow-up date and with whom, and instructions on when to return early.

The last three are the ones most often left incomplete, and each is a real safety gap: a discharge drug with no duration, a follow-up with no date, a discharge with no stated reason to come back.

**Referral letter.** Reason for referral stated as a question, what has been done and found, what has been tried, current medication, relevant history, what is specifically being asked of the receiving doctor, and how to reach the referring doctor. A referral with no specific question is the commonest failure in the form, and it wastes the consultation it asks for.

**Consultation note.** Presenting complaint in the patient's own terms, history, examination as recorded, working assessment as the clinician stated it, investigations ordered, plan, and what the patient was told.

**Operative or procedure note.** Date and time, indication, procedure performed, findings, technique as described, implants or devices with their identifiers, specimens sent, blood loss and complications as recorded, closure, post-procedure instructions, and the team. Implant identifiers and specimen disposition are the ones most often missing, and both matter later, one for claims and recalls, the other for diagnosis.

### 3. Handle abbreviations by reader, not by habit

Clinical shorthand is efficient inside a specialty and dangerous outside it. Expand anything ambiguous or anything the stated reader may not share, keeping the shorthand alongside where the clinician uses it.

Where an abbreviation could mean two things, do not choose between them. Raise it as a query.

### 4. Reconcile the content against itself, and report rather than fix

- A drug in the treatment narrative but missing from the discharge list, or the reverse
- A diagnosis stated one way in one section and differently in another
- A procedure mentioned with no date
- Dates that do not sequence
- An investigation referenced with no result given

Each becomes a query. This reconciliation is a large part of the value here, because it catches what the clinician would have caught if they were not writing at the end of a shift.

### 5. Raise gaps as questions, grouped by what they block

- **Cannot complete without this.** The document is not usable until answered.
- **Should have this.** It will be flagged in an audit or queried on a claim.
- **Would improve this.** Better for the next reader.

Every query is a specific question. "Duration not stated for the antibiotic on discharge, please specify" is a query. "Medication section incomplete" is a label.

### 6. Keep the clinician's voice

Short sentences, active voice, one fact per line wherever the reader has to act on it. Do not upgrade the register or add formality the clinician did not use. A note that reads as though a different person wrote it will not get signed, and it should not be.

## Output format

**1. Readiness line.** Whether this can be signed as it stands, and how many blocking queries there are.

**2. The document.** In its required structure, following the institution's format where one was supplied.

**3. Queries.** Grouped as cannot complete, should have, would improve. Each a specific question.

**4. Internal inconsistencies.** What one section says against another, reported not resolved.

**5. Abbreviations.** Those expanded, and those left as queries because they were ambiguous.

**6. Sign-off block.** Name, registration number, designation, date. Unfilled.

## Quality bar

- Is every clinical statement traceable to the supplied content, with nothing added
- Is every missing element a query rather than a filled gap
- Does every discharge medication carry dose, route, frequency and duration, or a query where it does not
- Does the follow-up carry a date and a named person, or a query
- Are instructions on when to return early present, or raised as a query
- Does a referral letter contain a specific question
- Are implant identifiers and specimen disposition present in an operative note, or queried
- Are ambiguous abbreviations queried rather than resolved
- Would the clinician recognise this as their own note
- Is the sign-off block present and unfilled

## What this skill does not do

- It does not diagnose, stage, grade or assess severity. It records what the clinician stated.
- It does not add a medication, a dose, a finding or a normal result that was not supplied.
- It does not assign a clinical code.
- It does not judge the care given. Where the record looks clinically incomplete it raises a query and offers no opinion on the treatment.
- It does not sign anything. The sign-off block stays empty, because the clinical content belongs to the clinician who provided it.
