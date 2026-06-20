#!/usr/bin/env python3
"""
vendor_into_repo.py - install the mind-* skills INTO a target repo that uses its
own skill system, then hand the user a copy-paste PROMPT so the repo's OWN AI agent
intakes them into whatever discovery scheme it uses (AGENTS.md, a generated INDEX.md,
a .claude/skills registry, required frontmatter, a gate, ...).

We deliberately do NOT edit the target's index ourselves: every repo's index scheme
differs, and guessing wrong corrupts it. Instead we copy the skill files and emit a
prompt for the in-repo AI to wire discoverability correctly, the assumption being that
anyone who wants skills is already running an AI agent in that repo.

This is the consumer / dev-vendoring path for harnesses that load skills from a repo
directory rather than via the Claude Code plugin manager. It is the inverse of
reflect_from_local.py (which curates a working copy's edits back upstream).

Usage:
    python tools/vendor_into_repo.py --target <repo> [--skills-dir REL] [--apply]

Default is a DRY RUN (prints what it would do + a preview of the prompt). Add --apply
to copy the skills and write the prompt file. Refuses any path containing 'memory'.
"""
import argparse
import shutil
import sys
from pathlib import Path

SKILL_GLOB = "mind-*"
PROMPT_FILENAME = "MIND-COHERENCE-INTAKE-PROMPT.md"
DEFAULT_SKILLS_DIRS = [".agents/skills", ".claude/skills", "skills"]  # auto-detect order


def repo_root():
    # this file is <root>/tools/vendor_into_repo.py
    return Path(__file__).resolve().parents[1]


def source_skills():
    src = repo_root() / "plugin" / "skills"
    return sorted(d for d in src.glob(SKILL_GLOB) if (d / "SKILL.md").is_file())


def parse_frontmatter(skill_md):
    """Minimal: pull name + description from the leading YAML frontmatter."""
    text = skill_md.read_text(encoding="utf-8")
    name = desc = ""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        fm = text[3:end] if end != -1 else ""
        for line in fm.splitlines():
            s = line.strip()
            if s.startswith("name:") and not name:
                name = s[len("name:"):].strip().strip('"').strip("'")
            elif s.startswith("description:") and not desc:
                desc = s[len("description:"):].strip().strip('"').strip("'")
    return name or skill_md.parent.name, desc


def detect_skills_dir(target, override):
    if override:
        return target / override
    for cand in DEFAULT_SKILLS_DIRS:
        if (target / cand).is_dir():
            return target / cand
    return target / DEFAULT_SKILLS_DIRS[0]  # default .agents/skills (created on --apply)


def build_prompt(skills_meta, rel_skills_dir):
    out = []
    out.append("# Intake request: Mind Coherence Suite skills")
    out.append("")
    out.append(
        f"I just added {len(skills_meta)} skills from the Mind Coherence Suite to this repo, under "
        f"`{rel_skills_dir}/`. They are epistemic-discipline skills for keeping a growing context + "
        "memory coherent (belief-vs-knowledge calibration with anti-facts, holding contradictions, "
        "internal + external audit, anti-sycophancy, and a one-time memory onboarding)."
    )
    out.append("")
    out.append(
        "Please INTAKE them into THIS repo's own skill-discovery system, using whatever convention this "
        "repo already uses (an `AGENTS.md` table, a generated `.agents/skills/INDEX.md`, a `.claude/skills` "
        "registry, required frontmatter, a discovery gate, etc.). Do it the way this repo already does it; "
        "do not invent a new scheme. After wiring them in, regenerate or validate the index and run the "
        "discovery gate if one exists."
    )
    out.append("")
    out.append("Skills added (name - description):")
    for name, desc in skills_meta:
        out.append(f"- **{name}** - {desc}")
    out.append("")
    out.append(
        f"Each skill is a folder under `{rel_skills_dir}/` containing a `SKILL.md` (Markdown + YAML "
        "frontmatter: name, description, version, metadata). Keep them ASCII-clean (no em-dash, curly "
        "quotes, or ellipsis)."
    )
    out.append("")
    out.append(
        "Once they are discoverable, a good first action is to run **mind-onboarding** to audit this "
        "repo's existing agent memory to a clean base state."
    )
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Vendor mind-* skills into a target repo + emit an intake prompt.")
    ap.add_argument("--target", required=True, help="target repo path")
    ap.add_argument("--skills-dir", help="skills dir under target (default: auto-detect .agents/skills | .claude/skills | skills)")
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry-run)")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    if "memory" in str(target).replace("\\", "/").lower():
        sys.exit("refusing: target path contains 'memory'")
    if not target.is_dir():
        sys.exit(f"target is not a directory: {target}")

    skills = source_skills()
    if not skills:
        sys.exit("no mind-* skills found under plugin/skills/")
    meta = [parse_frontmatter(d / "SKILL.md") for d in skills]

    dest_dir = detect_skills_dir(target, args.skills_dir)
    rel = dest_dir.relative_to(target).as_posix()
    mode = "APPLY" if args.apply else "DRY-RUN"

    print(f"[{mode}] vendor {len(skills)} skills -> {dest_dir}")
    for d in skills:
        print(f"  - {d.name}/  ->  {rel}/{d.name}/")
    print("NOTE: the target's index is intentionally NOT edited; the emitted prompt asks the repo's own AI to wire discoverability.")

    if args.apply:
        dest_dir.mkdir(parents=True, exist_ok=True)
        for d in skills:
            shutil.copytree(d, dest_dir / d.name, dirs_exist_ok=True)
        (target / PROMPT_FILENAME).write_text(build_prompt(meta, rel), encoding="utf-8")
        print(f"\nCopied {len(skills)} skills. Wrote intake prompt -> {target / PROMPT_FILENAME}")
        print("Paste that prompt into the AI agent that manages this repo to enable skill discoverability.")
    else:
        print(f"\n(dry-run) would copy the skills above and write the intake prompt -> {target / PROMPT_FILENAME}")
        print("\n----- INTAKE PROMPT PREVIEW -----")
        print(build_prompt(meta, rel), end="")
        print("----- END PREVIEW -----")
        print("Re-run with --apply to copy the skills and write the prompt file.")


if __name__ == "__main__":
    main()
