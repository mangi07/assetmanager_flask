https://docs.pytest.org/en/latest/getting-started.html

Tests use relative imports to import application modules tested.

Run from project root:
$ pytest tests -s -v

Optionally, test specific test file:
$ pytest tests/file_name.py -s -v

Flags:
-s for print statements in console
-v for verbose (eg: to see full diff when asserting data structure)


## File Name Convention:

test_<folder>_<file>.py

Eg: test_queries_asset_queries.py
tests the functions in ./../queries/asset_queries.py

