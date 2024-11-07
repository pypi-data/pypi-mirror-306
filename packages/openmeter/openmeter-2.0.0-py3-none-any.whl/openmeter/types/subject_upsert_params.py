# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SubjectUpsertParams", "Body"]


class SubjectUpsertParams(TypedDict, total=False):
    body: Required[Iterable[Body]]


class Body(TypedDict, total=False):
    key: Required[str]
    """A unique, human-readable identifier for the subject."""

    current_period_end: Annotated[Union[str, datetime], PropertyInfo(alias="currentPeriodEnd", format="iso8601")]
    """
    [RFC3339](https://tools.ietf.org/html/rfc3339) formatted date-time string in
    UTC.
    """

    current_period_start: Annotated[Union[str, datetime], PropertyInfo(alias="currentPeriodStart", format="iso8601")]
    """
    [RFC3339](https://tools.ietf.org/html/rfc3339) formatted date-time string in
    UTC.
    """

    display_name: Annotated[Optional[str], PropertyInfo(alias="displayName")]
    """A human-readable display name for the subject."""

    metadata: Optional[Dict[str, object]]

    stripe_customer_id: Annotated[Optional[str], PropertyInfo(alias="stripeCustomerId")]
