#!/usr/bin/env python3
"""Lint memory files for the confidence + anti-fact invariants from mind-belief-vs-knowledge.

Heuristic frontmatter scan (no pyyaml dependency); a best-effort guard, not a parser.
Run it against YOUR memory dir (which is private and lives outside this repo).

General rule (Cromwell), any file with a confidence:
  - confidence must be a probability in (0, 1); never exactly 0 or 1 (un-updatable = closed-minded).

Anti-fact invariants (when metadata.stance == anti_fact):
  - confidence in (0, 0.15]          (confidence ALWAYS = P(claim-as-written is TRUE); low, never 0)
  - correction present and non-empty  (the affirmative TRUE statement, no double negatives)
  - retained_because in {myth, debunked_prior, trap}
  - description leads with an "ANTI-FACT" marker, so even a bare read states falseness

Exit nonzero if anything violates an invariant.

Usage:  python tools/validate_anti_facts.py /path/to/your/memory
"""
import argparse, pathlib, re, sys

ANTI_FACT_MAX = 0.15  # mirror of the strong-affirm bar (~0.85); calibrate over time

def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""

def field(fm, key):
    m = re.search(rf"(?mi)^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", fm)
    return m.group(1).strip().strip('"\'') if m else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("memory_dir", help="path to the memory directory (private; outside this repo)")
    a = ap.parse_args()
    d = pathlib.Path(a.memory_dir)
    if not d.is_dir():
        sys.exit(f"not a directory: {d}")

    problems, n_af, n_conf = [], 0, 0
    for f in sorted(d.glob("*.md")):
        fm = frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        stance = field(fm, "stance")
        conf_raw = field(fm, "confidence")
        errs = []

        # General Cromwell check on any confidence value.
        conf = None
        if conf_raw is not None:
            n_conf += 1
            try:
                conf = float(conf_raw)
                if not (0.0 < conf < 1.0):
                    errs.append(f"confidence must be in (0,1), never 0 or 1 (got {conf_raw})")
            except ValueError:
                errs.append(f"confidence not a number: {conf_raw}")

        if stance == "anti_fact":
            n_af += 1
            corr, rb = field(fm, "correction"), field(fm, "retained_because")
            desc = field(fm, "description") or ""
            if conf is None:
                errs.append("anti_fact requires a confidence")
            elif not (0.0 < conf <= ANTI_FACT_MAX):
                errs.append(f"anti_fact confidence must be in (0, {ANTI_FACT_MAX}] (got {conf_raw})")
            if not corr:
                errs.append("correction (affirmative truth) required and non-empty")
            if rb not in {"myth", "debunked_prior", "trap"}:
                errs.append(f"retained_because must be myth|debunked_prior|trap (got {rb})")
            if "ANTI-FACT" not in desc.upper():
                errs.append("description must lead with an ANTI-FACT marker (truth-forward)")

        if errs:
            problems.append((f.name, errs))

    for name, errs in problems:
        print(f"FAIL {name}")
        for e in errs:
            print(f"   - {e}")
    print(f"\nchecked {n_conf} file(s) with confidence ({n_af} anti-fact); {len(problems)} with violations.")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
