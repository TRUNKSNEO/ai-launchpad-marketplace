# Claude Code Platform Capabilities

Last updated: 2026-03-05

## Hook Lifecycle Events

| Event | When | Elle Uses? | Notes |
|-------|------|-----------|-------|
| SessionStart (startup) | New session | Yes | Trigger check + bootstrap |
| SessionStart (compact) | After compaction | Yes | Context restoration |
| UserPromptSubmit | Every user message | No (removed in v2) | Was v1 delivery mechanism |
| PreToolUse | Before tool execution | No | Could gate dangerous tools |
| PostToolUse | After tool execution | No | Could log tool usage |
| PermissionRequest | Permission prompt shown | No | Could auto-approve safe tools |
| Stop | Claude finishes response | Yes (sound only) | v1 had blocked context update (removed) |
| Notification | Various notifications | Yes (sound) | permission_prompt, idle_prompt |
| PreCompact | Before compaction | No | Could save session state |
| SessionEnd | Session ends | No | Could trigger final context update |
| SubagentStart/Stop | Subagent lifecycle | No | Could monitor subagent work |
| InstructionsLoaded | Rules/instructions loaded | No | Could verify elle-core.md |

## Rules System

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| ~/.claude/rules/ directory | Yes | elle-core.md lives here |
| Project-level .claude/rules/ | No | Could add project-specific Elle behavior |
| Rule file auto-loading | Yes | Core delivery mechanism |
| Survives compaction | Yes | Key advantage over hooks |

## Skill Features

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| user-invocable | Yes | All Elle skills |
| disable-model-invocation | Yes | sync-context, context-health |
| allowed-tools | No | Could restrict tool access per skill |
| context: fork | No | Could isolate skill execution |
| agent mode | No | Could enable multi-turn skill execution |
| hooks (skill-level) | No | Could add per-skill hooks |

## Auto Memory

| Feature | Elle Uses? | Notes |
|---------|-----------|-------|
| MEMORY.md per project | Boundary defined | Project-specific only |
| Separation from Elle context | Yes | Clear boundary in output style |
