# tests/cli/test_output.py
from unittest.mock import Mock, call

from rich.table import Table

from src.cli.commands.base import CommandResult
from src.cli.output import ConsoleOutput, MultiOutput, OutputFormatter

# Constants for test assertions
EXPECTED_PRINTS_FOR_STATUS_TEST = 4  # 2 messages + 2 tables
EXPECTED_PRINTS_FOR_EMPTY_TEST = 2  # Only message printed


class TestConsoleOutput:
    """Test cases for ConsoleOutput."""

    def test_display_success_message(self, mock_console):
        """Test displaying success message."""
        output = ConsoleOutput()
        result = CommandResult(success=True, message="Test message")

        output.display(result)

        mock_console.print.assert_called_with("\n[green]Test message[/green]\n")

    def test_display_error_message(self, mock_console):
        """Test displaying error message."""
        output = ConsoleOutput()
        result = CommandResult(success=False, message="Error message")

        output.display(result)

        mock_console.print.assert_called_with("\n[red]Error: Error message[/red]\n")

    def test_display_table_data(self, mock_console, sample_data):
        """Test displaying tabular data."""
        output = ConsoleOutput()
        result = CommandResult(
            success=True, message="Found books", data=sample_data["multiple"]
        )

        output.display(result)

        # Check success message was printed
        assert mock_console.print.call_args_list[0] == call(
            "\n[green]Found books[/green]\n"
        )

        # Get the table object from the second print call
        table_call = mock_console.print.call_args_list[1]
        table = table_call[0][0]

        assert isinstance(table, Table)
        assert table.show_header is True
        assert table.header_style == "bold magenta"

    def test_display_dict_data(self, mock_console, sample_data):
        """Test displaying dictionary data."""
        output = ConsoleOutput()
        result = CommandResult(
            success=True, message="Book details", data=sample_data["single"]
        )

        output.display(result)

        # Check success message was printed
        assert mock_console.print.call_args_list[0] == call(
            "\n[green]Book details[/green]\n"
        )

        # Get the table object from the second print call
        table_call = mock_console.print.call_args_list[1]
        table = table_call[0][0]

        assert isinstance(table, Table)
        assert table.show_header is False
        assert table.box is None

    def test_display_status_formatting(self, mock_console):
        """Test status field formatting."""
        output = ConsoleOutput()

        # Test available status
        available_data = {"status": "available", "title": "Book 1"}
        output.display(
            CommandResult(success=True, message="Status test", data=available_data)
        )

        # Test borrowed status
        borrowed_data = {"status": "borrowed", "title": "Book 2"}
        output.display(
            CommandResult(success=True, message="Status test", data=borrowed_data)
        )

        # Verify both tables were printed
        assert len(mock_console.print.call_args_list) == EXPECTED_PRINTS_FOR_STATUS_TEST

    def test_empty_data_handling(self, mock_console):
        """Test handling empty data."""
        output = ConsoleOutput()

        # Test empty list
        result = CommandResult(success=True, message="No data", data=[])
        output.display(result)
        assert mock_console.print.call_count == 1  # Only message printed

        # Test None data
        result = CommandResult(success=True, message="No data", data=None)
        output.display(result)
        assert mock_console.print.call_count == EXPECTED_PRINTS_FOR_EMPTY_TEST

    def test_date_formatting(self, mock_console, sample_data):
        """Test date formatting in output."""
        output = ConsoleOutput()
        data = sample_data["single"]
        result = CommandResult(success=True, message="Test", data=data)

        output.display(result)

        table_call = mock_console.print.call_args_list[1]
        table = table_call[0][0]
        assert isinstance(table, Table)


class TestMultiOutput:
    """Tests for MultiOutput."""

    def test_multiple_formatters(self):
        """Test multiple formatter handling."""
        formatter1 = Mock(spec=OutputFormatter)
        formatter2 = Mock(spec=OutputFormatter)
        output = MultiOutput(formatter1, formatter2)
        result = CommandResult(success=True, message="Test")

        output.display(result)
        output.error("Test error")

        # Check both formatters received the calls
        for formatter in (formatter1, formatter2):
            formatter.display.assert_called_once_with(result)
            formatter.error.assert_called_once_with("Test error")

    def test_no_formatters(self):
        """Test behavior with no formatters."""
        output = MultiOutput()
        result = CommandResult(success=True, message="Test")

        # Should not raise exceptions
        output.display(result)
        output.error("Test")
