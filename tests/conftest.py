# tests/conftest.py
import io
import sys
from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from rich.console import Console

from src.cli.app import BookManagerCLI
from src.cli.commands.add import AddCommand
from src.cli.commands.base import BaseCommand, CommandResult
from src.cli.commands.delete import DeleteCommand
from src.cli.commands.list import ListCommand
from src.cli.commands.search import SearchCommand
from src.cli.commands.status import StatusCommand
from src.cli.output import ConsoleOutput, OutputFormatter
from src.models.book import Book, BookStatus
from src.storage.abstract import AbstractStorage
from src.storage.json_storage import InMemoryStorage, JsonStorage


@pytest.fixture
def mock_current_time(monkeypatch) -> datetime:
    """
    Fixture that mocks the current time for consistent testing.

    Args:
        monkeypatch: pytest's monkeypatch fixture

    Returns:
        Fixed datetime object
    """
    initial_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
    time_increment = 1  # increment in minutes

    class MockDatetime:
        _current_time = initial_time

        @classmethod
        def now(cls, tz=None):
            cls._current_time += timedelta(minutes=time_increment)
            return cls._current_time

        @classmethod
        def fromisoformat(cls, date_string):
            return datetime.fromisoformat(date_string)

    monkeypatch.setattr("src.models.book.datetime", MockDatetime)
    return initial_time


@pytest.fixture
def valid_book_data() -> dict[str, Any]:
    """
    Fixture that returns valid book data for testing.

    Returns:
        Dictionary containing valid book data
    """
    return {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925}


@pytest.fixture
def valid_book(valid_book_data, mock_current_time) -> Book:
    """
    Fixture that returns a valid Book instance.

    Args:
        valid_book_data: Dictionary with valid book data (fixture)
        mock_current_time: Mocked datetime for consistent testing

    Returns:
        Valid Book instance
    """
    return Book.create(**valid_book_data)


@pytest.fixture
def borrowed_book(valid_book, mock_current_time) -> Book:
    """
    Fixture that returns a book with 'borrowed' status.

    Args:
        valid_book: Valid Book instance (fixture)
        mock_current_time: Mocked datetime for consistent testing

    Returns:
        Book instance with borrowed status
    """
    valid_book.update_status(BookStatus.BORROWED)
    return valid_book


@pytest.fixture
def sample_books(mock_current_time) -> list[Book]:
    """
    Fixture that returns a list of sample books for testing.

    Returns:
        List of Book instances
    """
    books_data = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
        {"title": "1984", "author": "George Orwell", "year": 1949},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813},
    ]
    return [Book.create(**data) for data in books_data]


@pytest.fixture
def value_objects(valid_book) -> dict[str, Any]:
    """
    Fixture that returns instances of all value objects for testing.

    Args:
        valid_book: Valid Book instance (fixture)

    Returns:
        Dictionary containing instances of all value objects
    """
    return {
        "book_id": valid_book.id,
        "title": valid_book.title,
        "author": valid_book.author,
        "year": valid_book.year,
    }


@pytest.fixture
def invalid_book_data() -> dict[str, dict[str, Any]]:
    """
    Fixture that returns various invalid book data for negative testing.

    Returns:
        Dictionary containing different cases of invalid book data
    """
    return {
        "empty_title": {"title": "", "author": "Valid Author", "year": 2020},
        "empty_author": {"title": "Valid Title", "author": "", "year": 2020},
        "future_year": {"title": "Valid Title", "author": "Valid Author", "year": 2525},
        "too_old_year": {"title": "Valid Title", "author": "Valid Author", "year": 999},
        "long_title": {"title": "x" * 201, "author": "Valid Author", "year": 2020},
        "long_author": {"title": "Valid Title", "author": "x" * 101, "year": 2020},
    }


@pytest.fixture
def storage_file(tmp_path) -> Path:
    """Create a temporary storage file."""
    return tmp_path / "test_storage.json"


@pytest.fixture(params=[JsonStorage, InMemoryStorage])
def storage(request, storage_file) -> AbstractStorage:
    """
    Parametrized fixture providing both storage implementations.

    For JsonStorage, uses a temporary file.
    For InMemoryStorage, the file parameter is ignored.
    """
    storage_class: type[AbstractStorage] = request.param
    if storage_class == JsonStorage:
        return JsonStorage(storage_file)
    return InMemoryStorage()


class MockCommand(BaseCommand):
    """Mock command for testing."""

    def __init__(self, name: str, result: CommandResult) -> None:
        self.mock_name = name
        self.result = result
        super().__init__()

    @property
    def name(self) -> str:
        return self.mock_name

    def configure(self, parser):
        pass

    def execute(self, args):
        return self.result


class MockOutput(OutputFormatter):
    """Mock output formatter for testing."""

    def __init__(self) -> None:
        self.displayed_results: list[CommandResult] = []
        self.errors: list[str] = []

    def display(self, result: CommandResult) -> None:
        self.displayed_results.append(result)

    def error(self, message: str) -> None:
        self.errors.append(message)


@pytest.fixture
def mock_command_result() -> CommandResult:
    """Fixture providing a mock command result."""
    return CommandResult(success=True, message="Test succeeded", data=None)


@pytest.fixture
def mock_command(mock_command_result) -> MockCommand:
    """Fixture providing a mock command."""
    return MockCommand("test", mock_command_result)


@pytest.fixture
def mock_output() -> MockOutput:
    """Fixture providing a mock output formatter."""
    return MockOutput()


@pytest.fixture
def capture_stdout() -> Generator[io.StringIO, None, None]:
    """Fixture for capturing stdout."""
    stdout = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout
    yield stdout
    sys.stdout = old_stdout


@pytest.fixture
def capture_stderr() -> Generator[io.StringIO, None, None]:
    """Fixture for capturing stderr."""
    stderr = io.StringIO()
    old_stderr = sys.stderr
    sys.stderr = stderr
    yield stderr
    sys.stderr = old_stderr


@pytest.fixture
def rich_console(monkeypatch: MonkeyPatch) -> Console:
    """Fixture providing a Rich console with captured output."""
    output = io.StringIO()
    console = Console(file=output, force_terminal=True)
    monkeypatch.setattr("src.cli.output.Console", lambda: console)
    return console


@pytest.fixture
def console_output(rich_console) -> ConsoleOutput:
    """Fixture providing a ConsoleOutput instance."""
    return ConsoleOutput()


@pytest.fixture
def cli_args() -> dict[str, dict[str, Any]]:
    """Fixture providing various CLI argument combinations."""
    return {
        "add": {
            "valid": ["add", "Test Book", "Test Author", "2020"],
            "invalid_year": ["add", "Test Book", "Test Author", "invalid"],
            "missing_args": ["add", "Test Book"],
        },
        "delete": {
            "valid": ["delete", "test_id"],
            "missing_id": ["delete"],
        },
        "search": {
            "valid": ["search", "test", "--field", "title"],
            "invalid_field": ["search", "test", "--field", "invalid"],
        },
        "list": {
            "valid": ["list"],
        },
        "status": {
            "valid": ["status", "test_id", "borrowed"],
            "invalid_status": ["status", "test_id", "invalid"],
        },
    }


@pytest.fixture
def cli_commands(storage) -> list[BaseCommand]:
    """Fixture providing default CLI commands."""
    return [
        AddCommand(storage),
        DeleteCommand(storage),
        ListCommand(storage),
        SearchCommand(storage),
        StatusCommand(storage),
    ]


@pytest.fixture
def cli_app(storage, cli_commands) -> BookManagerCLI:
    """Fixture providing a CLI application instance."""
    return BookManagerCLI(storage, cli_commands)


@pytest.fixture
def mock_console(monkeypatch) -> Mock:
    """Fixture providing a mocked Rich console."""
    console = Mock(spec=Console)
    monkeypatch.setattr("src.cli.output.Console", lambda: console)
    return console


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Fixture providing sample test data."""
    now = datetime.now(UTC)
    return {
        "single": {
            "id": "book_1",
            "title": "Test Book",
            "author": "Test Author",
            "year": 2024,
            "status": "available",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        },
        "multiple": [
            {
                "id": "book_1",
                "title": "Book 1",
                "author": "Author 1",
                "status": "available",
            },
            {
                "id": "book_2",
                "title": "Book 2",
                "author": "Author 2",
                "status": "borrowed",
            },
        ],
    }
