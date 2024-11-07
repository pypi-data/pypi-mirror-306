# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SubjectParam"]


class SubjectParam(TypedDict, total=False):
    key: Required[str]

    current_period_end: Annotated[Union[str, datetime, None], PropertyInfo(alias="currentPeriodEnd", format="iso8601")]

    current_period_start: Annotated[
        Union[str, datetime, None], PropertyInfo(alias="currentPeriodStart", format="iso8601")
    ]

    display_name: Annotated[Optional[str], PropertyInfo(alias="displayName")]

    metadata: Optional[Dict[str, object]]

    stripe_customer_id: Annotated[Optional[str], PropertyInfo(alias="stripeCustomerId")]
