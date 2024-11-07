# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["NotificationChannel"]


class NotificationChannel(BaseModel):
    id: str
    """Identifies the notification channel."""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Timestamp of when the resource was created."""

    name: str
    """User friendly name of the channel."""

    type: Literal["WEBHOOK"]
    """Notification channel type."""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Timestamp of when the resource was last updated."""

    url: str
    """Webhook URL where the notification is sent."""

    custom_headers: Optional[Dict[str, str]] = FieldInfo(alias="customHeaders", default=None)
    """Custom HTTP headers sent as part of the webhook request."""

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)
    """Timestamp of when the resource was permanently deleted."""

    disabled: Optional[bool] = None
    """Whether the channel is disabled or not."""

    signing_secret: Optional[str] = FieldInfo(alias="signingSecret", default=None)
    """Signing secret used for webhook request validation on the receiving end.

    Format: `base64` encoded random bytes optionally prefixed with `whsec_`.
    Recommended size: 24
    """
