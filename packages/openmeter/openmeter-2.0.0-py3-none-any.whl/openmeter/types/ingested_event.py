# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["IngestedEvent", "Event"]


class Event(BaseModel):
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


class IngestedEvent(BaseModel):
    event: Event
    """CloudEvents Specification JSON Schema"""

    ingested_at: datetime = FieldInfo(alias="ingestedAt")
    """The date and time the event was ingested."""

    stored_at: datetime = FieldInfo(alias="storedAt")
    """The date and time the event was stored."""

    validation_error: Optional[str] = FieldInfo(alias="validationError", default=None)
    """The validation error if the event failed validation."""
