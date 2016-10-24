# [Mybi CI] command line tool [![Build Status](https://travis-ci.org/periket2000/mybi-ci.svg?branch=master)](https://travis-ci.org/periket2000/mybi-ci)

This tool is intended to provide a CI build tool for your projects.

## Options for running the tool

### 1. Running it as a develoer

Clone the repository.

```sh
# Create a virtualenv and activate it with python 3.5 or python 2.7
# get into the project dir
cd mybi-ci
# setup environment
export  MYBICI_SETUP_FILE=$PWD/env.pro
export MYBICI_SETUP_FILE_SECTIONS=global
export PYTHONPATH=$PWD/src:$PYTHONPATH
# install dependencies
pip install -f requirements.txt
# run tests
pytest
# run the tool
python ./bin/mybi-ci
```

### 2. Installing the package locally
```python
python setup.py install
```

### 3. Installing the package with Pypi
```python
pip install mybi-ci
```

## Mandatory setup

### Configuration file

* Define a configuration file with the following contents:
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

* Export the variables to point this file and load the global section:
```sh
export  MYBICI_SETUP_FILE="/PATH/TO/THE/FILE/ABOVE"
export MYBICI_SETUP_FILE_SECTIONS="global"
```

## Running modes

### 1. Execute Standalone tasks from a definition files

```sh
# test mode (only check if the build definition is ok)
mybi-ci -t <build_file>

# build mode (starts the building)
mybi-ci -b <build_file>
```

### 2. Runing it as server accepting json tasks (opens a port on localhost:5000)

You can run the server like this:
```sh
mybi-ci -s
```

After that we can access the rest api (it's open)
```sh
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
```sh
http://localhost:5000/log/<build_id>/<log_file>
http://localhost:5000/log/9760836c-8974-11e6-861c-60f81db6415a/helpers.task.Frontoffice.build.starter-2016-10-03_16:20:53.log
```

## Misc topics

### Notes on Logging

* Commands and Tasks name should be unique because if not, the loggers are going to log several times

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

* The system log is configured depending on the 'global':'log_consolidate_only' config value.
If this value is True, all the tasks and sub tasks log to the global consolidated log file.
If this value if False, all the tasks logs to its own log file and to its ancestors (not only the parent) log file.

* By default, each Task/Command comes with its own log file configured when the object is created.
But if we choose log_consolidated_only=True, this log file is overwrite by the global system log file. 

```python
task = Task(config, name) -> comes with its own log file configured (based on the name and config)
cmd = Command(config, name) -> comes with its own log file configured (based on the name and config)
```

### Tests

Tests are developed with pytest and are marked by categories.
If no category is given, all tests bt those marked as skip are executed.
If a category is give, only those with the category are executed.

```sh
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
