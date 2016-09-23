import mock
import pytest
import os
import helpers.task
import helpers.env
from commands.command import Command

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_env()


@pytest.mark.helpers
class TestTask:

    def test_not_callable(self):
        task = helpers.task.Task(env, 'test_not_callable')
        assert task.is_runnable("shit") is False

    def test_callable(self):
        task = helpers.task.Task(env, 'test_callable')
        assert task.is_runnable(task) is True

    """
    log comes without any order
    """
    @pytest.mark.tryfirst
    def test_parallel(self):
        task = helpers.task.Task(env, 'test_parallel_tasks')
        c1 = Command(env, 'c1_parallel')
        c1.set_command('ls -l')
        c2 = Command(env, 'c2_parallel')
        c2.set_command('df -h')
        c3 = Command(env, 'c3_parallel')
        c3.set_command('echo Hi!')
        task.add_task(c1, sequential=False)
        task.add_task(c2, sequential=False)
        task.add_task(c3, sequential=False)
        task.run()

    """
    log comes ordered sequentially
    """
    @pytest.mark.trylast
    def test_sequential(self):
        task = helpers.task.Task(env, 'test_sequential_tasks')
        c1 = Command(env, 'c1_sequential')
        c1.set_command('ls -l')
        c2 = Command(env, 'c2_sequential')
        c2.set_command('df -h')
        c3 = Command(env, 'c3_sequential')
        c3.set_command('echo Hi!')
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        task.run()