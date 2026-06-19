# Working Agreement: Memory Stays Private

This is the plugin's working agreement with every consumer. **By installing, forking, or
otherwise using the Mind Coherence Suite, you agree to operate it as a memory-management
*system* and never to commit memory *content* to this repo or to any shared fork of it.**

The suite is a *system for managing memory*. It is not, and must never become, a store of
any agent's memory **content**.

## The agreement

- **Ships / may be shared:** the skills (the method), the formats, and the tooling,
  including the anti-fact *format* (how to represent a believed-false item).
- **Never ships / never shared:** actual memory *entries*, an agent's specific beliefs,
  anti-facts, provenance, or private notes. Those belong to each agent and live outside
  this repo (for a Claude Code agent, in its own `~/.claude` memory directory).

## Why

Memories are personal and frequently sensitive; this plugin is public and shared. Mixing
them would leak private content, and it would also violate the suite's own ethos: your
beliefs are yours to audit and diverge; only the *method* is shared.

## Enforcement (defense-in-depth)

- `.gitignore` refuses `memory/`, `*.memory.md`, and `MEMORY.md`.
- `tools/reflect_from_local.py` copies **only** `mind-*` skill files and refuses any
  source path containing `memory`.
- Reviewer rule: reject any change (or fork PR) that adds a concrete belief or anti-fact
  *entry* rather than the *format* for one.

The anti-fact feature is the clearest illustration: the *format* (the `stance`,
`correction`, `retained_because` fields, the truth-forward conventions) ships here; the
*specific things an agent believes are false* stay private, forever.
