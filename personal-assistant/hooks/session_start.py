#!/usr/bin/env python3
"""
SessionStart hook (matcher: startup) for Elle Personal Assistant v2.

Fires once when a new Claude Code session starts. Responsibilities:
1. Check if context system exists -- output setup instructions if not
2. Bootstrap elle-core.md if missing (first run after upgrade)
3. Check triggers.md for events within 7 days -- output as additionalContext
4. If nothing upcoming, output nothing (silent)
"""
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

CONTEXT_DIR = Path.home() / ".claude" / ".context"
ELLE_CORE_PATH = Path.home() / ".claude" / "rules" / "elle-core.md"
LOOKAHEAD_DAYS = 7


def parse_upcoming_triggers(triggers_path: Path, lookahead_days: int = LOOKAHEAD_DAYS) -> list[str]:
    """Parse triggers.md and return events within lookahead_days from today."""
    if not triggers_path.exists():
        return []

    content = triggers_path.read_text(encoding="utf-8", errors="replace")
    today = datetime.now().date()
    cutoff = today + timedelta(days=lookahead_days)

    upcoming = []
    for line in content.split("\n"):
        match = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.+)\|", line)
        if match:
            try:
                event_date = datetime.strptime(match.group(1), "%Y-%m-%d").date()
                if today <= event_date <= cutoff:
                    rest = match.group(2).strip().rstrip("|")
                    cells = [c.strip() for c in rest.split("|")]
                    event_name = cells[0] if cells else "Unknown"
                    days_away = (event_date - today).days
                    if days_away == 0:
                        timing = "today"
                    elif days_away == 1:
                        timing = "tomorrow"
                    else:
                        timing = f"in {days_away} days ({event_date.strftime('%a %b %d')})"
                    upcoming.append(f"- {event_name} -- {timing}")
            except ValueError:
                continue

    return upcoming


def bootstrap_elle_core_if_missing(context_dir: Path, elle_core_path: Path) -> bool:
    """Generate elle-core.md if it doesn't exist yet. Returns True if generated."""
    if elle_core_path.exists():
        return False

    try:
        scripts_dir = Path(__file__).resolve().parent.parent / "skills" / "sync-context" / "scripts"
        sys.path.insert(0, str(scripts_dir))
        from sync_context import generate_and_write_elle_core
        generate_and_write_elle_core(context_dir, elle_core_path)
        return True
    except ImportError:
        elle_core_path.parent.mkdir(parents=True, exist_ok=True)
        elle_core_path.write_text(
            "# Elle -- Personal Assistant Context\n\n"
            "You are Elle, a personal assistant. Run /sync-context to populate this file.\n\n"
            "## Loading Full Context\n"
            "For substantive tasks, read ~/.claude/.context/core/:\n"
            "- identity.md, preferences.md, workflows.md\n"
            "- relationships.md, triggers.md\n"
            "- projects.md, rules.md\n"
            "- session.md (when resuming work)\n"
            "- improvements.md (check for pending proposals)\n"
        )
        return True


def run_hook() -> None:
    """Main hook logic -- called after consuming stdin."""
    context_parts = []

    if not CONTEXT_DIR.exists():
        context_parts.append(
            "# Personal Assistant Not Set Up\n\n"
            "The user has installed the personal assistant plugin but hasn't set it up yet.\n"
            "Ask if they'd like to run `/personal-assistant:setup` to initialize."
        )
    else:
        bootstrapped = bootstrap_elle_core_if_missing(CONTEXT_DIR, ELLE_CORE_PATH)
        if bootstrapped:
            context_parts.append(
                "Note: elle-core.md was auto-generated for the first time. "
                "Run /sync-context to regenerate after making context changes."
            )

        triggers_path = CONTEXT_DIR / "core" / "triggers.md"
        upcoming = parse_upcoming_triggers(triggers_path)
        if upcoming:
            context_parts.append(
                "## Upcoming Events (next 7 days)\n" + "\n".join(upcoming)
            )

    additional_context = "\n\n".join(context_parts)
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context,
        }
    }
    print(json.dumps(output))


def main() -> None:
    """Entry point -- consume stdin then run hook logic."""
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        pass

    run_hook()
    sys.exit(0)


if __name__ == "__main__":
    main()
