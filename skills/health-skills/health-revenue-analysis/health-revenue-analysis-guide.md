# Revenue, Payer Mix and Collections

Turns a billing export into payer mix, realisation against tariff, deduction analysis, receivables ageing by status, and the services that were delivered and never billed.

---

## Who this is for

Anyone answerable for what a facility earns: hospital and clinic administrators, practice owners, billing and revenue cycle managers, finance staff in healthcare, diagnostics and daycare chain operations, and consultants running their own practice.

## The problem it solves

You know what you billed. You know what you banked. The gap between them is where the business actually lives, and it is spread thin across four places that no single system reports together.

Payer deductions, which arrive without a reason code anyone has grouped. Concessions given at the front desk with nobody's approval attached. Claims sitting unsubmitted for forty days, which looks identical to a claim the payer is sitting on. And services that were delivered, recorded in the notes, and never charged at all.

The last one is the largest and the least visible. Nothing in a billing system flags a consumable that was used and not billed, because from the system's point of view nothing happened.

By hand this means reconciling billing against collections, grouping deductions by payer, ageing receivables twice on different dates, and cross-checking encounters for missing charges. Two to three days, done quarterly at best. This does it in one pass, monthly.

---

## What you give it

**Minimum:** a billing export with bill or encounter number, date, department or service, payer, gross amount, and amount collected or outstanding.

| Extra data | What it unlocks |
|---|---|
| **The collections file alongside billing** | The gross-to-realised waterfall, which is the whole analysis |
| **Your tariff or rate list** | Realisation against tariff, the single biggest upgrade to the output |
| Deduction reason codes | Deductions grouped by cause rather than reported as one number |
| Claim submission dates | Ageing from submission as well as bill date, which separates your delay from theirs |
| Consultant and discount approver | Revenue by consultant on billed and realised, and concessions attributed with unattributed totalled separately |

**Handled automatically:** files at bill level against bill-line level, cancelled and re-raised bills, credit notes held as positive rows, advances mixed in with collections, package headers that double count against their components, interim bills superseded by a final bill, header rows, brackets for negatives and Indian digit grouping.

**Before anything else** it names which columns identify a patient and says plainly that this analysis needs none of them. It needs the encounter number, department, payer, dates and amounts. It will run on a de-identified export.

## What you get back

1. Headline: gross billed, realised, realisation rate, largest single leak, and **which revenue definition is being reported**
2. **Gross to realised waterfall**, every deduction step valued and marked controllable or not
3. **Payer mix**: share of billed against share of realised, realisation rate, deduction rate, days to pay, outstanding
4. Department and consultant view, ranked on billed and on realised
5. Realisation against tariff, where a rate list was supplied
6. Concessions by approver and department, with unattributed shown separately
7. **Unbilled candidates**, with the pattern that flagged each, labelled as needing verification
8. Receivables ageing by payer and by status, from bill date and submission date
9. The concentration, in one sentence
10. Data quality and exclusions, each with its value

An Excel version with one sheet per view is offered at the end.

---

## Four numbers are all called revenue

Conversations about revenue go wrong because two people are holding different ones. The output states which it is reporting, every time.

| Term | What it means |
|---|---|
| **Gross billed** | Value of bills raised, before any deduction |
| **Net billed** | After approved discounts, concessions and package adjustments |
| **Realised** | Cash actually received against those bills |
| **Recognised** | What accounting will book, which may differ from all three |

The walk from gross to realised is presented as a waterfall, every step valued and marked controllable or not, which is what makes it actionable rather than descriptive.

## Why payer mix beats department reporting

Payer mix is the structure that governs healthcare revenue, and a department-wise report hides it completely.

A department can rank first on billed value and last on realised value, because its case mix skews to a slow, high-deduction payer. Nobody discovers that from a department report, and it is usually the most useful sentence the analysis produces. So every payer category gets its share of billed **and** its share of realised, and the difference between those two shares is the finding.

## The unbilled hunt

This is what administrators actually pay for, and no dashboard shows it. It looks for encounters missing a service that almost always accompanies another: consumables against a procedure that requires them, oxygen or monitoring against a stay that recorded it, investigation charges against a stay with recorded results, consultation charges against days of admission.

These come back as **candidates with the pattern that flagged them**, valued at tariff, never as confirmed loss. Each needs checking against the case file, because the pattern can be wrong and a number shown to a board has to survive that check.

## What good output looks like

A strong result names the leak in one sentence: "Two payers hold 71 percent of the over-90-day outstanding, and in both cases the query is for the same missing document."

The ageing split by status is usually the uncomfortable part. Claims sitting **not yet submitted** are your delay, not the payer's, and most facilities find more sitting there than they expected.

If the realisation rate looks fine and nothing shows as a leak, check whether you supplied the collections file. Billing data alone can only report what was raised, so the waterfall collapses and the whole analysis becomes a revenue summary.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill runs Python on your export and will not work without it.
2. Download this folder, or make a folder named `health-revenue-analysis` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the export and say what you are trying to find out.

Examples that work:

- "Billing and collections for last quarter. Where is the gap?"
- "Which payers are actually worth having? Show me realisation, not billing."
- "Receivables are 3.4 crore. Split it by payer and tell me whose delay it is."
- "Find services we delivered and never charged for."

Supplying the tariff and the collections file together is what turns this from a report into a diagnosis.

---

## How it protects accuracy

- Gross minus every deduction step is proved equal to realised plus outstanding, exactly
- Cancelled, interim and superseded bills are excluded with their value stated, never dropped silently
- Advances and deposits are excluded from revenue and reported separately, because an advance is not revenue
- Package headers are never counted alongside their component services
- Payer shares are proved to sum to 100 percent, on billed and on realised independently
- Unbilled items are labelled candidates with their flagging pattern, never presented as confirmed loss, and the whole analysis runs on a de-identified export

## Limits worth knowing

- It does not assign or verify a clinical code, and does not decide what a service should have been billed as.
- It does not decide whether a payer deduction was contractually valid. It quantifies and groups them so you can take it up.
- It does not confirm an unbilled item. It flags the pattern for verification against the case file.
- It does not advise on GST, TDS or accounting treatment for healthcare services.
- It reads the export. It cannot see the case file, the claim portal or the bank.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Revenue far higher than you expect | File is at bill-line level with the bill total repeated | It detects and states the level. Re-export at one level. |
| No waterfall produced | Only billing data supplied, no collections | Add the collections file. Without it there is no realised figure. |
| Deductions shown as one number | No reason codes in the export | Supply reason codes and they group by cause. |
| Large unbilled list | Often genuine, sometimes a pattern mismatch | They are candidates. Verify a sample against case files first. |
| Ageing looks better than reality | Aged from bill date only | Supply submission dates. Unsubmitted claims are your delay. |

---

Part of the [Healthcare skills](../README.md) in the [Claude Skills Library](../../README.md).
