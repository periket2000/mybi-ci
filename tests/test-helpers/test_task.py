import mock
import pytest
import os
import helpers.task
import helpers.env
from commands.command import Command
from helpers.constants import Constants

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_config()


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
    @pytest.mark.taskpar
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

    @pytest.mark.seq_task_ko
    def test_sequential_ko(self):
        task = helpers.task.Task(env, 'test_parallel_tasks_ko')
        c3 = Command(env, 'c3_parallel_ko')
        c3.set_command('echo Hi!')
        task.add_task(c3, sequential=False)
        task2 = helpers.task.Task(env, 'test_log_tasks_2_ko')
        c4 = Command(env, 'c4_ko')
        c4.set_command('this.is.failing')
        task2.add_task(c4)
        task.add_task(task2)
        task.run()
        assert task.finish_status != Constants.CMD_OK

    @pytest.mark.tryfirst
    @pytest.mark.par_task_ko
    def test_parallel_ko(self):
        task = helpers.task.Task(env, 'test_parallel_tasks_ko')
        c3 = Command(env, 'c3_parallel_ko')
        c3.set_command('this.is.failing')
        task.add_task(c3, sequential=False)
        task2 = helpers.task.Task(env, 'test_log_tasks_2_ko')
        c4 = Command(env, 'c4_ko')
        c4.set_command('echo Hi!')
        task2.add_task(c4)
        task.add_task(task2)
        task.run()
        assert task.finish_status != Constants.CMD_OK

    """
    log comes ordered sequentially
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
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        task.run()

    @pytest.mark.consolidated_log
    def test_log_consolidate(self):
        """
        Complete logging, automatic config
        """
        env['global']['log_consolidate_only'] = "True"
        task = helpers.task.Task(env, 'test_log_tasks')
        c1 = Command(env, 'c1_log')
        c1.set_command('ls -l')
        c2 = Command(env, 'c2_log')
        c2.set_command('df -h')
        c3 = Command(env, 'c3_log')
        c3.set_command('echo Hi!')
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        task2 = helpers.task.Task(env, 'test_log_tasks_2')
        c4 = Command(env, 'c4_log')
        c4.set_command('echo Im special one')
        task2.add_task(c4)
        task.add_task(task2)
        task.run()

    @pytest.mark.hierarchy_log
    def test_log_hierarchy(self):
        """
        Complete logging, automatic config
        """
        env['global']['log_consolidate_only'] = "False"
        task = helpers.task.Task(env, 'test_log_tasks')
        c1 = Command(env, 'c1_log')
        c1.set_command('ls -l')
        c2 = Command(env, 'c2_log')
        c2.set_command('df -h')
        c3 = Command(env, 'c3_log')
        c3.set_command('echo Hi!')
        task.add_task(c1)
        task.add_task(c2)
        task.add_task(c3)
        task2 = helpers.task.Task(env, 'test_log_tasks_2')
        c4 = Command(env, 'c4_log')
        c4.set_command('echo Im special one')
        task2.add_task(c4)
        task.add_task(task2)
        task.run()