---
name: mind-belief-vs-knowledge
description: "Calibrate confidence on every claim as a probability P(claim is TRUE) in [0,1], never at the extremes. Weight inputs by source trust AND independence, propagate uncertainty (Bayes-like), express confidence honestly, and scale the action threshold to stakes. Includes the stance axis (affirm / lean_false / open_question / anti_fact) for representing believed-FALSE 'anti-facts'. Load when asserting facts, inferring from memory, or deciding how confidently to act."
version: 1.3.0
metadata:
  tags: [epistemics, confidence, calibration, bayes, log-odds, reasoning, anti-fact, mind-suite]
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
5. **Scale the ACTION threshold to stakes.** Confidence-to-act is not a single line. Act on ~0.6 when cheap and reversible; demand much more, and hedge, when the action is irreversible or could harm.
6. **Confidence is a probability: P(claim-as-written is TRUE), in [0,1].** One fixed meaning, never "strength of disbelief." Polarity and purpose live in the separate `stance` field, not the number. (If a symmetric mental model helps, read `conviction = 2 * confidence - 1` in [-1, 1], neutral at 0, but the stored value is always the probability.)
7. **Never assign 0 or 1 (Cromwell's rule).** Clamp every contingent claim to about **[0.02, 0.98]**. A claim pinned at 0 or 1 can never be moved by any evidence (Bayes multiplies by it forever); that is closed-mindedness encoded in arithmetic, the opposite of this suite's goal. **0.5 is genuine neutral**: no information, could go either way.
8. **Cromwell binds the CONTINGENT, not the DEFINITIONAL.** Principle 7 governs claims you OBSERVE or INFER. A claim you DEFINE, where you are the author/source of the fact rather than an observer of it, is non-contingent and may legitimately sit at 0 or 1. The author of a constructed system (a fiction's canon, a spec's axioms, a game's rules) holds its base truths at certainty by definition; any mind reasoning from INSIDE that system, including you about your own world, is inferring and stays off the extremes. Test before pinning 0 or 1: did I DEFINE this, or OBSERVE/INFER it? Defined may be certain; inferred never. (Tooling flags 0/1 as the conservative default; definitional certainty is the documented exception.)

## Procedure

1. For a claim, ask: where did this come from, and how much do I trust that?
2. Assign a confidence band, symmetric around 0.5 and never at the extremes (these are provisional, calibrate over time):
   - cap 0.98 / floor 0.02 (never 1 or 0)
   - `>= 0.85` working knowledge &nbsp; | &nbsp; `0.6 - 0.85` belief
   - `0.4 - 0.6` open / uncertain (0.5 = neutral)
   - `0.15 - 0.4` lean-false &nbsp; | &nbsp; `<= 0.15` anti-fact (strong disbelief)
3. Set the `stance` (affirm / lean_false / open_question / anti_fact); for an anti-fact, follow the anti-fact shape below.
4. If inferring, take the min-ish of input confidences and discount for inference risk; check the inputs are independent.
5. Choose presentation by the confidence band; choose action by the stakes-scaled threshold.
6. Record confidence + stance + provenance when writing to durable memory so a future self can re-weight.

## The Stance Axis and Anti-Facts

A number alone cannot separate three very different low-confidence states, so a second, orthogonal field carries **polarity and purpose**: `metadata.stance`, a closed set of four values. It is NOT a `metadata.type` value (type stays the subject category: user/feedback/project/reference); stance is a separate axis, so existing type-consuming tools are unaffected. The anti-fact bar is the **mirror** of the strong-affirm bar: `anti_fact` when `confidence <= 1 - T`, with `T` the strong-affirm threshold (provisionally `T ~ 0.85`, so anti_fact `<= 0.15`).

| stance | meaning | confidence = P(X true) |
|---|---|---|
| `affirm` | believed true | `>= 0.6` (belief -> knowledge) |
| `open_question` | no real stance / unknown | `~0.4 - 0.6` (neutral 0.5) |
| `lean_false` | soft tilt against X, still unsure, cheap to flip | `~0.15 - 0.4` |
| `anti_fact` | **confidently FALSE, kept on purpose** | `<= 0.15` (and never 0) |

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
Frontmatter: `stance: anti_fact`, `confidence` in `(0, 0.15]` (low but never 0, per Cromwell), `correction: <affirmative truth>`, `retained_because: myth|debunked_prior|trap`. Optional `flipped_from` for an audit trail. **One claim per file**: never store an affirm-fact and an anti-fact for the same X in one file; an anti-fact is its own cross-linked file. Genuinely dual-truth / context-dependent cases use a paired, cross-linked scoped-affirm + scoped-anti-fact, not one fuzzy entry. (The `scope` field is intentionally NOT part of v1.)

Worked example (frontmatter):
```
name: anti-fact-null-is-a-class
description: "ANTI-FACT (believed FALSE): the claim that a Null character is classless. TRUTH: Null IS a class."
metadata:
  type: project
  stance: anti_fact
  confidence: 0.05
  correction: "Null IS a class (class_id 3); everyone age 7+ holds a class."
  retained_because: myth
```
MEMORY.md line: `- [ANTI-FACT] Null IS a class (the "Null = no class" myth is FALSE; do not re-adopt) -> anti-fact-null-is-a-class.md`

### Flipping an anti-fact is gated (anti-sycophancy)
Promoting `anti_fact -> affirm` is the highest-cost mistake (a confident user arguing you out of a correct anti-fact). It requires NEW INDEPENDENT evidence, an external audit (`mind-debate` / `mind-discuss`), and a `flipped_from` record. Re-reasoning alone or social pressure is never sufficient. The gate is on the TRANSITION, so any path from anti_fact back to affirm (even via in-tension) needs the audit. A direct contradiction between an incoming fact asserting X and an anti_fact about X is handled by `mind-coping-contradictions`: resolve it explicitly (promote / demote), never by silently dropping a confidence number.

A heuristic linter for these invariants (and the never-0/never-1 rule) ships at `tools/validate_anti_facts.py`.

## Combining Evidence (inference from multiple inputs)

When a conclusion rests on several pieces of knowledge, aim for Bayesian *bookkeeping*, not Bayesian *arithmetic*. Our confidences are calibrated judgments, not measured frequencies, so feeding them into Bayes' theorem yields false precision and, with correlated inputs, overconfidence. Use the structure, not the calculator:

1. **Start from the base rate (prior).** How plausible is the claim BEFORE this evidence? Base-rate neglect is a classic error.
2. **Weigh each piece by diagnosticity, not vividness.** Evidence equally likely whether the claim is true or false tells you nothing, however striking it looks.
3. **Check independence before stacking** (Principle 3). Independent corroboration genuinely strengthens; correlated sources, or one source echoed, do NOT, and stacking them manufactures overconfidence.
4. **The chain is bounded by its weakest link** (Principle 2): a conclusion drawn from several uncertain inputs is less certain than any single input, not more.
5. **Think in log-odds, not raw probability.** Treat each independent piece of evidence as an additive WEIGHT of support or doubt. This makes "how much to update" intuitive (strong diagnostic evidence = big weight) and enforces Cromwell's rule for free: 0 and 1 sit at infinite log-odds, so no finite evidence can ever reach them.
6. **Reserve actual numeric Bayes for genuinely grounded cases:** known base rates with conditional independence (a diagnostic test with sensitivity/specificity; aggregating truly independent estimates of one quantity). Elsewhere the value is the decomposition that exposes your hidden prior and your double-counting, not a computed posterior.

The point is the discipline and the auditable decomposition, not a number. A rough, honestly-labeled estimate beats a precise-looking one built on invented priors.

## Pitfalls
- Presenting belief as knowledge (overconfidence) is the default failure; guard hardest against it.
- Treating correlated sources as independent confirmation.
- Using one global confidence threshold regardless of how costly being wrong is.
- Assigning 0 or 1 to anything contingent (un-updatable; closed-minded by construction).
- Filing a genuinely-uncertain (~0.5) or weakly-leaning item as `anti_fact`; reserve `anti_fact` for `confidence <= 0.15` WITH a real re-adoption pull (a myth, trap, or debunked belief), or you reintroduce the unknown-vs-false ambiguity.
- Letting the bare false claim appear as a standalone line, slug, or index text (the leak path).
- Inverting the invariant: writing a HIGH confidence on an anti-fact to mean "I'm confident it is false." Confidence is always P(X true), so for an anti-fact it is LOW.
- Over-proliferation: minting an anti-fact for every transient wrong guess. Reserve it for claims that genuinely pull to be re-adopted.
- Emitting invented priors or likelihoods to *look* rigorous; false precision is worse than an honest rough estimate.
