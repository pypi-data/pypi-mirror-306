# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["MeterQueryResult", "Data"]


class Data(BaseModel):
    value: float

    window_end: datetime = FieldInfo(alias="windowEnd")

    window_start: datetime = FieldInfo(alias="windowStart")

    group_by: Optional[Dict[str, str]] = FieldInfo(alias="groupBy", default=None)

    subject: Optional[str] = None
    """The subject of the meter value."""


class MeterQueryResult(BaseModel):
    data: List[Data]

    from_: Optional[datetime] = FieldInfo(alias="from", default=None)

    to: Optional[datetime] = None

    window_size: Optional[Literal["MINUTE", "HOUR", "DAY"]] = FieldInfo(alias="windowSize", default=None)
    """Aggregation window size."""
