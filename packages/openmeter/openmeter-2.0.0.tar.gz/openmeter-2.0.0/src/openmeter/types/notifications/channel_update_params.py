# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ChannelUpdateParams"]


class ChannelUpdateParams(TypedDict, total=False):
    name: Required[str]
    """User friendly name of the channel."""

    type: Required[Literal["WEBHOOK"]]
    """Notification channel type."""

    url: Required[str]
    """Webhook URL where the notification is sent."""

    custom_headers: Annotated[Dict[str, str], PropertyInfo(alias="customHeaders")]
    """Custom HTTP headers sent as part of the webhook request."""

    disabled: bool
    """Whether the channel is disabled or not."""

    signing_secret: Annotated[str, PropertyInfo(alias="signingSecret")]
    """Signing secret used for webhook request validation on the receiving end.

    Format: `base64` encoded random bytes optionally prefixed with `whsec_`.
    Recommended size: 24
    """
