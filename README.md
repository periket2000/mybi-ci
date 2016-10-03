# [Mybi CI] command line tool [![Build Status](https://travis-ci.org/periket2000/mybi-ci.svg?branch=master)](https://travis-ci.org/periket2000/mybi-ci)

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

### Runing it as server (opens a port on localhost:5000)

1. Define a configuration file with the following contents:
```sh
[global]
program=MYBI-CI
log_dir=/tmp
log_file=mybi-ci.log
log_level=
log_format=
# False, each task logs to its file and its ancestors file
# True, every task logs to the global file
log_consolidate_only=False
#server port
server_port=5000
```

2. Export the variables to point this file and load the global section:
```sh
export  MYBICI_SETUP_FILE="/PATH/TO/THE/FILE/ABOVE"
export MYBICI_SETUP_FILE_SECTIONS="global"
```

3. After this, you can run the server like this:
```python
mybi-ci -s
```

After that we can access the rest api (it's open)
```python
http://localhost:5000/
```

and this shows the API posible calls
```json
{
  "title": "Mybi-ci REST API", 
  "urls": [
    "/ (GET)", 
    "/run (POST)", 
    "/log/<build_id>/<log_file> (GET)"
  ]
}
```
and we can send build task like this (by post, try with postman or curl)

* Note: $MYBICI_BUILD_ID is a built-in variable with a unique identifier to the build.
```json
{
  "build": "My build",
  "starter": {
    "id": "My.build.starter",
    "env": [
      {
        "WORKSPACE": "/tmp",
        "MAVEN_HOME": "/maven/install/dir/apache-maven-3.3.9",
        "PATH": "$PATH:$MAVEN_HOME/bin"
      }
    ],
    "sequential_tasks": [
      {
        "id": "setup.centralized.dir",
        "cmd": "mkdir -p $WORKSPACE/$MYBICI_BUILD_ID"
      },
      {
        "id": "svn.checkout",
        "env": [{
          "USER": "username",
          "PASS": "user_password"
        }],
        "cmd": "svn co --non-interactive --trust-server-cert --username=$USER --password=$PASS https://svn_dir/trunk $WORKSPACE/$MYBICI_BUILD_ID/SVN"
      },
      {
        "id": "mvn.build",
        "cmd": "cd $WORKSPACE/$MYBICI_BUILD_ID/SVN; mvn clean install -Dmaven.test.skip=true"
      }
    ]
  }
}
```

Once executed you'll get a response like:
```json
{
    "build_id": "9760836c-8974-11e6-861c-60f81db6415a",
    "log_file": "helpers.task.Frontoffice.build.starter-2016-10-03_16:20:53.log",
    "task": "helpers.task.Frontoffice.build.starter"
}
```

And you'll be able to see the task logs with the following url:
```python
http://localhost:5000/log/<build_id>/<log_file>
http://localhost:5000/log/9760836c-8974-11e6-861c-60f81db6415a/helpers.task.Frontoffice.build.starter-2016-10-03_16:20:53.log
```

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
# because the logger is defined twice and both share the same log file
# c1.logger is called "MYBI-CI.commands.command.c1"
# cn.logger is called "MYBI-CI.commands.command.c1"
```

2. The system log is configured depending on the 'global':'log_consolidate_only' config value.
If this value is True, all the tasks and sub tasks log to the global consolidated log file.
If this value if False, all the tasks logs to its own log file and to its ancestors (not only the parent) log file.

3. By default, each Task/Command comes with its own log file configured when the object is created.
But if we choose log_consolidated_only=True, this log file is overwrite by the global system log file. 

```python
task = Task(config, name) -> comes with its own log file configured (based on the name and config)
cmd = Command(config, name) -> comes with its own log file configured (based on the name and config)
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
