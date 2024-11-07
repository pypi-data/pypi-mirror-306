# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from .feature import Feature
from ..._models import BaseModel

__all__ = ["ListFeaturesResult", "FeaturePaginatedResponse"]


class FeaturePaginatedResponse(BaseModel):
    items: List[Feature]
    """The items in the current page."""

    page: int
    """The items in the current page."""

    page_size: int = FieldInfo(alias="pageSize")
    """The items in the current page."""

    total_count: int = FieldInfo(alias="totalCount")
    """The items in the current page."""


ListFeaturesResult: TypeAlias = Union[List[Feature], FeaturePaginatedResponse]
