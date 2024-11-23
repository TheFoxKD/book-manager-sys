# src/cli/commands/base.py

from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Any


@dataclass
class CommandResult:
    """Base class for command execution results."""

    success: bool
    message: str
    data: Any | None = None


class BaseCommand(ABC):
    """Base class for all CLI commands."""

    def __init__(self) -> None:
        self.name = self.__class__.__name__.lower().replace("command", "")

    @abstractmethod
    def configure(self, parser: ArgumentParser) -> None:
        """Configure command arguments and options."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, args: Namespace) -> CommandResult:
        """Execute the command logic."""
        raise NotImplementedError
