# Cash Flow and Scenario Planning

Builds a 13-week rolling cash forecast from receivables, payables and fixed costs, stress tests it, and names the exact week cash gets tight.

---

## Who this is for

Finance professionals who own the cash question: finance managers and controllers, FP&A analysts, accountants advising small business clients, and finance leads at startups and SMEs where the runway question comes up weekly.

## The problem it solves

Cash forecasting is rebuilt from scratch almost every time it is needed, usually in a hurry, usually with one optimistic assumption buried in it: that invoices collect on their due date. They do not. That single assumption is why most cash forecasts fail in exactly the week they were supposed to warn about.

This skill derives collection behaviour from what actually happened, runs three scenarios, and gives a dated answer rather than a mood. Saves two to four hours per forecast and makes a weekly cash view practical instead of a quarterly panic.

---

## What you give it

**Required:**

| Input | Detail |
|---|---|
| Opening cash balance | As at the forecast start date |
| Receivables ageing | Customer, invoice, amount, due date or ageing bucket |
| Payables ageing | Vendor, amount, due date |
| Fixed monthly outflows | Salaries, rent, EMIs, anything recurring |

**Each of these sharpens the forecast:**

| Extra data | What it unlocks |
|---|---|
| Historical collection data | Collection assumptions derived from actual behaviour rather than estimated |
| Credit line limit and drawn amount | Headroom line and realistic drawdown sizing |
| Known one-offs (capex, bonus, advance tax, loan repayment) | Removes the most common source of forecast surprise |
| Your minimum operating balance | Warnings fire at your real threshold, not at zero |
| Customer payment terms per account | More accurate cohort timing |

**Handled automatically:** Dr/Cr columns, brackets for negatives, Indian digit grouping, ageing buckets held as text, subtotal rows. It will ask whether your ageing runs from invoice date or due date, because the two give different answers and the file rarely says.

## What you get back

1. A two-line verdict: can you cover the window, and if not, when it breaks and by how much
2. The 13-week table, dated weeks as columns
3. Three scenarios compared, each with its assumption stated on the same line as its result
4. Dated pressure points, with amounts, not vague warnings
5. Ranked actions naming the specific overdue accounts and payables from your file
6. Every assumption listed plainly, including the ones you could not supply

An Excel version with switchable scenario inputs is offered at the end.

---

## The three scenarios

Only collection speed varies. Outflows stay constant, because most are contractual and varying both sides at once produces a forecast nobody can read.

| Scenario | Assumption |
|---|---|
| Base | Collection behaviour observed in your own history, or the rate you supply |
| Downside | Collections slip 15 days further, anything past 90 days collects nothing |
| Upside | Terms hold, and follow-up on the largest overdue accounts lands inside the window |

Receivables over 120 days are either heavily discounted or excluded from the base case, with the excluded amount always stated.

## Statutory payments

It will ask you to confirm your GST, TDS, PF and ESI payment dates against your own compliance calendar, and offers common ones only as a starting point flagged for confirmation.

It places the outflow on the grid. It does not compute a tax liability or tell you when a payment is due. Deadlines change and vary by taxpayer category, so that stays with you and your advisor.

## What good output looks like

A strong forecast gives you a date, not a mood: "Closing balance falls to a shortfall of 18 lakh in the week of 12 October under the base case, and the week of 28 September under downside." The actions name real accounts from your own file, largest first, and every assumption sits next to the number it affects.

If all three scenarios look nearly identical, your receivables sit in the current bucket and collection timing is not your risk. That is a finding. If the base case looks optimistic, no collection history was supplied and stated defaults were used.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities.
2. Download this folder, or make a folder named `finance-cash-flow-forecast` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the ageing files and give the opening balance.

Examples that work:

- "Build a 13-week cash flow from these ageing reports, opening balance 42 lakh"
- "Can we make payroll on the 30th if collections stay as they are"
- "What happens to cash if our top three customers pay 30 days late"
- "Which overdue accounts do I chase first to cover next month"

---

## How it protects accuracy

- Each week's opening balance is proved equal to the prior week's closing balance in code
- Modelled collections can never exceed receivables actually outstanding
- Excluded old receivables are stated with their value, never dropped quietly
- Every assumption appears in the output, including each one you could not supply
- Scenarios differ only through the collection assumption, so the comparison means something

## Limits worth knowing

- It is a forecast, not a promise. Accuracy rests on the collection assumption, which is why that assumption is always visible.
- It does not compute tax liabilities or confirm statutory due dates.
- It does not recommend borrowing or any specific financial product. It sizes the gap and its timing and leaves the decision with you.
- It cannot see your bank or ledger. It models the files you provide.
- It shows the impact of delaying a payable. It does not decide which vendor to delay.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Forecast looks too optimistic | No collection history supplied, so defaults were used | Provide historical collection data, or give your own rate. |
| Weeks do not chain correctly | Ageing basis was ambiguous | Confirm whether buckets run from invoice date or due date. |
| A known payment is missing | Not in either file and not mentioned | List recurring and one-off outflows when you upload. |
| Scenarios look almost identical | Receivables concentrated in current bucket | Expected. It means collection timing is not your risk. |
| Nothing happens on upload | Code execution is off | Turn it on in Settings, under Capabilities. |

---

Part of the [Finance skills](../README.md) in the [Claude Skills Library](../../README.md).
