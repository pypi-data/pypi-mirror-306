# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EventListParams"]


class EventListParams(TypedDict, total=False):
    from_: Annotated[Union[str, datetime], PropertyInfo(alias="from", format="iso8601")]
    """Start date-time in RFC 3339 format. Inclusive."""

    limit: int
    """Number of events to return"""

    to: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """End date-time in RFC 3339 format. Inclusive."""
