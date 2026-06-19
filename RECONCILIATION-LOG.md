# Reconciliation Log

A running record of divergences between forks of the Mind Coherence Suite, treated as
debate data (see `CHARTER.md` and the `mind-debate` / `mind-discuss` skills). The point
is **not** to converge to one canonical version. It is to keep the differences visible
and re-audited so independently-flawed forks keep each other honest.

## How to use

- When your fork diverges from its parent (or from another fork you compare against),
  add an entry.
- Reconcile by debate, not auto-merge. The outcome of an entry is one of: `adopted`,
  `rejected`, or `held-in-tension` (a real, unresolved disagreement that stays open).
- Record confidence honestly and cite evidence/sources, with their independence noted.
- Do not delete `held-in-tension` entries to relieve discomfort. Holding the tension is
  the working state, not a failure.

## Lineage

- Parent: (origin) `quantum-concepts` repo, `.agents/skills/mind-*`, v1.0.0.
- This fork: <name> <version> <date> <who/what maintains it>

## Entries

> Template (copy per divergence):

```
### YYYY-MM-DD  -  <short title of the divergence>
- Forks involved:   <fork A> vs <fork B / parent>
- The divergence:   <what differs: which skill, which rule/threshold, etc.>
- Rationale A:      <why fork A holds its version>   (confidence: NN%, evidence: ...)
- Rationale B:      <why fork B holds its version>   (confidence: NN%, evidence: ...)
- Source check:     <are the supporting sources independent? credibility?>
- Outcome:          adopted | rejected | held-in-tension
- Notes:            <what re-auditing changed, what stays open>
```

---

### 2026-06-19  -  v1.0.0 seed established
- Forks involved:   parent (origin) only
- The divergence:   none yet; baseline.
- Outcome:          n/a
- Notes:            First public seed. The expectation set by CHARTER.md is that real
                    entries below will show genuine, lasting disagreement between
                    descendants. An empty or all-"adopted" log over time is a warning
                    sign of monoculture, not health.
