# src/cli/app.py
import argparse
import logging
import sys
from collections.abc import Sequence
from pathlib import Path

from src.cli.commands.base import BaseCommand
from src.storage.abstract import AbstractStorage
from src.storage.json_storage import StorageError


class BookManagerCLI:
    """Main CLI application class."""

    def __init__(
        self, storage: AbstractStorage, commands: Sequence[BaseCommand] | None = None
    ) -> None:
        """Initialize CLI application."""
        self.storage = storage
        self.logger = logging.getLogger(__name__)

        self.parser = argparse.ArgumentParser(
            description="Book Manager CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self.subparsers = self.parser.add_subparsers(
            dest="command", help="Available commands"
        )

        self._register_commands(commands or [])

    def _register_commands(self, commands: Sequence[BaseCommand]) -> None:
        """Register CLI commands."""
        self.commands = {}
        for cmd in commands:
            subparser = self.subparsers.add_parser(cmd.name)
            cmd.configure(subparser)
            self.commands[cmd.name] = cmd

    def run(self, args: list[str] | None = None) -> int:
        """Run the CLI application with the given arguments."""
        if not args:
            self.parser.print_help(sys.stdout)
            return 0

        try:
            parsed_args = self.parser.parse_args(args)
            if not parsed_args.command:
                self.parser.print_help(sys.stdout)
                return 0

            command = self.commands[parsed_args.command]
            result = command.execute(parsed_args)

            if not result.success:
                self.logger.error(result.message)
                return 1

            self.logger.info(result.message)
            return 0

        except StorageError as e:
            self.logger.error("Storage error: %s", str(e))
            return 2

        except Exception as e:
            self.logger.error("Unexpected error: %s", str(e))
            return 3


def main() -> None:
    """CLI entry point."""
    try:
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        # Setup storage
        storage_path = Path.home() / ".book-manager" / "books.json"
        storage_path.parent.mkdir(parents=True, exist_ok=True)

        from src.cli.commands.add import AddCommand
        from src.cli.commands.delete import DeleteCommand
        from src.cli.commands.list import ListCommand
        from src.cli.commands.search import SearchCommand
        from src.cli.commands.status import StatusCommand
        from src.storage.json_storage import JsonStorage

        storage = JsonStorage(storage_path)
        commands = [
            AddCommand(storage),
            DeleteCommand(storage),
            ListCommand(storage),
            SearchCommand(storage),
            StatusCommand(storage),
        ]

        app = BookManagerCLI(storage, commands)
        sys.exit(app.run(sys.argv[1:]))

    except Exception as e:
        logging.error("Failed to initialize application: %s", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
