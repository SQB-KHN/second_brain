# Where the Money Actually Comes From

Splits your sales into contribution by product, customer, channel and outlet, so you can see what makes money, what quietly loses it, and how concentrated the profit really is.

---

## Who this is for

Anyone who owns the whole result: founders of small and medium businesses, SME proprietors in manufacturing, trading and distribution, D2C and ecommerce founders, agency and consultancy owners, restaurant, retail, clinic and gym owners, professional practice owners, and second-generation family business managers.

## The problem it solves

The business is profitable, so it must be working.

Underneath that single number, some products lose money on every sale. Two customers are subsidising the rest. One part of the business has quietly funded another for three years. None of this is visible in a P&L, because a P&L answers "did we make money" and never "where did it come from".

Nobody looks, for a reason that is not laziness. Doing it properly means deciding which costs vary with a sale, netting off discounts and returns that sit in three different places, deduplicating customers who exist under two codes, then ranking correctly rather than by margin percentage. Two or three days, and the accountant was not hired to do it. So the decision that follows, which products to stop and which customers to reprice, gets made on instinct, and instinct usually protects the largest customer, who is often worth least.

---

## What you give it

**Minimum:** sales with enough detail to split them, and the costs that vary with those sales.

| Extra data | What it unlocks |
|---|---|
| **Which costs vary with each sale** | Contribution, which is the only honest number for a keep-or-drop decision |
| Dimensions: product, customer, channel, outlet, region | Every cut of profitability. More dimensions, more findings |
| **Discounts, returns and credit notes** | The real price. Sales recorded gross of discount overstate every margin |
| Cost history, and what you want to decide | Where cost moved and price did not, the commonest silent loss-maker, and what gets allocated |

**Handled automatically:** discounts held separately from sales, returns as positive rows, free samples and replacements at zero value, related-party sales at non-market prices, the same customer under several codes, standard cost against actual, header rows, brackets and Indian digit grouping.

It names the identifying columns first and offers to run de-identified. It needs a customer identifier, not a name.

## What you get back

1. Total contribution, where it comes from, and the largest single loss
2. **Contribution by dimension**, ranked by total contribution with margin alongside
3. **Concentration in three directions**: revenue, profit, and loss
4. **The below-zero list**: every item or customer with negative contribution, annualised
5. The long tail: how much produces almost nothing
6. A fully allocated view where you ask for one, with contribution beside it
7. **Watch list**: where cost has moved and price has not
8. Decisions, each with its consequence
9. What the data cannot settle, and what would settle it

An Excel version with one sheet per dimension is offered at the end.

---

## Why it leads with contribution, not profit

Contribution is revenue minus the costs that vary with the sale. It is the honest number for a keep-or-drop decision, because **dropping a product removes its contribution and leaves the fixed costs exactly where they were.**

Allocating rent and salaries across products makes something look unprofitable when it is in fact helping pay for the roof, and owners close working product lines over this every year. So you get both views, labelled:

| View | The question it answers |
|---|---|
| **Contribution** | Should we stop selling this |
| **Fully allocated** | Is the business as a whole covering its costs |

And an allocated loss is never presented as a reason to drop something without the contribution figure beside it.

## Ranked by total, never by percentage

A 60 percent margin on something you sell twice a year is worth less than 18 percent on something you sell every day.

Ranking by margin percentage is the commonest way an owner drops the wrong product, because percentage feels like the measure of a good one. Everything here ranks by **total contribution**, with the percentage alongside.

## Three concentrations, and the second is the finding

Revenue concentration is the one everybody knows: a few customers are most of the turnover.

**Profit concentration is usually far sharper**, and it is the number nobody has: it is common for a minority of customers to produce all the profit while the rest consume part of it. Loss concentration then names the specific items below zero, costed per year rather than per unit.

One sentence usually carries the whole analysis: "Three customers are 61 percent of profit, and eleven are below zero contribution costing 4.2 lakh a year."

## What good output looks like

A strong result names something you were protecting. Usually a high-revenue customer whose contribution, once discounts and servicing costs are netted, turns out to be near zero.

It should also refuse to recommend dropping anything on margin alone. Every candidate comes with what else it carries: volume that absorbs fixed cost, a relationship that brings other business, a product that completes a range. **Dropping on margin alone is how a business loses the product that was making the others sellable.** If everything comes back healthy, check whether discounts and returns were included. Sales recorded gross of discount overstate every margin in the file, and it is the commonest reason this analysis looks reassuring.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This runs on your file and will not do the arithmetic in prose.
2. Download this folder, or make a folder named `owner-unit-economics` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the sales file and say what varies with a sale.

Examples that work:

- "A year of sales by product and customer. Materials and freight vary, everything else is fixed. What is losing money?"
- "I think two customers are carrying the whole business. Am I right?"
- "My accountant says this product line loses money. Check that before I close it."
- "Costs went up 14 percent last year. Where has that landed?"

Saying which costs vary and which do not is the input that decides whether the answer is useful.

---

## How it protects accuracy

- Contribution by dimension is proved to sum to total contribution, and revenue to the file's own total
- Discounts, returns and credit notes are netted with their value stated, because gross sales overstate every margin
- **Every allocation states its basis**, and no allocated figure appears without contribution beside it
- Rankings are by total contribution, and any percentage ranking is labelled as such
- Below-zero items are annualised, so the cost is a real number rather than a rate
- Duplicate customer or product codes are proposed and shown rather than merged silently, and excluded rows are always stated with their value

## Limits worth knowing

- It does not tell you to drop a customer or product. It sizes the decision and names what else that item carries.
- It does not decide your cost allocation, and it will say that a different basis gives a different answer.
- It does not give tax or accounting advice. These figures are for management decisions, not for filing.
- It cannot see costs you did not give it, including your own time and the working capital a slow payer ties up.
- It reads the file. If the file is wrong the analysis is confidently wrong, which is why exclusions are always stated.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Margins higher than you expect | Sales recorded gross of discount | Supply the discount data. It is the commonest reason this looks reassuring. |
| A product shown as profitable that you believe loses money | Contribution view, not fully allocated | Both are shown. Check which question you are asking. |
| Your biggest customer ranks low | Revenue and profit rank differently | Usually the finding. Check the discount and servicing cost. |
| One customer appears twice | Two codes for one relationship | It proposes the merge and shows it. Confirm and rerun. |
| It will not recommend dropping anything | It names what else the item carries | Deliberate. Margin alone is not a reason. |
| Thin analysis | Only one dimension in the file | Add customer, channel or outlet. Each one is a different finding. |

---

Part of the [Business Owners skills](../README.md) in the [Claude Skills Library](../../README.md).
