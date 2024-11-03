import json
from json import JSONDecodeError
from typing import Union

from jsonschema import validate, ValidationError

task_config_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Task Configuration",
    "description": "A task configuration schema",
    "properties": {
        "task_name": {
            "type": "string",
            "description": "The name of the task."
        },
        "nodes": {
            "type": "string",
            "description": "The nodes definition of the task."
        },
        "datasource": {
            "type": "object",
            "description": "The datasource configuration.",
            "patternProperties": {
                "^.*$": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL of the database."
                        }
                    },
                    "required": ["url"]
                }
            },
            "additionalProperties": False
        },
        "drn": {
            "type": "object",
            "description": "the db reader node config",
            "properties": {
                "from_db": {
                    "type": "string",
                    "description": "The datasource name."
                },
                "from_table": {
                    "type": "string",
                    "description": "The table name to read from."
                },
                "incr_key": {
                    "type": "string",
                    "description": "The incremental key."
                },
                "incr_key_value": {
                    "type": "string",
                    "description": "The incremental key value."
                },
                "page_size": {
                    "type": "integer",
                    "description": "The page size for pagination."
                },
                "sql_template": {
                    "type": "string",
                    "description": "the sync sql format"
                }
            },
            "required": ["from_db", "from_table", "incr_key", "incr_key_value", "page_size", "sql_template"]
        },
        "dwn": {
            "type": "object",
            "description": "the db writer node",
            "properties": {
                "to_db": {
                    "type": "string",
                    "description": "The datasource name."
                },
                "to_table": {
                    "type": "string",
                    "description": "The table name to write to."
                }
            },
            "required": ["to_db", "to_table"]
        }
    },
    "required": ["task_name", "nodes",]
}


def validate_task_config_json(task_config_json: str) -> Union[str | None]:
    try:
        task_config_dict = json.loads(task_config_json)
    except JSONDecodeError as ex:
        return f'not a valid json format,error:{ex.msg}'
    try:
        validate(task_config_dict, schema=task_config_schema)
    except ValidationError as ex:
        return ex.message
    return None
