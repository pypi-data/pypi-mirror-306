# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["TokenListParams"]


class TokenListParams(TypedDict, total=False):
    limit: int
    """Number of portal tokens to return. Default is 25."""
