# tests/conftest.py
from datetime import UTC, datetime
from typing import Any

import pytest

from src.models.book import Book, BookStatus


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
    next_time = datetime(2024, 1, 1, 12, 1, 0, tzinfo=UTC)  # 1 minute later
    times = [initial_time, next_time]
    current_index = 0

    class MockDatetime:
        @classmethod
        def now(cls, tz=None):  # Add tz parameter
            nonlocal current_index
            time = times[current_index]
            if current_index < len(times) - 1:
                current_index += 1
            return time

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
