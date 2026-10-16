# Customer Language Synthesis

Turns reviews, support tickets, surveys and call notes into the exact words your customers use, with objections and triggers ranked by how often they come up.

---

## Who this is for

Anyone who writes or approves customer-facing words: copywriters, content and brand marketers, growth and performance marketers, product marketers, founders writing their own site, and agency strategists starting on a new client.

## The problem it solves

Copy sounds generic because it is written in the company's vocabulary instead of the customer's. The fix is not better writing. It is having the customer's actual words in front of you before you start.

Most companies already hold everything needed for this. Reviews, tickets, survey responses and call notes sit in four different systems and nobody reads them systematically, because doing it by hand takes a day and produces a document nobody updates.

This does it in minutes and produces something you will actually use. It is also the single most effective defence against output that reads like AI wrote it, because real customer phrasing does not sound like anything a model would generate on its own.

---

## What you give it

Raw customer text. More sources make it stronger.

| Source | What it is good for | How it is skewed |
|---|---|---|
| **Public reviews** | Emotional language, comparisons, deal-breakers | Delighted and furious customers write reviews. The satisfied middle does not. |
| **Competitor reviews** | Often the richest source. Unmet needs described in detail. | Same extremity skew |
| **Support tickets** | What actually breaks, and expectation mismatches | Problems only, by definition |
| **Survey open-ends** | Direct answers to specific questions | Whoever bothered to respond, and the question shapes the answer |
| **Sales call notes** | Objections, trigger events, alternatives considered | Filtered through the salesperson's memory |
| **Win and loss interviews** | The richest source there is | Rarest, and usually a small sample |

**Tell it which source each file is.** Each one skews differently, and the output states that skew rather than pretending the sample is neutral.

## What you get back

1. Sources analysed and what each one skews toward
2. **The vocabulary gap table**, your words beside theirs
3. Problems ranked by mention count, with verbatims underneath
4. **Trigger events**, what made people start looking
5. Objections ranked, with counts
6. Alternatives they considered, in their words
7. **A swipe file** of verbatim phrases strong enough to use directly in copy
8. Themes, clearly labelled as interpretation, each showing its evidence
9. What this data cannot tell you, and which source would

---

## The rule that makes it work

**Verbatim, never paraphrased.**

It pulls the customer's actual words, including awkward phrasing and imperfect grammar. The moment a phrase is tidied up it becomes the company's voice again and the entire value is gone.

Every quote traces to a source row. It will not write a quote that is not in your data, and if a phrase is shortened at all, it is marked.

## The vocabulary gap

Usually the most useful thing you get.

Companies say solution, platform, streamline, optimise. Customers say the thing that stops me chasing invoices every month.

Seeing the two columns side by side changes how people write faster than any amount of advice about tone of voice.

## Evidence and interpretation stay apart

**Verbatims are evidence.** The customer said this.

**Themes are interpretation.** You concluded this from a group of verbatims.

Themes are labelled as such, show the verbatims they rest on, and carry a count. Anything resting on fewer than three mentions is labelled a hypothesis rather than a theme, because one vivid quote is the easiest way to talk a team into a wrong decision.

## What good output looks like

A strong result surprises you at least once. Usually it is a trigger event nobody had thought about, or an objection that turns out to be the top one by volume when everyone assumed it was price.

The swipe file should contain phrases that feel slightly wrong to a marketer, because they are not polished. Those are the ones that work.

If everything in the output confirms what you already believed, check the sample size and add competitor reviews, which tend to be the most revealing source.

---

## A note on personal data

Customer text routinely contains names, emails, phone numbers and order details.

It says so once if it finds any and asks whether you are permitted to share the file. This analysis needs the language, not the identity, so it will offer to work with those fields removed. It states this once and then continues with whatever you decide.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. Not strictly required, but it lets the skill count mentions properly on large files rather than estimating.
2. Download this folder, or make a folder named `marketing-customer-language` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the text and say what each source is.

Examples that work:

- "Here are 200 reviews of our product and 300 of our main competitor. Pull out the language."
- "Six months of support tickets. What do people actually complain about, ranked?"
- "Sales call notes from Q2. What objections keep coming up and what are they comparing us against?"
- "Our copy sounds like every other company in the category. Here is our review export, fix the input."

---

## Limits worth knowing

- It does not invent or improve quotes. Tidied language defeats the purpose of the exercise.
- It does not claim your sample is representative. It tells you what this sample said and how it is skewed.
- It does not write copy. It gives you the raw material that makes copy sound human.
- It cannot analyse text you do not have, and it will name which source would answer the questions this one cannot.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Findings feel obvious | Single source, usually your own reviews | Add competitor reviews. They describe unmet needs far more directly. |
| Quotes read too polished | Source was already summarised, not raw | Use raw text rather than someone's write-up of it. |
| Everything is a complaint | Support tickets only | Add reviews or win interviews for the other side. |
| Themes look thin | Small sample | Anything under three mentions is labelled a hypothesis. That is honest, not a fault. |
| Counts look approximate | Code execution off on a large file | Turn it on in Settings, under Capabilities. |

---

Part of the [Marketing skills](../README.md) in the [Claude Skills Library](../../README.md).
