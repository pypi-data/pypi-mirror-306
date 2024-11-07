# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Meter"]


class Meter(BaseModel):
    id: str
    """A unique identifier for the meter."""

    aggregation: Literal["SUM", "COUNT", "UNIQUE_COUNT", "AVG", "MIN", "MAX"]
    """The aggregation type to use for the meter."""

    event_type: str = FieldInfo(alias="eventType")
    """The event type to aggregate."""

    slug: str
    """
    A unique, human-readable identifier for the meter. Must consist only
    alphanumeric and underscore characters.
    """

    window_size: Literal["MINUTE", "HOUR", "DAY"] = FieldInfo(alias="windowSize")
    """Aggregation window size."""

    description: Optional[str] = None
    """A description of the meter."""

    group_by: Optional[Dict[str, str]] = FieldInfo(alias="groupBy", default=None)
    """Named JSONPath expressions to extract the group by values from the event data.

    Keys must be unique and consist only alphanumeric and underscore characters.

    TODO: add key format enforcement
    """

    value_property: Optional[str] = FieldInfo(alias="valueProperty", default=None)
    """
    JSONPath expression to extract the value from the ingested event's data
    property.

    The ingested value for SUM, AVG, MIN, and MAX aggregations is a number or a
    string that can be parsed to a number.

    For UNIQUE_COUNT aggregation, the ingested value must be a string. For COUNT
    aggregation the valueProperty is ignored.
    """
