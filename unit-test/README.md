# Placement Unit Tests

Unit test code for the Foster Care Case Management System final report, Section 4.

The unit under test is the `Placement` class from the class diagram (Section 2.5.2). It covers adding a placement, ending the current placement, and viewing placement history (FR04, FR05, FR06, NFR03, NFR13).

## Files

| File                | What it holds                                 |
| `placement.py`      | The unit: the `Placement` class and its rules |
| `test_placement.py` | 14 automated test cases, TC-1 to TC-14        |
| `requirements.txt`  | Test dependencies                             |

## Run the tests locally

1. Install Python 3.10 or newer from https://www.python.org/downloads/. On Windows, check "Add Python to PATH" during setup.
2. Open a terminal in this folder.
3. Install the dependencies:

   python -m pip install -r requirements.txt

4. Run the tests:

   python -m pytest -v

5. Run the tests with a coverage report:

   python -m pytest -v --cov=placement --cov-report=term-missing

## Environment variables

None. The unit runs in memory and does not connect to a database or network.

## Expected result

All 14 tests pass. Line coverage of `placement.py` is 98%.
