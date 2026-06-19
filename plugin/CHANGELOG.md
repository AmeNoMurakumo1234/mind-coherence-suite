# Changelog

All notable changes to the Mind Coherence plugin.

## 1.2.0 - 2026-06-19

- `mind-belief-vs-knowledge`: new **Combining Evidence** section - Bayesian *bookkeeping*,
  not arithmetic. Base rate first; weigh by diagnosticity; check independence before
  stacking; chain bounded by its weakest link; **think in log-odds** (which enforces the
  never-0/1 Cromwell rule for free); reserve numeric Bayes for genuinely grounded cases.
  Decided via debate: mandated posterior computation was declined (inputs are judgments,
  not frequencies -> false precision; correlated inputs -> overconfidence).
- **LICENSE: MIT.** Author set to **Ame No Murakumo**; manifests updated.
- Memory privacy elevated to a first-class **Working Agreement** with all consumers
  (README section + `MEMORY-SEPARATION.md`).
- README: removed the "Before you publish" section (resolved).

## 1.1.1 - 2026-06-19

Calibration refinement to the confidence model (decided via debate, not capitulation).

- Confidence stays a probability `P(claim is TRUE)` in [0,1]. A signed [-1,1] correlation-style
  scale was considered and **declined for storage** (it breaks the single P(X) invariant and
  reopens the sign-inversion trap) but is offered as an optional derived `conviction = 2p - 1`
  view for human intuition.
- **Cromwell's rule**: never assign 0 or 1 to a contingent claim (clamp ~[0.02, 0.98]); a pinned
  claim can never update by any evidence. 0.5 is genuine neutral.
- **Anti-fact threshold loosened and symmetric** with the strong-affirm bar: `anti_fact` when
  `confidence <= 1 - T` (provisionally `<= 0.15`, was 0.1; calibrate over time), and never 0.
- Symmetric provisional bands around 0.5. `tools/validate_anti_facts.py` now enforces
  `(0, 0.15]` for anti-facts and flags any confidence of exactly 0 or 1.
- Diagram updated to state the never-0 / never-1 rule.

## 1.1.0 - 2026-06-19

Adds the **anti-fact** feature and the fork-and-diverge tooling.

- `mind-belief-vs-knowledge`: new **stance axis** (`affirm` / `lean_false` /
  `open_question` / `anti_fact`), orthogonal to `metadata.type`. Confidence is fixed as
  P(claim-as-written is TRUE) on one 0-1 scale. An **anti-fact** is a claim kept BECAUSE
  it is believed false (myth / debunked_prior / trap); safety lives in truth-forward file
  text (correction-first, truth-forward name, `[ANTI-FACT]` index line), not in tooling.
  Flips are gated against capitulation.
- `mind-coping-contradictions`: handles a fact-vs-anti-fact contradiction explicitly.
- `mind-coherence-cycle`: diagram regenerated to show the stance spectrum and anti-facts.
- Tooling: `tools/reflect_from_local.py` (curated local -> repo upstreaming, skills only)
  and `tools/validate_anti_facts.py` (lints anti-fact invariants in a memory dir).
- `MEMORY-SEPARATION.md` + `.gitignore`: the plugin ships the memory-management SYSTEM,
  never memory CONTENT.

Design note: produced via a multi-lens + adversarial-verification workflow; the
verifiers' converged fixes (one confidence scale; stance not a 5th type; safety in file
text; drop the unresolved `scope` field; gate flips) are incorporated. Per the project's
propose-options-decide-greenlight rule, no bulk memory backfill of real anti-facts is
included; only the FORMAT ships.

## 1.0.0 - 2026-06-19

Initial seed.

- Seven skills: `mind-belief-vs-knowledge`, `mind-coping-contradictions`,
  `mind-meditation`, `mind-debate`, `mind-discuss`, `mind-anti-sycophancy`, and the
  overview `mind-coherence-cycle`.
- `mind-coherence-cycle` ships the cycle diagram (`coherence-cycle.png`) with its
  source (`.mmd` and a hand-laid `.html` that renders locally via headless Chrome,
  no external services).
- Fork-and-diverge charter and a reconciliation-log convention (see the marketplace
  root `CHARTER.md` and `RECONCILIATION-LOG.md`).

Maturity note: demonstrated working over roughly one full audit cycle; not yet
battle-tested over many. See README for the calibrated claim.
