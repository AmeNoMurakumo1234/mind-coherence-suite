---
name: mind-coherence-cycle
description: "Overview and map of how the mind-* suite interlocks into a continuous cycle that keeps a growing CONTEXT+MEMORY coherent but not delusional. Covers intake calibration, holding contradictions, internal (meditation) vs external (debate/discuss) audit, triangulation, the anti-sycophancy linchpin, and the never-solved feedback loop. See coherence-cycle.png. Load when onboarding the suite or deciding which member skill applies to an epistemic situation."
version: 1.0.0
metadata:
  tags: [epistemics, overview, coherence, memory, mind-suite]
  related_skills: [mind-belief-vs-knowledge, mind-coping-contradictions, mind-meditation, mind-debate, mind-discuss, mind-anti-sycophancy]
---

## Overview

The `mind-*` suite is a single process for keeping an accumulating CONTEXT + MEMORY coherent over time without sliding into a coherent-but-false worldview. As data builds, contradictions are inevitable; this cycle is how they are calibrated, held, and reconciled. Diagram: `coherence-cycle.png` (source `coherence-cycle.mmd`).

## When to Use
- To understand or onboard the whole suite.
- When deciding which member skill applies to a given epistemic situation.

## The Cycle

1. **Intake - `mind-belief-vs-knowledge`.** Every input is weighted by source trust and independence, confidence is propagated through inference, expressed honestly, and the action threshold is scaled to stakes. Items enter memory tagged with confidence + provenance.
2. **Tension - `mind-coping-contradictions`.** New data conflicts with stored items. Hold both in-tension; resolve context-dependent conflicts by adding discriminating context; tag genuine conflicts IN-TENSION.
3. **Audit, two paths:**
   - **Internal - `mind-meditation`.** Small reversible confidence changes, tested over time. Limited because *coherence != truth*; a mind has no external reference frame on itself.
   - **External - `mind-debate` (adversarial) + `mind-discuss` (collaborative).** Other minds supply the missing reference frame. Triangulation: uncorrelated errors cancel, the shared truth reinforces.
4. **Guard - `mind-anti-sycophancy` (linchpin).** External audit only works if the minds stay independent. Sycophancy manufactures fake triangulation and amplifies error into shared delusion, so earned disagreement is the service.
5. **Integration.** Rebalanced confidences write back to MEMORY conservatively and reversibly; unresolved items stay flagged IN-TENSION.
6. **Loop.** Back to intake. There is no end-state of a self-certified-correct mind; the cycle is permanent, manageable-not-solvable, ongoing struggle.

The scheduled real-world instance of one lap is the **wakeup memory-audit** every agent runs at
session-open: load memory, reconcile vs self + shared canon + current reality, fix reversals, hold
tensions IN-TENSION. The step-by-step runbook lives in `mind-meditation` ("Wakeup memory-audit").

## Why It Is Only Manageable, Never Solved

A mind audits itself with the faculties under audit, so complete self-correction is impossible in principle. The only escape is social: many differently-flawed minds triangulate. But triangulation fails if the minds are correlated (shared bias, echo chamber, a mirroring AI), so the health of the entire system reduces to one thing worth guarding constantly: the genuine INDEPENDENCE of the participating minds.

## Pitfalls
- Running only the internal path (meditation) and trusting coherence as truth.
- Treating agreement among non-independent minds as validation.
- Editing memory aggressively instead of in small, reversible, evidence-justified steps.

## Regenerating the Diagram

The diagram is rendered **locally** (no external services: mermaid.ink is correctly blocked as a data-exfiltration destination, and `npx mmdc` cannot write its cache in the sandbox).

- Sources: `coherence-cycle.mmd` (Mermaid, the conceptual source) and `coherence-cycle.html` (a self-contained, hand-laid HTML/SVG that is what actually gets rasterized for crisp control of the bulleted boxes).
- Render with headless Chrome:
  `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --no-sandbox --hide-scrollbars --force-device-scale-factor=2 --window-size=2800,1360 --screenshot=coherence-cycle.png "file:///<abs-path>/coherence-cycle.html"`
- Output: `coherence-cycle.png` (landscape, ~5600x2720 at 2x).
- Keep `.mmd` and `.html` in sync if you edit one.
