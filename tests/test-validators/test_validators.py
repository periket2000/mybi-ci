__author__ = 'marcoantonioalberoalbero'

import pytest
import os
import helpers.env
from validators.json_validator import JsonValidator


os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_config()


@pytest.mark.validators
class TestValidators:

    schema = {
        "type": "array",
        "items": {"type": "number", "enum": [1, 2, 3]},
        "minItems": 3,
    }
    json_not_valid = ["spam", 2]
    json_valid = [1, 2, 1]

    def test_json_not_valid(self):
        result = JsonValidator.validate(TestValidators.json_not_valid, TestValidators.schema)
        assert result['valid'] is False

    def test_json_valid(self):
        result = JsonValidator.validate(TestValidators.json_valid, TestValidators.schema)
        assert result['valid'] is True
