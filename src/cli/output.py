# src/cli/output.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from rich.console import Console
from rich.table import Table

from src.cli.commands.base import CommandResult


class OutputFormatter(ABC):
    """Abstract base class for formatting command output."""

    @abstractmethod
    def display(self, result: CommandResult) -> None:
        """Display command execution result."""

    @abstractmethod
    def error(self, message: str) -> None:
        """Display error message."""


class ConsoleOutput(OutputFormatter):
    """Rich console output formatter."""

    def __init__(self) -> None:
        self.console = Console()

    def display(self, result: CommandResult) -> None:
        """
        Display command result using Rich formatting.

        Args:
            result: Command execution result
        """
        if not result.success:
            self.error(result.message)
            return

        self.console.print(f"\n[green]{result.message}[/green]\n")

        if result.data:
            if isinstance(result.data, list):
                self._display_table(result.data)
            else:
                self._display_dict(result.data)

    def error(self, message: str) -> None:
        """
        Display error message in red.

        Args:
            message: Error message to display
        """
        self.console.print(f"\n[red]Error: {message}[/red]\n")

    def _display_table(self, data: list[dict[str, Any]]) -> None:
        """
        Display data as a formatted table.

        Args:
            data: List of dictionaries to display
        """
        if not data:
            return

        table = Table(show_header=True, header_style="bold magenta")

        # Add columns based on the first item's keys
        columns = list(data[0].keys())
        for column in columns:
            table.add_column(column.replace("_", " ").title())

        # Add rows
        for item in data:
            row = []
            for column in columns:
                cell_value = item[column]

                # Format dates
                if isinstance(cell_value, str) and "T" in cell_value:
                    try:
                        dt = datetime.fromisoformat(cell_value)
                        cell_value = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pass

                # Format status
                if column == "status":
                    if cell_value == "available":
                        cell_value = f"[green]{cell_value}[/green]"
                    else:
                        cell_value = f"[yellow]{cell_value}[/yellow]"

                row.append(str(cell_value))
            table.add_row(*row)

        self.console.print(table)

    def _display_dict(self, data: dict[str, Any]) -> None:
        """
        Display dictionary data in a formatted way.

        Args:
            data: Dictionary to display
        """
        table = Table(show_header=False, box=None)
        table.add_column("Field", style="bold blue")
        table.add_column("Value")

        for key, value in data.items():
            # Format the key
            formatted_key = key.replace("_", " ").title()

            # Format the value
            formatted_value = value
            if isinstance(value, str) and "T" in value:
                try:
                    dt = datetime.fromisoformat(value)
                    formatted_value = dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass

            if key == "status":
                if value == "available":
                    formatted_value = f"[green]{value}[/green]"
                else:
                    formatted_value = f"[yellow]{value}[/yellow]"

            table.add_row(formatted_key, str(formatted_value))

        self.console.print(table)


class MultiOutput(OutputFormatter):
    """Output formatter that combines multiple formatters."""

    def __init__(self, *formatters: OutputFormatter) -> None:
        """
        Initialize with multiple formatters.

        Args:
            formatters: Output formatters to combine
        """
        self.formatters = formatters

    def display(self, result: CommandResult) -> None:
        """Display using all formatters."""
        for formatter in self.formatters:
            formatter.display(result)

    def error(self, message: str) -> None:
        """Display error using all formatters."""
        for formatter in self.formatters:
            formatter.error(message)
