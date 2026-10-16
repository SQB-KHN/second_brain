# Claim and Pre-Authorisation Readiness

Checks a claim or pre-auth pack for what a payer will query, then drafts the justification letter or query response from what the treating doctor actually documented.

---

## Who this is for

Anyone whose week is shaped by payer queries: insurance and TPA desk staff, pre-authorisation coordinators, claims and denial management teams, billing managers, medical officers who sign pre-auths, and practice owners handling their own cashless approvals.

## The problem it solves

A claim gets queried for something that was in the file the whole time. Filed in the wrong place, attached without its report, or contradicted by another document in the same pack.

The query costs three weeks and two people, and it repeats next month, because nobody wrote down what caused it. Meanwhile the list of what each payer actually asks for lives in the head of whoever handles that payer, and leaves when they do.

The second problem is the justification letter. It has to make a clinical case, but it is usually written by someone who is not the clinician, working from a discharge summary, under time pressure. The temptation to make the patient sound a little sicker is constant, and giving in to it is both a clinical misrepresentation and a fraud exposure.

This runs the completeness and consistency checks before submission, and drafts the letter strictly from documented content, with every gap raised as a query rather than written around.

---

## What you give it

**Required:** the pack, or a list of what is in it, plus the clinical content the treating doctor has documented.

| Context | Why it matters |
|---|---|
| **Payer type** | Insurer direct, insurer via TPA, government scheme or corporate panel. Required documents and query patterns differ materially |
| **Which document this is** | A fresh pre-auth, an enhancement, a final claim, a query response or an appeal all argue different things |
| Policy constraints you know | Sum insured, room rent cap, sub-limits, waiting period, co-pay. These drive most deductions |
| **The payer's exact wording**, for a query or rejection | Paraphrasing loses the specific ground being cited, and the response has to answer that ground |
| What the doctor documented on indication and course | It will not invent this. Gaps come back as queries |

It names the identifying fields first and offers to work with them as placeholders, since the readiness check needs the clinical and administrative content rather than the identity.

## What you get back

1. **A verdict**: ready or not ready, and the blocker count, before any detail
2. Completeness table: every required item marked present, missing or inadequate, with who holds it
3. **Inconsistencies between documents**, and why each will be queried
4. Where the documentation does not substantiate what is being claimed
5. Blockers, weaknesses and acceptable, ranked with the fix for each
6. **Justification letter draft**, with bracketed queries wherever clinical content was missing
7. Query or rejection response draft, where a payer communication was supplied
8. Likely query grounds, so the desk can pre-empt them next time

---

## The check almost nobody runs

Most queries do not come from a missing document. They come from two documents in the same pack contradicting each other.

| Compared | The query it prevents |
|---|---|
| Pre-auth diagnosis against discharge summary diagnosis | The commonest single ground for a deduction |
| Length of stay claimed against admission and discharge dates | An arithmetic mismatch anyone can spot |
| Procedure billed against the procedure in the operative note | A high-value discrepancy |
| Implant invoice against the operative note and the sticker | Implant claims are queried more than anything else |
| Investigation dates against the admission date | An investigation dated before admission |
| Amount claimed against the itemised bill total | A pure reconciliation failure |
| Room category billed against what the policy allows | A deduction that is entirely avoidable |

Finding these before submission is the value of the skill. Finding them after costs three weeks.

## What it will not write

Every clinical statement in a drafted letter traces to something the doctor documented. Where a necessary element is absent it becomes a bracketed query inside the draft, not a plausible sentence.

That includes severity. **It will not write a patient sicker than the notes say**, however much easier that would make the approval. If the documented indication does not support inpatient admission, it says so plainly, because that is a finding for the treating team rather than a drafting problem to solve.

It also will not interpret the policy. Whether a condition is pre-existing, whether a waiting period applies, whether a deduction was contractually valid: those are decisions for the payer, your contract and whoever owns that relationship. It presents the clinical facts and the documents.

## What good output looks like

A strong result opens with a verdict you can act on: "Not ready. Three blockers: implant sticker missing, pre-auth diagnosis does not match the discharge summary, and length of stay claimed is five days against four recorded."

The justification letter should have brackets in it. Brackets mean it found gaps and asked rather than inventing, and a letter with three bracketed queries you can answer in a minute is far better than a smooth one you cannot verify.

Where a payer's deduction ground is factually correct, a strong response says so and states the correct position. Contesting an accurate deduction damages every subsequent claim from the same desk, and a response that argues everything gets read as a response that argues nothing.

---

## Installing it

1. Download this folder, or make a folder named `health-claim-readiness` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill, so it works on a free plan.

## Using it

Give it the pack and say which payer type and which document.

Examples that work:

- "Pre-auth for a knee replacement, insurer via TPA. Check it before I submit."
- "This claim came back queried. Here is their exact wording and here is our file."
- "Final claim at discharge. Does the documentation support the five day stay?"
- "Draft the justification letter. Here is what the surgeon documented."
- "Rejection received. Is this ground factually correct or worth appealing?"

Pasting the payer's exact wording, rather than summarising it, changes the response substantially.

---

## How it protects accuracy

- Every item in the required set is marked present, missing or inadequate, with none left unassessed
- Amount claimed is reconciled to the itemised bill total in code, not compared by eye
- Length of stay claimed is checked against the admission and discharge dates
- Diagnosis is compared across the pre-auth and the discharge summary, and any difference is reported
- Every clinical statement in a drafted letter traces to documented content, and missing content appears as a bracketed query rather than as prose
- The recoverable and the unverifiable are totalled separately, so the headline number cannot flatter itself

## Limits worth knowing

- It does not invent clinical content, and will not make a patient sound sicker than the record says.
- It does not assign or verify a clinical code.
- It does not interpret a policy, decide on pre-existing conditions or waiting periods, or rule on whether a deduction was valid.
- It does not submit anything and does not communicate with a payer.
- It does not guarantee approval. It finds what will be queried, and tells you when the documentation does not support the claim.
- It works on what you give it. It cannot see the portal, the policy wording you did not supply, or the rest of the chart.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Letter is full of brackets | Clinical content was thin | Correct behaviour. Answer the brackets; they are specific questions. |
| It says documentation does not support the claim | It genuinely does not | That is a finding for the treating team, not a drafting problem. |
| It refuses to argue a deduction | The ground rests on policy interpretation | It gives you the clinical facts. The policy argument belongs to whoever owns that contract. |
| Completeness list feels generic | Payer type not stated | Say insurer, TPA, government scheme or panel. Requirements differ. |
| Response misses the point of the query | Query was paraphrased on input | Paste the payer's exact wording. |

---

Part of the [Healthcare skills](../README.md) in the [Claude Skills Library](../../README.md).
