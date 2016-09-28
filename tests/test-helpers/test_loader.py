import pytest
import os
import helpers.task
import helpers.env
import json
from validators.json_validator import JsonValidator
from helpers.loader import Loader

os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_config()


@pytest.mark.loader
class TestLoader:

    def test_load_build1(self):
        t = None
        schema_file = os.path.dirname(os.path.realpath(__file__)) + "/../builds/schema.json"
        with open(schema_file) as data_file:
            schema = json.load(data_file)
        build_file = os.path.dirname(os.path.realpath(__file__)) + "/../builds/build1.json"
        with open(build_file) as data_file:
            build = json.load(data_file)
        result = JsonValidator.validate(build, schema)
        if result['valid']:
            t = Loader.load(build["starter"])
        assert t is not None