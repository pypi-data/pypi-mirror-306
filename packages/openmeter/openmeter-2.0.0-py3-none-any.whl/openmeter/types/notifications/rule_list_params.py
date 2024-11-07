# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["RuleListParams"]


class RuleListParams(TypedDict, total=False):
    channel: List[str]
    """Filtering by multiple notifiaction channel ids.

    Usage: `?channel=01ARZ3NDEKTSV4RRFFQ69G5FAV&channel=01J8J2Y5X4NNGQS32CF81W95E3`
    """

    feature: List[str]
    """Filtering by multiple feature ids/keys.

    Usage: `?feature=feature-1&feature=feature-2`
    """

    include_deleted: Annotated[bool, PropertyInfo(alias="includeDeleted")]
    """Include deleted notification rules in response.

    Usage: `?includeDeleted=true`
    """

    include_disabled: Annotated[bool, PropertyInfo(alias="includeDisabled")]
    """Include disabled notification rules in response.

    Usage: `?includeDisabled=false`
    """

    order: Literal["ASC", "DESC"]
    """The order direction."""

    order_by: Annotated[Literal["id", "type", "createdAt", "updatedAt"], PropertyInfo(alias="orderBy")]
    """The order by field."""

    page: int
    """Start date-time in RFC 3339 format.

    Inclusive.
    """

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """Number of items per page.

    Default is 100.
    """
