"""Tests for session_start.py -- SessionStart (startup) hook."""
import json
import sys
import textwrap
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

HOOKS_DIR = Path(__file__).resolve().parents[2] / "personal-assistant" / "hooks"
sys.path.insert(0, str(HOOKS_DIR))


class TestParseTriggers:
    def test_finds_upcoming_events(self, tmp_context):
        from session_start import parse_upcoming_triggers
        future_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        triggers_content = textwrap.dedent(f"""\
            ---
            name: Triggers
            ---
            ## Upcoming

            | Date | Event | Action |
            |------|-------|--------|
            | {future_date} | Client demo | Prepare slides |
        """)
        triggers_path = tmp_context / "core" / "triggers.md"
        triggers_path.write_text(triggers_content)
        result = parse_upcoming_triggers(triggers_path, lookahead_days=7)
        assert len(result) == 1
        assert "Client demo" in result[0]

    def test_ignores_past_events(self, tmp_context):
        from session_start import parse_upcoming_triggers
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        triggers_content = textwrap.dedent(f"""\
            ---
            name: Triggers
            ---
            ## Upcoming

            | Date | Event | Action |
            |------|-------|--------|
            | {past_date} | Old event | Was done |
        """)
        triggers_path = tmp_context / "core" / "triggers.md"
        triggers_path.write_text(triggers_content)
        result = parse_upcoming_triggers(triggers_path, lookahead_days=7)
        assert len(result) == 0

    def test_ignores_far_future_events(self, tmp_context):
        from session_start import parse_upcoming_triggers
        far_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        triggers_content = textwrap.dedent(f"""\
            ---
            name: Triggers
            ---
            ## Upcoming

            | Date | Event | Action |
            |------|-------|--------|
            | {far_date} | Far event | Not yet |
        """)
        triggers_path = tmp_context / "core" / "triggers.md"
        triggers_path.write_text(triggers_content)
        result = parse_upcoming_triggers(triggers_path, lookahead_days=7)
        assert len(result) == 0

    def test_handles_missing_triggers_file(self, tmp_path):
        from session_start import parse_upcoming_triggers
        result = parse_upcoming_triggers(tmp_path / "nonexistent.md")
        assert result == []

    def test_handles_malformed_dates(self, tmp_context):
        from session_start import parse_upcoming_triggers
        triggers_content = textwrap.dedent("""\
            ---
            name: Triggers
            ---
            ## Upcoming

            | Date | Event | Action |
            |------|-------|--------|
            | not-a-date | Bad event | Nothing |
        """)
        triggers_path = tmp_context / "core" / "triggers.md"
        triggers_path.write_text(triggers_content)
        result = parse_upcoming_triggers(triggers_path, lookahead_days=7)
        assert len(result) == 0


class TestBootstrapElleCoreIfMissing:
    def test_generates_elle_core_if_missing(self, tmp_context, tmp_rules_dir):
        from session_start import bootstrap_elle_core_if_missing
        output_path = tmp_rules_dir / "elle-core.md"
        result = bootstrap_elle_core_if_missing(tmp_context, output_path)
        assert result is True
        assert output_path.exists()

    def test_skips_if_already_exists(self, tmp_context, tmp_rules_dir):
        from session_start import bootstrap_elle_core_if_missing
        output_path = tmp_rules_dir / "elle-core.md"
        output_path.write_text("existing content")
        result = bootstrap_elle_core_if_missing(tmp_context, output_path)
        assert result is False
        assert output_path.read_text() == "existing content"


class TestMainOutput:
    def test_outputs_valid_json(self, tmp_context, tmp_rules_dir, capsys):
        from session_start import run_hook
        output_path = tmp_rules_dir / "elle-core.md"
        future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        triggers_content = textwrap.dedent(f"""\
            ---
            name: Triggers
            ---
            ## Upcoming

            | Date | Event | Action |
            |------|-------|--------|
            | {future_date} | Big meeting | Prepare |
        """)
        (tmp_context / "core" / "triggers.md").write_text(triggers_content)
        with patch("session_start.CONTEXT_DIR", tmp_context), \
             patch("session_start.ELLE_CORE_PATH", output_path):
            run_hook()
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "hookSpecificOutput" in output
        assert "additionalContext" in output["hookSpecificOutput"]
        assert "Big meeting" in output["hookSpecificOutput"]["additionalContext"]

    def test_silent_when_nothing_upcoming(self, tmp_context, tmp_rules_dir, capsys):
        from session_start import run_hook
        output_path = tmp_rules_dir / "elle-core.md"
        output_path.write_text("existing")
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        (tmp_context / "core" / "triggers.md").write_text(textwrap.dedent(f"""\
            ---
            name: Triggers
            ---
            ## Upcoming

            | Date | Event | Action |
            |------|-------|--------|
            | {past_date} | Old event | Done |
        """))
        with patch("session_start.CONTEXT_DIR", tmp_context), \
             patch("session_start.ELLE_CORE_PATH", output_path):
            run_hook()
        captured = capsys.readouterr()
        if captured.out.strip():
            output = json.loads(captured.out)
            ctx = output.get("hookSpecificOutput", {}).get("additionalContext", "")
            assert ctx == "" or "upcoming" not in ctx.lower()

    def test_outputs_setup_instructions_if_no_context(self, tmp_path, capsys):
        from session_start import run_hook
        with patch("session_start.CONTEXT_DIR", tmp_path / "nonexistent"), \
             patch("session_start.ELLE_CORE_PATH", tmp_path / "rules" / "elle-core.md"):
            run_hook()
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        ctx = output["hookSpecificOutput"]["additionalContext"]
        assert "setup" in ctx.lower() or "not set up" in ctx.lower()
