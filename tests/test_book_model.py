# tests/test_book_model.py
from datetime import UTC, datetime

import pytest

from src.models.book import Author, Book, BookId, BookStatus, BookTitle, PublicationYear


class TestValueObjects:
    def test_book_id_validation(self, value_objects):
        """Test book ID validation with valid and invalid values."""
        # Valid ID
        value_objects["book_id"].validate()

        # Invalid IDs
        with pytest.raises(ValueError, match="must be a non-empty string"):
            BookId("").validate()
        with pytest.raises(ValueError, match="must not exceed 50 characters"):
            BookId("x" * 51).validate()

    def test_book_title_validation(self, value_objects):
        """Test book title validation with valid and invalid values."""
        # Valid title
        value_objects["title"].validate()

        # Test invalid cases
        with pytest.raises(ValueError, match="must be a non-empty string"):
            BookTitle("").validate()
        with pytest.raises(ValueError, match="must not exceed 200 characters"):
            BookTitle("x" * 201).validate()

    def test_author_validation(self, value_objects):
        """Test author validation with valid and invalid values."""
        # Valid author
        value_objects["author"].validate()

        # Test invalid cases
        with pytest.raises(ValueError, match="must be a non-empty string"):
            Author("").validate()
        with pytest.raises(ValueError, match="must not exceed 100 characters"):
            Author("x" * 101).validate()

    def test_publication_year_validation(self, value_objects, mock_current_time):
        """Test publication year validation with valid and invalid values."""
        # Valid year
        value_objects["year"].validate()

        # Test invalid cases
        with pytest.raises(ValueError, match="must be between"):
            PublicationYear(999).validate()
        with pytest.raises(ValueError, match="must be between"):
            PublicationYear(mock_current_time.year + 1).validate()


class TestBook:
    def test_book_creation(self, valid_book, valid_book_data):
        """Test successful book creation with valid data."""
        assert isinstance(valid_book.id, BookId)
        assert valid_book.title.value == valid_book_data["title"]
        assert valid_book.author.value == valid_book_data["author"]
        assert valid_book.year.value == valid_book_data["year"]
        assert valid_book.status == BookStatus.AVAILABLE
        assert isinstance(valid_book.created_at, datetime)
        assert isinstance(valid_book.updated_at, datetime)

    def test_invalid_book_creation(self, invalid_book_data):
        """Test book creation with various invalid scenarios."""
        expected_error_patterns = {
            "empty_title": "Book title must be a non-empty string",
            "empty_author": "Author must be a non-empty string",
            "future_year": "Publication year must be between",
            "too_old_year": "Publication year must be between",
            "long_title": "Book title must not exceed 200 characters",
            "long_author": "Author name must not exceed 100 characters",
        }

        for case, invalid_data in invalid_book_data.items():
            with pytest.raises(ValueError, match=expected_error_patterns[case]):
                Book.create(**invalid_data)

    def test_status_update(self, valid_book, mock_current_time):
        """Test book status updates with valid and invalid values."""
        # Test valid status update
        original_updated_at = valid_book.updated_at
        valid_book.update_status(BookStatus.BORROWED)

        assert valid_book.status == BookStatus.BORROWED
        assert valid_book.updated_at > original_updated_at

        # Test invalid status update
        with pytest.raises(ValueError, match="Invalid status"):
            valid_book.update_status("invalid_status")

    def test_serialization(self, valid_book):
        """Test book serialization and deserialization."""
        # Convert to dict and back
        book_dict = valid_book.to_dict()
        restored_book = Book.from_dict(book_dict)

        # Verify all fields match
        assert restored_book.id == valid_book.id
        assert restored_book.title == valid_book.title
        assert restored_book.author == valid_book.author
        assert restored_book.year == valid_book.year
        assert restored_book.status == valid_book.status
        assert restored_book.created_at == valid_book.created_at
        assert restored_book.updated_at == valid_book.updated_at

    def test_borrowed_book_status(self, borrowed_book):
        """Test that borrowed book has correct status."""
        assert borrowed_book.status == BookStatus.BORROWED

    @pytest.mark.parametrize("status", ["invalid", "pending", None, 123, ""])
    def test_invalid_status_updates(self, valid_book, status):
        """Test that invalid status updates are rejected."""
        with pytest.raises(ValueError, match="Invalid status"):
            valid_book.update_status(status)


def test_value_objects_equality(value_objects):
    """Test equality comparison of value objects."""
    # Create new instances with same values
    same_book_id = BookId(value_objects["book_id"].value)
    same_title = BookTitle(value_objects["title"].value)
    same_author = Author(value_objects["author"].value)
    same_year = PublicationYear(value_objects["year"].value)

    # Test equality
    assert value_objects["book_id"] == same_book_id
    assert value_objects["title"] == same_title
    assert value_objects["author"] == same_author
    assert value_objects["year"] == same_year

    # Test inequality
    assert value_objects["book_id"] != BookId("different_id")
    assert value_objects["title"] != BookTitle("Different Title")
    assert value_objects["author"] != Author("Different Author")
    assert value_objects["year"] != PublicationYear(2000)


@pytest.mark.parametrize(
    ("field", "invalid_value", "expected_error"),  # Now using a tuple
    [
        ("title", "", "Book title must be a non-empty string"),
        ("title", "x" * 201, "Book title must not exceed 200 characters"),
        ("author", "", "Author must be a non-empty string"),
        ("author", "x" * 101, "Author name must not exceed 100 characters"),
        ("year", 999, "Publication year must be between 1000"),
        ("year", datetime.now(UTC).year + 1, "Publication year must be between"),
    ],
)
def test_field_validations(valid_book_data, field, invalid_value, expected_error):
    """Test specific validation error messages for each field."""
    test_data = valid_book_data.copy()
    test_data[field] = invalid_value

    with pytest.raises(ValueError, match=expected_error):
        Book.create(**test_data)
