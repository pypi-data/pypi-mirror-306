# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ChannelListParams"]


class ChannelListParams(TypedDict, total=False):
    include_deleted: Annotated[bool, PropertyInfo(alias="includeDeleted")]
    """Include deleted notification channels in response.

    Usage: `?includeDeleted=true`
    """

    include_disabled: Annotated[bool, PropertyInfo(alias="includeDisabled")]
    """Include disabled notification channels in response.

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
