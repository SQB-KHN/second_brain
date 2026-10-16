# Account Plan and Whitespace

Turns what an account buys into computed concentration risk, a whitespace grid that separates opportunity from ignorance, relationship coverage, and plays ranked by winnability.

---

## Who this is for

Anyone who grows existing accounts rather than only finding new ones: key account managers, enterprise account executives, regional and area sales managers, channel and distributor managers, customer success and renewals owners, and founders managing a handful of large customers.

## The problem it solves

Account plans get written once a year for a review, in a template, and never opened again.

Meanwhile the account's revenue is concentrated in one product, one business unit and one relationship, and nobody has noticed because the total still looks healthy. Then the contact moves job, or one product gets replaced, and 60 percent of the account leaves in a quarter.

The second failure is the whitespace slide. Every empty cell gets presented as opportunity, when the honest description of most is that nobody has ever asked. Those need completely different work, one a sales motion and the other research, and calling both "pipeline" is how account plans produce nothing. Doing this properly means breaking revenue down three ways, mapping who you know against who decides, and being honest about which cells are genuine gaps. It takes a day per account, so it happens annually, which is about four times too rarely.

---

## What you give it

**Minimum:** what the account buys today, and from which parts of their organisation.

| Extra data | What it unlocks |
|---|---|
| Purchase history by product and by unit or location, with values | Makes whitespace real rather than theoretical, and computes all three concentrations |
| **Who you know there, by role** | Relationship coverage, the most predictive input available and almost never written down |
| **Their stated priorities, in their own words** | Plays connected to what they are actually trying to do, rather than to what you sell |
| Contract and renewal dates, competitors inside, and your capacity | Risks ordered ahead of growth, cells marked taken rather than empty, and a ranked list that becomes a plan for this quarter |

It names the contacts in your input first, and offers to work with roles rather than names.

## What you get back

1. Headline: current revenue, the largest concentration risk, and the highest-winnability play
2. **Revenue today, three ways**: by product, by unit, by buyer, each with a computed concentration percentage
3. **Risks before growth**: renewals, concentration, single-threading, competitors inside, silence
4. **Whitespace grid**, with unknown cells distinguished from genuine no-need cells
5. Relationship coverage per unit, with single-threaded revenue counted and valued
6. Their priorities, in their words where supplied and marked inferred where not
7. **Plays ranked by winnability against value**, each with what has to be true
8. Capacity check: what is possible this quarter against what you have
9. Review triggers

An Excel version with the whitespace grid as a working sheet is offered at the end.

---

## Three concentrations, three different ways to lose the account

| Broken down by | What concentration means |
|---|---|
| **Product or service** | One product decision can end the account |
| **Business unit, or buyer** | One customer inside one customer, or one person leaving with the revenue |

Each is computed as a percentage, not described. Where any one exceeds a majority, it is named as the account's primary risk **ahead of any growth plan**, because a growth plan layered on unmanaged concentration is the wrong priority order, and it is the order most account plans use.

## The whitespace grid, and the cells that matter most

Rows are what you could sell. Columns are the units that could buy it. Every cell carries one of four states, and none is left blank:

- **Bought from us**, with the value
- **Bought from somebody else**, with who where known
- **Not bought by anyone**, meaning the need may genuinely not exist
- **Unknown**

The unknown cells are the finding. A plan presenting them as opportunity will not convert, because you cannot run a sales motion against something you have not established exists. Separating them tells you which cells need a conversation and which need a question.

## The question the section exists for

For every unit that matters: who do you know, would they take your call, have you met anyone who could say no, and **if your main contact left tomorrow, what would happen to this revenue?**

That last one converts a vague worry into a number. Single-threaded revenue gets counted and valued, and once somebody sees the figure it usually stops being a vague worry.

## Winnability beats value in the ranking

Plays get ranked on winnability against value, not on value alone.

The biggest number is rarely the next move; that is usually the one where you already have the relationship and the evidence. Ranking on value is why account plans list five plays and deliver none, and why the capacity check is in the output.

## What good output looks like

A strong plan puts something uncomfortable in the first two lines: a concentration percentage you had not computed, or a renewal inside the horizon with one relationship behind it.

The plays section should be shorter than you expected and ordered differently from how you would have ordered it, and the grid should have unknown cells in it, because an account where you know every cell is one you have already fully mapped. If everything comes back as opportunity with no unknowns, you supplied assumptions about their needs as facts.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill computes the concentrations and the grid, and will not do it in prose.
2. Download this folder, or make a folder named `sales-account-plan` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Give it the purchase history and who you know.

Examples that work:

- "Our biggest account, 2.8 crore a year. QBR next month. Where is the risk and where is the growth?"
- "This distributor has been flat for two years. What are we not selling them?"
- "Renewal in ten weeks and my champion just moved teams. Assess it."
- "Map the whitespace. Here is what they buy and here are their business units."

Supplying their own words about their priorities, rather than your read on them, changes which plays come out on top.

---

## How it protects accuracy

- Revenue by product, by unit and by buyer are each proved to sum to the account total
- Concentration percentages are computed in code rather than described
- Every whitespace cell carries one of four states, with none left blank
- **Unknown cells are counted separately from no-need cells**, because they need different work
- Single-threaded revenue is counted and valued rather than mentioned, and every play names which stated priority it connects to or is marked as connecting to none
- Priorities taken from the account's own words are kept distinct from inferred ones
- Risks appear before growth plays in the output, every time

## Limits worth knowing

- It does not forecast what the account will buy. It sizes plays and ranks them on winnability.
- It does not call an empty whitespace cell an opportunity. Where nobody has asked, it says nobody has asked.
- It does not advise on pricing, discount or contract terms.
- It does not research the account for you. It works on what you supply, and marks inferences as inferences.
- It cannot see your CRM, their org chart or their budget.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Concentration higher than you thought | Usually genuine, and usually the finding | Address the concentration before the growth plan. |
| Most whitespace cells are unknown | Nobody has asked those units | Correct. Those need a question, not a pitch. |
| Plays ordered differently from your instinct | Ranked on winnability, not value | Check the reason on each. The big one is usually not the next one. |
| It puts renewal risk above expansion | A renewal sits inside the horizon | Deliberate. Expansion on an unsecured renewal is the wrong order. |
| Priorities marked inferred | You did not supply their own words | Paste their annual report, a public statement, or a stated internal goal. |

---

Part of the [Sales skills](../README.md) in the [Claude Skills Library](../../README.md).
