import mock
import pytest
import os
from commands.command import Command
import helpers.env

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_config()


@pytest.mark.commands
class TestCommand:

    @pytest.mark.skip
    def test_run_mvn(self):
        command = Command(env, 'command.mvn')
        command.add_env_var('MAVEN_HOME', '/Users/marcoantonioalberoalbero/Documents/OHIM/bin/apache-maven-3.3.9')
        command.set_command('cd /Users/marcoantonioalberoalbero/Documents/OHIM/src/SP-FO-1.0.0-JAVA8-SPRING4-UPGRADE/external && mvn test')
        command.run()

    def test_run_ls(self):
        command = Command(env, 'command.ls')
        command.add_env_var('MYENV_VAR', 'ROCK!')
        command.set_command('ls -l')
        command.run()