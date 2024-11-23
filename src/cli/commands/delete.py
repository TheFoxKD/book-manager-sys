# src/cli/commands/delete.py
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from src.cli.commands.base import BaseCommand, CommandResult
from src.storage.abstract import AbstractStorage


@dataclass
class DeleteCommandResult(CommandResult):
    """Result of delete command execution."""


class DeleteCommand(BaseCommand):
    """Command for deleting a book from the library."""

    def __init__(self, storage: AbstractStorage) -> None:
        super().__init__()
        self.storage = storage

    def configure(self, parser: ArgumentParser) -> None:
        parser.add_argument("book_id", help="Book ID to delete")

    def execute(self, args: Namespace) -> CommandResult:
        try:
            book = self.storage.get(args.book_id)
            if not book:
                return DeleteCommandResult(
                    success=False, message=f"Book with ID {args.book_id} not found"
                )

            self.storage.delete(args.book_id)

            return DeleteCommandResult(
                success=True,
                message=f"Book '{book.title.value}' deleted successfully",
                data=book.to_dict(),
            )

        except ValueError as e:
            return DeleteCommandResult(
                success=False, message=f"Failed to delete book: {e!s}"
            )
        except Exception as e:
            return DeleteCommandResult(
                success=False, message=f"Unexpected error: {e!s}"
            )
