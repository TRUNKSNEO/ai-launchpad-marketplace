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

# Abbreviated month names for the approximate date parser
_MONTH_ABBREVS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def parse_date_flexible(date_str: str) -> "date | None":
    """Parse a date string in various human-readable formats.

    Supported formats:
    - ISO: 2026-03-29
    - Month Day, Year: Dec 19, 2025 / Mar 29, 2026
    - Month Day (no year): Mar 29 (assumes current year)
    - Day-of-week prefix: Sat Feb 28, 2026
    - Bold markdown: **Jan 31, 2026**
    - Approximate: ~Feb-Mar 2026 (uses first month, day 1)

    Returns a date object or None if unparseable.
    """
    from datetime import date as date_type

    if not date_str or not date_str.strip():
        return None

    s = date_str.strip()

    # Strip markdown bold
    s = s.replace("**", "")

    # Strip emoji and status prefixes
    s = re.sub(r"^[^\w~*]+", "", s).strip()

    # Strip leading ~ for approximate dates
    is_approximate = s.startswith("~")
    if is_approximate:
        s = s[1:].strip()

    # Handle approximate range: "Feb-Mar 2026" -> use first month, day 1
    approx_match = re.match(r"([A-Za-z]{3})-[A-Za-z]{3}\s+(\d{4})", s)
    if approx_match:
        month_str = approx_match.group(1).lower()
        year = int(approx_match.group(2))
        month = _MONTH_ABBREVS.get(month_str)
        if month:
            try:
                return date_type(year, month, 1)
            except ValueError:
                return None
        return None

    # Strip day-of-week prefix: "Sat Feb 28, 2026" -> "Feb 28, 2026"
    # Only strip when followed by another alpha word (the month name)
    s = re.sub(r"^[A-Z][a-z]{2}\s+(?=[A-Z][a-z])", "", s)

    # Try ISO format: YYYY-MM-DD
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        pass

    # Try Month Day, Year: "Dec 19, 2025"
    try:
        return datetime.strptime(s, "%b %d, %Y").date()
    except ValueError:
        pass

    # Try Month Day (no year): "Mar 29" -> assume current year
    try:
        parsed = datetime.strptime(s, "%b %d").date()
        return parsed.replace(year=datetime.now().year)
    except ValueError:
        pass

    return None


def parse_upcoming_triggers(triggers_path: Path, lookahead_days: int = LOOKAHEAD_DAYS) -> list[str]:
    """Parse triggers.md and return events within lookahead_days from today."""
    if not triggers_path.exists():
        return []

    content = triggers_path.read_text(encoding="utf-8", errors="replace")
    today = datetime.now().date()
    cutoff = today + timedelta(days=lookahead_days)

    upcoming = []
    for line in content.split("\n"):
        stripped = line.strip()
        # Must be a table row
        if not stripped.startswith("|"):
            continue
        # Skip separator rows (|---|---|)
        if re.match(r"^\|[\s\-|]+\|$", stripped):
            continue

        cells = [c.strip() for c in stripped.split("|") if c.strip()]
        if len(cells) < 2:
            continue

        date_cell = cells[0]
        rest_cells = cells[1:]

        # Skip rows marked as completed
        row_text = " ".join(rest_cells)
        if any(marker in row_text for marker in ("✅", "❌")):
            continue
        if any(marker in date_cell for marker in ("✅", "❌")):
            continue

        event_date = parse_date_flexible(date_cell)
        if event_date is None:
            continue

        if today <= event_date <= cutoff:
            event_name = rest_cells[0] if rest_cells else "Unknown"
            days_away = (event_date - today).days
            if days_away == 0:
                timing = "today"
            elif days_away == 1:
                timing = "tomorrow"
            else:
                timing = f"in {days_away} days ({event_date.strftime('%a %b %d')})"
            upcoming.append(f"- {event_name} -- {timing}")

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
