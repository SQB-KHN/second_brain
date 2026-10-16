# Techies Skills for Claude

Five skills for the engineering work that is not coding: the postmortem, the readiness review, the design doc, the rollout plan and the brief for people who do not write software.

They run inside your own Claude account, on evidence you paste. Nothing to install on your machine, nothing to connect, no coding.

---

## Who these are for

Anyone whose job includes writing engineering down: software engineers at any level, SREs and platform engineers, DevOps and release engineers, data engineers, QA and test engineers, support and L2 or L3 engineers, tech leads and engineering managers, solution and enterprise architects, and founders who are still the technical lead.

All five need no export from any system. They work on what you paste, so an engineer with no access to production, CI or the monitoring stack can use every one of them.

## The five skills

| Skill | Give it | Get back |
|---|---|---|
| **[Incident Postmortem](tech-postmortem/tech-postmortem-guide.md)** | Timestamps, bridge logs, deploys, what people remember | A timeline that reconciles, four separate durations, contributing factors in the plural, and actions somebody will do |
| **[Production Readiness Review](tech-readiness-review/tech-readiness-review-guide.md)** | What is shipping and what it depends on | Blast radius, a readiness table, and blockers separated strictly from debt |
| **[Design Doc and ADR](tech-design-doc/tech-design-doc-guide.md)** | The problem, and what you are considering | Alternatives that could genuinely win, the tradeoff stated, and what would change the decision |
| **[Rollout and Migration Plan](tech-rollout-plan/tech-rollout-plan-guide.md)** | What is changing and what it touches | The change classified by reversibility, phased by blast radius, with abort criteria and a real rollback |
| **[Engineering Brief](tech-status-brief/tech-status-brief-guide.md)** | Technical facts, and who is reading | The consequence first, costed in the reader's currency, with what you suspect kept out of what you know |

Each skill has its own guide with the exact inputs it needs, the phrasings that trigger it, what good output looks like, its limits, and a troubleshooting table.

## What is in the folder

```
tech-skills/
├── README.md                           ← this file
├── tech-postmortem/
│   ├── SKILL.md                        ← the skill
│   └── tech-postmortem-guide.md        ← how to use it
├── tech-readiness-review/
│   ├── SKILL.md
│   └── tech-readiness-review-guide.md
├── tech-design-doc/
│   ├── SKILL.md
│   └── tech-design-doc-guide.md
├── tech-rollout-plan/
│   ├── SKILL.md
│   └── tech-rollout-plan-guide.md
└── tech-status-brief/
    ├── SKILL.md
    └── tech-status-brief-guide.md
```

Every skill sits in its own folder. Inside, the file is always called `SKILL.md`, because that is the filename Claude looks for. Do not rename it. The guide beside it is named after the skill, so it stays identifiable once you have several downloaded.

---

## Why there is no code review skill here

Because asking Claude to review code, write tests, refactor something, explain a function or debug a stack trace already works, and works better with your actual repository open in front of it. A skill there would add ceremony, not capability, and you would notice immediately.

The same filter removes most of what people expect. Anything needing repository, CI, monitoring, cloud console or production access is out, because these run on what you paste and nothing else. That excludes a lot of genuinely valuable engineering AI work, and it is more honest to say so than to pretend a skill can see your logs. What is left is the half of engineering that is documents. The postmortem, the design doc, the readiness review, the rollout plan, the brief upward. Every engineer above junior level produces these, almost nobody was taught how, and they are exactly where an AI writing unaided does the most damage, because the failure mode is fluency.

## The line none of these cross

**No invented system behaviour.**

Nothing here describes how your system works, why it failed, or what it would do under load, from anything other than the evidence you supplied.

This matters more in engineering than almost anywhere, because a plausible engineering document is indistinguishable from a real one at a glance. A postmortem naming one confident root cause reads like competence. A design doc with two strawmanned alternatives reads like diligence. A readiness review that passes something nobody checked reads like a gate. All three get filed, believed, and acted on.

So every skill here works the same way: it reasons from what you gave it, states plainly what it could not see, and turns a gap into a question rather than a sentence.

---

## Why these five

**Postmortem.** Written by the person who was up all night, three days later, for an audience including their manager. So it names one root cause and the actions never get done. **Readiness review.** A service ships because it works, which is the lowest bar available, and the gap between working and operable by somebody else is invisible until it is expensive.

**Design doc.** Two alternatives added afterwards so the section is not empty, both written to lose. Experienced reviewers spot it in ten seconds and stop trusting the rest.

**Rollout plan.** "Deploy it and watch" holds until the rollback you assumed exists needs a schema change that has already run. **Engineering brief.** Every detail, so the reader decides from paragraph two, or simplified until it is no longer true.

## They work together

Each stands alone. In sequence they cover a change from proposal to aftermath:

```
A problem            →  Design Doc and ADR        →  a decision somebody can audit in a year
Before it ships      →  Readiness Review          →  three blockers, not thirty
Getting it out       →  Rollout and Migration     →  abort criteria set before anyone is under pressure
When it goes wrong   →  Incident Postmortem       →  factors in the plural, actions that get done
Explaining any of it →  Engineering Brief         →  a reader who can decide
```

Three pairings worth knowing. The readiness review's blockers are usually rollout plan inputs, since "no tested rollback" is a plan problem before it is a launch gate. The postmortem's response findings feed back into the next readiness review, the loop most teams never close. And the postmortem is what the engineering brief should be written from, because drafting a customer update off the raw timeline is how suspected causes escape.

---

## What makes these different from asking directly

**No single root cause.** Any incident worth writing up is several conditions holding at once. A postmortem with one root cause stopped looking as soon as it found something, and the conditions it did not name are all still there.

**Four durations, not one.** Detect, acknowledge, mitigate and resolve point at four different problems. Fast detection with a slow mitigate is a runbook or access problem; the reverse is a monitoring problem, and collapsing them hides which you have.

**Blameless is enforced, and it is technical rather than polite.** A postmortem naming a person produces exactly one outcome, that person being more careful, which fixes nothing for whoever is on call next month.

**Gaps stay gaps, and alternatives have to be able to win.** Where nobody was taking notes the timeline says so, because a reconstructed gap becomes fact the moment it is written down. And if you cannot describe a world in which an option is the right choice, it is not an alternative but a rhetorical device; doing nothing and the simplest thing that could work are always included.

**Reversibility sets the depth, and abort criteria are written before anyone is under pressure.** A choice undone in a week gets a paragraph; one load-bearing for five years gets the argument, and most documents give both the same treatment. During a rollout every number is arguable, and the person arguing is the one who wants it to work.

**Blockers are triaged by what happens at three in the morning.** If the person paged can still see the problem, understand it and stop it, it is not a blocker. That is why the list comes back short, and short lists get acted on.

**Nothing runs, and suspected causes stay out of live incident updates.** No command is handed over to execute against production in any of the five; steps get described for an engineer to write and review. And a confident wrong cause gets forwarded, turns out to be wrong, and costs more credibility than silence would have.

---

## Getting started

1. Take one skill's folder and compress it to a `.zip`. The file inside must stay named `SKILL.md`, because that is what Claude looks for. The guide beside it is not needed and can be left out.
2. Go to **Customize**, then **Skills**, then add a skill and upload the zip.
3. Repeat for each skill you want.

Only the postmortem uses code execution, to convert timezones and compute durations. The other four need nothing, so most of this set runs on a free plan. Skills you upload stay private to your account, and once installed they work in Chat and Cowork.

**Where to start.** Run the postmortem on an incident you already wrote up. It will usually name three contributing factors where your document named one, and that comparison is the fastest way to see what this set is for.

## Using them

Paste the evidence and describe the task the way you would to a colleague.

- "Bridge log, alert times and the deploy record. Checkout was down 40 minutes."
- "New payments webhook going live Thursday. What are the blockers?"
- "We keep losing order confirmations when payments is slow. Test the alternatives properly."
- "Schema change with a backfill. It cannot be rolled back once the old column is dropped."
- "Outage update for our biggest client. We know the impact, not the cause."

---

## What these will not do

- **No code work.** No review, tests, refactoring, debugging or generation. Claude already does that unaided and better with your repo open.
- **No system access.** No repository, CI, monitoring, cloud console, database or production. These read what you paste, and they state what they could not see.
- **Nothing runs.** No command is handed over to execute, least of all at three in the morning. Steps are described for an engineer to write and review.
- **No invented system behaviour.** No performance figures, capacity numbers or benchmarks you did not supply. Those come back as open questions.
- **No single root cause, no named individuals as causes, and no speculation in a live incident update.** None of these is negotiable in any version.
- **No certification.** A readiness review is an assessment for the people who own the decision, not a sign-off.
- **No decision made for you.** These set the criteria, name the tradeoff and rank the blockers. Shipping, proceeding and escalating stay with the people accountable.

## What you need

- A Claude account. Code execution only for the postmortem
- Your evidence pasted in: timestamps, logs, chat, descriptions
- Nothing else. No installation, no terminal, nothing to connect

---

Part of the [Claude Skills Library](../README.md).
