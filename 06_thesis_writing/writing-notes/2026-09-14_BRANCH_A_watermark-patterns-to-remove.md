---
name: 2026-09-14_BRANCH_A_watermark-patterns-to-remove
description: NOTE - The machine-writing patterns that must be swept from the prose before submission. Each pattern with what it looks like, why it reads as generated, and how to break it. Cumulative - add to it whenever another is spotted.
category: reference
applies-to: [all chapters, submission preparation]
triggers: [watermark removal, does this read as AI, final prose pass, style sweep]
created: 2026_09_14-16_40
updated: 2026_09_14-16_40
snapshot: 2026-09-14_16-21_post-comment-pass-archive
status: open - sweep not yet run
---

# Machine-writing patterns to remove before submission

**This file exists because two Word threads (Ch3, "criterion:" and "not
incidental;") flagged the same class of problem and it is larger than two
sentences.** It is cumulative: add a row whenever another pattern is spotted, so
the final sweep is one pass rather than a re-derivation.

⚠ **This is a style sweep, not a content edit.** Nothing here changes a claim, a
number or an argument. If a fix would change meaning, it is the wrong fix.

---

# Why this matters, stated plainly

An assessor who suspects generated prose reads the whole document differently —
every claim is weighed against the suspicion rather than on its merits. The
patterns below are the ones that trigger it, and most are **habits rather than
content**, so they can be broken without touching what the thesis says.

**The prose in this thesis is substantively good.** The arguments are the
authors', the numbers are verified, and the negative results are honestly
reported. It would be a poor outcome for that work to be discounted over
sentence rhythm.

---

# The patterns

## P1 — `word:` as a lead-in (flagged, Ch3 threads 67, 68)

**What it looks like:** a colon after a single word or short phrase, introducing
an elaboration.

> "the pragmatist criterion for success is not whether the artefact reveals deep
> structural features of retail demand, but whether it enables..."
>
> "This stance has practical methodological implications: it motivates careful
> data quality assessment..."

**Why it reads as generated:** a human writing at length varies how they
introduce an elaboration. The colon-elaboration is one move, and generated prose
reaches for it at a rate far above human baseline — often several times per page.

**How to break it, in order of preference:**

| Fix | Example |
|---|---|
| Full stop, then the elaboration as its own sentence | "This stance has practical methodological implications. It motivates careful data quality assessment..." |
| Subordinate the clause | "Because this stance is methodological rather than abstract, it motivates careful data quality assessment..." |
| Keep the colon where it introduces a genuine list | *"...three categories: CSD, danskvand and RTD."* ✅ **legitimate — leave it** |

⚠ **Do not remove every colon.** A colon before an actual list or a quotation is
ordinary English. The pattern is the colon before *prose*, and specifically the
rhythm of naming-then-expanding.

---

## P2 — `not X; it is Y` and `not X, but Y` (flagged, Ch3 thread 68)

**What it looks like:**

> "The consistency between the philosophical position and the research
> methodology is not incidental; it reflects the deliberate choice..."
>
> "The choice is not conventional but theoretical."

**Why it reads as generated:** the contrastive-corrective frame is a signature
move. It manufactures emphasis by first denying something nobody claimed.

**How to break it:** state the positive directly and cut the denial.

| Before | After |
|---|---|
| "is not incidental; it reflects the deliberate choice" | "reflects a deliberate choice" |
| "The choice is not conventional but theoretical." | "The choice follows from scoring-function theory rather than from convention." |

⚠ **Sometimes the denial is doing real work** — when a reader would otherwise
assume the thing being denied. *"This is a limitation of the application, not of
Prophet"* is earning its contrast. **Keep those.**

---

## P3 — the rule of three

**What it looks like:** three parallel items where two or four would be natural.

> "accuracy, memory efficiency, and category specialization"
>
> "reliability, uncertainty, and traceability"
>
> "correctness, consistency, and replicability"

⚠ **Most of these are legitimate here** — they name three actual research
dimensions, and SRQ2 genuinely has three properties. **Do not break a triple that
corresponds to something real.**

**The tell is a triple in ordinary prose**, where the third item adds nothing:
*"careful, deliberate, and considered"*. Sweep for those.

---

## P4 — "It is worth noting that" and the hedge stack

**What it looks like:** "It is worth noting", "It is important to emphasise",
"Notably", "Crucially", "Importantly".

**How to break it:** delete. If the point is worth making, make it. If it needs
flagging as important, the structure around it is not doing its job.

---

## P5 — the summarising final sentence

**What it looks like:** a paragraph that ends by restating what it just said,
often beginning "In other words", "That is to say", "Put differently", or "This
is precisely the..."

**Why it reads as generated:** a paragraph that has made its point does not need
to make it again. Generated prose adds the restatement because it reads as
closure.

⚠ **This one needs judgement.** A restatement that *advances* the argument — by
naming a consequence, or connecting to the next section — is good writing. One
that merely re-says is padding. **Read each on its own.**

---

## P6 — em-dash density

**What it looks like:** em dashes used several times per page for parenthetical
asides.

**How to break it:** convert to commas, parentheses, or separate sentences. Vary
the punctuation rather than eliminating one mark.

⚠ **Check what the .docx actually contains.** The snapshot renders some dashes as
hyphens, so count in Word rather than in the markdown mirror.

---

## P7 — parenthetical asides carrying load-bearing content (flagged, Ch3 threads 123, 124)

**What it looks like:**

> "(the Prometheus production system, whose Graph Engine is the concrete
> integration target examined under SRQ3)"

**Why it is a problem beyond style:** a parenthesis signals *"this is
skippable"*. When the content inside is load-bearing, the punctuation is lying
about its own importance.

**How to break it:** promote to a clause or its own sentence. ✅ **The Ch3 rewrite
already did both of these** — see the applied note for the pattern.

---

# How to run the sweep

**Do it once, late, on a locked document.** Running it early means re-running it
after every prose pass.

**Suggested order:**

1. **P4 and P7 first** — mechanical, no judgement required, and they are the most
   visible.
2. **P1 and P2 next** — search for `: ` and `; it ` in Word; each hit is a
   decision, most take seconds.
3. **P5 last** — it needs a read of each paragraph, and it is the one where
   over-correction does damage.
4. **P3 and P6** — only if time allows. These are the weakest signals.

⚠ **Do not batch-replace anything.** Every one of these patterns has legitimate
instances, and a find-and-replace will produce prose that is wrong in a new way.

⚠ **Vary the fixes.** If every `word:` becomes a full stop, the result has a new
uniform rhythm — which is the same tell wearing different clothes.

---

# What this sweep does NOT cover

**Vocabulary.** Words like "leverage", "delve", "robust", "nuanced",
"multifaceted" are commonly cited as markers. ⚠ **I have not audited the thesis
for them**, and several ("robust") are legitimate technical terms here. **Add a
row if you want this covered.**

**Structural uniformity.** Every chapter opening with a one-sentence orientation
paragraph, every section closing by naming the next — that consistency is itself
a signal. But it is also *good thesis structure*, and Chapter 2's section-closing
handoffs were praised in the flow read as the best in the document. **Leave it.**

---

# Related

- `ch3_methodology/.archive/2026-09-14_ch3-rewrite-applied.md` — Fix 3 shows the
  reword pattern for P1, P2 and P7
- Word threads **67** and **68** in Chapter 3 are the two that prompted this file
  and remain open until the sweep runs
