# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["EventIngestParams"]


class EventIngestParams(TypedDict, total=False):
    id: Required[str]
    """Identifies the event."""

    source: Required[str]
    """Identifies the context in which an event happened."""

    specversion: Required[str]
    """The version of the CloudEvents specification which the event uses."""

    subject: Required[str]
    """
    Describes the subject of the event in the context of the event producer
    (identified by source).
    """

    type: Required[str]
    """
    Contains a value describing the type of event related to the originating
    occurrence.
    """

    data: Union[str, object, None]
    """The event payload."""

    datacontenttype: Optional[str]
    """Content type of the data value. Must adhere to RFC 2046 format."""

    dataschema: Optional[str]
    """Identifies the schema that data adheres to."""

    time: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Timestamp of when the occurrence happened. Must adhere to RFC 3339."""
