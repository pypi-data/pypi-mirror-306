# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["EventIngestResponse"]


class EventIngestResponse(BaseModel):
    id: str
    """Identifies the event."""

    source: str
    """Identifies the context in which an event happened."""

    specversion: str
    """The version of the CloudEvents specification which the event uses."""

    subject: str
    """
    Describes the subject of the event in the context of the event producer
    (identified by source).
    """

    type: str
    """
    Contains a value describing the type of event related to the originating
    occurrence.
    """

    data: Union[str, object, None] = None
    """The event payload."""

    datacontenttype: Optional[str] = None
    """Content type of the data value. Must adhere to RFC 2046 format."""

    dataschema: Optional[str] = None
    """Identifies the schema that data adheres to."""

    time: Optional[datetime] = None
    """Timestamp of when the occurrence happened. Must adhere to RFC 3339."""
