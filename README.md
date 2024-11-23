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

## Usage

```bash
python src/main.py
```

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
mypy src tests

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
