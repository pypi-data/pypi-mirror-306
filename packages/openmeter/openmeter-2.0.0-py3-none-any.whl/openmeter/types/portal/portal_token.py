# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["PortalToken"]


class PortalToken(BaseModel):
    subject: str

    id: Optional[str] = None

    token: Optional[str] = None
    """The token is only returned at creation."""

    allowed_meter_slugs: Optional[List[str]] = FieldInfo(alias="allowedMeterSlugs", default=None)
    """Optional, if defined only the specified meters will be allowed"""

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)

    expired: Optional[bool] = None

    expires_at: Optional[datetime] = FieldInfo(alias="expiresAt", default=None)
