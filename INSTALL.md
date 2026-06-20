# Installing and using Mind Coherence Suite

This repo is both a Claude Code marketplace and the `mind-coherence` plugin it hosts.
Source of truth: `https://github.com/AmeNoMurakumo1234/mind-coherence-suite`.

## TL;DR
1. Add the marketplace `AmeNoMurakumo1234/mind-coherence-suite`.
2. Install the `mind-coherence` plugin.
3. Skills invoke as `/mind-coherence:mind-<skill>` (start with `/mind-coherence:mind-onboarding`
   on any pre-existing memory). Plugin skills are always namespaced by the plugin name.
4. Mind the **scope** (account-global vs per-repo) and the **duplication gotcha** below.

## Quick start (from scratch, terminal CLI)
If you do not already have the Claude Code CLI:
1. **Install it** (Node.js 18+): `npm install -g @anthropic-ai/claude-code` (or the native
   installer / Homebrew / WinGet; see the official [setup guide](https://code.claude.com/docs/en/setup)).
2. **Start it and log in:** run `claude`; on first use it opens your browser to authenticate your
   Claude account (Pro / Max / Team / Enterprise or Console) and walks you through a few setup
   prompts. Full first-run walkthrough: the official [quickstart](https://code.claude.com/docs/en/quickstart).
3. **Add this marketplace + install the plugin** (inside the `claude` session):
   ```
   /plugin marketplace add AmeNoMurakumo1234/mind-coherence-suite
   /plugin install mind-coherence@mind-coherence-suite
   ```
   To skip the TUI, run them from your shell instead:
   `claude plugin marketplace add AmeNoMurakumo1234/mind-coherence-suite` then
   `claude plugin install mind-coherence@mind-coherence-suite`.

Already set up? Skip to step 3.

## Pick your surface

**Desktop app.** The Customize > Plugins GUI is **curated-only**: it installs from the official
marketplace and CANNOT add a third-party one like this. On desktop, use either:
- the **standalone Claude Code CLI** (Quick start above), since the desktop app has no built-in
  terminal, or
- a committed **`.claude/settings.json` pin** (see "Pin it in a repo").

There is no `/plugin` slash command in the desktop app; it is a CLI surface. Desktop installs default to account /
global scope, and the desktop app keeps plugin state in an app-data location (not the CLI's
`~/.claude/plugins/`, which stays empty).

**Terminal CLI.**
```
/plugin marketplace add AmeNoMurakumo1234/mind-coherence-suite
/plugin install mind-coherence@mind-coherence-suite        # add --scope user|project|local
```
Non-interactive (scriptable):
```
claude plugin marketplace add AmeNoMurakumo1234/mind-coherence-suite
claude plugin install mind-coherence@mind-coherence-suite --scope project
```

**Pin it in a repo (declarative).** Commit a `.claude/settings.json` to the repo:
```json
{
  "extraKnownMarketplaces": {
    "mind-coherence-suite": { "source": { "source": "github", "repo": "AmeNoMurakumo1234/mind-coherence-suite" } }
  },
  "enabledPlugins": { "mind-coherence@mind-coherence-suite": true }
}
```
Anyone who opens and trusts that repo is prompted to install and enable it. (A local
filesystem path can be used as the marketplace source for local development.)

## Scope: where the plugin is active
| Scope | Active where | Stored |
|---|---|---|
| **user** (default) | ALL your projects | `~/.claude/` (account) |
| **project** | that repo, for everyone (committed) | `.claude/settings.json` |
| **local** | that repo, for you only | `.claude/settings.local.json` (gitignore it) |

To limit the plugin to one repo, install at **project** or **local** scope. The desktop app
installs at account scope by default; if its dialog offers a scope choice, use it.

## The duplication gotcha (read this)
Installing the plugin is **purely additive** (each skill is its own `/mind-coherence:mind-<skill>` command): it
never hides, disables, or reorders your existing skills. The only failure mode is **double-listing**,
never skill loss.

If a repo ALREADY carries these skills another way - for example it vendored the `mind-*`
skill bodies into its own skills directory with its own index/gate - do NOT also enable the
plugin account-wide for that repo. You will get each skill twice (once as
`/mind-coherence:mind-*` from the plugin, once from the repo's own loader). **Choose one
mechanism per repo:** the plugin, or vendored copies, not both.

## Updating to a new version
This is a third-party marketplace, so **auto-update is OFF by default** (only Anthropic's official
marketplace auto-updates). When a new version ships, pull it manually:
1. Refresh the marketplace listing: `/plugin marketplace update mind-coherence-suite`.
2. Update the plugin: press **Update** on it in Customize > Plugins (or `/plugin` -> Installed),
   then `/reload-plugins` to apply it in the current session.
3. Confirm with `claude plugin list` (the version should now read the new number).

To get future versions automatically, enable auto-update for this marketplace: `/plugin` ->
**Marketplaces** -> select `mind-coherence-suite` -> **Enable auto-update**. New versions then
install at startup and prompt you to `/reload-plugins`.

The plugin sets an explicit `version`, so consumers only receive an update when that field is
bumped (not on every commit).

## Uninstall / disable (it is reversible)
- Desktop: Customize > Plugins can toggle/uninstall plugins it manages, but adding or removing a CUSTOM marketplace is a terminal op (`/plugin marketplace remove ...`, or remove the `extraKnownMarketplaces` key).
- CLI: `/plugin`, then Installed, then disable/uninstall (or remove the `enabledPlugins` key).
- An account-level uninstall removes it from every project at once.

## Other harnesses (not Claude Code)
The portable core is the skill CONTENT, not the manifest. Each `SKILL.md` is plain Markdown
with simple YAML frontmatter; copy the `plugin/skills/` bodies into any harness that ingests
skill files or system-prompt fragments, and re-wrap the manifest for that harness. See the
README "Porting" section.

## Vendor into a repo that uses its own skill system
Some repos load skills from a directory (e.g. `.agents/skills/` with their own index or gate)
rather than via the Claude Code plugin manager. For those, vendor the skills in and let the
repo's OWN AI wire discoverability (the script never edits a foreign repo's index):
```
python tools/vendor_into_repo.py --target /path/to/repo          # dry-run: preview + the prompt
python tools/vendor_into_repo.py --target /path/to/repo --apply  # copy skills + write the prompt file
```
It copies `plugin/skills/mind-*` into the target's skills dir (auto-detected, or `--skills-dir`)
and writes `MIND-COHERENCE-INTAKE-PROMPT.md` for you to paste into the repo's AI agent, which then
intakes the skills using that repo's own convention. The inverse, `reflect_from_local.py`, curates
a repo's skill edits back upstream for a PR.

## Your memory stays yours
This plugin manages the memory SYSTEM; it never collects or ships your memory CONTENT. Your
beliefs, anti-facts, and notes stay private and local. See `MEMORY-SEPARATION.md`.
