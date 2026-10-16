# Marketing Skills for Claude

Five skills for the decisions behind marketing work: who you are talking to, what you say, why, and whether it worked.

They run inside your own Claude account, on files and pages you already have. Nothing to install on your machine, nothing to connect, no coding.

---

## Who these are for

Marketers who own outcomes rather than output: growth and performance marketers, brand and product marketers, marketing managers, agency strategists and account leads, and founders doing their own marketing.

If your week involves deciding what the company says, spending a budget, or explaining why the numbers moved, these are built for your job.

---

## The five skills

| Skill | Give it | Get back |
|---|---|---|
| **[Positioning and Messaging Brief](marketing-positioning-brief/marketing-positioning-brief-guide.md)** | What you sell, who buys, what competitors claim | A positioning brief with proof behind every claim and a do-not-say list |
| **[Customer Language Synthesis](marketing-customer-language/marketing-customer-language-guide.md)** | Reviews, tickets, surveys, call notes | The words your customers actually use, with objections and triggers ranked |
| **[Campaign Plan](marketing-campaign-plan/marketing-campaign-plan-guide.md)** | Objective, budget, audience, timeline | Funnel maths, channel split, message per stage, and kill criteria set before launch |
| **[Ad Performance Diagnosis](marketing-ad-diagnosis/marketing-ad-diagnosis-guide.md)** | A Meta or Google export | Which layer of the account is broken, ranked, with fatigue separated from saturation |
| **[Funnel and Landing Page Audit](marketing-funnel-audit/marketing-funnel-audit-guide.md)** | The page, plus funnel numbers | Where people drop, why, and fixes ranked by impact against effort |

Each has its own guide with the exact inputs it needs, the phrasings that trigger it, its limits, and a troubleshooting table.

## What is in the folder

```
marketing-skills/
├── README.md                                 ← this file
├── marketing-positioning-brief/
│   ├── SKILL.md                              ← the skill
│   └── marketing-positioning-brief-guide.md  ← how to use it
├── marketing-customer-language/
│   ├── SKILL.md
│   └── marketing-customer-language-guide.md
├── marketing-campaign-plan/
│   ├── SKILL.md
│   └── marketing-campaign-plan-guide.md
├── marketing-ad-diagnosis/
│   ├── SKILL.md
│   └── marketing-ad-diagnosis-guide.md
└── marketing-funnel-audit/
    ├── SKILL.md
    └── marketing-funnel-audit-guide.md
```

Every skill sits in its own folder. Inside, the file is always called `SKILL.md`, because that is the filename Claude looks for. Do not rename it. The guide beside it is named after the skill, so it stays identifiable once you have several downloaded.

---

## Why these five

**These are decision skills, not writing skills.** You will not find "write me a caption" here, and that is deliberate. Asking any AI for a caption already works. What does not already work is knowing which claim you can actually substantiate, whether your budget can reach your target, or whether your ads are failing because of the creative or because of your landing page. Those decisions are what marketing work is actually judged on.

**Positioning.** Every other marketing output inherits whatever was decided here. Teams that skip it spend the next year arguing about taglines, because there is no agreed answer to appeal to.

**Customer language.** Copy sounds generic because it is written in the company's vocabulary rather than the customer's. Most companies already hold everything needed to fix that, sitting unread across four systems.

**Campaign plan.** Most plans are a list of channels and a budget. Whether the numbers can reach the target, and what result means stop, are both missing, and both have to be settled before launch.

**Ad diagnosis.** When an account stops working the usual response is to change the creative, because creative is the visible part. Often the creative is fine and the problem is three steps further down.

**Funnel audit.** The cheapest performance gain available to any marketer, and the one most often done by guessing.

## They work together

Each stands alone. In sequence they cover a marketing cycle:

```
Reviews and tickets  →  Customer Language Synthesis  →  the words that actually land
Product and market   →  Positioning and Messaging    →  what you can claim, and prove
Objective and budget →  Campaign Plan                →  a plan with maths and kill criteria
Ad export            →  Ad Performance Diagnosis     →  which layer is broken
The page             →  Funnel and Landing Page Audit →  where the loss is, and what to fix
```

Two pairings worth knowing. Run customer language before positioning, so the brief is built on real words rather than internal ones. And when ad diagnosis points below the click, take the page straight to the funnel audit.

---

## What makes these different from asking directly

**Nothing gets claimed without proof.** Every claim in a positioning brief needs named evidence: data you hold, customer results, something demonstrable, or third-party validation. Anything without proof moves to a separate list of claims you cannot make yet, along with the evidence that would unlock it. No statistic, testimonial or market position is ever invented to fill a gap.

**Quotes are never tidied.** Customer language is extracted verbatim, including awkward phrasing and imperfect grammar, and every quote traces to a source row. The moment a phrase is polished it becomes the company's voice again and the value is gone.

**Assumptions are labelled every time.** A campaign plan built on an assumed conversion rate says so, next to the number. You always know what the plan is resting on.

**No invented forecasts.** No skill here tells you a change will lift conversion by a particular percentage. Nobody can know that, and an invented number gets quoted back later as though it were real. You get the metric to watch instead.

**It refuses to act on noise.** The ad diagnosis will not recommend pausing or scaling anything with too few conversions to support the call. Pausing on noise is how working ads get killed.

**Source bias is stated, not hidden.** Reviews skew to extremes. Support tickets are problems by definition. Sales notes are filtered through the salesperson. Every analysis says what its sample is skewed toward.

**They will tell you the plan does not work.** If the funnel maths shows your budget cannot reach your target, that is said first and clearly, before anything is spent.

---

## Getting started

1. Open Settings in Claude, go to **Capabilities**, and turn on **code execution and file creation**. Ad diagnosis needs it. Customer language and funnel audit use it when you supply data. Positioning and campaign plan work without it.
2. Take one skill's folder and compress it to a `.zip`. The file inside must stay named `SKILL.md`, because that is what Claude looks for. The guide beside it is not needed and can be left out.
3. Go to **Customize**, then **Skills**, then add a skill and upload the zip.
4. Repeat for each skill you want.

Skills you upload stay private to your account. Once installed they work in Chat and Cowork, and Claude picks the right one from what you ask.

**Where to start.** Run the customer language skill on reviews you have never systematically read, ideally including a competitor's. It takes minutes and usually surfaces a trigger event or an objection nobody in the team had ranked correctly.

## Using them

Upload what you have and describe the task the way you would to a colleague.

- "Build our positioning brief, here is what our competitors say"
- "200 of our reviews and 300 of a competitor's. Pull out the language."
- "3 lakh budget, six weeks, need 150 demo bookings. Can this work?"
- "CPA doubled in three weeks. Here is the Meta export."
- "Here is the page and the funnel numbers. Where are we losing people?"

---

## A note on personal data

Reviews, tickets and call notes routinely contain names, emails, phone numbers and order details.

The customer language skill says so once if it finds any and asks whether you are permitted to share the file. That analysis needs the language, not the identity, so it will offer to work with those fields removed, then continue with whatever you decide.

## What these will not do

- **No invented evidence.** No fabricated statistics, testimonials or market positions, ever. Unsubstantiated claims are a real exposure under advertising standards, and the fastest way to lose a buyer who checks.
- **No copy or creative.** These decide what to say and why. They do not write the caption, the blog post or the ad script.
- **No promised lift.** No skill claims a change will produce a particular percentage improvement.
- **No system access.** They work on exports, pasted pages and files you provide. They never connect to your ad account, analytics or website.
- **No legal clearance.** Claims that need review are flagged and go to whoever owns that in your organisation.
- **No guarantee a campaign will work.** They show what would have to be true, and say clearly when the maths does not close.

## What you need

- A Claude account, with code execution turned on for the data-driven skills
- Your exports in Excel or CSV, and page copy pasted or screenshotted
- Nothing else. No installation, no terminal, nothing to connect

---

Part of the [Claude Skills Library](../README.md).
