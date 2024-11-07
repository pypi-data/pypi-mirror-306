# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Subject"]


class Subject(BaseModel):
    id: str
    """A unique identifier for the subject."""

    key: str
    """A unique, human-readable identifier for the subject."""

    current_period_end: Optional[datetime] = FieldInfo(alias="currentPeriodEnd", default=None)
    """
    [RFC3339](https://tools.ietf.org/html/rfc3339) formatted date-time string in
    UTC.
    """

    current_period_start: Optional[datetime] = FieldInfo(alias="currentPeriodStart", default=None)
    """
    [RFC3339](https://tools.ietf.org/html/rfc3339) formatted date-time string in
    UTC.
    """

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)
    """A human-readable display name for the subject."""

    metadata: Optional[Dict[str, object]] = None

    stripe_customer_id: Optional[str] = FieldInfo(alias="stripeCustomerId", default=None)
