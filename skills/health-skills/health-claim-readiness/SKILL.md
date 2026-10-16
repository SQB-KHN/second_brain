---
name: health-claim-readiness
description: Check a claim or pre-auth pack for what a payer will query, then draft the justification letter or query response from clinician content. Use for pre-auth, claims or denials.
---

# Claim and Pre-Authorisation Readiness

A claim gets queried for something that was in the file the whole time, filed in the wrong place or never attached. The query costs three weeks and two people, and it repeats next month because nobody wrote down what caused it. Almost nobody checks a pack against what the payer will actually ask for, because that list lives in the head of whoever handles that payer.

## When to use this

Trigger on: pre-auth, pre-authorisation, cashless approval, claim submission, claim query, claim rejection, TPA query, denial management, claim readiness, appeal, reimbursement claim, "will this get rejected", "how do I answer this query".

## Before you start

Required: the pack, or a list of what is in it, plus the clinical content the treating doctor has documented.

Ask, briefly:
1. **Payer type.** Insurer direct, insurer through a TPA, government scheme, or a corporate panel. Required documents and query patterns differ materially between them.
2. **Which document this is.** A fresh pre-auth, an enhancement, a final claim at discharge, a response to a query, or an appeal against a rejection. Each argues a different thing.
3. Policy or scheme constraints already known: sum insured, room rent cap, sub-limits, waiting period, co-pay. These drive most deductions.
4. **If answering a query or rejection, the payer's exact wording.** Paraphrasing loses the specific ground being cited, and a response has to answer that ground rather than the general topic.
5. What the treating doctor has actually documented about indication and expected course. This skill will not invent it.

## Check for patient identifiers first

Name the identifying fields present. Say once that the readiness check works on the clinical and administrative content rather than the identity, and that identifiers can be held as placeholders which the team reinstates on the real submission. Continue with whatever they choose, and do not repeat it.

## Workflow

### 1. Establish which document you are producing, before checking anything

A pre-auth argues that admission is necessary and appropriate. A final claim proves what was done and what it cost. A query response answers one specific ground. An appeal contests a stated reason.

Mixing them is the commonest reason a well-written document still fails. It answers a question nobody asked.

### 2. Run the completeness check for this payer type

Mark every item present, missing or inadequate. Inadequate matters as much as missing: an investigation named without its report attached is a query waiting to happen.

- Identity and policy: policy or scheme document, ID, KYC where required
- Treating doctor's request, signed, with registration number
- Indication for admission, stated clinically, in the doctor's words
- Provisional or final diagnosis as documented
- Proposed line of treatment, and expected length of stay with a reason
- Investigations supporting the diagnosis, with reports and not just names
- Past history, and any pre-existing condition disclosure
- For surgery: operative note, implant invoice and sticker, anaesthesia record
- For a final claim: discharge summary, itemised bill, receipts, investigation reports
- Estimate consistent with the proposed treatment

For every missing item, name who holds it. "Missing" with no owner does not get fixed.

### 3. Check the documents against each other

This is the highest-yield step in the skill and the one almost nobody runs. Most queries come from documents contradicting each other, not from a document being absent.

- Diagnosis on the pre-auth against diagnosis on the discharge summary
- Length of stay claimed against admission and discharge dates
- Procedure billed against the procedure in the operative note
- Implant on the invoice against the implant in the operative note and on the sticker
- Dates that contradict: an investigation dated before admission, a discharge summary dated before the last recorded service
- Amount claimed against the itemised bill total, computed in code rather than compared by eye
- Room category billed against the category the policy allows

Every inconsistency here becomes a query. Finding them before submission is the point of the exercise.

### 4. Check whether the documentation supports what is claimed

This is not code assignment. The question is whether the record substantiates a claim a human has already made:

- Does the documented indication support inpatient admission rather than day care or OPD
- Does the documented course support the length of stay claimed
- Is every billed service traceable to something in the record
- Is any high-value item claimed with no clinical narrative behind it

Where the documentation does not support the claim, say so plainly. That is a finding for the treating team, not something to write around.

### 5. Draft the justification letter from what the clinician provided

Structure it as indication, relevant findings with the investigations that show them, why this line of treatment, why inpatient care rather than an alternative, expected course and duration, and what is being requested.

Four rules, none negotiable:

- Every clinical statement traces to something the doctor documented. Nothing is added, inferred or upgraded.
- Where a necessary element is missing, it becomes a bracketed query inside the draft, never a plausible sentence.
- **No severity the record does not support.** Writing a patient sicker than the notes say is the failure mode here, and it is a clinical misrepresentation and a fraud exposure at the same time.
- A sign-off block for the treating doctor, because the letter is their clinical statement and not the drafter's.

### 6. Answer the actual ground in a query or rejection response

Identify the specific ground from the payer's own wording. Then:

- State the ground as the payer put it
- Answer only that ground, with the document or clinical fact that addresses it
- Name the specific evidence being attached
- **Where the ground is factual and the payer is right, say so**, and state the correct position. Contesting an accurate deduction damages the next twenty claims from the same desk.
- Where the ground rests on a policy interpretation, present the clinical facts and stop. Do not argue policy construction.

### 7. Rank the fixes and give a verdict

- **Blockers.** It will be queried or rejected without these.
- **Weaknesses.** Likely to attract a query, worth fixing now.
- **Acceptable.** Complete.

Then say plainly whether the pack is ready. If it is not, say that first, before the detail.

## Output format

**1. Verdict.** Ready or not ready, and the blocker count. One or two lines.

**2. Completeness table.**

| Item | Required for this payer type | Status | Who holds it |

**3. Inconsistencies between documents.** What one says against another, and why it will be queried.

**4. Documentation support.** Where the record does not substantiate what is claimed.

**5. Blockers, weaknesses, acceptable.** Ranked, with the fix for each.

**6. Justification letter draft.** With bracketed queries wherever clinical content was missing.

**7. Query or rejection response draft.** Only where a payer communication was supplied.

**8. Likely query grounds.** Based on the gaps found, so the desk can pre-empt them next time.

## Checks to run before delivering

- Every item in the required set is marked present, missing or inadequate, with none unassessed
- Amount claimed reconciles to the itemised bill total
- Length of stay claimed matches the admission and discharge dates
- Diagnosis is compared across the pre-auth and the discharge summary, and any difference is reported
- Every clinical statement in the drafted letter traces to documented content
- Missing clinical content appears as a bracketed query, never as drafted prose
- Every missing item names who holds it
- The readiness verdict is stated at the top, before the detail

## What this skill does not do

- It does not invent clinical content, and it will not make a patient sound sicker than the record says. Missing clinical elements go back to the treating doctor as queries.
- It does not assign or verify a clinical code.
- It does not interpret a policy, decide whether a condition is pre-existing, whether a waiting period applies, or whether a deduction was contractually valid. It presents the clinical facts and the documents.
- It does not submit anything and does not communicate with a payer.
- It does not guarantee approval. It finds what will be queried, and tells you plainly when the documentation does not support the claim.
