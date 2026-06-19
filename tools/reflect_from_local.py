#!/usr/bin/env python3
"""Reflect locally-mutated mind-* skills from a working copy back INTO this plugin
repo (plugin/skills) - the curated upstream step of the fork-and-diverge loop.

Direction: LOCAL (where daily work happens) -> THIS REPO (shared source). It copies
ONLY mind-* skill files and NEVER reads or copies memory content. It runs an ASCII /
AI-tell gate before accepting. Dry-run by default; --apply to write. It never commits
or pushes - that stays a deliberate, reviewed step.

Usage:
  python tools/reflect_from_local.py --from /path/to/project/.agents/skills          # dry-run
  python tools/reflect_from_local.py --from /path/to/project/.agents/skills --apply  # write
"""
import argparse, pathlib, sys, shutil, difflib

def non_ascii(text):
    return sorted({c for c in text if ord(c) > 127})

def main():
    here = pathlib.Path(__file__).resolve().parent
    default_to = here.parent / "plugin" / "skills"
    ap = argparse.ArgumentParser(description="Reflect local mind-* skills into the plugin repo (curated upstream).")
    ap.add_argument("--from", dest="src", required=True, help="local skills dir, e.g. <project>/.agents/skills")
    ap.add_argument("--to", dest="dst", default=str(default_to), help="plugin skills dir (default: ./plugin/skills)")
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry-run)")
    a = ap.parse_args()

    src, dst = pathlib.Path(a.src), pathlib.Path(a.dst)
    if not src.is_dir():
        sys.exit(f"source not found: {src}")
    if "memory" in str(src).lower():
        sys.exit("refusing: source path contains 'memory'. This tool syncs SKILLS only, never memory content.")
    dst.mkdir(parents=True, exist_ok=True)

    skills = sorted(p for p in src.glob("mind-*") if p.is_dir())
    if not skills:
        sys.exit(f"no mind-* skill dirs under {src}")

    # Gate every SKILL.md for AI-tell / non-ascii BEFORE accepting anything.
    gate_fail = []
    for sdir in skills:
        skf = sdir / "SKILL.md"
        if skf.exists():
            na = non_ascii(skf.read_text(encoding="utf-8"))
            if na:
                gate_fail.append((sdir.name, [hex(ord(c)) for c in na]))
    if gate_fail:
        print("GATE FAILED (AI-tell / non-ascii chars). Fix before reflecting:")
        for n, na in gate_fail:
            print(f"  {n}: {na}")
        sys.exit(2)

    changed = 0
    for sdir in skills:
        ddir = dst / sdir.name
        for f in sorted(p for p in sdir.rglob("*") if p.is_file()):
            rel = f.relative_to(sdir)
            target = ddir / rel
            old = target.read_bytes() if target.exists() else None
            new = f.read_bytes()
            if old == new:
                continue
            changed += 1
            print(("NEW " if old is None else "CHG ") + f"{sdir.name}/{rel.as_posix()}")
            if old is not None and f.suffix in {".md", ".mmd", ".html"}:
                diff = difflib.unified_diff(
                    old.decode("utf-8", "replace").splitlines(),
                    new.decode("utf-8", "replace").splitlines(),
                    lineterm="", n=1)
                for line in list(diff)[:40]:
                    print("    " + line)
            if a.apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)

    print(f"\n{'APPLIED' if a.apply else 'DRY-RUN'}: {changed} file(s) {'written' if a.apply else 'would change'}.")
    if changed and not a.apply:
        print("Re-run with --apply to write, then review `git diff`, then commit + push deliberately.")

if __name__ == "__main__":
    main()
