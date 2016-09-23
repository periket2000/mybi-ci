# [Mybi CI] command line tool

This tool is intended to provide a CI build tool for your projects.

### Installing the package locally
```python
python setup.py install
```

### Installing the package with Pypi
```python
pip install mybi-ci
```

### Executable inteface

After install the command line tool, you'll get a "mybi-ci" comman line tool ready to run.

### Tests

Tests are developed with pytest and are marked by categories.
If no category is given, all tests but those marked as skip are executed.
If a category is give, only those with the category are executed.

```python
# execute all tests but those with skip mark
pytest

# execute all test with helpers mark
pytest -m helpers

# execute all test with commands mark
pytest -m commands

# execute a set of tests (be careful with the spaces in the list of marks)
pytest -m commands,helpers
```

[Mybi CI]: <https://www.mybi.es>
