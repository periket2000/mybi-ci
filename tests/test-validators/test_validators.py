__author__ = 'marcoantonioalberoalbero'

import pytest
import os
import helpers.env
from validators.json_validator import JsonValidator
import json


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

    schema2 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "definitions": {
            "task": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "pattern": "^[A-Za-z0-9\\.-_]+$"
                    },
                    "parallel_tasks": {
                        "type": "array",
                        "properties": {
                            "anyOf": [
                                {
                                    "$ref": "#/definitions/task"
                                },
                                {
                                    "$ref": "#/definitions/command"
                                }
                            ]
                        }
                    },
                    "sequential_tasks": {
                        "type": "array",
                        "properties": {
                            "anyOf": [
                                {
                                    "$ref": "#/definitions/task"
                                },
                                {
                                    "$ref": "#/definitions/command"
                                }
                            ]
                        }
                    }
                },
                "required": [
                    "id"
                ],
                "anyOf": [
                    {
                        "required": ["parallel_tasks"]
                    },
                    {
                        "required": ["sequential_tasks"]
                    }
                ],
                "additionalProperties": False
            },
            "command": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "pattern": "^[A-Za-z0-9\\.-_]+$"
                    },
                    "env": {
                        "type": "array",
                        "properties": {
                            "property": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string"
                            }
                        }
                    },
                    "cmd": {
                        "type": "string"
                    }
                },
                "required": [
                    "id", "cmd"
                ],
                "additionalProperties": False
            }
        },

        "type": "object",
        "properties": {
            "build": {
                "type": "string"
            },
            "starter": {
                "anyOf": [
                    {
                        "$ref": "#/definitions/task"
                    },
                    {
                        "$ref": "#/definitions/command"
                    }
                ]
            }
        },
        "required": ["build", "starter"],
        "additionalProperties": False
    }

    json_build = {
        "build": "my brand new build",
        "starter": {
            "id": "My_task_id_125.task",
            "sequential_tasks": []
        }
    }

    json_build2 = {
        "build": "my brand new build",
        "starter": {
            "id": "My_task_id_125.task",
            "parallel_tasks": []
        }
    }

    json_build3 = {
        "build": "my brand new build",
        "starter": {
            "id": "My_task_id_125.task",
            "parallel_tasks": [],
            "sequential_tasks": []
        }
    }

    json_build4 = {
        "build": "my brand new build",
        "starter": {
            "id": "My_task_id_125.task",
            "cmd": "ls -l"
        }
    }

    json_build5 = {
        "build": "my brand new build",
        "starter": {
            "id": "My_task_id_125.task"
        }
    }

    json_build6 = {
        "build": "my brand new build",
        "starter": {
            "id": "My_task_id_125.task",
            "cmd": "ls -l"
        },
        "additional": "not allowed"
    }

    def test_json_build(self):
        result = JsonValidator.validate(TestValidators.json_build, TestValidators.schema2)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build2, TestValidators.schema2)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build3, TestValidators.schema2)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build4, TestValidators.schema2)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build5, TestValidators.schema2)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build6, TestValidators.schema2)
        assert result['valid'] is False

    def test_json_from_schema_file(self):
        schema_file = os.path.dirname(os.path.realpath(__file__)) + "/schema.json"
        with open(schema_file) as data_file:
            schema = json.load(data_file)
        result = JsonValidator.validate(TestValidators.json_build, schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build2, schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build3, schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build4, schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build5, schema)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build6, schema)
        assert result['valid'] is False

    def test_json_file_from_schema_file(self):
        schema_file = os.path.dirname(os.path.realpath(__file__)) + "/schema.json"
        with open(schema_file) as data_file:
            schema = json.load(data_file)
        build_file = os.path.dirname(os.path.realpath(__file__)) + "/build1.json"
        with open(build_file) as data_file:
            build = json.load(data_file)
        result = JsonValidator.validate(build, schema)
        assert result['valid'] is True