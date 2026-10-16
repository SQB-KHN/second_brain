# Purchase and Freight Bill Audit

Audits vendor and transporter invoices against the PO, the goods receipt and the rate card, and returns a valued exception list you can raise a debit note from.

---

## Who this is for

Anyone who signs off invoices or answers for what was paid: purchase and procurement managers, accounts payable and bill passing teams, logistics and dispatch managers, stores and materials managers, plant finance, and founders approving their own vendor bills.

## The problem it solves

Bill passing is a signature at the end of a queue. The rate was agreed months ago by somebody else, the goods were received by somebody else, and the person approving has thirty invoices and an afternoon.

So the checks that get done are the visible ones: does the invoice add up, is the vendor correct. The one that matters, whether the amount billed is the amount owed, needs three documents open at once and a rate card nobody can find. It gets skipped, and overcharges survive for years because nothing about them looks wrong.

Freight is worse. Chargeable weight, slab boundaries, fuel surcharge formulas, detention clocks and out-of-area charges are all contractual, all arithmetic, and almost never checked line by line. This runs the full match, values every exception, and separates what you can recover from what you cannot yet prove. Most first runs find money.

---

## What you give it

**Required:** the invoices, plus whatever states the entitlement. For purchases that is the purchase order and the goods receipt note. For freight it is the rate card or the transport contract. The invoice is the claim; the other document is the agreement.

**Each of these sharpens it:**

| Extra data | What it unlocks |
|---|---|
| Line-level rather than header-level data | Price and quantity variance per item, instead of a total that hides both |
| Several periods of invoices at once | Duplicate detection, and cumulative over-billing against one PO |
| Shipment dimensions and weights | Chargeable weight recomputation, the largest single freight leak |
| Contracted free time and the event it starts from | Detention and demurrage verification |
| Whether freight and packing sit inside the PO rate | Resolves a large share of apparent overcharges before they are raised |

**Handled automatically:** PO and invoice references formatted differently between systems, such as `PO/2026-27/0042` against `PO20262742`. Also header rows, brackets for negatives, Indian digit grouping, and tax split across CGST, SGST and IGST columns.

If you have invoices but no PO or rate card, it will say plainly that this becomes a duplicate and arithmetic check rather than an audit, then run that.

## What you get back

1. **Recoverable total**, one line at the top, separated from the value that cannot be verified
2. Exception list: billed, owed, difference, category, the evidence, and who resolves it
3. **Duplicate candidates**, both rows shown side by side
4. Freight findings, each quoting the contract clause or rate card line it rests on
5. Received not billed, the liability side, stated separately
6. Unverifiable invoices, what is missing and who can supply it
7. Arithmetic differences, netted inside tolerance and itemised above it
8. Data quality notes

An Excel workbook with one sheet per category is offered at the end.

---

## What the three-way match actually tests

Six different failures, each with a different owner. Most manual checking finds only the first.

| Test | The failure it catches |
|---|---|
| **Price variance** | Rate billed above the rate on the PO |
| **Quantity variance** | Billed for what was ordered rather than what arrived. The most common overcharge there is |
| **Cumulative over-billing** | Every invoice passes on its own while the total exceeds the PO. Line-by-line checking cannot see this |
| **Unordered items** | Billed but not on the PO at all |
| **Received not billed** | A liability you have not recorded. Not an overcharge, and reported separately |
| **Missing GRN** | An invoice nobody can verify. Not a variance, and it should not be passed |

## Where freight money actually leaks

| Test | What goes wrong |
|---|---|
| **Chargeable weight** | Volumetric weight computed on a divisor that is not the one in your contract, which inflates every bill on the lane |
| **Slab boundaries** | A 480 kg shipment billed at the 500 kg slab, which may or may not be correct under your contract |
| **Lane and area** | Out-of-delivery-area charges applied to a location that is inside the covered area |
| **Minimum and fuel** | A minimum applied on top of a rate that includes it, or last quarter's surcharge carried forward |
| **Detention** | Free time counted from the wrong event, or clocked through hours the contract excludes |
| **Accessorials** | Loading, waiting and multi-point charges with nothing in the contract behind them |

Every finding quotes the clause it rests on, because a freight claim without the clause attached does not survive the vendor call.

## Why recoverable and unverifiable stay apart

An overcharge with a rate card behind it is a debit note. An invoice with no goods receipt is a question for your stores team. Reported as one number, the total looks better than it is and collapses in the first vendor meeting when half the items turn out to have no evidence. The output totals them separately, every time.

## What good output looks like

A strong result leads with a number you can act on: "4.7 lakh recoverable against evidence, a further 2.1 lakh on invoices that cannot be verified without a GRN." Then every line traces to a rate card entry, a PO line or a receipt quantity.

Duplicates come back as candidates, never as accusations, with both rows side by side so you can see for yourself.

If almost everything comes back clean, check whether the PO data is line-level. Header totals will match while every underlying rate is wrong, and that is the most common reason a bill audit finds nothing.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill runs Python on your files and will not work without it.
2. Download this folder, or make a folder named `ops-bill-audit` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the invoices and the entitlement side, and say which is which.

Examples that work:

- "Three-way match these. PO file, GRN file, and last month's vendor invoices."
- "Here are six months of transporter bills and our rate card. What have we overpaid?"
- "This vendor billed 11.2 lakh, our PO says 10.4. Find the difference line by line."
- "Are the detention charges on these bills supportable under this contract?"

---

## How it protects accuracy

- Every invoice line is either matched or listed as an exception, proved in code, with none unaccounted for
- Quantity comparisons are blocked until all three documents share a unit of measure, since a PO in boxes against an invoice in pieces shows a twelvefold overcharge that does not exist
- Cumulative billing per PO line is always tested, not just invoice by invoice
- Every recoverable rupee traces to a specific rate card line, PO line or receipt quantity
- Duplicates are labelled candidates rather than confirmed, since a false accusation costs a relationship, and rounding differences inside tolerance are netted into one figure rather than padding the list

## Limits worth knowing

- It does not raise a debit note, withhold a payment or contact a vendor. It produces the evidence.
- It does not decide tax rates, tax heads, input credit eligibility, or any customs or HS classification.
- It does not interpret genuinely ambiguous contract wording; it quotes the clause and names the question. It cannot audit against an entitlement it was not given, so no rate card means no rate audit.
- It reads documents, not reality. If the goods receipt is wrong, the audit inherits that.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Almost no exceptions found | Header-level data instead of line-level | Re-export at line level. Header totals hide every rate error. |
| Huge overcharges on everything | Unit of measure differs between PO and invoice | It flags this and stops. Supply the conversion. |
| Real invoices shown as unmatched | Reference formats differ too far to bridge | Tell it your PO numbering pattern. |
| Duplicates flagged that are genuine | Legitimate part-billing reusing the same amount | They are candidates only. Confirm from the two rows shown. |
| Freight findings without amounts | Rate card supplied without the slab or divisor rules | Supply the full rate card, including the volumetric divisor. |

---

Part of the [Operations and Supply Chain skills](../README.md) in the [Claude Skills Library](../../README.md).
