# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["EventListParams"]


class EventListParams(TypedDict, total=False):
    channel: List[str]
    """Filtering by multiple channel ids.

    Usage: `?channel=01J8J4RXH778XB056JS088PCYT&channel=01J8J4S1R1G9EVN62RG23A9M6J`
    """

    feature: List[str]
    """Filtering by multiple feature ids or keys.

    Usage: `?feature=feature-1&feature=feature-2`
    """

    from_: Annotated[Union[str, datetime], PropertyInfo(alias="from", format="iso8601")]
    """Start date-time in RFC 3339 format. Inclusive."""

    order: Literal["ASC", "DESC"]
    """The order direction."""

    order_by: Annotated[Literal["id", "createdAt"], PropertyInfo(alias="orderBy")]
    """The order by field."""

    page: int
    """Start date-time in RFC 3339 format.

    Inclusive.
    """

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """Number of items per page.

    Default is 100.
    """

    rule: List[str]
    """Filtering by multiple rule ids.

    Usage: `?rule=01J8J2XYZ2N5WBYK09EDZFBSZM&rule=01J8J4R4VZH180KRKQ63NB2VA5`
    """

    subject: List[str]
    """Filtering by multiple subject ids or keys.

    Usage: `?subject=subject-1&subject=subject-2`
    """

    to: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """End date-time in RFC 3339 format. Inclusive."""
