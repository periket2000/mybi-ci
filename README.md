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

### Notes on Logging

1. Commands and Tasks name should be unique because if not, the loggers are going to log several times

```python
# if we run
c1 = Command(env, 'c1')
c1.set_command('ls')
...
c1.run()

# and in other part of the program we run
cn = Command(env, 'c1')
cn.set_command('du -h')
...
cn.run()

# cn is going to be logged twice!!!
# because the logger is defined twice.
# c1.logger is called "MYBI-CI.commands.command.c1"
# cn.logger is called "MYBI-CI.commands.command.c1"
```

2. By default, each Task/Command comes with its own log file configured when the object is created.
We can add a new logger file (for example the global log or the parent task log) with the method
task.set_log() for the global log or task.set_log(log_dir='/tmp', log_file='shit.log' for a new file
(could be the parent log).

```python
task = Task(config, name) -> comes with its own log file configured (based on the name and config)
cmd = Command(config, name) -> comes with its own log file configured (based on the name and config)
```

3. We can onsolidate logs on the set_log only file with the flag consolidate (True by default)

```python
task.set_log(consolidate=False) -> writes to it's own file and to the global file.
command.set_log(consolidate=False) -> idem
task.set_log(log_dir='/tmp', log_file='other.log', consolidate=False) -> writes to it's own file and to /tmp/other.log
...
task.set_log() / task.set_log(consolidate=True) -> writes to the global file.
command.set_log() / command.set_log(consolidate=True) -> idem
task.set_log(log_dir='/tmp', log_file='other.log') / task.set_log(log_dir='/tmp', log_file='other.log', consolidate=True) -> writes to /tmp/other.log
```

### Tests

Tests are developed with pytest and are marked by categories.
If no category is given, all tests bt those marked as skip are executed.
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

# want to see default pytest markers?
pytest --markers
```

[Mybi CI]: <https://www.mybi.es>
