# Ad Performance Diagnosis

Finds which layer of your ad account is actually broken, before you change the creative for the third time.

---

## Who this is for

Anyone responsible for paid performance: performance and growth marketers, media buyers, agency account managers running several accounts, and founders managing their own ads.

## The problem it solves

When an account stops working, the usual response is to change the creative, because creative is the visible part.

Often the creative is fine and the problem is three steps further down. Clicks are not reaching the page because of a redirect. The landing page converts at half what it used to. Six ad sets are splitting one budget so none of them ever leaves the learning phase. Changing the creative fixes none of that, and each change restarts learning, which makes things worse.

This works down the funnel in order and stops at the first stage that is genuinely broken. Saves an afternoon of diagnosis and considerably more in budget spent on the wrong fix.

---

## What you give it

An export from Meta Ads or Google Ads, at campaign, ad set or ad level.

**Four things it will ask, and the first one matters more than people expect:**

| Question | Why |
|---|---|
| **Attribution window and model** | Rarely stated and changes everything. Seven-day click reports very different numbers from one-day click, and comparing across a window change is meaningless. |
| When it was working, and roughly when it changed | A step change on a date points to something that happened. A drift points to something that is happening. |
| What you have already changed | A recent edit is frequently the cause |
| Your target CPA or ROAS | So performance is judged against your goal, not a general benchmark |

**Much stronger with:** daily rather than summed data, the period from when it was working, your landing page, and conversion numbers from your own analytics alongside the platform's.

## What you get back

1. A two-line verdict: which layer is broken and what it takes to fix
2. **Funnel table**, each stage, current rate against prior, with the worst deterioration marked
3. Ranked diagnosis with the evidence behind each issue
4. **Creative fatigue or audience saturation**, the call and the evidence
5. Structural issues: learning phase, audience overlap, budget splitting
6. Data adequacy: which comparisons hold and which do not
7. **What not to change**, with reasons
8. Next actions, ranked, each with how you will know whether it worked

---

## The funnel order it follows

Fixing the wrong layer is the most common waste in ad management.

| Stage | What a problem here means |
|---|---|
| **1. Delivery** | Not spending. Bid, budget, audience size, or a rejected asset. Nothing downstream matters until this is fixed. |
| **2. Impressions to clicks** | Creative or audience match. This is the only stage where changing creative is the right first move. |
| **3. Clicks to landing page views** | Almost never marketing. Page speed, broken link, redirect, or tracking not firing. Twenty percent or more of clicks not registering is a technical issue. |
| **4. Page views to conversion** | A page problem, not an ad problem. Better traffic to a page that does not convert changes nothing. This is where most budgets are actually lost. |
| **5. Conversion to revenue or qualified lead** | Volume is fine, value is not. Offer, pricing, or targeting attracting the wrong people. |

## Fatigue against saturation

These look nearly identical in a dashboard and have opposite fixes, which is why so much budget goes into the wrong one.

| | Creative fatigue | Audience saturation |
|---|---|---|
| **Frequency** | Rising | Rising |
| **CTR** | Falling | Often stable |
| **CPM** | Roughly stable | Rising |
| **Reach** | Unchanged | Plateauing |
| **What it means** | The same people have seen it too often | You are running out of people to reach |
| **Fix** | New creative | New audience. New creative will not help. |

If the data cannot distinguish them, it says so rather than guessing.

## The structural problems it checks

- **Learning phase never exiting.** An ad set needs roughly fifty conversions a week to leave learning. Too many ad sets splitting one budget means none gets there, and the account underperforms while every individual campaign looks reasonable.
- **Audience overlap**, where your own ad sets bid against each other and raise their own costs
- **Too many variants for the budget**, so nothing accumulates enough data to judge
- **Recent budget changes**, which reset learning and invalidate before-and-after comparisons for several days

## What good output looks like

A strong diagnosis names one layer, not five, and gives you the evidence for it. If it says the ads are fine and your landing page conversion halved in the second week of the month, that is a good result even though it is not the answer you expected.

It should also tell you to leave several things alone. If the "what not to change" section is empty, either the account is genuinely broken everywhere or the data was too thin, and it will say which.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill runs Python and will not work without it.
2. Download this folder, or make a folder named `marketing-ad-diagnosis` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the export and say what changed.

Examples that work:

- "CPA doubled over three weeks. Here is the Meta export, seven-day click attribution."
- "Should I change the creative or is something else wrong? Here is the last 60 days daily."
- "This account has 14 ad sets on a 2 lakh monthly budget. Tell me what is structurally wrong."
- "ROAS dropped after we raised budgets. Is that real or is it the learning reset?"

---

## How it protects accuracy

- Every rate is recomputed from raw numbers rather than trusting a derived column, since exports often carry stale or differently defined calculated fields
- The attribution window is stated in the output, so nobody compares across a window change
- It says whether conversions are platform-attributed or from analytics, because the two disagree, often substantially
- **It will not recommend pausing or scaling anything that has too few conversions to support the call.** An ad with four conversions against another with seven is not a finding, and pausing on noise destroys ads that were working.
- Periods containing a budget or structural change are flagged as not comparable

## Limits worth knowing

- It does not access your ad account. It works on the export you provide.
- It does not write or judge creative. It tells you whether creative is the problem.
- It cannot see your landing page unless you supply it, and page problems are frequently the real cause.
- It does not guarantee a fix. It ranks what is broken by evidence and tells you how to know whether the fix worked.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It says there is not enough data | Too few conversions to support a comparison | That is the finding. Acting on noise is how working ads get killed. |
| Diagnosis points at your landing page | The drop is below the click | Supply the page and run the funnel audit skill on it. |
| Numbers do not match your dashboard | Attribution window or conversion source differs | It states which it used. Match them and rerun. |
| It cannot separate fatigue from saturation | Export is summed rather than daily | Re-export with daily rows. |
| Nothing happens on upload | Code execution is off | Turn it on in Settings, under Capabilities. |

---

Part of the [Marketing skills](../README.md) in the [Claude Skills Library](../../README.md).
