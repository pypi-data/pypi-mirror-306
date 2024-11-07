# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .entitlement_grant import EntitlementGrant

__all__ = ["GrantListResponse"]

GrantListResponse: TypeAlias = List[EntitlementGrant]
