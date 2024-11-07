# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["EntitlementHistoryParams"]


class EntitlementHistoryParams(TypedDict, total=False):
    subject_id_or_key: Required[Annotated[str, PropertyInfo(alias="subjectIdOrKey")]]

    window_size: Required[Annotated[Literal["MINUTE", "HOUR", "DAY"], PropertyInfo(alias="windowSize")]]
    """Windowsize"""

    from_: Annotated[Union[str, datetime], PropertyInfo(alias="from", format="iso8601")]
    """Start of time range to query entitlement: date-time in RFC 3339 format.

    Defaults to the last reset. Gets truncated to the granularity of the underlying
    meter.
    """

    to: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """End of time range to query entitlement: date-time in RFC 3339 format.

    Defaults to now. If not now then gets truncated to the granularity of the
    underlying meter.
    """

    window_time_zone: Annotated[str, PropertyInfo(alias="windowTimeZone")]
    """The timezone used when calculating the windows."""
