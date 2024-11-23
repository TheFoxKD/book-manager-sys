# src/storage/abstract.py
from abc import ABC, abstractmethod

from src.models.book import Book


class AbstractStorage(ABC):
    """Abstract base class defining the storage interface for the book management
    system."""

    @abstractmethod
    def add(self, book: Book) -> None:
        """
        Add a new book to the storage.

        Args:
            book: Book instance to store

        Raises:
            ValueError: If book with the same ID already exists
            StorageError: If storage operation fails
        """

    @abstractmethod
    def get(self, book_id: str) -> Book | None:
        """
        Retrieve a book by its ID.

        Args:
            book_id: Unique identifier of the book

        Returns:
            Book instance if found, None otherwise

        Raises:
            StorageError: If storage operation fails
        """

    @abstractmethod
    def update(self, book: Book) -> None:
        """
        Update an existing book in storage.

        Args:
            book: Book instance with updated data

        Raises:
            ValueError: If book doesn't exist
            StorageError: If storage operation fails
        """

    @abstractmethod
    def delete(self, book_id: str) -> None:
        """
        Delete a book from storage.

        Args:
            book_id: Unique identifier of the book to delete

        Raises:
            ValueError: If book doesn't exist
            StorageError: If storage operation fails
        """

    @abstractmethod
    def list_all(self) -> list[Book]:
        """
        Retrieve all books from storage.

        Returns:
            List of all Book instances

        Raises:
            StorageError: If storage operation fails
        """

    @abstractmethod
    def search(self, query: str, field: str) -> list[Book]:
        """
        Search for books by a specific field.

        Args:
            query: Search query string
            field: Field to search in ('title', 'author', or 'year')

        Returns:
            List of matching Book instances

        Raises:
            ValueError: If field is invalid
            StorageError: If storage operation fails
        """
