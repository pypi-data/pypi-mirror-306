# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "IndexGetResponse",
    "Configuration",
    "ConfigurationFields",
    "ConfigurationFieldsCrawlable",
    "ConfigurationFieldsFilterable",
    "ConfigurationFieldsSearchable",
    "ConfigurationIndexType",
]


class ConfigurationFieldsCrawlable(BaseModel):
    allow: List[str]


class ConfigurationFieldsFilterable(BaseModel):
    allow: List[str]


class ConfigurationFieldsSearchable(BaseModel):
    allow: List[str]


class ConfigurationFields(BaseModel):
    crawlable: ConfigurationFieldsCrawlable

    filterable: ConfigurationFieldsFilterable

    searchable: ConfigurationFieldsSearchable

    types: Dict[str, Literal["string", "int", "float", "bool", "datetime", "geo"]]


class ConfigurationIndexType(BaseModel):
    name: str

    version: str


class Configuration(BaseModel):
    fields: ConfigurationFields

    index_type: ConfigurationIndexType


class IndexGetResponse(BaseModel):
    id: str

    configuration: Configuration

    created_at: str
