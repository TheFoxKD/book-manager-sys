# src/storage/json_storage.py
import json
from pathlib import Path
from threading import Lock
from typing import Any  # Add this import at the top with other imports

from src.models.book import Book

from .abstract import AbstractStorage


class StorageError(Exception):
    """Custom exception for storage-related errors."""


class JsonStorage(AbstractStorage):
    """JSON file-based implementation of book storage."""

    def __init__(self, file_path: str | Path) -> None:
        """
        Initialize JSON storage.

        Args:
            file_path: Path to the JSON storage file
        """
        self.file_path = Path(file_path)
        self._lock = Lock()  # For thread-safe file operations
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Ensure storage file exists and is valid JSON."""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                self._save_data({})
            except Exception as e:
                raise StorageError(f"Failed to create storage file: {e}") from e
        else:
            try:
                self._load_data()
            except json.JSONDecodeError as e:
                raise StorageError(f"Storage file contains invalid JSON: {e}") from e

    def _load_data(self) -> dict[str, dict[str, Any]]:
        """Load data from JSON file."""
        try:
            with self._lock, open(self.file_path, encoding="utf-8") as f:
                return json.load(f)  # type: ignore
        except Exception as e:
            raise StorageError(f"Failed to load storage: {e}") from e

    def _save_data(self, data: dict) -> None:
        """Save data to JSON file."""
        try:
            with self._lock, open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise StorageError(f"Failed to save to storage: {e}") from e

    def add(self, book: Book) -> None:
        data = self._load_data()
        if book.id.value in data:
            raise ValueError(f"Book with ID {book.id.value} already exists")

        data[book.id.value] = book.to_dict()
        self._save_data(data)

    def get(self, book_id: str) -> Book | None:
        data = self._load_data()
        book_data = data.get(book_id)
        return Book.from_dict(book_data) if book_data else None

    def update(self, book: Book) -> None:
        data = self._load_data()
        if book.id.value not in data:
            raise ValueError(f"Book with ID {book.id.value} not found")

        data[book.id.value] = book.to_dict()
        self._save_data(data)

    def delete(self, book_id: str) -> None:
        data = self._load_data()
        if book_id not in data:
            raise ValueError(f"Book with ID {book_id} not found")

        del data[book_id]
        self._save_data(data)

    def list_all(self) -> list[Book]:
        data = self._load_data()
        return [Book.from_dict(book_data) for book_data in data.values()]

    def search(self, query: str, field: str) -> list[Book]:
        if field not in {"title", "author", "year"}:
            raise ValueError(f"Invalid search field: {field}")

        data = self._load_data()
        results = []

        for book_data in data.values():
            if field == "year":
                # For year, convert query to int and do exact match
                try:
                    if int(query) == book_data["year"]:
                        results.append(Book.from_dict(book_data))
                except ValueError:
                    continue
            # For strings, do case-insensitive partial match
            elif str(query).lower() in str(book_data[field]).lower():
                results.append(Book.from_dict(book_data))

        return results


class InMemoryStorage(AbstractStorage):
    """In-memory implementation of book storage for testing."""

    def __init__(self) -> None:
        """Initialize in-memory storage."""
        self._storage: dict[str, dict] = {}

    def add(self, book: Book) -> None:
        if book.id.value in self._storage:
            raise ValueError(f"Book with ID {book.id.value} already exists")
        self._storage[book.id.value] = book.to_dict()

    def get(self, book_id: str) -> Book | None:
        book_data = self._storage.get(book_id)
        return Book.from_dict(book_data) if book_data else None

    def update(self, book: Book) -> None:
        if book.id.value not in self._storage:
            raise ValueError(f"Book with ID {book.id.value} not found")
        self._storage[book.id.value] = book.to_dict()

    def delete(self, book_id: str) -> None:
        if book_id not in self._storage:
            raise ValueError(f"Book with ID {book_id} not found")
        del self._storage[book_id]

    def list_all(self) -> list[Book]:
        return [Book.from_dict(book_data) for book_data in self._storage.values()]

    def search(self, query: str, field: str) -> list[Book]:
        if field not in {"title", "author", "year"}:
            raise ValueError(f"Invalid search field: {field}")

        results = []
        for book_data in self._storage.values():
            if field == "year":
                try:
                    if int(query) == book_data["year"]:
                        results.append(Book.from_dict(book_data))
                except ValueError:
                    continue
            elif str(query).lower() in str(book_data[field]).lower():
                results.append(Book.from_dict(book_data))
        return results
