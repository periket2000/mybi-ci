import mock
import pytest
import os
import helpers.task
import helpers.env
from commands.command import Command
from helpers.logging import Log

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_config()


@pytest.mark.helpers
class TestTask:

    def test_not_callable(self):
        task = helpers.task.Task(env, 'test_not_callable')
        Log.set_log(task)
        assert task.is_runnable("shit") is False

    def test_callable(self):
        task = helpers.task.Task(env, 'test_callable')
        Log.set_log(task)
        assert task.is_runnable(task) is True

    """
    log comes without any order, log_file=None -> general log
    """
    @pytest.mark.tryfirst
    @pytest.mark.taskpar
    def test_parallel(self):
        task = helpers.task.Task(env, 'test_parallel_tasks')
        c1 = Command(env, 'c1_parallel')
        c1.set_command('ls -l')
        c2 = Command(env, 'c2_parallel')
        c2.set_command('df -h')
        c3 = Command(env, 'c3_parallel')
        c3.set_command('echo Hi!')
        # log to global log (consolidate_only=True)
        Log.set_log(c1)
        Log.set_log(c2)
        Log.set_log(c3)
        task.add_task(c1, sequential=False)
        task.add_task(c2, sequential=False)
        task.add_task(c3, sequential=False)
        Log.set_log(task)
        task.run()

    """
    log comes ordered sequentially, log_file=None -> general log
    """
    @pytest.mark.trylast
    @pytest.mark.taskseq
    def test_sequential(self):
        task = helpers.task.Task(env, 'test_sequential_tasks')
        c1 = Command(env, 'c1_sequential')
        c1.set_command('ls -l')
        c2 = Command(env, 'c2_sequential')
        c2.set_command('df -h')
        c3 = Command(env, 'c3_sequential')
        c3.set_command('echo Hi!')
        # log to global log (consolidate_only=True)
        Log.set_log(c1)
        Log.set_log(c2)
        Log.set_log(c3)
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        Log.set_log(task)
        task.run()

    @pytest.mark.trylast
    @pytest.mark.tasklog
    def test_log_hierarchy(self):
        """
        Complete logging, each task/command writes to its own file,
        the commands to its parent task, and everyone to the consolidated log.
        """
        task = helpers.task.Task(env, 'test_log_tasks')
        c1 = Command(env, 'c1_log')
        c1.set_command('ls -l')
        c2 = Command(env, 'c2_log')
        c2.set_command('df -h')
        c3 = Command(env, 'c3_log')
        c3.set_command('echo Hi!')
        # each command write to its own file and to the global file
        Log.set_log(c1, consolidate_only=False)
        Log.set_log(c2, consolidate_only=False)
        Log.set_log(c3, consolidate_only=False)
        # each command write to the task log file too
        Log.set_log(c1, consolidate_only=False, l_file=task.log_file)
        Log.set_log(c2, consolidate_only=False, l_file=task.log_file)
        Log.set_log(c3, consolidate_only=False, l_file=task.log_file)
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        Log.set_log(task, consolidate_only=False)
        task2 = helpers.task.Task(env, 'test_log_tasks_2')
        c4 = Command(env, 'c4_log')
        c4.set_command('echo Im special one')
        Log.set_log(c4, consolidate_only=False)
        Log.set_log(c4, consolidate_only=False, l_file=task2.log_file)
        Log.set_log(c4, consolidate_only=False, l_file=task.log_file)
        task2.add_task(c4)
        Log.set_log(task2, consolidate_only=False)
        Log.set_log(task2, consolidate_only=False, l_file=task.log_file)
        task.add_task(task2)
        task.run()

    @pytest.mark.trylast
    @pytest.mark.tasklogconsolidate
    def test_log_consolidate(self):
        """
        Complete logging, all consolidated
        """
        task = helpers.task.Task(env, 'test_log_tasks')
        c1 = Command(env, 'c1_log')
        c1.set_command('ls -l')
        c2 = Command(env, 'c2_log')
        c2.set_command('df -h')
        c3 = Command(env, 'c3_log')
        c3.set_command('echo Hi!')
        # each command write to the global file
        Log.set_log(c1)
        Log.set_log(c2)
        Log.set_log(c3)
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        Log.set_log(task)
        task2 = helpers.task.Task(env, 'test_log_tasks_2')
        c4 = Command(env, 'c4_log')
        c4.set_command('echo Im special one')
        Log.set_log(c4)
        task2.add_task(c4)
        Log.set_log(task2)
        task.add_task(task2)
        task.run()