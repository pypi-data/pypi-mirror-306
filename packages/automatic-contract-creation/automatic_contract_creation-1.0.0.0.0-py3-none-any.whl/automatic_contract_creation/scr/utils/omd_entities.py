from pydantic import ConfigDict
from pydantic import BaseModel as PydanticBaseModel
from typing import Optional, Sequence

class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        populate_by_name=True,  # allow to use field name or alias to populate a model
        frozen=True,  # make instance immutable and hashable
    )
class ColumnTable(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Table(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    fullyQualifiedName: Optional[str] = None
    columns: Optional[Sequence[ColumnTable]] = None
