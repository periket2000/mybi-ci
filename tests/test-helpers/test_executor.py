__author__ = 'marcoantonioalberoalbero'
import pytest
import os
import helpers.env
from helpers.executor import Executor

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_config()


@pytest.mark.executor
class TestExecutor:

    def test_executor(self):
        build_file = os.path.dirname(os.path.realpath(__file__)) + "/../builds/build1.json"
        with pytest.raises(SystemExit) as cm:
            Executor().run(["-b", build_file])
        assert cm.value.code == 0