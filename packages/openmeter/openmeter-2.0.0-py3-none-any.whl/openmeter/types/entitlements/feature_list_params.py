# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["FeatureListParams"]


class FeatureListParams(TypedDict, total=False):
    include_archived: Annotated[bool, PropertyInfo(alias="includeArchived")]
    """Include archived features."""

    limit: int
    """Number of entries to return"""

    offset: int
    """Number of entries to skip"""

    order_by: Annotated[Literal["id", "createdAt", "updatedAt"], PropertyInfo(alias="orderBy")]
    """Order by field"""
