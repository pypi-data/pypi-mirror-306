# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..subjects.entitlements.entitlement_grant import EntitlementGrant

__all__ = ["GrantPaginatedResponse"]


class GrantPaginatedResponse(BaseModel):
    items: List[EntitlementGrant]
    """The items in the current page."""

    page: int
    """The items in the current page."""

    page_size: int = FieldInfo(alias="pageSize")
    """The items in the current page."""

    total_count: int = FieldInfo(alias="totalCount")
    """The items in the current page."""
