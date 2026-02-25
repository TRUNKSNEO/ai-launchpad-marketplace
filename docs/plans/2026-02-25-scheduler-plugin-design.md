# Scheduler Plugin Design

## Overview

A `scheduler` plugin for the AI Launchpad Marketplace that manages launchd-based scheduled tasks through conversational Claude Code interaction. Enables scheduling of skill invocations, freeform prompts, and shell scripts with macOS-native reliability.

## Architecture

Single orchestrator skill (`scheduler:manage`) backed by a Python engine (`scheduler.py`) that generates and manages launchd plists, wrapper scripts, and a task registry.

## Plugin Structure

```
scheduler/
├── .claude-plugin/
│   └── plugin.json                    # v1.0.0
├── README.md
└── skills/
    └── manage/
        ├── SKILL.md                   # Orchestrator skill
        ├── scripts/
        │   └── scheduler.py           # Core engine (PEP 723, uv run)
        └── references/
            └── wrapper-template.sh    # Template for generated wrapper scripts
```

### Generated Files (Runtime)

```
~/.claude/scheduler/
├── registry.json                      # All task definitions
├── wrappers/                          # Generated shell scripts per task
│   ├── note-ideas.sh
│   └── yt-comments.sh
├── results/                           # Task output (markdown)
│   └── 2026-02-25/
│       └── note-ideas.md
└── logs/                              # Execution logs
    └── 2026-02-25-note-ideas.log

~/Library/LaunchAgents/
├── com.ailaunchpad.scheduler.note-ideas.plist
└── com.ailaunchpad.scheduler.yt-comments.plist
```

## Task Registry Schema

```json
{
  "version": 1,
  "tasks": {
    "note-ideas": {
      "id": "note-ideas",
      "name": "Generate Substack note ideas",
      "type": "skill",
      "target": "substack:generate-note-ideas",
      "working_directory": "/Users/kennethliao/projects/ai-launchpad-marketplace",
      "schedule": {
        "cron": "0 8 * * 1",
        "human": "Every Monday at 8:00 AM"
      },
      "safety": {
        "max_turns": 20,
        "timeout_minutes": 15
      },
      "status": "active",
      "created_at": "2026-02-25T10:00:00-08:00",
      "last_run": {
        "timestamp": "2026-02-24T08:00:12-08:00",
        "exit_code": 0,
        "duration_seconds": 94,
        "result_file": "~/.claude/scheduler/results/2026-02-24/note-ideas.md"
      }
    }
  }
}
```

### Task Types

| Type | `target` field | Execution |
|------|---------------|-----------|
| `skill` | `"substack:generate-note-ideas"` | `claude -p "/generate-note-ideas"` |
| `prompt` | `"Pull comments and summarize..."` | `claude -p "the prompt text"` |
| `script` | `"/path/to/script.sh"` | `bash /path/to/script.sh` |

### Status Values

- `active` — launchd plist loaded and running
- `paused` — plist unloaded via `launchctl bootout`
- `error` — last run failed, still scheduled

## Python Engine (`scheduler.py`)

PEP 723 script with single dependency: `croniter>=2.0.0`.

### Commands

```bash
# CRUD
uv run scheduler.py add --id ID --name NAME --type TYPE --target TARGET \
  --cron EXPR --max-turns N --timeout M --workdir DIR
uv run scheduler.py list
uv run scheduler.py get --id ID
uv run scheduler.py remove --id ID

# Lifecycle
uv run scheduler.py pause --id ID
uv run scheduler.py resume --id ID
uv run scheduler.py run --id ID

# Observability
uv run scheduler.py logs --id ID
uv run scheduler.py results --id ID [--all]

# Maintenance
uv run scheduler.py update-last-run --id ID --exit-code N --duration S --result-file PATH
uv run scheduler.py repair
```

### `add` Flow

1. Validate inputs (cron via croniter, unique ID, script exists)
2. Write task to `registry.json`
3. Generate wrapper script from template → `~/.claude/scheduler/wrappers/{id}.sh`
4. Generate launchd plist → `~/Library/LaunchAgents/com.ailaunchpad.scheduler.{id}.plist`
5. Load plist via `launchctl bootstrap gui/{uid} {plist_path}`

### `remove` Flow

1. Unload plist via `launchctl bootout`
2. Delete plist file and wrapper script
3. Remove from `registry.json`
4. Keep results and logs (don't delete history)

## Wrapper Script Template

```bash
#!/bin/bash
set -euo pipefail

TASK_ID="{id}"
TASK_TYPE="{type}"
TASK_TARGET="{target}"
MAX_TURNS={max_turns}
TIMEOUT_MINUTES={timeout_minutes}
WORKDIR="{working_directory}"

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

# Optional: load API key if available (not required for subscription auth)
API_KEY="$(security find-generic-password -s 'anthropic-api-key' -w 2>/dev/null || echo '')"
if [ -n "$API_KEY" ]; then
  export ANTHROPIC_API_KEY="$API_KEY"
fi

DATE=$(date '+%Y-%m-%d')
RESULT_DIR="$HOME/.claude/scheduler/results/$DATE"
LOG_FILE="$HOME/.claude/scheduler/logs/$DATE-$TASK_ID.log"
RESULT_FILE="$RESULT_DIR/$TASK_ID.md"
mkdir -p "$RESULT_DIR" "$(dirname "$LOG_FILE")"

START_TIME=$(date +%s)
echo "=== $TASK_ID started at $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

cd "$WORKDIR"

case "$TASK_TYPE" in
  skill)
    timeout "${TIMEOUT_MINUTES}m" claude -p "/$TASK_TARGET" \
      --max-turns "$MAX_TURNS" --output-format text \
      > "$RESULT_FILE" 2>> "$LOG_FILE"
    ;;
  prompt)
    timeout "${TIMEOUT_MINUTES}m" claude -p "$TASK_TARGET" \
      --max-turns "$MAX_TURNS" --output-format text \
      > "$RESULT_FILE" 2>> "$LOG_FILE"
    ;;
  script)
    timeout "${TIMEOUT_MINUTES}m" bash "$TASK_TARGET" \
      > "$RESULT_FILE" 2>> "$LOG_FILE"
    ;;
esac

EXIT_CODE=$?
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "=== Completed: exit=$EXIT_CODE duration=${DURATION}s ===" >> "$LOG_FILE"

if [ $EXIT_CODE -eq 0 ]; then
  osascript -e "display notification \"Completed in ${DURATION}s\" with title \"Scheduler: $TASK_ID\" sound name \"Glass\""
else
  osascript -e "display notification \"Failed (exit $EXIT_CODE)\" with title \"Scheduler: $TASK_ID\" sound name \"Basso\""
fi
```

## SKILL.md Interaction Flow

Invoked via `/schedule`. Conversational orchestrator that presents options:

1. Add a new scheduled task
2. List all scheduled tasks
3. Pause/resume a task
4. Remove a task
5. View results from a task
6. View logs for a task
7. Run a task now (test)

### Add Flow

- Asks for name, type, target, schedule (natural language → cron), safety limits
- Confirms summary table before creating
- Auto-generates slug ID from name

### First-Time Setup

- Checks `claude -p "hello" --max-turns 1` succeeds (any auth method)
- Creates `~/.claude/scheduler/` directory structure

## Notifications

- Success: macOS notification with "Glass" sound
- Failure: macOS notification with "Basso" sound
- Via `osascript -e 'display notification ...'`

## Error Handling

- **Invalid cron**: Validated by croniter before writing
- **Duplicate IDs**: Rejected with suggestion
- **Missing plist**: Detected by `list`, repaired by `repair`
- **Auth failure**: Wrapper script lets claude CLI handle auth; fails with notification
- **Claude not in PATH**: Wrapper checks `command -v claude` first
- **Laptop asleep**: launchd catches up one run on wake (coalesces missed intervals)
- **Already loaded/unloaded**: Caught and reported gracefully

## Future Enhancements (Not in v1.0)

- Log rotation (`cleanup --older-than 30d`)
- Slack/email notifications
- Linux systemd support (cross-platform)
- MCP server layer for conversational management
- Cost tracking per task
