# Pre-publication Check

Registers every factual claim in a draft with its source status, verifies the numbers, tests the headline against the body, and flags originality and compliance risks before anything goes out.

---

## Who this is for

Anyone who publishes, or approves what gets published: editors and content leads, content writers and copywriters, brand and communications managers, social media managers, agency account leads signing off client work, and anyone who is both the writer and the last person before publish.

## The problem it solves

The draft is finished, the deadline is now, and the person about to publish is the person who wrote it.

So the checks that get skipped are exactly the ones only an outsider would run. Does every number actually appear in the source it is attributed to. Does the headline promise what the body delivers. Is that unusually fluent paragraph somebody else's work. And does "we tested 40 tools" mean anyone tested 40 tools.

AI-assisted drafting has made one of these urgent. A fabricated citation is fluent, plausible, specific and completely wrong, which is precisely the combination that gets published. It does not look like an error, because it looks like every other sentence in the piece.

Doing this properly means extracting every assertion into a list and checking each one, which nobody does under deadline. This does the extraction mechanically, then gives you a verdict you can act on.

---

## What you give it

**Required:** the draft.

| Context | Why it matters |
|---|---|
| Where it publishes, and under whose name | A bylined expert piece, a brand blog and a regulated communication carry different standards |
| A voice guide, style guide or approved claims list | It applies yours instead of a general standard |
| **Whether any of it was AI-generated or assembled from other sources** | Asked plainly and without judgement. The answer decides where the effort goes, and it is the most useful thing you can say |
| Sources for the claims, where you have them | It can verify against a source it can see. It cannot verify one it cannot |
| Any regulated territory involved | Health, finance, legal, employment, children, or a named competitor |

## What you get back

1. **A verdict**: ready, ready with fixes, or not ready, and the blocker count
2. **The claim register**: every factual assertion, its type, its source status, and what has to happen to it
3. Number checks: each number against its cited source
4. **Headline against body**: promises kept, broken, and missing
5. Originality flags, with the limits of what was checked stated plainly
6. Compliance flags, each routed to an owner
7. Structural notes, in order of impact
8. Line notes, only after the structural ones
9. What was not checked, and why

---

## The claim register is the whole idea

Every factual assertion gets extracted into a list before anybody reads the piece for quality. A factual assertion is anything a reader could check and find wrong: a number, a date, a percentage, a comparison, an attribution, a superlative, a causal statement, or a description of what somebody else does.

Doing it mechanically, as a list, separated from reading the piece, is the point. It surfaces the claims that read as harmless background and are in fact assertions nobody checked.

Then each one gets a status:

| Status | What it means |
|---|---|
| **Sourced** | A named, checkable source is cited |
| **Sourceable** | True and checkable, source not yet cited |
| **Internal** | Rests on your own data, and must be stated as your own |
| **Experience** | Rests on something you did. **The one to interrogate hardest** |
| **Unsupported** | No source exists or could be found |
| **Unverifiable** | Cannot be checked either way |

"Experience" is where content lies most and gets caught least. "We tested 40 tools", "in our experience", "having worked with hundreds of teams" all need somebody to have actually done that.

## Numbers get trusted more and checked less

- Does the number appear in the cited source at all, or is it an approximation of something adjacent
- Is it current, and is the year stated
- **Is a percentage's base stated?** A rise of 30 percent from 1 to 1.3 percent is a very different claim from 30 to 39 percent, and only one of them is impressive
- Is a total consistent with its parts everywhere it appears
- Is the statistic attributed to a body that would plausibly publish it

## Structural notes come before line notes, always

Most reviews do this backwards, polishing sentences in a piece whose structure is wrong. That work gets thrown away when the structure changes, so it goes second here, every time.

## What it is honest about not doing

**It is not a plagiarism scanner and says so.** What it can do is flag passages whose register or specificity differs sharply from the rest, close paraphrase of a cited source where quoting was the honest option, and uncredited use of somebody else's framework or coined term. Where the risk is real it tells you to run an actual scan rather than implying it already has.

**It does not rule on compliance.** Health, financial, legal and employment language, competitor claims, anything involving children, undisclosed paid relationships: it flags each and names who in your organisation resolves it. It does not offer the legal opinion.

## What good output looks like

A strong result gives you a verdict, not a list of suggestions: "Not ready. Two unsupported claims and a headline promising a comparison the body does not make."

The claim register should be longer than you expect, because most drafts contain assertions the writer did not experience as claims. And the verdict is "not ready" whenever an unsupported claim survives, however good the writing is, because that is not a style problem.

If the register comes back short on a research-heavy piece, check whether background statements were treated as claims. Anything a reader could check belongs in the register.

---

## Installing it

1. Download this folder, or make a folder named `content-prepublication-check` and put `SKILL.md` inside it. The guide does not need to go in.
2. Compress the folder to a `.zip`.
3. Go to Customize, then Skills, then add a skill and upload the zip.

Code execution is not required for this skill, so it works on a free plan.

## Using it

Paste the draft and say where it is going.

Examples that work:

- "Check this before it goes on the blog. Some of it was drafted with AI."
- "Bylined piece under our CEO's name. Tear it apart."
- "Every stat in here came from a search. Verify what you can and flag what you cannot."
- "Does the headline actually match what this piece delivers?"
- "Client work, going out tomorrow. What are the compliance flags?"

Telling it which parts were AI-drafted is not an admission, it is the most useful input you can give.

---

## How it protects accuracy

- Every factual assertion is extracted into the register, with none skipped as background
- Every register entry carries a source status, and none is left blank
- Numbers are checked against their cited source in code, so a total that is right in one paragraph and wrong in another gets caught
- Percentages are checked for a stated base, because a relative figure without one is not a claim anybody can verify
- Experience claims are separated from sourced ones and interrogated on their own
- The verdict is "not ready" while any unsupported claim survives, regardless of how good the writing is
- The limits of the originality check are stated rather than implied

## Limits worth knowing

- It is not a plagiarism scanner. It flags signals and tells you when to run a real one.
- It does not give legal, medical, financial or regulatory advice. It flags and routes.
- It cannot verify a source it cannot see. An uncited claim is marked uncited, never assumed true.
- It does not rewrite the piece unless you ask. It tells you what has to change and why.
- It does not decide whether a risk is acceptable. The publishing decision stays yours.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Register is very long | Most drafts carry more assertions than the writer noticed | That is the finding. Work down by status; unsupported first. |
| Verdict is "not ready" on good writing | An unsupported claim survives | Deliberate. Cite it, soften it to something true, or cut it. |
| It cannot verify most numbers | No sources supplied | Paste the sources. Without them it can only mark claims uncited. |
| Flags a passage as possibly lifted | Register or specificity differs from the rest | It is a signal, not a finding. Run a real scan on that passage. |
| No compliance flags | Nothing in the draft touched regulated territory | Fine. If you expected some, name the territory and rerun. |

---

Part of the [Content skills](../README.md) in the [Claude Skills Library](../../README.md).
