# Book Manager System

[![CI](https://github.com/TheFoxKD/book-manager-sys/actions/workflows/ci.yml/badge.svg)](https://github.com/TheFoxKD/book-manager-sys/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/TheFoxKD/book-manager-sys/branch/main/graph/badge.svg)](https://codecov.io/gh/TheFoxKD/book-manager-sys)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A lightweight command-line library management system with JSON storage and intuitive CLI interface.

## Features

- Add/remove books with auto-generated IDs
- Search books by title, author, or year
- Track book availability status
- Persistent JSON storage
- Error handling and input validation
- 100% type-annotated code
- High test coverage

## Installation

```bash
git clone https://github.com/TheFoxKD/book-manager-sys.git
cd book-manager-sys
pip install -r requirements.txt
```

> **Note on dependencies**: While the core business logic has no external dependencies, we use the Rich library
> for enhanced CLI output formatting and better user experience. This design choice separates presentation concerns
> from core functionality.

## Usage Examples

> **Note**: All commands must be run from the root directory of the project (book-manager-sys) using the `-m` flag.

### Basic Usage

```bash
# Show help and available commands
python -m src.cli.app

# Add a new book
python -m src.cli.app add "The Art of Computer Programming" "Donald Knuth" 1968

# List all books
python -m src.cli.app list

# Delete a book by ID
python -m src.cli.app delete book_1633024800.123456

# Search for books
python -m src.cli.app search --title "Computer"     # Search by title
python -m src.cli.app search --author "Knuth"       # Search by author
python -m src.cli.app search --year 1968            # Search by year

# Change book status
python -m src.cli.app status book_1633024800.123456 borrowed    # Mark as borrowed
python -m src.cli.app status book_1633024800.123456 available   # Mark as available
```

### Detailed Command Reference

1. **Adding Books**
   ```bash
   # Basic add command
   python -m src.cli.app add "Clean Code" "Robert C. Martin" 2008

   # Example with a legendary programming book
   python -m src.cli.app add "Design Patterns: Elements of Reusable Object-Oriented Software" "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides" 1994
   ```
    - Titles and authors with spaces must be enclosed in quotes
    - Year must be a valid number
    - Books are automatically assigned a unique ID, e.g., book_1633024800.123456

2. **Listing Books**
   ```bash
   # List all books
   python -m src.cli.app list
   ```
    - Displays ID, title, author, year, and status
    - Books are sorted by ID by default

3. **Searching Books**
   ```bash
   # Search by title (partial match)
   python -m src.cli.app search --field title "Patterns"

   # Search by author (partial match)
   python -m src.cli.app search --field author "Martin"

   # Search by exact year
   python -m src.cli.app search --field year 2008

   ```
    - Searches are case-insensitive
    - Partial matches work for title and author
    - Year must be an exact match

4. **Managing Book Status**
   ```bash
   # Mark book as borrowed
   python -m src.cli.app status book_1633024800.123456 borrowed

   # Mark book as available
   python -m src.cli.app status book_1633024800.123456 available
   ```
    - Valid statuses are: available and borrowed
    - Requires a valid book ID

5. **Deleting Books**
   ```bash
   # Delete by ID
   python -m src.cli.app delete book_1633024800.123456
   ```
    - Deletion is permanent
    - Requires a valid book ID
    - Will fail if the ID doesn’t exist

### Error Handling

- Invalid commands show usage help
- Non-existent book IDs return appropriate error
- Invalid status values show valid options
- Missing required arguments prompt for correct usage

### Data Storage

- Books are stored in `data/books.json`
- File is created automatically on first run

## Development

### Testing and Quality Assurance

The project uses several tools to ensure code quality:

- **pytest**: For unit testing
- **mypy**: For static type checking
- **ruff**: For linting and code formatting
- **pre-commit**: For automated code quality checks

### Continuous Integration

The project uses GitHub Actions for CI/CD with the following checks:

- Code linting and formatting
- Type checking
- Unit tests with coverage reporting
- Dependency updates via Dependabot

### Pre-commit Hooks

Before committing, ensure pre-commit hooks are installed:

```bash
pip install pre-commit
pre-commit install
```

### Running Tests Locally

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=./src --cov-report=term-missing

# Run type checking
mypy src

# Run linting
ruff check .
```

## Requirements

- Python 3.12+
- No external dependencies required

## Project Structure

- `src/` - Main source code
- `data/` - JSON storage
- `tests/` - Unit tests

## License

MIT
