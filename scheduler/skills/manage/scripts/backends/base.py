"""Abstract base class for platform-specific scheduler backends."""

from __future__ import annotations

import abc
from pathlib import Path


class PlatformBackend(abc.ABC):
    """Interface for platform-specific scheduling operations.

    Each platform (macOS, Linux, Windows) implements this interface to
    handle schedule installation, wrapper generation, and scheduler
    interaction using native OS facilities.
    """

    # --- Required methods ---

    @abc.abstractmethod
    def install_schedule(
        self,
        task_id: str,
        task: dict,
        wrapper_path: Path,
        scheduler_dir: Path,
        logs_dir: Path,
    ) -> None:
        """Create schedule artifacts and register with the platform scheduler.

        For macOS: generates a plist and loads it via launchctl.
        For Linux: generates systemd .service + .timer units and enables them.
        For Windows: generates XML and imports via schtasks.
        """

    @abc.abstractmethod
    def uninstall_schedule(self, task_id: str) -> None:
        """Remove a scheduled task entirely (unload + delete artifacts)."""

    @abc.abstractmethod
    def load_schedule(self, task_id: str) -> None:
        """Resume/load a previously installed schedule."""

    @abc.abstractmethod
    def unload_schedule(self, task_id: str) -> None:
        """Pause/unload a schedule without removing artifacts."""

    @abc.abstractmethod
    def schedule_artifact_exists(self, task_id: str) -> bool:
        """Check whether schedule artifacts exist (for repair detection)."""

    @abc.abstractmethod
    def generate_wrapper(
        self,
        task: dict,
        scheduler_dir: Path,
        scheduler_py_path: Path,
        wrappers_dir: Path,
    ) -> Path:
        """Generate a wrapper script for the task. Returns the wrapper path."""

    @abc.abstractmethod
    def wrapper_extension(self) -> str:
        """Return the file extension for wrapper scripts (e.g. '.sh', '.ps1')."""

    @abc.abstractmethod
    def run_wrapper(self, wrapper_path: Path) -> int:
        """Execute a wrapper script directly. Returns the process exit code."""

    @abc.abstractmethod
    def skip_scheduling(self) -> bool:
        """Whether to skip platform scheduler interactions (for testing)."""

    @abc.abstractmethod
    def default_schedule_dir(self) -> Path:
        """Return the default directory for schedule artifacts."""

    # --- Optional methods (default no-ops) ---

    def get_api_key(self, service_name: str) -> str | None:
        """Retrieve an API key from the platform's secret store."""
        return None

    def send_notification(
        self, title: str, message: str, is_error: bool = False
    ) -> None:
        """Send a desktop notification."""
