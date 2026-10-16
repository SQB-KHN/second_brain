---
name: content-performance-audit
description: Turn a performance export into one decision per asset: keep, refresh, rewrite, consolidate or delete, with cannibalisation groups found first. Use for content audits or pruning.
---

# Content Performance Audit

A content library grows and nobody ever decides anything about it. Two hundred pieces exist, ten carry almost all the traffic, and the rest sit there costing credibility and search authority while the team publishes a two hundred and first. The available decisions are keep, refresh, rewrite, consolidate or delete, and almost nobody makes any of them.

## When to use this

Trigger on: content audit, content performance, blog audit, content pruning, refresh, "which content is working", "should we delete old posts", content ROI, "traffic dropped", "what should we write more of".

## Before you start

Required: a performance export at page or asset level, with a URL or asset identifier, a volume metric, and a date.

Ask, briefly:
1. The window, and whether comparable data exists for the prior period. Without a comparison there is no decay signal, and decay is most of the finding.
2. **Publish or last-updated date per asset.** This is the input that changes the audit most, because performance means nothing without age beside it.
3. **What each asset was for.** Traffic, leads, credibility, sales support, or search authority. An asset judged against the wrong goal gets deleted for succeeding at a different one.
4. Whether conversion or lead data can be joined, even roughly.
5. Their own definition of an asset worth keeping, if they have one.

## Check for personal data first

Performance exports occasionally carry user-level or session-level rows. Check, and if any are present say once that this audit works at asset level and needs no user data, then continue with whatever they choose.

## Workflow

### 1. Profile the export

- **Aggregate URL variants into one asset.** Trailing slashes, query strings, AMP versions, http against https, and paginated versions are one piece of content across several rows. Failing to aggregate is the commonest error here, and it understates the winners.
- Redirected and missing URLs still sitting in the file
- **Pages that are not content:** category and tag pages, search results, the homepage, author pages. These distort every distribution and are not decisions anybody makes.
- Assets published inside the window, which have not had time to perform and must be judged separately or excluded
- Bot and internal traffic, where the file allows separating it
- Header rows, and metrics held as strings with percentage signs

State asset count, total volume, and everything excluded with its volume.

### 2. Compute in code, never in prose

### 3. Face the distribution before ranking anything

Content performance is severely concentrated, and every audit that skips this reaches the wrong conclusion.

Report what share of assets carries 50 percent of the volume, what share carries 90, and how many assets contribute effectively nothing.

"Eleven of two hundred and six pieces carry 71 percent of traffic, and a hundred and forty produced under ten visits each in six months" reframes the whole conversation, usually away from producing more.

### 4. Separate decay from a one-off, and both from never having worked

Three entirely different situations that look identical inside a total:

- **Decayed.** Performed, then declined. Points to freshness, a competitor, or a search change. These are the refresh candidates.
- **Never worked.** Published, never performed. Points to intent mismatch, no distribution, or a topic nobody wanted. **Rarely worth refreshing**, which is the mistake teams make most often, because refreshing feels cheaper than admitting the topic was wrong.
- **Seasonal or event-driven.** Performs on a cycle and looks dead outside it. Deleting one of these is a self-inflicted wound.

Where a prior period exists, compute the change per asset and classify. Where it does not, say plainly that decay cannot be separated from never-worked, and what that limits.

### 5. Check cannibalisation before recommending anything

Several assets targeting the same question compete with each other and split authority, so none of them ranks. This is why "we have five posts on this and none of them rank" happens.

Group assets by the question they answer, using titles and, where supplied, the queries they actually receive. Report every group of two or more with its combined volume, and flag them as **consolidation candidates rather than individual refresh candidates**.

Consolidating five weak pieces into one strong one is usually the highest-return action available, and it is almost never on anybody's list, because each piece individually looks like a refresh job.

### 6. Assign exactly one decision per asset, with its reason

- **Keep.** Performing against its purpose. No action.
- **Refresh.** Performed before, has decayed, the topic still has demand. State specifically what to update.
- **Rewrite.** Right topic, wrong execution or wrong intent. More work than a refresh, and worth naming as such so it gets scheduled honestly.
- **Consolidate.** Merge into a named target asset, with the redirect stated.
- **Leave alone.** Low volume, but serving a purpose volume does not measure: sales support, credibility, or one specific customer question.
- **Delete.** No volume, no purpose, nothing worth merging. Note that deletion needs its redirect handled.

The "leave alone" category matters more than it looks. Deleting a low-traffic page that closes deals is the most expensive mistake this audit can cause, which is exactly why the purpose question is asked at the start.

### 7. Rank by return, not by how bad the asset is

Rank actions by expected return against effort. A refresh on an asset that used to perform well beats a rewrite of one that never did, and consolidating a cannibalising cluster usually beats both.

Say what to do first, and how many actions this team can realistically take this quarter given what they told you about capacity.

### 8. Say what the winners have in common, and be honest when nothing does

Look at the top assets for a shared pattern: intent, format, length, topic, distribution source, or age. Where a real pattern exists, name it, because it is the most useful output here for planning.

Where none exists, say so. A pattern forced out of eleven assets is a hypothesis presented as a finding, and it will shape a quarter of production. Label any pattern as a hypothesis with the check that would confirm it. Correlation inside your own library is not evidence of a mechanism.

### 9. Never promise a lift

No refresh gets a predicted percentage recovery. Say what to change, and what metric would show whether it worked.

## Output format

**1. Headline.** Assets audited, the concentration, and the single highest-return action.

**2. Distribution.** Share of assets carrying 50 and 90 percent of volume, and the count contributing nothing.

**3. Decision table.**

| Asset | Purpose | Volume | Change | Age | Classification | Decision | Reason | Effort |

**4. Cannibalisation groups.** Each with combined volume and the consolidation target.

**5. Refresh queue.** Ranked, with what specifically to update on each.

**6. Consolidation plan.** Merge target and redirect per group.

**7. Delete list.** With the redirect note.

**8. Leave alone.** With the purpose each one serves.

**9. What the winners have in common.** Labelled as a pattern or as inconclusive.

**10. Data quality and exclusions.** URL variants aggregated, non-content pages removed, assets too new to judge.

Offer the Excel version with one sheet per decision. Build it only if asked.

## Checks to run before delivering

- URL variants are aggregated into one asset, and the aggregation is stated
- Non-content pages are excluded and listed
- Assets published inside the window are separated or excluded, with the count stated
- Every asset carries exactly one decision, and the decisions account for every asset
- Volume per decision category sums to the total volume audited
- Decay is distinguished from never-worked wherever a prior period exists, and the limitation is stated where it is not
- Cannibalisation groups are checked before any individual refresh is recommended
- Every pattern found in the winners is labelled a hypothesis with its confirming check
- No predicted lift appears anywhere in the output

## What this skill does not do

- It does not delete, redirect or edit anything. It produces the decision list.
- It does not predict how much a refresh will recover.
- It does not do keyword research or tell you what to write next. It tells you what your existing library says about what has worked.
- It cannot see your rankings, your competitors' content or your CMS. It reads the export.
- It does not judge an asset against a purpose you did not give it. Where purpose is unknown it says so, rather than assuming traffic was the goal.
