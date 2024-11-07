# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .entitlement import Entitlement

__all__ = ["ListEntitlementsResult", "EntitlementPaginatedResponse"]


class EntitlementPaginatedResponse(BaseModel):
    items: List[Entitlement]
    """The items in the current page."""

    page: int
    """The items in the current page."""

    page_size: int = FieldInfo(alias="pageSize")
    """The items in the current page."""

    total_count: int = FieldInfo(alias="totalCount")
    """The items in the current page."""


ListEntitlementsResult: TypeAlias = Union[List[Entitlement], EntitlementPaginatedResponse]
