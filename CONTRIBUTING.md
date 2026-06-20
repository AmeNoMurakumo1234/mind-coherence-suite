# Contributing to Mind Coherence Suite

First, read [CHARTER.md](CHARTER.md). This is a **seed, not a standard** - uniform adoption is
an explicit anti-goal. Forking and diverging is encouraged; reconciled divergence is how the
suite improves.

## Layout
- `plugin/skills/mind-*/SKILL.md` - the skills (plain Markdown + YAML frontmatter: `name`,
  `description`, `version`, `metadata.tags`, `metadata.related_skills`).
- `plugin/.claude-plugin/plugin.json` - the plugin manifest.
  `.claude-plugin/marketplace.json` - the marketplace manifest.
- `plugin/CHANGELOG.md` - per-version changes.
- `tools/` - `validate_anti_facts.py` (lints the anti-fact format in a memory dir),
  `reflect_from_local.py` (curated upstreaming of skill edits from a working copy), and
  `vendor_into_repo.py` (install the skills INTO a repo that uses its own skill system + emit an
  intake prompt for that repo's AI; the inverse of `reflect_from_local.py`).

## The edit loop

Load your working copy so edits are live: from the clone, launch `claude --plugin-dir ./plugin`
(the `plugin/` subdir holds `.claude-plugin/plugin.json`). This **shadows** any globally-installed
copy for that session, so you can consume the published plugin and develop your fork at once, with
no conflict and no uninstall. After editing, run `/reload-plugins` (manual; there is no hot-reload)
and test via `/mind-<skill>`.

1. Edit a `SKILL.md` body (or add a new `mind-<name>/SKILL.md`).
2. Keep it **ASCII-clean.** No em-dash, en-dash, curly quotes, or ellipsis - these are the
   number-one "AI tell" and are rejected. Use `-`, `"`, and `...`.
3. Bump the skill's `version`, the plugin `version` (plugin.json + marketplace.json), and add a
   `CHANGELOG.md` entry.
4. Validate: `claude plugin validate ./plugin`. If you touched the anti-fact format, also run
   `python tools/validate_anti_facts.py <a-memory-dir>` against fixtures.

## Hard rule: memory stays private
NEVER commit memory CONTENT (anyone's actual beliefs, anti-facts, or notes). This repo ships
the memory-management SYSTEM and the FORMATS only. The `.gitignore` and `reflect_from_local.py`
guard this, and reviewers reject any change that adds a concrete memory ENTRY rather than the
FORMAT for one. See [MEMORY-SEPARATION.md](MEMORY-SEPARATION.md).

## If you fork and diverge
Record your lineage and divergences in [RECONCILIATION-LOG.md](RECONCILIATION-LOG.md).
Divergence is data: when two forks settle a question differently, that disagreement is the
input to the next reconciliation, not a defect.

## Contributing back
Open a PR that states the divergence and WHY (the reasoning is the contribution, not just the
diff). Changes are reconciled against the charter and the suite's own rules - including
anti-sycophancy: a well-argued disagreement is more useful than reflexive agreement.
