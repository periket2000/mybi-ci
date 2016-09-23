import mock
import pytest
import os
import helpers.logging
import helpers.env

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'


class TestLogging:

    def test_init(self):
        log = helpers.logging.Log()
        env = helpers.env.read_env()
        logger = log.setup(env, 'helpers.logging.log')
        logger.info('Testing logger')
