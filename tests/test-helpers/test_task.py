import mock
import pytest
import os
import helpers.task
import helpers.env

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_env()


class TestTask:
    def test_not_callable(self):
        task = helpers.task.Task(env, 'test_not_callable')
        assert task.is_runnable("shit") is False

    def test_callable(self):
        task = helpers.task.Task(env, 'test_callable')
        assert task.is_runnable(task) is True