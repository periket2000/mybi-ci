import mock
import pytest
import os
import helpers.task
import helpers.env

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'


class TestTask:

    def test_init(self):
        env = helpers.env.read_env()
        task = helpers.task.Task(env, 'task1')
        task.test()
