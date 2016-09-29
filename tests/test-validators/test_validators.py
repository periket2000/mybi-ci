__author__ = 'marcoantonioalberoalbero'

import pytest
import os
import helpers.env
from validators.json_validator import JsonValidator
from validators.tasks_schema import TasksSchema
import json


os.environ['MYBICI_SETUP_FILE'] = os.path.dirname(os.path.realpath(__file__)) + '/../../conf/env.pro'
os.environ['MYBICI_SETUP_FILE_SECTIONS'] = 'global'
env = helpers.env.read_config()


@pytest.mark.validators
class TestValidators:
    schema2 = {
        "type": "string",
        "pattern": "^[a-z]+$"
    }
    json_not_valid = "a_b"
    json_valid = "ab"

    def test_json_not_valid(self):
        result = JsonValidator.validate(TestValidators.json_not_valid, TestValidators.schema2)
        assert result['valid'] is False

    def test_json_valid(self):
        result = JsonValidator.validate(TestValidators.json_valid, TestValidators.schema2)
        assert result['valid'] is True

    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "definitions": {
            "identifier": {
                "type": "string",
                "pattern": "^[A-Za-z0-9\\.-_]+$"
            },
            "task": {
                "type": "object",
                "properties": {
                    "id": {"$ref": "#/definitions/identifier"},
                    "env": {
                        "type": "array",
                        "items": {
                            "property": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string"
                            }
                        }
                    },
                    "parallel_tasks": {
                        "type": "array",
                        "items": {
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
                        "items": {
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
                    "id": {"$ref": "#/definitions/identifier"},
                    "env": {
                        "type": "array",
                        "items": {
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
            "id": "My_task_identifier.123",
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

    json_build7 = {
        "build": "my brand new build",
        "starter": {
            "id": "My_task_id_125.task",
            "parallel_tasks": [
                {
                    "id": "command ls",
                    "env": [
                        {"DIR": "/tmp"},
                        {"FILE": "*"}
                    ],
                    "cmd": "ls $DIR/$FILE"
                },
                {
                    "id": "command df",
                    "cmd": "df -h"
                }
            ]
        }
    }

    json_build8 = {
        "build": "my brand new build",
        "starter": {
            "id": "wrong id",
            "cmd": "ls -l"
        }
    }

    json_build9 = {
        "build": "my brand new build",
        "starter": {
            "id": "1id",
            "env": []
        }
    }

    def test_json_build(self):
        result = JsonValidator.validate(TestValidators.json_build, TestValidators.schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build2, TestValidators.schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build3, TestValidators.schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build4, TestValidators.schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build5, TestValidators.schema)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build6, TestValidators.schema)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build8, TestValidators.schema)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build7, TestValidators.schema)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build9, TestValidators.schema)
        assert result['valid'] is False

    def test_json_from_schema_file(self):
        result = JsonValidator.validate(TestValidators.json_build, TasksSchema.schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build2, TasksSchema.schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build3, TasksSchema.schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build4, TasksSchema.schema)
        assert result['valid'] is True
        result = JsonValidator.validate(TestValidators.json_build5, TasksSchema.schema)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build6, TasksSchema.schema)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build7, TasksSchema.schema)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build8, TestValidators.schema)
        assert result['valid'] is False
        result = JsonValidator.validate(TestValidators.json_build9, TestValidators.schema)
        assert result['valid'] is False

    def test_json_file_from_schema_file(self):
        schema_file = os.path.dirname(os.path.realpath(__file__)) + "/../builds/schema.json"
        with open(schema_file) as data_file:
            schema = json.load(data_file)
        build_file = os.path.dirname(os.path.realpath(__file__)) + "/../builds/build1.json"
        with open(build_file) as data_file:
            build = json.load(data_file)
        result = JsonValidator.validate(build, schema)
        assert result['valid'] is True

    def test_json_file_from_schema_file_local(self):
        schema_file = os.path.dirname(os.path.realpath(__file__)) + "/schema.json"
        with open(schema_file) as data_file:
            schema = json.load(data_file)
        build_file = os.path.dirname(os.path.realpath(__file__)) + "/build1.json"
        with open(build_file) as data_file:
            build = json.load(data_file)
        result = JsonValidator.validate(build, schema)
        assert result['valid'] is False