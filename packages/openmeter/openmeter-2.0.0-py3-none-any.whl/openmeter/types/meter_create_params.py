# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["MeterCreateParams"]


class MeterCreateParams(TypedDict, total=False):
    aggregation: Required[Literal["SUM", "COUNT", "UNIQUE_COUNT", "AVG", "MIN", "MAX"]]
    """The aggregation type to use for the meter."""

    event_type: Required[Annotated[str, PropertyInfo(alias="eventType")]]
    """The event type to aggregate."""

    slug: Required[str]
    """
    A unique, human-readable identifier for the meter. Must consist only
    alphanumeric and underscore characters.
    """

    window_size: Required[Annotated[Literal["MINUTE", "HOUR", "DAY"], PropertyInfo(alias="windowSize")]]
    """Aggregation window size."""

    description: str
    """A description of the meter."""

    group_by: Annotated[Dict[str, str], PropertyInfo(alias="groupBy")]
    """Named JSONPath expressions to extract the group by values from the event data.

    Keys must be unique and consist only alphanumeric and underscore characters.

    TODO: add key format enforcement
    """

    value_property: Annotated[str, PropertyInfo(alias="valueProperty")]
    """
    JSONPath expression to extract the value from the ingested event's data
    property.

    The ingested value for SUM, AVG, MIN, and MAX aggregations is a number or a
    string that can be parsed to a number.

    For UNIQUE_COUNT aggregation, the ingested value must be a string. For COUNT
    aggregation the valueProperty is ignored.
    """
