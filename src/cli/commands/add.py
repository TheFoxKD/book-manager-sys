# src/cli/commands/add.py
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from src.cli.commands.base import BaseCommand, CommandResult
from src.models.book import Book
from src.storage.abstract import AbstractStorage


@dataclass
class AddCommandResult(CommandResult):
    """Result of add command execution."""


class AddCommand(BaseCommand):
    """Command for adding a new book to the library."""

    def __init__(self, storage: AbstractStorage) -> None:
        super().__init__()
        self.storage = storage

    def configure(self, parser: ArgumentParser) -> None:
        parser.add_argument("title", help="Book title")
        parser.add_argument("author", help="Book author")
        parser.add_argument("year", type=int, help="Publication year")

    def execute(self, args: Namespace) -> CommandResult:
        try:
            book = Book.create(title=args.title, author=args.author, year=args.year)
            self.storage.add(book)

            return AddCommandResult(
                success=True,
                message=f"Book '{book.title.value}' added successfully",
                data=book.to_dict(),
            )

        except ValueError as e:
            return AddCommandResult(success=False, message=f"Failed to add book: {e!s}")
        except Exception as e:
            return AddCommandResult(success=False, message=f"Unexpected error: {e!s}")
