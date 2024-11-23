# src/models/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime

# Constants for validation
MAX_BOOK_ID_LENGTH = 50
MAX_BOOK_TITLE_LENGTH = 200
MAX_AUTHOR_NAME_LENGTH = 100
MIN_PUBLICATION_YEAR = 1000


class ValueObject(ABC):
    """Base class for all value objects in the domain."""

    @abstractmethod
    def validate(self) -> None:
        """Validate the value object's data."""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__dict__ == other.__dict__


@dataclass(frozen=True)
class BookId(ValueObject):
    """Value object representing a book's unique identifier."""

    value: str

    def validate(self) -> None:
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Book ID must be a non-empty string")
        if len(self.value) > MAX_BOOK_ID_LENGTH:
            raise ValueError(f"Book ID must not exceed {MAX_BOOK_ID_LENGTH} characters")


@dataclass(frozen=True)
class BookTitle(ValueObject):
    """Value object representing a book's title."""

    value: str

    def validate(self) -> None:
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Book title must be a non-empty string")
        if len(self.value) > MAX_BOOK_TITLE_LENGTH:
            raise ValueError(
                f"Book title must not exceed {MAX_BOOK_TITLE_LENGTH} characters"
            )


@dataclass(frozen=True)
class Author(ValueObject):
    """Value object representing a book's author."""

    value: str

    def validate(self) -> None:
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Author must be a non-empty string")
        if len(self.value) > MAX_AUTHOR_NAME_LENGTH:
            raise ValueError(
                f"Author name must not exceed {MAX_AUTHOR_NAME_LENGTH} characters"
            )


@dataclass(frozen=True)
class PublicationYear(ValueObject):
    """Value object representing a book's publication year."""

    value: int

    def validate(self) -> None:
        current_year = datetime.now(tz=UTC).year
        if not isinstance(self.value, int):
            raise ValueError("Publication year must be an integer")
        if self.value < MIN_PUBLICATION_YEAR or self.value > current_year:
            raise ValueError(
                f"Publication year must be between "
                f"{MIN_PUBLICATION_YEAR} and {current_year}"
            )


class BookStatus:
    """Enumeration of possible book statuses."""

    AVAILABLE = "available"
    BORROWED = "borrowed"

    @classmethod
    def is_valid(cls, status: str) -> bool:
        """Check if a status value is valid."""
        return status in {cls.AVAILABLE, cls.BORROWED}
