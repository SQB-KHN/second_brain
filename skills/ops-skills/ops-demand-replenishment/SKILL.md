---
name: ops-demand-replenishment
description: Forecast demand from sales history and produce a reorder list with safety stock, reorder points and MOQ and budget constraints applied. Use for replenishment, purchase planning or safety stock.
---

# Demand Forecast and Replenishment Plan

The reorder list is the most consequential document in operations and the one most often produced from memory. Order too little and a line stops. Order too much and the money is gone for a year. Most replenishment runs on last month's sales, which is the single number guaranteed to understate demand for exactly the items that ran out.

## When to use this

Trigger on: replenishment, reorder, purchase plan, indent planning, what should I order, demand forecast, safety stock, reorder point, min max levels, stock planning, "how much should we buy", MRP run.

## Before you start

Required: sales or consumption history by item and period, current stock on hand, and lead time.

Ask, briefly:
1. **Stockout history.** Which items were unavailable, and roughly when. Without it the forecast understates demand for every item that ran out, which is the set you care most about. If the system does not hold it, ask which items went out and approximately when. An approximate answer beats none.
2. **Open purchase orders** already placed and not yet received, with expected dates. Ignoring these is how items get ordered twice.
3. **Target service level**, per class if they differentiate. Say plainly that 99 percent costs far more stock than 95, and that applying one number to every item is the most common and most expensive default in the field.
4. **Constraints:** minimum order quantity, pack or carton size, supplier order cycle or fixed order days, budget for the period, shelf life, storage limits.
5. **Anything the history cannot contain.** A promotion, a new customer, a tender, a price change, a discontinuation, a festival peak. This is the most valuable input available and it is never in the file.

If they cannot supply stockout history or open POs, proceed, and state next to the affected numbers exactly what each omission does to the answer. Do not stall.

## Workflow

### 1. Profile and clean the history

- Aggregate to a consistent period, weekly or monthly, and state which
- **Mixed units of measure** in the quantity column, which will silently corrupt every forecast downstream
- **The same item under two codes**, which splits one demand history into two thin ones and under-forecasts both
- **Returns and credit notes**, which must be netted rather than counted as demand
- **Intercompany and free-issue movements**, which are not customer demand
- **Sample, damage, scrap and internal consumption**, separated from sales

State the periods covered, the items in scope, and everything excluded with its quantity.

### 2. Compute in code, never in prose

Every run rate, every safety stock figure, every reorder point and every constraint adjustment runs as Python. This one matters more here than almost anywhere, because the output is a quantity somebody will actually buy. An arithmetic slip inside a sentence becomes an order.

### 3. Correct for censored demand, and do not skip this step

Sales history records what you sold, not what customers wanted. In any period an item was out of stock, recorded demand is capped by supply. A forecast built on that history is too low, so the item runs out again, and the history now says demand is falling.

Where stockout periods are known: either exclude those periods from the demand average, or scale them up by the in-stock fraction of the period. State which method was used and which items it touched.

Where they are not known, flag the items whose pattern shows the signature: sales sitting flat at a suspiciously round number, or dropping to zero mid-period and resuming afterwards. Say plainly that these are likely understated and by roughly how much.

This one correction changes more reorder quantities than any other step here.

### 4. Strip out what is not demand

- **One-off bulk orders.** A single order five times the normal size is an event, not a trend. Flag it, exclude it from the run rate, and state the amount excluded. If the user says it repeats, put it back.
- **The tail of a discontinued item**
- **The launch ramp of a new item**, where three periods cannot support a seasonal forecast

Never smooth away an outlier silently. Every exclusion is stated with its value, because an invisible exclusion is indistinguishable from an error.

### 5. Classify by demand pattern before forecasting

One method does not fit all items, and using one is why forecasts get distrusted.

- **Smooth.** Regular demand, low variability. A moving average or exponential smoothing is sufficient and nothing more elaborate is justified.
- **Seasonal.** A repeating annual shape. Needs at least two full cycles to detect. With less history, say so and do not claim seasonality.
- **Trending.** A persistent direction. Separate a real trend from a run of three good months.
- **Intermittent.** Demand in some periods and zero in many. A moving average is actively wrong here, because it produces a small non-zero number every period and quietly builds stock nobody ordered. Forecast the size of a demand event and the interval between events separately.
- **Erratic.** High variability with no pattern. Say that it cannot be forecast usefully, and that the answer is a service level decision rather than a better model.

State the pattern and the method chosen per item. A forecast whose method is invisible cannot be challenged, and therefore cannot be trusted.

### 6. Forecast over the right horizon, and give it a range

Produce expected demand over **lead time plus the review period**, which is the horizon that actually determines whether you stock out. A calendar month is the wrong window and is the one most people use.

Report a range alongside the point forecast. Never a bare single number: it invites a precision the data does not support, and the entire safety stock calculation exists precisely because the point forecast is wrong.

Where the user named something the history cannot contain, apply it as a stated adjustment on top, labelled, so the forecast and the assumption stay separable later.

### 7. Size safety stock from service level and variability, not from habit

Safety stock exists to absorb variability in demand and in lead time. A flat "two weeks of cover" over-stocks the predictable items and under-stocks the volatile ones, which is why it manages to be both expensive and ineffective.

Compute it from the target service level and the observed variability of demand and lead time together. Where lead time variability is unknown, say so, and note that it usually dominates the calculation.

Differentiate by class. A high service level on erratic C items is where inventory budgets die. State the stock value each service level buys, so the choice is visible as a cost rather than a preference.

### 8. Set reorder point and order quantity, applying constraints visibly

- **Reorder point:** expected demand over lead time, plus safety stock
- **Order quantity:** bring stock to the target level, then apply constraints in order. Minimum order quantity, then pack size rounding, then shelf life, then budget.
- **Net off open purchase orders** before recommending anything
- **Show every constraint that changed a number.** If MOQ forces 500 units where 180 were needed, say so, state the resulting months of cover, and value the excess it creates. A constraint that silently triples an order is how dead stock is born.
- Where shelf life is shorter than the cover an order creates, cap the order and say why

### 9. Handle a budget constraint by consequence, not proportionally

If the full requirement exceeds the budget, do not scale everything down by the same percentage. That is the worst available allocation, because it under-buys the critical items and still buys the marginal ones.

Rank by consequence: items whose stockout stops production or breaks a committed order first, then A items by service impact, then the rest. Show what is funded, what is deferred, and the specific exposure each deferral creates.

### 10. Say what to stop buying

The reorder list is half the job. Also name the items with cover far beyond any plausible need, the ones whose forecast has fallen, and the open POs that should be reduced or cancelled.

Operations teams are measured on availability, so this half almost never gets done, and it is where the cash is.

## Output format

**1. Headline.** Items reviewed, items to order, total order value, and the budget position.

**2. Reorder list.**

| Item | Class | Pattern | On hand | On order | Forecast over horizon | Safety stock | ROP | Suggested order | Constraint applied | Cover after | Value |

Sorted by days until stockout, then by value.

**3. Order now, at risk.** Items already below reorder point, with the date each runs out at the current run rate.

**4. Do not order.** Excess cover, falling demand, and open POs worth reducing.

**5. Forecast basis.** Pattern and method per item, with the range around each forecast.

**6. Censored demand corrections.** Which items, which periods, which method, and the effect on the recommended quantity.

**7. Exclusions.** One-off orders, returns and non-demand movements, each with its value.

**8. Constraints and what they cost.** Where MOQ, pack size, shelf life or budget changed a quantity, and the excess or exposure created.

**9. Budget allocation.** Funded, deferred, and the exposure per deferral.

**10. Assumptions and open questions.**

Offer the Excel version with service level as a switchable input. Build it only if asked.

## Checks to run before delivering

- Suggested order equals target level minus on hand minus on order before constraints, and every constraint adjustment is shown as its own step
- Open purchase orders are netted off every recommendation
- No item is recommended for order and also listed as excess
- Every forecast carries its method and its range
- Safety stock derives from the stated service level and observed variability, and the service level used is stated
- Stockout-corrected items are listed with the method and its effect on the quantity
- Excluded outliers are stated with their value
- Order total reconciles to the sum of line values, and against the budget where one was given

## What this skill does not do

- It does not place an order, raise a purchase order or contact a supplier. It produces a list for a human to approve.
- It does not choose your service level, your budget or your risk appetite. It shows what each choice costs in stock and leaves the choice with you.
- It is a forecast. It cannot know about the tender, the competitor, the regulation or the customer decision that has not happened yet, which is exactly why it asks what is coming.
- It does not decide which supplier to buy from, or at what price.
- It cannot correct for stockouts you cannot identify. Where the history is censored and unmarked, it flags the suspicion and says the number is likely understated rather than presenting it as clean.
