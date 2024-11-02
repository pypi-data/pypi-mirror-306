# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ObjectListResponse", "Metadata", "Object", "ObjectStatus", "ObjectStatusIndex", "Pagination"]


class Metadata(BaseModel):
    count: float


class ObjectStatusIndex(BaseModel):
    id: str
    """Index ID"""

    status: Literal["UPLOADED", "PROCESSING", "READY", "ERROR", "INCOMPLETE"]
    """Index Status Type"""


class ObjectStatus(BaseModel):
    indexes: List[ObjectStatusIndex]


class Object(BaseModel):
    id: str

    date_created: str

    date_updated: str

    status: ObjectStatus

    object: Optional[builtins.object] = None


class Pagination(BaseModel):
    next: Optional[str] = None

    prev: Optional[str] = None


class ObjectListResponse(BaseModel):
    metadata: Metadata

    objects: List[Object]

    pagination: Pagination
