# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["MeterQueryParams"]


class MeterQueryParams(TypedDict, total=False):
    filter_group_by: Annotated[Dict[str, str], PropertyInfo(alias="filterGroupBy")]
    """Simple filter for group bys with exact match.

    Usage: `?filterGroupBy[type]=input&filterGroupBy[model]=gpt-4`
    """

    from_: Annotated[Union[str, datetime], PropertyInfo(alias="from", format="iso8601")]
    """Start date-time in RFC 3339 format. Inclusive."""

    group_by: Annotated[List[str], PropertyInfo(alias="groupBy")]
    """
    If not specified a single aggregate will be returned for each subject and time
    window. `subject` is a reserved group by value.
    """

    to: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """End date-time in RFC 3339 format. Inclusive."""

    window_size: Annotated[Literal["MINUTE", "HOUR", "DAY"], PropertyInfo(alias="windowSize")]
    """
    If not specified, a single usage aggregate will be returned for the entirety of
    the specified period for each subject and group.
    """

    window_time_zone: Annotated[str, PropertyInfo(alias="windowTimeZone")]
    """
    The value is the name of the time zone as defined in the IANA Time Zone Database
    (http://www.iana.org/time-zones). If not specified, the UTC timezone will be
    used.
    """
