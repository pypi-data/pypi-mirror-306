# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import TypeAlias

from .grant_paginated_response import GrantPaginatedResponse
from ..subjects.entitlements.entitlement_grant import EntitlementGrant

__all__ = ["GrantListResponse"]

GrantListResponse: TypeAlias = Union[List[EntitlementGrant], GrantPaginatedResponse]
