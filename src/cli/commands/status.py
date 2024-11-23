# src/cli/commands/status.py
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from src.cli.commands.base import BaseCommand, CommandResult
from src.models.book import BookStatus
from src.storage.abstract import AbstractStorage


@dataclass
class StatusCommandResult(CommandResult):
    """Result of status update command execution."""


class StatusCommand(BaseCommand):
    """Command for updating a book's status."""

    def __init__(self, storage: AbstractStorage) -> None:
        super().__init__()
        self.storage = storage

    def configure(self, parser: ArgumentParser) -> None:
        parser.add_argument("book_id", help="Book ID")
        parser.add_argument(
            "status",
            choices=[BookStatus.AVAILABLE, BookStatus.BORROWED],
            help="New status",
        )

    def execute(self, args: Namespace) -> CommandResult:
        try:
            book = self.storage.get(args.book_id)
            if not book:
                return StatusCommandResult(
                    success=False, message=f"Book with ID {args.book_id} not found"
                )

            book.update_status(args.status)
            self.storage.update(book)

            return StatusCommandResult(
                success=True,
                message=f"Book status updated to {args.status}",
                data=book.to_dict(),
            )

        except ValueError as e:
            return StatusCommandResult(
                success=False, message=f"Failed to update status: {e!s}"
            )
        except Exception as e:
            return StatusCommandResult(
                success=False, message=f"Unexpected error: {e!s}"
            )
