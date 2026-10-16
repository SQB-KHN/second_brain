# Demand Forecast and Replenishment Plan

Forecasts demand from your sales history and produces a reorder list with safety stock, reorder points, and every MOQ, pack size, shelf life and budget constraint applied visibly.

---

## Who this is for

Anyone who decides what to buy and how much: demand and supply planners, inventory and materials managers, PPC executives, purchase managers, retail and multi-store buyers, ecommerce and D2C operations managers, and founders placing their own orders.

## The problem it solves

The reorder list is the most consequential document in operations and the one most often produced from memory. Order too little and a line stops or an order goes short. Order too much and the money is gone for a year, sitting on a shelf.

Most replenishment runs on last month's sales. That is the single number guaranteed to understate demand for exactly the items that ran out, because you cannot sell what you did not have. So the item that stocked out gets under-ordered, stocks out again, and the history now says its demand is falling.

The rest of the errors are structural. One safety stock rule applied to every item, so the predictable ones are overstocked and the volatile ones still run short. A minimum order quantity that quietly triples an order and nobody notices until it is dead stock. Open purchase orders forgotten, so the same item gets bought twice. This does the arithmetic properly, and shows you every place a constraint changed the answer.

---

## What you give it

**Minimum:** sales or consumption history by item and period, current stock on hand, and lead time.

**These change the answer, not just its precision:**

| Extra data | What it unlocks |
|---|---|
| **Stockout history**, even approximate | Correction for censored demand. Without it, every item that ran out gets under-ordered again |
| **Open purchase orders** with expected dates | Stops items being ordered twice, which is the most common single error |
| Target service level, ideally per class | Safety stock sized to a decision rather than a habit |
| MOQ, pack size, supplier order days | Quantities you can actually place, with the cost of each constraint shown |
| Shelf life and period budget | Orders capped before they create expiry risk, and allocation by consequence rather than an across-the-board cut |
| **Anything the history cannot contain** | A promotion, a new customer, a tender, a discontinuation, a festival peak. The most valuable input available and never in the file |

**Handled automatically:** mixed units of measure flagged rather than silently corrupted, the same item under two codes, returns and credit notes netted off, intercompany and free-issue movements separated, sample and scrap issues excluded, header rows, brackets for negatives and Indian digit grouping.

## What you get back

1. Items reviewed, items to order, total order value, and where that leaves the budget
2. **Reorder list** with the constraint applied and the cover it creates shown per line
3. **Order now, at risk**: items already below reorder point, with the date each runs out at the current run rate
4. **Do not order**: excess cover, falling demand, and open POs worth reducing or cancelling
5. Forecast basis: the demand pattern and method per item, with a range around each forecast
6. **Censored demand corrections**: which items, which periods, which method, and the effect on the quantity
7. Exclusions, each with its value
8. **Constraints and what they cost**: where MOQ, pack size, shelf life or budget changed a number
9. Budget allocation: funded, deferred, and the exposure created by each deferral
10. Assumptions and open questions

An Excel version with service level as a switchable input is offered at the end.

---

## The correction almost nobody makes

Your sales history records what you sold, not what customers wanted.

In any period an item was out of stock, recorded demand is capped by what you had on the shelf. Build a forecast on that and it comes out low. Order to the low forecast, stock out again, and the history now shows demand declining on an item that is actually growing.

Where you can tell it which items were out and roughly when, it either excludes those periods from the run rate or scales them up by the in-stock fraction, and states which method it used per item. Where you cannot, it looks for the signature: sales sitting flat at a suspiciously round number, or dropping to zero mid-period and resuming. Those get flagged as likely understated rather than quietly forecast too low. This one correction changes more reorder quantities than anything else the skill does.

## One forecasting method does not fit every item

| Pattern | What it means | What it needs |
|---|---|---|
| **Smooth** | Regular demand, low variability | A moving average. Nothing more elaborate is justified |
| **Seasonal** | A repeating annual shape | Two full cycles of history. With less, it will not claim seasonality |
| **Trending** | A persistent direction | Separating a real trend from three good months |
| **Intermittent** | Demand in some periods, zero in many | Size and interval forecast separately. A moving average is actively wrong here and quietly builds stock |
| **Erratic** | High variability, no pattern | An honest statement that it cannot be forecast, and a service level decision instead |

The pattern and the method are stated per item, because a forecast whose method is invisible cannot be challenged and therefore should not be trusted.

## Constraints are shown, never absorbed

If you need 180 units and the minimum order quantity is 500, the answer is 500. But the output says so explicitly, states the months of cover 500 creates, and values the excess.

A constraint that silently triples an order is how dead stock is born, and it is invisible in any report that shows only the final number. The same applies to budget. When the requirement exceeds what you have, it does not scale everything down proportionally, which is the worst available allocation because it under-buys the critical items and still buys the marginal ones. It ranks by consequence, funds down the list, and states the exposure on everything deferred.

## What good output looks like

A strong plan is uncomfortable in two places. The censored demand section usually shows that several items have been under-ordered for months. And the constraints section usually shows that a few orders are three times larger than the need, because of a minimum order quantity nobody has renegotiated.

The "do not order" list should not be empty. Operations teams are measured on availability, so the half of replenishment that is about stopping purchases almost never gets done, and that is where the cash is. If every forecast comes back wide and erratic, the history is too short or too thin; twelve months at weekly granularity changes the output substantially.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill runs Python on your history and will not work without it.
2. Download this folder, or make a folder named `ops-demand-replenishment` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the history and current stock, and say what constraints you are working under.

Examples that work:

- "Build this month's reorder list. Here is 12 months of sales, current stock and lead times."
- "18 lakh budget and this is the full requirement. What do I buy first?"
- "These items keep stocking out. Here is the history and the dates they were unavailable."
- "Set min-max levels for our A items at 97 percent service level."

Mentioning anything the history cannot know, a promotion, a new customer, a discontinuation, is the highest value sentence you can add.

---

## How it protects accuracy

- Suggested order equals target minus on hand minus on order before constraints, and every constraint adjustment is shown as its own step
- Open purchase orders are netted off every recommendation
- No item is recommended for order and also listed as excess
- Every forecast carries its method and a range, never a bare point estimate
- Safety stock derives from the stated service level and observed variability, and the service level used is printed
- Stockout-corrected items are listed with the method and its effect, and excluded outliers are stated with their value so nothing is smoothed away invisibly

## Limits worth knowing

- It does not place an order or contact a supplier. It produces a list for you to approve.
- It does not choose your service level, budget or risk appetite. It shows what each choice costs in stock and leaves the decision with you.
- It is a forecast. It cannot know about the tender, the competitor or the customer decision that has not happened yet, which is exactly why it asks what is coming.
- It does not choose your supplier or negotiate your price.
- It cannot correct for stockouts you cannot identify. Where history is censored and unmarked, it flags the suspicion rather than presenting the number as clean.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Quantities look too low on your problem items | Stockout periods not supplied, so demand is censored | Say which items were out and roughly when. Approximate is enough. |
| An item recommended that you already ordered | Open POs not supplied | Provide open orders with expected dates. It nets them off. |
| Orders far larger than the need | MOQ or pack size forcing it up | That is stated in the constraint column with the excess valued. Renegotiate the MOQ. |
| Everything labelled erratic | History too short, or too granular for the demand | Supply twelve months. Aggregate weekly rather than daily for slow movers. |
| Safety stock looks very high | Service level applied uniformly across all classes | Differentiate by class. It shows the stock value each level buys. |

---

Part of the [Operations and Supply Chain skills](../README.md) in the [Claude Skills Library](../../README.md).
