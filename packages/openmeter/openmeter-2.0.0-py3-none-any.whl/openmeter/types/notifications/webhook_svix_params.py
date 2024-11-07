# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

__all__ = ["WebhookSvixParams"]


class WebhookSvixParams(TypedDict, total=False):
    data: Required[Dict[str, str]]
    """The payload of the Svix operational webhook request."""

    type: Required[
        Literal[
            "endpoint.created",
            "endpoint.deleted",
            "endpoint.disabled",
            "endpoint.updated",
            "message.attempt.exhausted",
            "message.attempt.failing",
            "message.attempt.recovered",
        ]
    ]
    """The type of the Svix operational webhook request."""
