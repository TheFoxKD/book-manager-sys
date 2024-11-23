# tests/cli/test_commands.py
from argparse import Namespace

import pytest

from src.cli.commands.add import AddCommand
from src.cli.commands.delete import DeleteCommand
from src.cli.commands.list import ListCommand
from src.cli.commands.search import SearchCommand
from src.cli.commands.status import StatusCommand
from src.models.book import BookStatus


class TestAddCommand:
    def test_add_valid_book(self, storage, valid_book_data):
        """Test adding a valid book."""
        cmd = AddCommand(storage)
        args = Namespace(**valid_book_data)
        result = cmd.execute(args)

        assert result.success
        assert "added successfully" in result.message
        assert result.data is not None
        assert result.data["title"] == valid_book_data["title"]

    def test_add_invalid_book(self, storage, invalid_book_data):
        """Test adding invalid books."""
        cmd = AddCommand(storage)

        for _case, data in invalid_book_data.items():
            args = Namespace(**data)
            result = cmd.execute(args)

            assert not result.success
            assert "Failed to add book" in result.message


class TestDeleteCommand:
    def test_delete_existing_book(self, storage, valid_book):
        """Test deleting an existing book."""
        storage.add(valid_book)
        cmd = DeleteCommand(storage)
        args = Namespace(book_id=valid_book.id.value)
        result = cmd.execute(args)

        assert result.success
        assert "deleted successfully" in result.message
        assert storage.get(valid_book.id.value) is None

    def test_delete_nonexistent_book(self, storage):
        """Test deleting a nonexistent book."""
        cmd = DeleteCommand(storage)
        args = Namespace(book_id="nonexistent")
        result = cmd.execute(args)

        assert not result.success
        assert "not found" in result.message


class TestListCommand:
    def test_list_empty_library(self, storage):
        """Test listing books in empty library."""
        cmd = ListCommand(storage)
        result = cmd.execute(Namespace())

        assert result.success
        assert "No books found" in result.message
        assert result.data == []

    def test_list_with_books(self, storage, sample_books):
        """Test listing multiple books."""
        for book in sample_books:
            storage.add(book)

        cmd = ListCommand(storage)
        result = cmd.execute(Namespace())

        assert result.success
        assert str(len(sample_books)) in result.message
        assert len(result.data) == len(sample_books)


class TestSearchCommand:
    @pytest.mark.parametrize(
        ("field", "query", "expected_count"),
        [
            ("title", "Great", 1),
            ("author", "Orwell", 1),
            ("year", "1949", 1),
            ("title", "nonexistent", 0),
        ],
    )
    def test_search_books(self, storage, sample_books, field, query, expected_count):
        """Test searching books by different fields."""
        for book in sample_books:
            storage.add(book)

        cmd = SearchCommand(storage)
        args = Namespace(field=field, query=query)
        result = cmd.execute(args)

        assert result.success
        assert len(result.data or []) == expected_count

    def test_search_invalid_field(self, storage):
        """Test searching with invalid field."""
        cmd = SearchCommand(storage)
        args = Namespace(field="invalid", query="test")
        result = cmd.execute(args)

        assert not result.success
        assert "Invalid search field" in result.message


class TestStatusCommand:
    def test_update_status(self, storage, valid_book):
        """Test updating book status."""
        storage.add(valid_book)
        cmd = StatusCommand(storage)
        args = Namespace(book_id=valid_book.id.value, status=BookStatus.BORROWED)
        result = cmd.execute(args)

        assert result.success
        assert "status updated" in result.message
        assert storage.get(valid_book.id.value).status == BookStatus.BORROWED

    def test_update_nonexistent_book(self, storage):
        """Test updating status of nonexistent book."""
        cmd = StatusCommand(storage)
        args = Namespace(book_id="nonexistent", status=BookStatus.BORROWED)
        result = cmd.execute(args)

        assert not result.success
        assert "not found" in result.message

    def test_update_invalid_status(self, storage, valid_book):
        """Test updating with invalid status."""
        storage.add(valid_book)
        cmd = StatusCommand(storage)
        args = Namespace(book_id=valid_book.id.value, status="invalid")
        result = cmd.execute(args)

        assert not result.success
        assert "Invalid status" in result.message
