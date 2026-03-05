# Elle Best Practices

Last updated: 2026-03-05

## File Size Guidelines

| File | Max Lines | Rationale |
|------|-----------|-----------|
| elle-core.md | 150 | Token budget for always-loaded rules |
| Output style (elle.md) | 120 | Loaded on every session |
| Individual context files | 100 | Keeps loading fast |
| SKILL.md files | 500 | Progressive disclosure limit |

## Hook Design

- Hooks should be **non-blocking** -- never use `"decision": "block"`
- SessionStart hooks should complete in < 2 seconds
- Always consume stdin even if unused (prevents pipe errors)
- Exit with code 0 for Claude to see stdout
- Use `additionalContext` for injecting content, not `reason`

## Context Management

- **Rules are verbatim** -- never summarize corrections
- **Preferences replace** -- new preference overwrites old
- **Triggers expire** -- clean up past dates
- **Session is ephemeral** -- clear on major context switch
- **Journal appends at top** -- newest first

## Notification Dedup

- Check `~/.claude/settings.json` before adding notification hooks
- Plugin hooks.json and settings.json can both register hooks
- Duplicate sounds are annoying -- dedup during setup

## Version Management

- Always bump version in plugin.json when making changes
- Use semver: major for breaking changes, minor for features, patch for fixes
