---
name: mind-onboarding
description: "One-time runbook for auditing an EXISTING memory corpus to a clean base state when you adopt this suite. Read-only audit, then a proposed plan, then the human ratifies, then apply in small reversible steps: reconcile index vs file bodies, move in-flight status out of memory, convert believed-false-but-kept items to anti-facts. Load right after installing the suite into a repo or agent that already has accumulated memory."
version: 1.0.0
metadata:
  tags: [onboarding, memory-audit, cleanup, anti-fact, calibration, mind-suite]
  related_skills: [mind-belief-vs-knowledge, mind-coping-contradictions, mind-meditation, mind-anti-sycophancy, mind-coherence-cycle]
---

## Overview

The rest of this suite keeps memory coherent GOING FORWARD. But most agents adopt it with a pile of memory already on disk, accumulated before any of these disciplines were in place. This skill is the ONE-TIME cleanup that brings that existing pile to a clean, maintainable base state. It is the same disciplines applied to the backlog instead of to each new item.

## When to Use
- Right after installing this suite into a repo or agent that ALREADY has memory.
- Periodically, as a re-audit, when memory has grown and you suspect drift.
- Before relying on memory for an important decision, if it has never been audited.

## Core stance (read before touching anything)
- **Memory edits are dangerous self-surgery** ([[mind-meditation]]): tiny, reversible changes, never a bulk auto-rewrite.
- **Audit is READ-ONLY; the human ratifies.** Produce a PROPOSED plan, then let the human approve it piece by piece. The human is the independent external axis ([[mind-anti-sycophancy]], [[mind-discuss]]); the agent never rewrites the memory wholesale on its own judgment.
- **Trust the body, not the summary.** If your memory has an index or table of contents, it has probably DRIFTED from the actual file bodies. Audit the bodies; treat the index as a lossy summary to be reconciled, not as truth.

## The audit procedure
1. **Inventory.** List every memory item (and the index, if one exists). For a large corpus, fan the classification out across several passes or agents so each handles a batch.
2. **Classify each item.** Record its category, a one-line gist, and any flags: stale / now-wrong, duplicate or overlapping, contradicts another item, anti-fact candidate, miscategorized, thin provenance, load-bearing.
3. **Reconcile index vs bodies.** Where an index line disagrees with its file body, fix the index to match the body.
4. **Move in-flight status OUT of memory.** Build status, "X is done / shipped", and open to-do leads do not belong in long-term memory; route them to your task tracker or working notes. Memory keeps only the durable LESSON distilled from them.
5. **Anti-fact pass.** Any item that records a believed-FALSE claim kept on purpose (a live myth, a debunked prior, a tempting-but-false trap, often signaled by words like RETIRED, superseded, NOT, debunked, or "was X, now Y") should be converted to the anti-fact format in [[mind-belief-vs-knowledge]]: stance anti_fact, low confidence, correction stated FIRST, truth-forward name and text. Never leave a bare false claim phrased as if true.
6. **Contradiction pass.** Hold genuine conflicts IN-TENSION ([[mind-coping-contradictions]]) rather than forcing a collapse; for dated or superseded conflicts, the newer item is current truth and the older becomes historical.
7. **De-duplicate.** Merge overlapping items or cross-link them; never silently drop one side of a conflict.
8. **Calibrate confidence SELECTIVELY.** Add confidence and stance only where they change behavior (anti-facts, in-tension items, load-bearing beliefs). A blanket retrofit across every file is high churn for low value; skip it.

## Apply and verify
- Present the plan; apply only what the human ratifies, smallest and most reversible first.
- After applying, VERIFY: re-scan for the stale phrases you fixed; confirm every memory item has an index entry and every index entry resolves to a real item (no orphans, no dangling links); run the anti-fact linter if your toolchain has one.

## Pitfalls
- Bulk-stamping stance and confidence onto every file (churn, no value).
- Deleting instead of relocating: move content to its correct home BEFORE removing any pointer to it.
- Letting a confident user, or your own re-reasoning, flip a correct anti-fact without new independent evidence (that transition is gated, see [[mind-belief-vs-knowledge]]).
- Treating the audit's own classifications as ground truth: they are proposals, the human is the ratifier.
- Forgetting the working agreement: memory CONTENT is private and the user's own; this suite manages the SYSTEM, it never collects or ships the content.
