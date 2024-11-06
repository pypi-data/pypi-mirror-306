# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["IndexFinetuneParams", "Feedback"]


class IndexFinetuneParams(TypedDict, total=False):
    feedback: Required[Iterable[Feedback]]


class Feedback(TypedDict, total=False):
    query: Required[str]

    label: Literal["GREAT", "OK", "BAD"]

    object_id: str
