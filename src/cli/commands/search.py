# src/cli/commands/search.py
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from src.cli.commands.base import BaseCommand, CommandResult
from src.storage.abstract import AbstractStorage


@dataclass
class SearchCommandResult(CommandResult):
    """Result of search command execution."""


class SearchCommand(BaseCommand):
    """Command for searching books in the library."""

    def __init__(self, storage: AbstractStorage) -> None:
        super().__init__()
        self.storage = storage

    def configure(self, parser: ArgumentParser) -> None:
        parser.add_argument("query", help="Search query")
        parser.add_argument(
            "--field",
            choices=["title", "author", "year"],
            default="title",
            help="Field to search in",
        )

    def execute(self, args: Namespace) -> CommandResult:
        try:
            books = self.storage.search(args.query, args.field)

            if not books:
                return SearchCommandResult(
                    success=True,
                    message="No books found matching the search criteria",
                    data=[],
                )

            return SearchCommandResult(
                success=True,
                message=f"Found {len(books)} matching books",
                data=[book.to_dict() for book in books],
            )

        except ValueError as e:
            return SearchCommandResult(success=False, message=f"Search failed: {e!s}")
        except Exception as e:
            return SearchCommandResult(
                success=False, message=f"Unexpected error: {e!s}"
            )
