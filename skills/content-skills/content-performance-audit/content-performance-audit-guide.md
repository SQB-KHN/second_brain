# Content Performance Audit

Turns a performance export into exactly one decision per asset: keep, refresh, rewrite, consolidate, leave alone or delete, with cannibalising clusters found before anything is recommended.

---

## Who this is for

Anyone accountable for a content library rather than a single piece: content leads and managers, SEO and organic growth managers, content marketers, editors, agency account leads auditing a client's back catalogue, and founders whose blog has quietly grown to two hundred posts.

## The problem it solves

A content library grows and nobody ever decides anything about it.

Two hundred pieces exist, ten of them carry almost all the traffic, and the rest sit there costing credibility and search authority while the team publishes a two hundred and first. The available decisions are keep, refresh, rewrite, consolidate or delete, and almost nobody makes any of them, because making them means reading two hundred pieces and having an argument about each.

The default instead is to produce more, which is the one action guaranteed not to help. Meanwhile five posts on the same question compete with each other, splitting authority so none of them ranks, and each looks individually like a refresh job. Doing this by hand takes a week and produces a spreadsheet nobody acts on. This produces a decision list ranked by return, and says how many actions you can realistically take this quarter.

---

## What you give it

**Minimum:** a performance export at page or asset level, with a URL or asset identifier, a volume metric, and a date. Analytics, Search Console, a platform export, all work.

| Extra data | What it unlocks |
|---|---|
| **Publish or last-updated date per asset** | The input that changes the audit most. Performance means nothing without age beside it |
| **Comparable data for the prior period** | Separates decay from never-worked, which is most of the finding |
| **What each asset was for** | Traffic, leads, credibility, sales support or authority. An asset judged on the wrong goal gets deleted for succeeding at a different one |
| The queries each asset receives, and conversion data | Sharper cannibalisation grouping than titles alone, and low-traffic assets that close deals do not get deleted |
| Your team's realistic capacity | Turns a ranked list into a plan for this quarter |

**Handled automatically:** URL variants aggregated to one asset (trailing slashes, query strings, AMP, http against https, paginated versions), redirected and missing URLs, non-content pages such as tags and category and author pages, assets published inside the window that have not had time to perform, and metrics held as strings with percentage signs.

## What you get back

1. Headline: assets audited, the concentration, and the single highest-return action
2. **The distribution**: what share of assets carries 50 and 90 percent of volume, and how many contribute nothing
3. **Decision table**: one decision per asset, with its classification, reason and effort
4. **Cannibalisation groups**, with combined volume and a consolidation target
5. Refresh queue, ranked, with what specifically to update on each
6. Consolidation plan, with merge target and redirect per group
7. Delete list, with the redirect note
8. **Leave alone**, with the purpose each one serves
9. What the winners have in common, labelled as a pattern or as inconclusive
10. Data quality and exclusions

An Excel version with one sheet per decision is offered at the end.

---

## The distribution comes before the ranking

Content performance is severely concentrated, and every audit that skips this reaches the wrong conclusion.

"Eleven of two hundred and six pieces carry 71 percent of traffic, and a hundred and forty produced under ten visits each in six months" reframes the entire conversation, usually away from producing more. That sentence is the output most teams need and almost never have.

## Three situations that look identical in a total

| Classification | What it means | What to do |
|---|---|---|
| **Decayed** | Performed, then declined | Refresh candidate. Freshness, a competitor, or a search change |
| **Never worked** | Published, never performed | **Rarely worth refreshing.** Intent mismatch, no distribution, or a topic nobody wanted |
| **Seasonal** | Performs on a cycle, looks dead outside it | Leave it. Deleting one is a self-inflicted wound |

Refreshing a piece that never worked is the mistake teams make most, because a refresh feels cheaper than admitting the topic was wrong. Separating these needs prior-period data; without it the skill says plainly that it cannot, and what that limits.

## Cannibalisation gets checked before anything is recommended

Several assets targeting the same question compete with each other and split authority, so none of them ranks. This is why "we have five posts on this and none of them rank" happens.

Consolidating five weak pieces into one strong one is usually the highest-return action available, and it is almost never on anybody's list, because each of the five looks individually like a refresh job. So the grouping happens first, and those assets are flagged as consolidation candidates rather than five separate refreshes.

## Why "leave alone" exists as a category

Deleting a low-traffic page that closes deals is the most expensive mistake this audit can cause.

Some assets serve a purpose volume does not measure: sales support, credibility with a specific buyer, or the answer to the one question that comes up in every call. In an export they look identical to dead content. That is why the audit asks what each asset was for before recommending anything, and why an asset with no traffic and a real purpose gets its own category rather than falling into the delete list.

## What good output looks like

A strong audit is uncomfortable about volume and specific about action. It names a consolidation group you had not seen as a group, and it puts something in "leave alone" that a traffic-only view would have deleted.

It also refuses to promise a lift. No refresh gets a predicted percentage recovery, because nobody can know that and an invented number gets quoted back as a forecast. You get what to change and the metric that would show it worked. And if it says the winners have no pattern in common, that is a real finding: a pattern forced out of eleven assets is a hypothesis presented as fact, and it would shape a quarter of production.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. This skill runs Python on your export and will not work without it.
2. Download this folder, or make a folder named `content-performance-audit` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the export and say what you are trying to decide.

Examples that work:

- "206 blog posts, six months of Search Console. What do we keep and what do we kill?"
- "Traffic is down 30 percent and we have not stopped publishing. What happened?"
- "We have five posts on the same topic and none of them rank. Sort it out."
- "Management wants to delete everything under 100 visits. Tell me what that would cost."

Supplying publish dates and what each asset was for is what turns this from a traffic report into a decision list.

---

## How it protects accuracy

- URL variants are aggregated into one asset and the aggregation is stated, because failing to do it understates your winners
- Non-content pages are excluded and listed, since tag and category pages distort every distribution
- Assets published inside the window are separated out, so nothing gets judged before it has had time to perform
- Every asset carries exactly one decision, and the decisions are proved to account for every asset
- Volume per decision category is proved to sum to the total audited
- Cannibalisation groups are checked before any individual refresh is recommended
- Every pattern in the winners is labelled a hypothesis with its confirming check, since correlation inside your own library is not a mechanism, and no predicted lift appears anywhere in the output

## Limits worth knowing

- It does not delete, redirect or edit anything. It produces the decision list.
- It does not predict how much a refresh will recover.
- It does not do keyword research or tell you what to write next. It tells you what your existing library says about what worked.
- It cannot see your rankings, your competitors' content or your CMS. It reads the export.
- It does not judge an asset against a purpose you did not give it. Where purpose is unknown it says so rather than assuming traffic was the goal.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Winners have less traffic than you thought | URL variants not aggregated in your own reporting | It aggregates and states it. Your dashboard was splitting them. |
| Everything is "never worked" | No prior-period data supplied | Add a comparable window. Without it decay cannot be separated. |
| It refuses to delete obvious dead weight | Purpose unknown, so it will not assume | Say what each was for. Unknown purpose gets "leave alone", deliberately. |
| Large consolidation groups | You have more overlap than you thought | Usually the highest-return finding in the whole audit. |
| No pattern in the winners | There genuinely is not one | Honest. A forced pattern would misdirect a quarter of production. |

---

Part of the [Content skills](../README.md) in the [Claude Skills Library](../../README.md).
