from typing import List, Union

from pydantic import BaseModel


class FieldInfo(BaseModel):
    """
    Represents information about a single field, including its name, type, and any nested fields.
    """

    name: str
    type: str
    nested_fields: Union[List["FieldInfo"], None] = None


class FieldsInfo(BaseModel):
    """
    Contains a list of FieldInfo instances representing the fields' structure.
    """

    fields: List[FieldInfo]
