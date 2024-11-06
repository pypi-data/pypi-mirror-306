import json
import os
from typing import Any, Dict, List, Set, Type, Union

from bs4 import BeautifulSoup
from loguru import logger
from openai import OpenAI
from pydantic import BaseModel, create_model

from perse import models, utils


class PerseError(Exception):
    pass


class FetchError(PerseError):
    pass


default_model = "gpt-4o-mini-2024-07-18"
default_api_key = os.getenv("PERSE_OPENAI_API_KEY")

if not default_api_key:
    default_api_key = os.getenv("OPENAI_API_KEY")


if not default_api_key:
    raise ValueError("PERSE_OPENAI_API_KEY or OPENAI_API_KEY is not set")


client = OpenAI(api_key=default_api_key)


def reduce_html_content(content: Union[str, BeautifulSoup], exclude_tags: Set[str] | None = None) -> BeautifulSoup:
    """
    Removes unnecessary tags and attributes from the HTML content.

    Args:
        content (str | BeautifulSoup): The HTML content to simmer.
        exclude_tags (Set[str]): The set of tags to exclude from the content (e.g., script, style, svg, iframe).

    Returns:
        BeautifulSoup: The cleaned HTML soup.
    """
    if not content:
        raise PerseError("HTML content is empty")

    soup = content
    if isinstance(soup, str):
        soup = BeautifulSoup(soup, "html.parser")

    if soup.body:
        utils.clean_up_beautiful_soup(soup, exclude_tags)
    return soup


def extract_relevant_fields(content: Union[str, BeautifulSoup], model: str = default_model) -> models.FieldsInfo:
    """
    Analyzes HTML content to extract field names and their data types.

    Args:
        content (str | BeautifulSoup): The HTML content to analyze which is assumed to be simmered.
        model (str): The Structured Output model that analyzes the content.
        exclude_tags (Set[str]): The set of tags to exclude from the content (e.g., script, style, svg, iframe).

    Returns:
        FieldsInfo: The extracted fields information.
    """
    if not content:
        raise ValueError("HTML content is empty")

    if isinstance(content, BeautifulSoup):
        content = content.prettify()

    logger.debug(f"Extracting relevant fields via {model}")

    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert at analyzing data. I will give you the contents of an HTML page and your goal is to come up with a list of field names and their data types, including nested structures. When selecting which fields to include, consider the following:
                - No markup or HTML tags or attributes should be included
                - For ul, ol, li tags, the data should be put into a list
                - For tables, the data should be put into a list of lists
                - Create nested structures when appropriate (e.g., for repeated elements or logical groupings)
                - Only lowest level text should be included as primitive data types
                - For images or videos, extract the url and choose a key based on context
                - List of object with single key-value pair should be simplified to a single list
                - No need to include html tags like svgs, canvas, etc.
                - For the type of data, always use a valid JSON data type (string, number, boolean, array, object)
                - Form forms, never include any styling, only the list of field names
                """,
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        response_format=models.FieldsInfo,
    )

    if not response.choices:
        raise FetchError("Field extraction failed")

    result_str = response.choices[0].message.content
    if not result_str:
        raise FetchError("Field extraction failed")

    result = json.loads(result_str)
    return models.FieldsInfo(**result)


def build_pydantic_model(fields: List[models.FieldInfo]) -> Type[BaseModel]:
    """
    Generates a Pydantic model based on the provided fields information.

    Args:
        fields_info (List[FieldInfo]): The list of fields information.

    Returns:
        Type[BaseModel]: The generated Pydantic model.
    """
    TYPE_MAPPING: Dict[str, Any] = {
        "string": str,
        "number": float,
        "boolean": bool,
        "array": List[Any],
        "object": Dict[str, Any],
    }

    fields_dict: Dict[str, Any] = {}

    for field in fields:
        if field.nested_fields:
            nested_model = build_pydantic_model(field.nested_fields)
            if field.type.lower() == "array":
                fields_dict[field.name] = (List[nested_model], ...)
            else:
                fields_dict[field.name] = (nested_model, ...)
        else:
            fields_dict[field.name] = (TYPE_MAPPING.get(field.type.lower(), Any), ...)

    return create_model("PydanticModel", **fields_dict)


def extract_json_fields(content: Union[str, BeautifulSoup], PydanticModel: Type[BaseModel], model: str = default_model) -> Dict[str, Any]:
    """
    Extracts JSON fields from HTML content using the provided Pydantic model.

    Args:
        content (str): The HTML content to extract data from.
        PydanticModel (BaseModel): The Pydantic model to follow for data extraction.
        model (str): The Structured Output model that performs the extraction.

    Returns:
        Dict[str, Any]: The extracted data as a dictionary.
    """
    if not content:
        raise ValueError("HTML content is empty")

    if isinstance(content, BeautifulSoup):
        content = content.prettify()

    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """
                You are given the contents of an HTML page. Your goal is to extract useful information from the page and fill the given DataObject type. The extracted should satisfy the following criteria:
                - No markup or HTML tags or attributes should be included
                - For ul, ol, li tags, the data should be put into JSON list
                - For tables, the data should be put into JSON list of lists
                - For all other tags, the data should be put into JSON dictionary
                - Only lowest level text should be included as primitive data types
                - For images or videos, extract the url and choose a key based on context
                - No need to include html tags like svgs, canvas, etc.
                """,
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        response_format=PydanticModel,
    )

    if not response.choices:
        raise FetchError("Data extraction failed")

    result_str = response.choices[0].message.content
    if not result_str:
        raise FetchError("Data extraction failed")

    result = json.loads(result_str)

    json_data = PydanticModel(**result)
    return utils.recursive_dump_base_model(json_data)


def perse(content: str, exclude_tags: Set[str] | None = None) -> Dict[str, Any]:
    """
    Processes HTML content to extract structured data.

    Args:
        content (str): The HTML content to process.
        exclude_tags (Set[str]): The set of tags to exclude from the content (e.g., script, style, svg, iframe).

    Returns:
        Dict[str, Any]: The extracted structured data in dictionary format.
    """

    cleaned_soup = reduce_html_content(content=content, exclude_tags=exclude_tags)
    if not cleaned_soup:
        raise PerseError("Could not reduce HTML content")

    cleaned_content = cleaned_soup.prettify()
    logger.debug(f"Successfully loaded HTML context of size {utils.format_user_friendly_bytes(len(cleaned_content))}")

    relevant_fields = extract_relevant_fields(content=cleaned_content)
    if not relevant_fields:
        raise PerseError("Could not extract relevant fields")

    fields = relevant_fields.fields
    logger.debug(f"Identified {len(fields)} top-level fields: {', '.join([f.name for f in fields])}")

    PydanticModel = build_pydantic_model(fields=relevant_fields.fields)
    logger.debug("Successfully generated strictly typed data model")
    if not PydanticModel:
        raise PerseError("Could not build data model")

    logger.debug(f"Now performing data extraction using {default_model}")
    json_data = extract_json_fields(content, PydanticModel)
    if not json_data:
        raise PerseError("Could not extract data from HTML")

    return json_data


def perses(content: str, exclude_tags: Set[str] | None = None, indent: int = 2) -> str:
    """
    Processes HTML content and returns the extracted data as a JSON string.

    Args:
        content (str): The HTML content to process.
        exclude_tags (Set[str]): The set of tags to exclude from the content (e.g., script, style, svg, iframe).
        indent (int): The number of spaces to indent the JSON output.
    Returns:
        str: The extracted data in marshalled JSON string format.
    """
    return json.dumps(perse(content, exclude_tags), indent=indent)


if __name__ == "__main__":
    print(perses(open("./tests/input.html", "r", encoding="utf-8").read()))
