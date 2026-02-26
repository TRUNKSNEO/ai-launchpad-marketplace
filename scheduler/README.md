# Scheduler Plugin

Schedule automated Claude Code tasks across macOS, Linux, and Windows. Manage recurring execution of marketplace skills, freeform prompts, and shell scripts with safety controls and desktop notifications.

## Platform Support

| Platform | Scheduler Backend | Artifacts |
|----------|-------------------|-----------|
| macOS | launchd | `~/Library/LaunchAgents/com.ailaunchpad.scheduler.{id}.plist` |
| Linux | systemd user timers | `~/.config/systemd/user/ailaunchpad-scheduler-{id}.{service,timer}` |
| Windows | Task Scheduler | `schtasks.exe` with XML import (`\AILaunchpad\Scheduler\{id}`) |

The platform is auto-detected at runtime. Each task records which platform it was created on.

## Skills

### manage

Conversational orchestrator for scheduling tasks. Invoke via `/schedule`.

**Operations:**
- Add a new scheduled task (skill, prompt, or script)
- List all scheduled tasks
- Pause/resume a task
- Remove a task
- View results from a task
- View logs for a task
- Run a task now (test)

## How It Works

1. Tasks are defined in a JSON registry at `<project>/.claude/scheduler/registry.json`
2. Each task gets a wrapper script at `<scheduler_dir>/wrappers/{id}.sh` (or `.ps1` on Windows)
3. Each task gets a platform-native schedule artifact (plist, systemd units, or Task Scheduler entry)
4. The platform scheduler fires the wrapper at the scheduled time
5. The wrapper runs `claude -p` (for skills/prompts) or `bash`/PowerShell (for scripts)
6. Results saved to `<scheduler_dir>/results/YYYY-MM-DD/{id}-HHMMSS.md`
7. Desktop notification on completion or failure

## Architecture

```
scheduler/skills/manage/scripts/
  scheduler.py              # Core engine (delegates to platform backend)
  platform_detect.py        # Auto-detects OS and returns appropriate backend
  backends/
    base.py                 # PlatformBackend ABC
    macos.py                # launchd plist + launchctl
    linux.py                # systemd .service + .timer units
    windows.py              # Task Scheduler XML + schtasks.exe
```

## Requirements

- macOS, Linux, or Windows
- Claude Code CLI (`claude` in PATH)
- `uv` for running the Python engine
