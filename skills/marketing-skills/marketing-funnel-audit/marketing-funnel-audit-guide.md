# Funnel and Landing Page Audit

Finds where people actually leave your funnel, works out why, and ranks the fixes so effort goes where the loss is.

---

## Who this is for

Anyone responsible for what happens after the click: growth and performance marketers, conversion specialists, ecommerce managers, founders whose site is their main sales channel, and agency teams auditing a client's funnel.

## The problem it solves

Improving a page is the cheapest performance gain available to a marketer, and the one most often done by guessing.

Somebody dislikes the headline. The headline changes. Nothing happens. Meanwhile the form is losing two-thirds of the people who start it and nobody looked, because the form is not the part anyone argues about in meetings.

This finds the actual leak first, then explains it, then ranks the fixes by impact against effort. An hour of work that regularly finds a change worth more than a month of extra ad spend.

---

## What you give it

**Required:** the page content. Pasted copy, a layout description, or a screenshot.

**This is what changes it from opinion into diagnosis:**

| Input | What it unlocks |
|---|---|
| **Funnel numbers** | Visitors, page views, form starts, completions, purchases. Without these it is informed judgement. With them it is diagnosis. |
| **What the ad or email promised** | Message match is the single largest cause of bounce and cannot be assessed without knowing the promise |
| Mobile share of traffic | In most Indian markets mobile is the majority, which changes which problems matter |
| The one action the page must achieve | Stops it optimising for the wrong outcome |
| Known customer objections | Lets it check whether the page answers them |

If you have no numbers, it will say plainly that the audit is based on the page alone, rather than implying evidence it does not have.

## What you get back

1. A two-line verdict: where the loss is and what to fix first
2. **Funnel table** with drop percentage and absolute loss at each step, where numbers exist
3. **Message match**, what was promised against what the page says
4. First screen assessment against the three questions
5. Findings, each with what is wrong, why it matters, and the reasoning
6. **Ranked fixes**: do now, plan, ignore for now
7. What to test, and whether your traffic is sufficient to test it properly
8. What could not be assessed, stated plainly

---

## The order it works in

**1. Find the biggest leak, before reading the page.** Fix the largest loss, not the most visible problem. A headline everyone dislikes on a page converting at 8 percent matters less than a form losing two-thirds of its starts. It states the leak in both percentage and absolute terms, because 40 percent of 50 people is worth less than 12 percent of 5,000.

**2. Check message match.** What the ad promised against what the page says in its first screen. If these do not match, it stops there, because nothing else on the page matters. The visitor decided they were in the wrong place within seconds. This is the most common and most fixable cause of a poor conversion rate, and it is completely invisible if you only look at the page.

**3. The first screen.** A visitor decides in a few seconds. In that time the page must answer what is this, who is it for, and what do I do next. If any is unanswerable without scrolling, that usually outranks everything else.

**4. Then the rest of the page:**

| Checked | Looking for |
|---|---|
| **The single action** | Multiple competing calls to action mean no call to action |
| **Proof against claims** | Every claim needs something supporting it. Claims without proof read as noise. |
| **Objection handling** | Unhandled objections do not stop people, they make them leave to think about it, which is the same outcome |
| **Friction** | Every form field costs completions. Also account creation before value, hidden pricing, costs appearing late. |
| **Mobile** | Long forms, tables that do not fit, small tap targets, key content buried, pop-ups covering the page |
| **Trust** | Contact details, real address, policies, security signals at payment |

## The number it will never give you

It will not tell you a fix will increase conversion by 23 percent.

Nobody can know that, and an invented number gets quoted back later as though it were a forecast. Instead you get what the fix addresses, the evidence behind the concern, and the metric that would show whether it worked.

## What good output looks like

A strong audit tells you to ignore something. The ignore-for-now list is what stops a team spending a week on a change that will not move anything.

If you supplied numbers, the verdict should point at a step you were not focused on. That is usually the sign it worked, because the step everyone already talks about is rarely the one losing the most people.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. Only needed if you supply funnel numbers.
2. Download this folder, or make a folder named `marketing-funnel-audit` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Paste the page and, if you have them, the numbers.

Examples that work:

- "Here is our landing page copy and the funnel: 4,200 visitors, 380 form starts, 91 completions. Where are we losing people?"
- "Our ad promises a free trial and this is the page it goes to. Check the message match."
- "Conversion dropped after we redesigned. Here is the new page and the old numbers."
- "This checkout loses people at payment. Here is each step and the volume."

Pairs naturally with the ad diagnosis skill. If that one points below the click, bring the page here.

---

## Limits worth knowing

- It does not visit your page. It works on what you paste, describe or screenshot.
- It does not measure page speed, test rendering, or check technical behaviour. Those get flagged for you to check yourself.
- It does not promise a conversion lift from any change.
- It does not redesign the page or write new copy, though it says specifically what each element needs to do.
- Without funnel numbers it is informed judgement, and it will say so rather than dressing it up as evidence.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Findings feel generic | Page pasted without the traffic context | Add funnel numbers and what the ad promised. Both change the output substantially. |
| It stops at message match | Promise and page do not match | That is the finding. Nothing below it matters until it is fixed. |
| It says traffic is too low to test | Genuinely too low | Make the change on judgement, or wait for volume. It says which. |
| Fixes you expected are in ignore-for-now | Low impact relative to effort | Push back if you disagree. The reasoning is stated for each. |
| No lift percentage given | Deliberate | Nobody can forecast that honestly. You get the metric to watch instead. |

---

Part of the [Marketing skills](../README.md) in the [Claude Skills Library](../../README.md).
