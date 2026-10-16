# Healthcare Skills for Claude

Five skills for the work that happens around care rather than in it: the write-up, the claim, the patient's instructions, the money and the stock.

They run inside your own Claude account, on notes you paste or exports you already pull. Nothing to install on your machine, nothing to connect, no coding.

---

## Who these are for

The whole healthcare workforce, clinical and non-clinical.

**Clinical:** consultants in private practice, hospital doctors, residents and registrars, staff nurses and ward in-charges, physiotherapists, dietitians and patient educators. **Non-clinical:** hospital and clinic administrators, practice owners, billing and revenue cycle managers, insurance and TPA desk staff, pre-authorisation and denial teams, hospital and retail pharmacists, store in-charges, and medical records staff.

Two of the five need no export from any system at all. They work on dictation or pasted text, so an employed clinician with no access to the hospital software can use them on the first day.

## The five skills

| Skill | Give it | Get back |
|---|---|---|
| **[Clinical Documentation Builder](health-clinical-documentation/health-clinical-documentation-guide.md)** | Dictation or rough notes | A structured discharge summary, referral letter, consultation note or operative note, with every gap raised as a query |
| **[Claim and Pre-Authorisation Readiness](health-claim-readiness/health-claim-readiness-guide.md)** | The pack, plus what the doctor documented | What a payer will query, ranked, plus the justification letter or query response drafted from documented content |
| **[Patient Instruction Writer](health-patient-instructions/health-patient-instructions-guide.md)** | Clinician-supplied content | Plain-language instructions, a medication grid by time of day, red flags with thresholds, and a verbal script |
| **[Revenue, Payer Mix and Collections](health-revenue-analysis/health-revenue-analysis-guide.md)** | A billing export | Payer mix, realisation against tariff, deductions, receivables ageing by status, and unbilled services |
| **[Pharmacy and Consumables Planner](health-pharmacy-planner/health-pharmacy-planner-guide.md)** | A batch-level stock export | Expiry ladder built around supplier return windows, stockout risk by criticality, and a capped reorder list |

Each skill has its own guide with the exact inputs it needs, the phrasings that trigger it, what good output looks like, its limits, and a troubleshooting table.

## What is in the folder

```
health-skills/
├── README.md                                   ← this file
├── health-clinical-documentation/
│   ├── SKILL.md                                ← the skill
│   └── health-clinical-documentation-guide.md  ← how to use it
├── health-claim-readiness/
│   ├── SKILL.md
│   └── health-claim-readiness-guide.md
├── health-patient-instructions/
│   ├── SKILL.md
│   └── health-patient-instructions-guide.md
├── health-revenue-analysis/
│   ├── SKILL.md
│   └── health-revenue-analysis-guide.md
└── health-pharmacy-planner/
    ├── SKILL.md
    └── health-pharmacy-planner-guide.md
```

Every skill sits in its own folder. Inside, the file is always called `SKILL.md`, because that is the filename Claude looks for. Do not rename it. The guide beside it is named after the skill, so it stays identifiable once you have several downloaded.

---

## The line none of these cross

**No clinical content the clinician did not provide.**

Nothing here diagnoses, triages, doses, interprets a scan or a report, or assigns a clinical code. That much is obvious and easy.

The harder half is the same rule applied to writing. A documentation skill that quietly completes a note by inferring what the doctor probably meant has generated clinical content. So has a claims letter that makes a patient sound sicker than the notes support, and an instruction sheet that adds a sensible warning nobody gave. All three are the same failure, and all three are invisible once the document is signed.

So every skill here works the same way. It structures what it was given, and every gap comes back as a specific question rather than a plausible sentence. A missing element is safe, because somebody answers it. An invented one is not.

## Patient data stays out by default

These inputs carry patient identifiers, so this set works differently from the rest of the library.

**De-identified is the default, not the option.** Each skill names the identifying fields before doing anything, and none needs an identity to work. Revenue analysis needs encounter numbers, departments, payers and amounts. Documentation works on clinical content with identifiers held as placeholders you reinstate in your own system. Pharmacy planning needs item, batch and quantity.

No skill asks for an identifier it does not need, and none tells you whether you may share a file, because that is your organisation's data policy rather than a question a skill can answer. It is stated once, in place, and then the work continues with whatever you decide.

---

## Why these five

**Documentation.** The most consequential thing a clinician writes, produced at the moment they have least left. What goes missing is never the clinical thinking; it is the medication duration, the follow-up date, the implant identifier, the specific question in a referral. Every one is a known audit finding.

**Claim readiness.** A claim gets queried for something that was in the file all along, and the query costs three weeks. The list of what each payer actually asks for lives in one person's head and leaves when they do.

**Patient instructions.** Most non-adherence is a comprehension failure nobody checked for. The patient takes the tablet at two random times because "twice daily" reasonably means that, or stops the antibiotic on day three because nobody said how many days.

**Revenue and collections.** You know what you billed and what you banked. The gap lives in payer deductions nobody grouped, concessions nobody approved, claims nobody submitted, and services delivered and never charged. No single system reports all four.

**Pharmacy planning.** Pharmacy loss is quiet. Nothing breaks when a batch expires; the value simply leaves and shows up as a write-off six months later, while the item somebody needed was out of stock at two in the morning.

## They work together

Each stands alone. In sequence they follow an episode of care and its consequences:

```
Dictation           →  Clinical Documentation    →  the record that survives an audit
Pack plus notes     →  Claim Readiness           →  what a payer would have queried
Clinician content   →  Patient Instructions      →  a patient who knows what to do
Billing export      →  Revenue and Collections   →  where the money actually went
Batch stock export  →  Pharmacy Planner          →  what to return, and what to order
```

Two pairings worth knowing. A discharge summary built properly is what a claim needs, so run documentation before claim readiness and most completeness problems disappear. And the same discharge content drives the instruction sheet, so the two documents stop contradicting each other.

---

## What makes these different from asking directly

**Gaps come back as questions, not as prose.** "Duration not stated for the antibiotic on discharge, please specify" is answerable in four seconds. A skill that instead writes a plausible duration has created a clinical instruction nobody approved.

**No severity the record does not support.** A justification letter written to secure an approval is under constant pressure to overstate. Every clinical statement traces to documented content, and where the documentation does not support the claim, the skill says so rather than writing around it.

**Documents get checked against each other.** Most payer queries come from two documents in one pack contradicting each other, not from one being absent: diagnosis on the pre-auth against the discharge summary, procedure billed against the operative note, implant invoice against the sticker.

**Patient instructions carry no clinical abbreviations and no intervals.** Not BD, not OD, not TDS, not SOS, which are among the commonest causes of patient medication error, and where OD reads as once daily to a prescriber and as overdose to everyone else. Timings are clock times: "8 am and 8 pm" beats "twice daily", which a patient reads as any two times because that is what it says.

**Nothing is lost quietly.** Cancelled bills, advances, interim bills and credit notes are excluded from revenue with their values stated, and expired batches are separated from expiry risk and sized as a write-off.

**Findings that need verifying are labelled as candidates.** An unbilled service is flagged with the pattern that found it and its value at tariff, not presented as confirmed loss. And criticality outranks value where it should: a cheap vital item gets a buffer that makes no sense on value grounds alone, because running out of it has a clinical consequence rather than a financial one.

---

## Getting started

1. Open Settings in Claude, go to **Capabilities**, and turn on **code execution and file creation**. Revenue analysis and pharmacy planning need it; the other three do not, so they work on a free plan.
2. Take one skill's folder and compress it to a `.zip`. The file inside must stay named `SKILL.md`, because that is what Claude looks for. The guide beside it is not needed and can be left out.
3. Go to **Customize**, then **Skills**, then add a skill and upload the zip.
4. Repeat for each skill you want.

Skills you upload stay private to your account. Once installed they work in Chat and Cowork, and Claude picks the right one from what you ask.

**Where to start.** Take a discharge summary you have already written and run the documentation skill on the notes it came from. Comparing its query list against what you wrote is the fastest way to see what it catches and what it will not do for you.

## Using them

Paste the notes or upload the export, and describe the task the way you would to a colleague.

- "Discharge summary from these notes. Four day admission, here is what happened."
- "Pre-auth for a knee replacement, insurer via TPA. Check it before I submit."
- "Discharge instructions for a 68 year old with limited literacy, attendant will read it."
- "Billing and collections for last quarter. Where is the gap?"
- "What is expiring in six months, and what can still go back to the supplier?"

---

## What these will not do

- **No clinical decisions.** No diagnosis, triage, staging, severity assessment, dosing, drug interaction, therapeutic substitution, or interpretation of any scan, report or investigation.
- **No clinical coding.** No ICD or procedure code is assigned or verified. The claims skill checks whether documentation supports a code a person already chose; it does not choose one.
- **No invented clinical content.** Nothing is added, inferred or upgraded, no patient is written sicker than the record says, and gaps become queries.
- **No informed consent.** Consent is a legal instrument. Even simplifying its language is a decision for whoever owns consent in your organisation.
- **No policy or coverage rulings.** Whether a condition is pre-existing, whether a waiting period applies, whether a deduction was contractually valid: all payer and contract questions.
- **No disposal routes** for expired or controlled items, which are governed by regulation and your institution's own procedure, and **no validated translation**, since a translated sheet is a draft for a speaker to check.
- **No system access.** These work on notes you paste and exports you provide, never connecting to a hospital system, a claim portal or a pharmacy application.
- **Nothing is signed, submitted or sent.** Every sign-off block comes back empty, because the clinical content belongs to the clinician who provided it.

## What you need

- A Claude account, with code execution turned on for the two data-driven skills
- Your notes pasted or dictated, and your exports in Excel or CSV
- Nothing else. No installation, no terminal, no coding, nothing to connect

---

Part of the [Claude Skills Library](../README.md).
