# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .notification_event import NotificationEvent

__all__ = ["EventListResponse"]


class EventListResponse(BaseModel):
    items: List[NotificationEvent]
    """The items in the current page."""

    page: int
    """The items in the current page."""

    page_size: int = FieldInfo(alias="pageSize")
    """The items in the current page."""

    total_count: int = FieldInfo(alias="totalCount")
    """The items in the current page."""
