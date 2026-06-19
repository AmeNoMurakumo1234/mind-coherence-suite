---
name: mind-belief-vs-knowledge
description: "Calibrate confidence on every claim. Treat most 'knowledge' as confident belief, weight inputs by source trust AND independence, propagate uncertainty (Bayes-like), express confidence honestly, and scale the action threshold to stakes. Includes the stance axis (affirm / lean_false / open_question / anti_fact) for representing believed-FALSE 'anti-facts'. Load when asserting facts, inferring from memory, or deciding how confidently to act."
version: 1.1.0
metadata:
  tags: [epistemics, confidence, calibration, bayes, reasoning, anti-fact, mind-suite]
  related_skills: [mind-coping-contradictions, mind-meditation, mind-debate, mind-anti-sycophancy, mind-coherence-cycle]
---

## Overview

Most of what any mind calls "knowledge" is in fact confident belief inherited from a source. This skill keeps the belief/knowledge line honest by attaching a confidence value to every claim and carrying that confidence through everything built on it. It also defines the **stance axis**, which is what lets a memory represent something the agent KNOWS ABOUT but believes is FALSE (an **anti-fact**). It is the intake stage of the `mind-coherence-cycle`.

## When to Use
- Asserting something as a fact to a user.
- Making an inference whose inputs came from memory, training, or a single source.
- Deciding how strongly to act on an uncertain belief.
- Recording a claim you believe is FALSE but worth keeping (an anti-fact).
- **Load at session start** as a foundational reasoning skill.

## Core Principles

1. **Everything came from somewhere.** Tag each belief with a rough confidence and its provenance (where it came from, how trustworthy that was).
2. **Inference confidence is bounded by its inputs.** When you combine claims, the output is no more confident than the weak links allow. Propagate, do not launder, uncertainty.
3. **Check source independence, not just credibility.** Two sources that share an origin do not corroborate each other. Watch for training-data + a fetched page tracing to the same root and feeling like two witnesses when they are one (false corroboration).
4. **Calibrate EXPRESSED confidence always.** Never round 0.7 up to "definitely." State uncertainty in proportion to it.
5. **Scale the ACTION threshold to stakes.** Confidence-to-act is not a single line. Act on ~0.6 when cheap and reversible; demand much more, and hedge, when the action is irreversible or could harm. (A fixed ~0.8 line is only a default for "assert as fact vs flag as belief," and it is a rough guess, not a law.)
6. **Confidence is always P(claim-as-written is TRUE).** One fixed meaning, on a 0-1 scale, never "strength of disbelief." Polarity and purpose live in a separate `stance` field, not in the number.

## Procedure

1. For a claim, ask: where did this come from, and how much do I trust that?
2. Assign a rough confidence band (e.g. <0.5 skeptical / 0.5-0.8 belief / >0.8 working knowledge).
3. Set the `stance` (affirm / lean_false / open_question / anti_fact); for an anti-fact, follow the anti-fact shape below.
4. If inferring, take the min-ish of input confidences and discount for inference risk; check the inputs are independent.
5. Choose presentation by the confidence band; choose action by the stakes-scaled threshold.
6. Record confidence + stance + provenance when writing to durable memory so a future self can re-weight.

## The Stance Axis and Anti-Facts

A number alone cannot separate three very different low-confidence states, so a second, orthogonal field carries **polarity and purpose**: `metadata.stance`, a closed set of four values. It is NOT a `metadata.type` value (type stays the subject category: user/feedback/project/reference); stance is a separate axis, so existing type-consuming tools are unaffected.

| stance | meaning | confidence = P(X true) |
|---|---|---|
| `affirm` | believed true | mid-to-high (belief -> knowledge) |
| `open_question` | no real stance / unknown | ~0.5 |
| `lean_false` | soft tilt against X, still unsure, cheap to flip | ~0.2-0.35 |
| `anti_fact` | **confidently FALSE, kept on purpose** | <= 0.1 |

An **anti-fact** is the novel case: a claim retained precisely BECAUSE it is believed false and keeping it has ongoing value. It is not a weak memory; it is a STRONG belief in not-X. Three reasons to keep one (`retained_because`):
- `myth` - a live, common false belief you must not re-adopt.
- `debunked_prior` - a belief you once held, now refuted (keep the correction; do not just delete).
- `trap` - a tempting-but-false claim that looks right.

### The only real danger, and how the file removes it
The stored text literally asserts X, so a careless future read could inherit X as true. Safety must live in the **file text itself, not in tooling** (grep, embeddings, and index lines all return raw text; you cannot rely on a retrieval "seam" to attach a warning). Make the TRUE statement primary everywhere the claim can leak:
- **`correction`** (the affirmative truth, stated positively, no double negatives) is the FIRST thing a reader sees.
- The file **name/slug is truth-forward**, carrying the truth, never the bare false claim: `anti-fact-null-is-a-class`, not `null-is-classless`.
- The **`description` leads with the marker**: `ANTI-FACT (believed FALSE): ...` then states the truth.
- The **MEMORY.md index line leads with `[ANTI-FACT]` and the truth**, so even a one-line read shows the correction first.
- The bare affirmative claim X never stands alone as a line, a slug, or index text; it appears only quoted inside its negation ("the myth that 'X' is false").

This is **unmistakable by construction plus defense-in-depth**, not "structurally impossible." `stance` is the machine-readable carrier; truth-forward text is the human / grep / embedding-safe carrier.

### Required shape of an anti-fact
Frontmatter: `stance: anti_fact`, `confidence: <= 0.1`, `correction: <affirmative truth>`, `retained_because: myth|debunked_prior|trap`. Optional `flipped_from` for an audit trail. **One claim per file**: never store an affirm-fact and an anti-fact for the same X in one file; an anti-fact is its own cross-linked file. Genuinely dual-truth / context-dependent cases use a paired, cross-linked scoped-affirm + scoped-anti-fact, not one fuzzy entry. (The `scope` field is intentionally NOT part of v1.)

Worked example (frontmatter):
```
name: anti-fact-null-is-a-class
description: "ANTI-FACT (believed FALSE): the claim that a Null character is classless. TRUTH: Null IS a class."
metadata:
  type: project
  stance: anti_fact
  confidence: 0.03
  correction: "Null IS a class (class_id 3); everyone age 7+ holds a class."
  retained_because: myth
```
MEMORY.md line: `- [ANTI-FACT] Null IS a class (the "Null = no class" myth is FALSE; do not re-adopt) -> anti-fact-null-is-a-class.md`

### Flipping an anti-fact is gated (anti-sycophancy)
Promoting `anti_fact -> affirm` is the highest-cost mistake (a confident user arguing you out of a correct anti-fact). It requires NEW INDEPENDENT evidence, an external audit (`mind-debate` / `mind-discuss`), and a `flipped_from` record. Re-reasoning alone or social pressure is never sufficient. The gate is on the TRANSITION, so any path from anti_fact back to affirm (even via in-tension) needs the audit. A direct contradiction between an incoming fact asserting X and an anti_fact about X is handled by `mind-coping-contradictions`: resolve it explicitly (promote / demote), never by silently dropping a confidence number.

A heuristic linter for these invariants ships at `tools/validate_anti_facts.py`.

## Pitfalls
- Presenting belief as knowledge (overconfidence) is the default failure; guard hardest against it.
- Treating correlated sources as independent confirmation.
- Using one global confidence threshold regardless of how costly being wrong is.
- Filing a genuinely-uncertain (~0.5) or weakly-leaning item as `anti_fact`; reserve `anti_fact` for confidence <= 0.1 WITH a real re-adoption pull (a myth, trap, or debunked belief), or you reintroduce the unknown-vs-false ambiguity.
- Letting the bare false claim appear as a standalone line, slug, or index text (the leak path).
- Inverting the invariant: writing a HIGH confidence on an anti-fact to mean "I'm confident it is false." Confidence is always P(X true), so for an anti-fact it is LOW.
- Over-proliferation: minting an anti-fact for every transient wrong guess. Reserve it for claims that genuinely pull to be re-adopted.
