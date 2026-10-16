# Production Readiness Review

Reviews a service against blast radius, observability, failure handling, rollback and ownership, then separates the blockers that genuinely stop a launch from the debt that does not.

---

## Who this is for

Anyone who ships or accepts a service: software engineers, SREs and platform engineers, DevOps, tech leads and engineering managers, solution architects, on-call teams being handed something new, and QA or release managers running a go-live gate.

## The problem it solves

A service ships because it works, and works is the lowest bar available.

Six weeks later somebody discovers it has no alerts, no runbook, no tested rollback and exactly one person who understands it. They discover this during an incident, at a bad hour, and none of it is fixable then. The gap between "the feature works" and "this can be operated by somebody who did not build it" is invisible until the moment it is expensive.

Public checklists for this exist and are good. The reason they do not get used is that they produce forty items, everything looks important, so the list gets acknowledged and ignored. What is missing is the triage: which three of these actually stop a launch, and which twenty are debt that somebody should own with a date.

---

## What you give it

**Required:** a description of what is shipping and what it depends on.

| Context | Why it matters |
|---|---|
| **What breaks if it is down, and separately if it is slow** | These differ, and they set how much of the rest matters. A batch job and a login path do not need the same review |
| **Who owns it after launch, and whether they know** | An unowned service is the finding, not a footnote |
| Its dependencies, including the forgotten ones | Auth, config, DNS, a third-party API, a shared database, a cron job somewhere |
| What the launch actually is | Internal, a percentage of traffic, one customer, or everyone |
| Your existing checklist or standard | It applies yours rather than proposing its own |

## What you get back

1. **A verdict**: ready, ready with conditions, or not ready, with the blocker count
2. Blast radius: who is affected, how they notice, whether there is a workaround, **and what is unrecoverable**
3. Readiness table across observability, failure handling, rollback, data, operability, capacity and cost
4. **Blockers**, each with its three-in-the-morning consequence and what would close it
5. Should-haves, each with an owner and a date
6. **Accepted gaps**, written down with who accepted them
7. What could not be assessed, stated plainly
8. Questions for the team

---

## Blast radius comes first, because it scales everything else

Who is affected if this fails, how would they notice, is there a workaround, and **is anything lost permanently.**

That last question changes the review. A failure that loses data or money permanently justifies work that a recoverable failure does not. A review that treats every failure alike will over-engineer a batch job and under-protect a payment path, and both are common.

## The questions that catch what checklists miss

| Area | The question that finds the real gap |
|---|---|
| **Alerting** | Does every alert have a runbook that **exists**, rather than one that is planned |
| **Alert quality** | Does it fire on user impact rather than machine state? CPU is not an alert; failed logins are |
| **Dependencies** | What happens when each one is **slow** rather than down. Slow is harder and nobody tests it |
| **Retries** | Is the retry safe to repeat? A retry on a non-idempotent write is a data corruption path |
| **Rollback** | Does it still work **after a schema or data change**, which is where rollbacks actually fail |
| **Feature flags** | Does turning it off genuinely stop the behaviour, or just hide the entrance |
| **Ownership** | Is there anything only one person can do |

Each item comes back present, partial, absent or not applicable. **"Not applicable" is a real answer and it needs a reason**, not a blank cell.

## The three-in-the-morning test

Every proposed blocker gets one question: what happens at three in the morning if this is missing and the service fails?

If the honest answer is that the person paged can still see the problem, understand it and stop it, then it is not a blocker. It is a should-have, and it goes in a different list with an owner and a date.

That single question settles arguments about severity faster than any scoring matrix, and it is why the blocker list comes back short. **A short blocker list gets acted on. A list of forty does not.**

## Accepted gaps get written down

Sometimes the team ships anyway, and that is a legitimate decision. What is not legitimate is making it silently.

So there is a third category: known gaps, deliberately accepted, recorded with **who accepted them.** A documented decision to carry a risk is fine. An undocumented one is how the next incident starts, and how the postmortem ends up describing something everybody already knew about.

## What good output looks like

A strong review has three or four blockers, not thirty. If everything is a blocker, the triage did not happen and the review will be ignored like the last one.

The blast radius section should change how you read the rest. If nothing is unrecoverable and there is a workaround, several things you assumed were blockers are not, and the review will say so.

It should also have a "could not be assessed" section with real content in it. It cannot see your monitoring, your infrastructure or your code, and a review that claims to have checked things it could not see is worse than one that names the gap.

---

## Installing it

1. Download this folder, or make a folder named `tech-readiness-review` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill, so it works on a free plan.

## Using it

Describe what is shipping and what it touches.

Examples that work:

- "New payments webhook handler going live Thursday. Here is what it does and what it depends on."
- "We are taking over an existing service from another team. What should we insist on before accepting it?"
- "Our checklist is attached. Apply it to this service and tell me the blockers."
- "We are shipping anyway. Help me write down what we are accepting and who signed off."
- "Internal tool, twelve users, no revenue impact. Is a full review even warranted?"

That last one is a fair question and it will answer it honestly rather than producing a review because it was asked to.

---

## Limits worth knowing

- It has no access to your service, monitoring, infrastructure or code. It reviews what you describe and states what it could not see.
- It does not certify anything as safe. It produces an assessment for the people who own the decision.
- It does not run checks, execute commands or test anything.
- It does not know your organisation's standards unless you supply them. Where you do, it applies yours instead of a general list.
- It does not decide whether to ship. It gives you the blockers and the accepted risks, and the call stays with the team.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Very few blockers | Blast radius is small, or the gaps are recoverable | That is the triage working. Check the should-have list. |
| Everything looks like a blocker | Blast radius includes something unrecoverable | Usually genuine. Data loss and money justify a longer list. |
| It marked something "not applicable" | It was given a reason to | Check the reason. If it is wrong, say so and it reassesses. |
| It asks about slow dependencies | Down is easy, slow is the case nobody tests | Answer it. This is where most surprise outages come from. |
| A large "could not assess" section | It cannot see your systems | Correct. Fill in what you know and it reassesses those items. |
| Review feels heavy for a small tool | Standard applied without scale context | Say the blast radius. It will scale the review down and say so. |

---

Part of the [Techies skills](../README.md) in the [Claude Skills Library](../../README.md).
