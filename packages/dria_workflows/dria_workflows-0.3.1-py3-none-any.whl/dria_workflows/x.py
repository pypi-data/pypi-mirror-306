from outlines_core.fsm.json_schema import (
    build_regex_from_schema,
)
from pydantic import BaseModel, Field, constr
from typing import List, Any, Union, Type
import json


def pydantic_to_openai(model: Type[BaseModel]) -> str:
    return json.dumps(json.dumps(model.model_json_schema()))


def pydantic_to_gemini_schema(model: Type[BaseModel]) -> str:
    def convert_type(field_type: Any) -> Union[dict, str]:
        if hasattr(field_type, "__origin__"):  # For generic types like List, Dict
            if field_type.__origin__ == list:
                return {
                    "type": "ARRAY",
                    "items": {"type": convert_type(field_type.__args__[0])},
                }
            elif field_type.__origin__ == dict:
                return {
                    "type": "OBJECT",
                    "properties": {
                        "key": {"type": convert_type(field_type.__args__[0])},
                        "value": {"type": convert_type(field_type.__args__[1])},
                    },
                }

        # Basic type mapping
        type_mapping = {str: "STRING", int: "INTEGER", float: "NUMBER", bool: "BOOLEAN"}
        return type_mapping.get(field_type, "STRING")

    properties = {}
    for name, field in model.__annotations__.items():
        if isinstance(field, type):
            properties[name] = {"type": convert_type(field)}
        else:
            properties[name] = convert_type(field)

    schema = {"type": "OBJECT", "properties": properties}

    return json.dumps(schema)


def from_pydantic():
    class QuestionAnswer(BaseModel):
        my_question: str = Field(...)
        my_answer: str = Field(...)
        keywords: List[str] = Field(...)

    schema = json.dumps(QuestionAnswer.model_json_schema())
    print(schema)
    print(json.dumps(pydantic_to_gemini_schema(QuestionAnswer)))
    schedule = build_regex_from_schema(schema)
    return schedule


def pydantic_to_llama(model: Type[BaseModel]) -> str:
    schema = json.dumps(model.model_json_schema())
    schedule = build_regex_from_schema(schema)
    schedule_bytes = schedule.encode("utf-8")
    base64_bytes = base64.b64encode(schedule_bytes)
    return base64_bytes.decode("utf-8")


if __name__ == "__main__":
    import base64

    schema = from_pydantic()
    print(json.dumps(schema))

    schema_bytes = schema.encode("utf-8")

    base64_bytes = base64.b64encode(schema_bytes)

    # Step 3: Convert Base64 bytes to string
    base64_string = base64_bytes.decode("utf-8")
    print("****\n")
    print("Base64 Encoded String:", base64_string)
