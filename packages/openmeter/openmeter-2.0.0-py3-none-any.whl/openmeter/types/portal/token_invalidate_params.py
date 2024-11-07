# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["TokenInvalidateParams"]


class TokenInvalidateParams(TypedDict, total=False):
    id: str
    """Invalidate a portal token by ID."""

    subject: str
    """Invalidate all portal tokens for a subject."""
