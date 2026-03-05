---
name: evolve
description: Audit Elle's architecture against current Claude Code capabilities and best practices. Use after Claude Code updates, when exploring new features, or periodically to ensure Elle is optimally using the platform. Also use when the user says "let's modernize Elle" or "what Claude Code features are we missing".
user-invocable: true
---

# Evolve -- System Architecture Audit

Audit Elle's architecture against current Claude Code capabilities and recommend improvements.

## Audit Steps

### 1. Platform Capabilities Audit

Read `${CLAUDE_SKILL_DIR}/references/platform-capabilities.md` for the known capability list.

Then check the latest Claude Code documentation and changelog for any new features:
- Search for recent Claude Code updates
- Check if any new hook events, rules features, or skill patterns are available
- Compare against what Elle currently uses

Report:
- Features Elle uses well
- Features available but not used (opportunities)
- Features Elle uses in deprecated ways (risks)

### 2. Plugin Version Check

Compare installed version vs marketplace source:

```bash
cat ~/.claude/plugins/marketplaces/ai-launchpad/personal-assistant/.claude-plugin/plugin.json
```

Report if the installed version is behind the source.

### 3. Architecture Health

Check the deployed system:

```bash
ls -la ~/.claude/rules/elle-core.md
ls -la ~/.claude/.context/core/
cat ~/.claude/settings.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('hooks',{}), indent=2))"
```

Verify:
- SessionStart hooks are registered (not UserPromptSubmit)
- elle-core.md exists in rules/
- No duplicate notification hooks between plugin and settings.json
- Output style is set correctly

### 4. Best Practices Review

Read `${CLAUDE_SKILL_DIR}/references/best-practices.md` for current guidelines.

Check:
- File sizes (rules < 200 lines, elle-core.md < 150 lines)
- Hook scripts are non-blocking (no `"decision": "block"`)
- Skills use appropriate frontmatter fields
- Context files follow XML tag conventions

### 5. Recommendations

Present a prioritized improvement list:

| Priority | Area | Current State | Recommendation | Effort |
|----------|------|---------------|----------------|--------|
| High | ... | ... | ... | ... |
| Medium | ... | ... | ... | ... |
| Low | ... | ... | ... | ... |

For each recommendation, provide:
- What to change
- Why it matters
- How to implement (specific commands or file edits)
- Whether it can be done now or needs a design session
