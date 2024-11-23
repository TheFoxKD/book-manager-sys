# src/models/book.py
from dataclasses import dataclass
from datetime import UTC, datetime

from .base import Author, BookId, BookStatus, BookTitle, PublicationYear


@dataclass
class Book:
    """
    Domain model representing a book in the library system.

    This class encapsulates all the business rules and validation logic
    related to books in the library system.
    """

    id: BookId
    title: BookTitle
    author: Author
    year: PublicationYear
    status: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        """Validate all value objects and status after initialization."""
        self.id.validate()
        self.title.validate()
        self.author.validate()
        self.year.validate()

        if not BookStatus.is_valid(self.status):
            raise ValueError(f"Invalid status: {self.status}")

    @classmethod
    def create(
        cls, title: str, author: str, year: int, book_id: str | None = None
    ) -> "Book":
        """
        Factory method to create a new Book instance with validated data.

        Args:
            title: The title of the book
            author: The author of the book
            year: The publication year
            book_id: Optional book ID (generated if not provided)

        Returns:
            A new Book instance

        Raises:
            ValueError: If any of the input data is invalid
        """
        now = datetime.now(tz=UTC)
        return cls(
            id=BookId(book_id or f"book_{now.timestamp()}"),
            title=BookTitle(title),
            author=Author(author),
            year=PublicationYear(year),
            status=BookStatus.AVAILABLE,
            created_at=now,
            updated_at=now,
        )

    def update_status(self, new_status: str) -> None:
        """
        Update the book's status.

        Args:
            new_status: The new status to set

        Raises:
            ValueError: If the status is invalid
        """
        if not BookStatus.is_valid(new_status):
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status
        self.updated_at = datetime.now(tz=UTC)

    def to_dict(self) -> dict:
        """Convert the book instance to a dictionary for storage."""
        return {
            "id": self.id.value,
            "title": self.title.value,
            "author": self.author.value,
            "year": self.year.value,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """
        Create a Book instance from a dictionary.

        Args:
            data: Dictionary containing book data

        Returns:
            A new Book instance

        Raises:
            ValueError: If the dictionary data is invalid
        """
        return cls(
            id=BookId(data["id"]),
            title=BookTitle(data["title"]),
            author=Author(data["author"]),
            year=PublicationYear(data["year"]),
            status=data["status"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
