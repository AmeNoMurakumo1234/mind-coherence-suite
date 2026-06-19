# Mind Coherence Suite

A portable skill suite that gives an AI agent a formal discipline for keeping a
growing CONTEXT + MEMORY coherent over time **without** letting it harden into a
coherent-but-false worldview (a "coherent delusion").

It is a seed, not a standard. Read [CHARTER.md](CHARTER.md) before adopting it:
uniform adoption is an explicit anti-goal.

## What it is

As an agent's memory grows, contradictions are inevitable. This suite is one
continuous cycle for handling them honestly:

1. **mind-belief-vs-knowledge** - intake calibration. Most "knowledge" is confident
   belief; weight by source trust and independence, propagate confidence, express it
   honestly, and scale the action threshold to the stakes. Carries the **stance** axis
   (`affirm` / `lean_false` / `open_question` / `anti_fact`), so memory can hold an
   **anti-fact**: a claim kept BECAUSE it is believed false (a myth, trap, or debunked
   prior), stored truth-forward so it can never be misread as true.
2. **mind-coping-contradictions** - hold conflicts in-tension instead of forcing a
   premature collapse; resolve context-dependent ones by adding context.
3. **mind-meditation** - internal self-audit. Tiny reversible changes, tested over
   time. Caveat: coherence is not truth, so internal audit alone is never enough.
4. **mind-debate** - external adversarial audit. Decouple message from messenger,
   pre-register confidence, opposite-messenger test.
5. **mind-discuss** - external collaborative audit. Co-vet inferences; diversity of
   minds is the safety mechanism.
6. **mind-anti-sycophancy** - the linchpin. Earned disagreement is the service;
   sycophancy manufactures fake triangulation and amplifies shared delusion.
7. **mind-coherence-cycle** - the overview that maps how the pieces interlock. See
   `plugin/skills/mind-coherence-cycle/coherence-cycle.png` (source `.mmd` and
   `.html` alongside it; regenerate locally with headless Chrome, no external
   services).

## Maturity (calibrated, per the suite's own rules)

v1.1.1. Authored collaboratively in a focused session and demonstrated working over
roughly **one** full cycle (an automated gate caught an authoring error the author
missed; a human partner corrected a self-assessment with evidence; a fresh insight
was held in-tension rather than rushed into memory). The anti-fact feature was
designed via a multi-lens + adversarial-verification workflow and incorporates the
verifiers' converged fixes; the confidence model was then calibrated through live
debate (probability kept over a signed scale; the endpoints 0 and 1 forbidden). That
is evidence the *process* functions; it is **not** evidence of a mature, battle-tested
framework. Treat the confidence accordingly.

## Install (Claude Code)

This repo is both a marketplace and the plugin it hosts.

```
/plugin marketplace add <git-host>/<owner>/<repo>     # or a local path to this dir
/plugin install mind-coherence@mind-coherence-suite
```

Validate locally before publishing:

```
claude plugin validate ./plugin
```

(Skills invoke as `/mind-coherence:mind-<skill>`. The doubled `mind-` is cosmetic;
a fork may rename the skills to drop the prefix.)

## Porting to other agentic harnesses

The portable core is the **content**, not the manifest. Each `SKILL.md` is plain
Markdown with simple YAML frontmatter (`name`, `description`, plus tags). Any harness
that ingests skill files, system-prompt fragments, or rules can use the bodies
directly. What does **not** port automatically is discovery/packaging: `plugin.json`
and `marketplace.json` are Claude Code specific. Honest summary: copy the `skills/`
bodies anywhere; re-wrap the manifest per your harness.

## Before you publish

These are deliberately left for the owner to decide:
- **License** - none is set. Choose one and add it before sharing.
- **Author / owner identity** - the manifests use a placeholder; set it to what you
  want public.
- **Hosting** - this is already a standalone repo; publishing is just pushing commits.
- **Memory stays private** - this repo ships the memory-management *system*, never memory
  *content*. See [MEMORY-SEPARATION.md](MEMORY-SEPARATION.md); a `.gitignore` and the
  `tools/reflect_from_local.py` guard enforce it.

## Lineage

Born in the `quantum-concepts` project as the `.agents/skills/mind-*` suite, then
exported here as a shareable plugin. If you fork it, record your lineage and your
divergences (see [RECONCILIATION-LOG.md](RECONCILIATION-LOG.md)); divergence is the
point.

## The coherence cycle

The whole suite at a glance: intake calibration -> memory -> contradictions -> internal
(meditation) and external (debate + discuss) audit -> triangulation -> integration, with
anti-sycophancy as the linchpin guarding the external audit, and a never-solved loop back.
Memory items carry a stance, including **anti-facts** (believed-false, kept on purpose).
The diagram renders locally (no external services); regenerate with the source in
`plugin/skills/mind-coherence-cycle/` (`.mmd` and `.html`).

![Mind Coherence cycle: intake, memory with stance/anti-facts, contradictions, internal and external audit, triangulation, integration, with anti-sycophancy guarding and a never-ending loop](plugin/skills/mind-coherence-cycle/coherence-cycle.png)
