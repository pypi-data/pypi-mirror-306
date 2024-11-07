# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["NotificationRule", "Channel", "Threshold", "Feature"]


class Channel(BaseModel):
    id: str
    """Identifies the notification channel."""

    type: Literal["WEBHOOK"]
    """Type of the notification channel."""


class Threshold(BaseModel):
    type: Literal["PERCENT", "NUMBER"]
    """Type of the rule in the balance threshold specification."""

    value: float
    """Value of the threshold."""


class Feature(BaseModel):
    id: str
    """Unique identifier of a feature."""

    key: str
    """
    The key is an immutable unique identifier of the feature used throughout the
    API, for example when interacting with a subject's entitlements.
    """


class NotificationRule(BaseModel):
    id: str
    """Identifies the notification rule."""

    channels: List[Channel]
    """List of notification channels the rule applies to."""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Timestamp of when the resource was created."""

    name: str
    """The user friendly name of the notification rule."""

    thresholds: List[Threshold]
    """List of thresholds the rule suppose to be triggered."""

    type: Literal["entitlements.balance.threshold"]
    """Notification rule type."""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Timestamp of when the resource was last updated."""

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)
    """Timestamp of when the resource was permanently deleted."""

    disabled: Optional[bool] = None
    """Whether the rule is disabled or not."""

    features: Optional[List[Feature]] = None
    """Optional field containing list of features the rule applies to."""
