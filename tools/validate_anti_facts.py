#!/usr/bin/env python3
"""Lint memory files for the anti-fact invariants from mind-belief-vs-knowledge.

Heuristic frontmatter scan (no pyyaml dependency); a best-effort guard, not a parser.
Run it against YOUR memory dir (which is private and lives outside this repo).

Anti-fact invariants (when metadata.stance == anti_fact):
  - confidence present and <= 0.1     (confidence ALWAYS = P(claim-as-written is TRUE))
  - correction present and non-empty  (the affirmative TRUE statement, no double negatives)
  - retained_because in {myth, debunked_prior, trap}
  - description leads with an "ANTI-FACT" marker, so even a bare read states falseness

Exit nonzero if any anti-fact violates an invariant.

Usage:  python tools/validate_anti_facts.py /path/to/your/memory
"""
import argparse, pathlib, re, sys

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

    problems, n_af = [], 0
    for f in sorted(d.glob("*.md")):
        fm = frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        if field(fm, "stance") != "anti_fact":
            continue
        n_af += 1
        conf, corr, rb = field(fm, "confidence"), field(fm, "correction"), field(fm, "retained_because")
        desc = field(fm, "description") or ""
        errs = []
        try:
            if conf is None or float(conf) > 0.1:
                errs.append(f"confidence must be present and <= 0.1 (got {conf})")
        except ValueError:
            errs.append(f"confidence not a number: {conf}")
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
    print(f"\nchecked {n_af} anti-fact file(s); {len(problems)} with violations.")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
