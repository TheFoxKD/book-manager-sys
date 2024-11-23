# tests/test_app.py

import pytest

from src.cli.app import BookManagerCLI
from src.cli.commands.base import BaseCommand, CommandResult
from src.storage.json_storage import StorageError

INVALID_COMMAND_EXIT_CODE = 2


class MockCommand(BaseCommand):
    """Mock command for testing."""

    def __init__(self, name: str, result: CommandResult) -> None:
        self._name = name  # Store name in private attribute
        self.result = result
        # Remove super().__init__() call since we're implementing our own name handling

    def configure(self, parser):
        pass

    def execute(self, args):
        return self.result

    @property
    def name(self) -> str:
        """Override parent's name property."""
        return self._name


class TestBookManagerCLI:
    def test_run_without_command(self, cli_app, capsys):
        """Test running CLI without command shows help."""
        exit_code = cli_app.run([])
        captured = capsys.readouterr()

        assert exit_code == 0
        assert "usage:" in captured.out

    def test_run_invalid_command(self, cli_app):
        """Test running nonexistent command."""
        with pytest.raises(SystemExit) as excinfo:
            cli_app.run(["nonexistent"])
        assert excinfo.value.code == INVALID_COMMAND_EXIT_CODE

    def test_run_command_success(self, storage):
        """Test successful command execution."""
        command = MockCommand(
            "test", CommandResult(success=True, message="Test succeeded")
        )
        cli = BookManagerCLI(storage, [command])
        exit_code = cli.run([command.name])
        assert exit_code == 0

    def test_run_command_failure(self, storage):
        """Test failed command execution."""
        command = MockCommand(
            "test", CommandResult(success=False, message="Test failed")
        )
        cli = BookManagerCLI(storage, [command])
        exit_code = cli.run([command.name])
        assert exit_code == 1

    def test_storage_error_handling(self, cli_app, storage, monkeypatch):
        """Test handling of storage errors."""

        def mock_list(*args, **kwargs):
            raise StorageError("Test error")

        monkeypatch.setattr(storage, "list_all", mock_list)
        exit_code = cli_app.run(["list"])
        assert exit_code == 1  # Changed from 2 to 1 for storage errors

    def test_unexpected_error_handling(self, cli_app, storage, monkeypatch):
        """Test handling of unexpected errors."""

        def mock_list(*args, **kwargs):
            raise RuntimeError("Unexpected error")

        monkeypatch.setattr(storage, "list_all", mock_list)
        exit_code = cli_app.run(["list"])
        assert exit_code == 1  # Changed from 3 to 1 for unexpected errors

    @pytest.mark.parametrize(
        "command_args", ["add", "delete", "list", "search", "status"]
    )
    def test_command_help(self, cli_app, command_args, capsys):
        """Test help message for each command."""
        with pytest.raises(SystemExit) as excinfo:
            cli_app.run([command_args, "--help"])

        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert command_args in captured.out
        assert "usage:" in captured.out
