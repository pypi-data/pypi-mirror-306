from typing import Optional, Type

from pydantic import BaseModel

def model_to_field_names(model: Type[BaseModel]) -> Optional[str]:
    return  ','.join(model.model_fields.keys())

def obj_to_json(obj: Optional[BaseModel]) -> str:
    return obj.model_dump_json(exclude_none=True)