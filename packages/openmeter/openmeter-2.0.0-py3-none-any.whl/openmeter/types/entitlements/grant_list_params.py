# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["GrantListParams"]


class GrantListParams(TypedDict, total=False):
    feature: List[str]
    """Filtering by multiple features.

    Usage: `?feature=feature-1&feature=feature-2`
    """

    include_deleted: Annotated[bool, PropertyInfo(alias="includeDeleted")]
    """Include deleted"""

    limit: int
    """Number of items to return.

    Default is 100.
    """

    offset: int
    """Number of items to skip.

    Default is 0.
    """

    order: Literal["ASC", "DESC"]
    """The order direction."""

    order_by: Annotated[Literal["id", "createdAt", "updatedAt"], PropertyInfo(alias="orderBy")]
    """The order by field."""

    page: int
    """Start date-time in RFC 3339 format.

    Inclusive.
    """

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """Number of items per page.

    Default is 100.
    """

    subject: List[str]
    """Filtering by multiple subjects.

    Usage: `?subject=customer-1&subject=customer-2`
    """
