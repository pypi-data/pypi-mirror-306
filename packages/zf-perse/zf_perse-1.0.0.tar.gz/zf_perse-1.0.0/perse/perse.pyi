from typing import Any, Type, Union
from pydantic import BaseModel
from bs4 import BeautifulSoup

default_model = "gpt-4o-mini-2024-07-18"

def extract_json_fields(content: Union[str, BeautifulSoup], PydanticModel: Type[BaseModel], model: str = default_model) -> dict[str, Any]: ...