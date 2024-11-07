# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["TokenCreateParams"]


class TokenCreateParams(TypedDict, total=False):
    subject: Required[str]

    allowed_meter_slugs: Annotated[List[str], PropertyInfo(alias="allowedMeterSlugs")]
    """Optional, if defined only the specified meters will be allowed"""
