Project name: Foster Care Case Management System

Team number: 3

## Requirements

- Python 3.13
- pip

## Installation

1. Clone the repository:

```bash
git clone https://github.com/shriya77/F26_3354_Team03.git
```

2. Open the unit test folder:

```bash
cd F26_3354_Team03/unit-test
```

3. Create and activate a virtual environment:

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

4. Install the testing dependencies:

```bash
python -m pip install pytest==9.1.1 pytest-cov==7.1.0
```

## Environment Variables

The Placement unit tests run in memory and do not require environment variables, a database connection, or network access.

## Running the Tests

From inside the `unit-test` folder, run:

```bash
python -m pytest -v
```

To run the tests with coverage:

```bash
python -m pytest --cov=placement --cov-report=term-missing
```

The test suite contains 14 tests for the Placement unit. The reported results were 14 tests passed with 98% statement coverage.
