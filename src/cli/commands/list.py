# src/cli/commands/list.py
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from src.cli.commands.base import BaseCommand, CommandResult
from src.storage.abstract import AbstractStorage


@dataclass
class ListCommandResult(CommandResult):
    """Result of list command execution."""


class ListCommand(BaseCommand):
    """Command for listing all books in the library."""

    def __init__(self, storage: AbstractStorage) -> None:
        super().__init__()
        self.storage = storage

    def configure(self, parser: ArgumentParser) -> None:
        pass  # No additional arguments needed

    def execute(self, args: Namespace) -> CommandResult:
        try:
            books = self.storage.list_all()

            if not books:
                return ListCommandResult(
                    success=True, message="No books found in the library", data=[]
                )

            return ListCommandResult(
                success=True,
                message=f"Found {len(books)} books",
                data=[book.to_dict() for book in books],
            )

        except Exception as e:
            return ListCommandResult(
                success=False, message=f"Failed to list books: {e!s}"
            )
