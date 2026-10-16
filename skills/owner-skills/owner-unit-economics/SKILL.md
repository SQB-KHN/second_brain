---
name: owner-unit-economics
description: Split sales into contribution by product, customer, channel and outlet to find what makes money, what loses it, and where the profit is concentrated. Use for profitability analysis.
---

# Where the Money Actually Comes From

The business is profitable, so it must be working. Underneath that single number, some products lose money on every sale, two customers are subsidising the rest, and one part of the business has quietly funded another for three years. Nobody looks, because the P&L does not ask that question and the accountant was not hired to.

## When to use this

Trigger on: profitability, unit economics, which products make money, customer profitability, margin analysis, contribution, loss-making, product mix, break-even, cost per order, "are we actually making money", "which customers are worth keeping".

## Before you start

Required: sales with enough detail to split them, and the costs that vary with those sales.

Ask, briefly:
1. **What one row represents.** An order, an invoice line, a project, or a month per customer. Everything downstream depends on this, and getting it wrong makes every number wrong.
2. Which costs vary with each sale and which do not. Materials, packing, freight, payment charges, commission and direct labour usually vary. Rent and salaries usually do not. If they cannot say, work with what clearly varies and state what was left out.
3. **What decision this is for.** Whether to drop a product, whether a customer is worth keeping, whether a channel pays. It changes what gets allocated and what does not.
4. Which dimensions the data carries: product, customer, channel, outlet, region, salesperson, project.
5. Whether returns, discounts and write-offs are inside the sales figure or sit elsewhere. They usually sit elsewhere, and they usually change the answer.

## Check for personal data first

Customer-level files carry names, phone numbers and addresses. Say once that this analysis needs a customer identifier rather than a name, and offer to run on a de-identified file. Then continue with whatever they choose.

## Workflow

### 1. Profile the file for the things that quietly break this analysis

- **Sales recorded gross of discount**, with the discount held somewhere else. The discounted price is the real price.
- Returns and credit notes held separately, or as positive rows
- Free samples, replacements and warranty issues recorded at zero value, which look like sales with no revenue
- Intercompany or related-party sales at non-market prices
- **The same customer under several codes**, which splits one relationship into three small ones
- Standard cost rather than actual cost, which is fine but changes what the answer means
- Header rows, brackets for negatives, Indian digit grouping

State row count, total sales, and everything excluded with its value.

### 2. Compute in code, never in prose

Every margin, allocation and ranking runs as Python. This analysis ends with somebody discontinuing a product, and an arithmetic slip inside a sentence becomes a decision.

### 3. Start with contribution, not with net profit

Contribution is revenue minus the costs that vary with the sale. It is the honest number for a keep-or-drop decision, because dropping a product removes its contribution and leaves the fixed costs exactly where they were.

Compute contribution per unit and in total, per dimension. **Rank by total contribution, never by margin percentage.** A 60 percent margin on something sold twice a year is worth less than 18 percent on something sold daily, and ranking by percentage is the commonest way an owner drops the wrong product.

### 4. Be explicit about allocating fixed costs

Allocating rent and salaries across products makes something look unprofitable that is in fact contributing. State plainly:

- **The contribution view**, which answers "should we stop selling this"
- **The fully allocated view**, which answers "is the business as a whole covering its costs"
- The basis used for any allocation, and that a different basis gives a different answer

Never present an allocated loss as a reason to drop something without showing contribution beside it. That single confusion has closed working product lines.

### 5. Find the concentration, in three directions

- **Revenue concentration.** What share comes from the top few customers, products or outlets.
- **Profit concentration**, which is usually far sharper than revenue concentration and is the actual finding. It is common for a minority of customers to produce all the profit while the rest consume it.
- **Loss concentration.** Which specific items or customers sit below zero contribution, and what that costs per year.

State it in one line with numbers. "Three customers are 61 percent of profit, and eleven are below zero contribution costing 4.2 lakh a year" is the whole analysis.

### 6. Look at what nobody examines

- **The long tail.** How many items or customers produce almost nothing, and what they cost in attention, stock and admin.
- **The high-revenue low-margin customer**, which is the one everybody protects and few examine.
- Products that only sell inside a bundle, whose standalone margin is misleading.
- **Anything where cost has moved and price has not**, which is the commonest source of a silent loss-maker.

### 7. Say what the data cannot settle

Owner data is usually incomplete. Name what is missing and what it would change: the cost of servicing a difficult customer, the owner's own time, the working capital a slow payer ties up, the storage a slow mover occupies.

Where a customer looks profitable on paper and is expensive in practice, say the data does not capture it and name what would.

### 8. Turn it into decisions, with the consequence of each

For each candidate to drop, raise or renegotiate: what the change is worth, what would be lost, and what has to be true for it to work.

**Never recommend dropping a customer or product on margin alone.** Name what else it carries: volume that absorbs fixed cost, a relationship that brings other business, a product that completes a range.

## Output format

**1. Headline.** Total contribution, where it comes from, and the largest single loss.

**2. Contribution by dimension.** Ranked by total contribution, with margin shown alongside.

**3. Concentration.** Revenue, profit and loss, each as a share and named.

**4. Below-zero list.** Every item or customer with negative contribution, annualised.

**5. The long tail.** Count and value of what produces almost nothing.

**6. Fully allocated view**, where asked for, with its basis stated and contribution beside it.

**7. Watch list.** Where cost has moved and price has not.

**8. Decisions**, each with its consequence.

**9. What the data cannot settle**, and what would settle it.

**10. Data quality and exclusions.**

Offer the Excel version with one sheet per dimension. Build it only if asked.

## Checks to run before delivering

- Contribution by dimension sums to total contribution, and revenue sums to the file's own total
- Discounts, returns and credit notes are netted, with their value stated
- Every allocation states its basis, and no allocated figure appears without the contribution figure beside it
- Rankings are by total contribution, and any percentage ranking is labelled as such
- Below-zero items are stated as an annual value, not only as a rate
- Duplicate customer or product codes are proposed for merging and shown
- Excluded rows are stated with their value
- Every figure was computed in code

## What this skill does not do

- It does not tell you to drop a customer or a product. It sizes the decision and names what else that item carries.
- It does not decide your cost allocation. It shows contribution and any allocated view separately, and says the basis changes the answer.
- It does not give tax or accounting advice. Its figures are for management decisions, not for filing.
- It cannot see costs you did not give it, including your own time.
- It reads the file. If the file is wrong the analysis is confidently wrong, which is why every exclusion is stated.
