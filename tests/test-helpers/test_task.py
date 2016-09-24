import mock
import pytest
import os
import helpers.task
import helpers.env
from commands.command import Command

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_config()


@pytest.mark.helpers
class TestTask:

    def test_not_callable(self):
        task = helpers.task.Task(env, 'test_not_callable')
        task.set_log()
        assert task.is_runnable("shit") is False

    def test_callable(self):
        task = helpers.task.Task(env, 'test_callable')
        task.set_log()
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
        # log to global log (config:env.pro)
        c1.set_log()
        c2.set_log()
        c3.set_log()
        task.add_task(c1, sequential=False)
        task.add_task(c2, sequential=False)
        task.add_task(c3, sequential=False)
        task.set_log()
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
        # log to global log (config:env.pro)
        c1.set_log()
        c2.set_log()
        c3.set_log()
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        task.set_log()
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
        c1.set_log(consolidate=False)
        c2.set_log(consolidate=False)
        c3.set_log(consolidate=False)
        # each command write to the task log file too
        c1.set_log(consolidate=False, l_file=task.log_file)
        c2.set_log(consolidate=False, l_file=task.log_file)
        c3.set_log(consolidate=False, l_file=task.log_file)
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        task.set_log(consolidate=False)
        task2 = helpers.task.Task(env, 'test_log_tasks_2')
        c4 = Command(env, 'c4_log')
        c4.set_command('echo Im special one')
        c4.set_log(consolidate=False)
        c4.set_log(consolidate=False, l_file=task2.log_file)
        c4.set_log(consolidate=False, l_file=task.log_file)
        task2.add_task(c4)
        task2.set_log(consolidate=False)
        task2.set_log(consolidate=False, l_file=task.log_file)
        task.add_task(task2)
        task.run()

    @pytest.mark.trylast
    @pytest.mark.tasklogconsolidate
    def test_log_hierarchy(self):
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
        c1.set_log()
        c2.set_log()
        c3.set_log()
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        task.set_log()
        task2 = helpers.task.Task(env, 'test_log_tasks_2')
        c4 = Command(env, 'c4_log')
        c4.set_command('echo Im special one')
        c4.set_log()
        task2.add_task(c4)
        task2.set_log()
        task.add_task(task2)
        task.run()