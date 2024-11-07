# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["EntitlementGrant", "Expiration", "Recurrence"]


class Expiration(BaseModel):
    count: int
    """The number of time units in the expiration period."""

    duration: Literal["HOUR", "DAY", "WEEK", "MONTH", "YEAR"]
    """The expiration duration enum"""


class Recurrence(BaseModel):
    anchor: datetime
    """A date-time anchor to base the recurring period on."""

    interval: Literal["DAY", "WEEK", "MONTH", "YEAR"]
    """The unit of time for the interval. One of: `day`, `week`, `month`, or `year`."""


class EntitlementGrant(BaseModel):
    id: str
    """Readonly unique ULID identifier."""

    amount: float
    """The amount to grant. Should be a positive number."""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Timestamp of when the resource was created."""

    effective_at: datetime = FieldInfo(alias="effectiveAt")
    """Effective date for grants and anchor for recurring grants.

    Provided value will be ceiled to metering windowSize (minute).
    """

    entitlement_id: str = FieldInfo(alias="entitlementId")
    """The unique entitlement ULID that the grant is associated with."""

    expiration: Expiration
    """The grant expiration definition"""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Timestamp of when the resource was last updated."""

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)
    """Timestamp of when the resource was permanently deleted."""

    expires_at: Optional[datetime] = FieldInfo(alias="expiresAt", default=None)
    """The time the grant expires."""

    max_rollover_amount: Optional[float] = FieldInfo(alias="maxRolloverAmount", default=None)
    """
    Grants are rolled over at reset, after which they can have a different balance
    compared to what they had before the reset. Balance after the reset is
    calculated as: Balance_After_Reset = MIN(MaxRolloverAmount,
    MAX(Balance_Before_Reset, MinRolloverAmount))
    """

    metadata: Optional[Dict[str, str]] = None
    """
    Set of key-value pairs. Metadata can be used to store additional information
    about a resource.
    """

    min_rollover_amount: Optional[float] = FieldInfo(alias="minRolloverAmount", default=None)
    """
    Grants are rolled over at reset, after which they can have a different balance
    compared to what they had before the reset. Balance after the reset is
    calculated as: Balance_After_Reset = MIN(MaxRolloverAmount,
    MAX(Balance_Before_Reset, MinRolloverAmount))
    """

    next_recurrence: Optional[datetime] = FieldInfo(alias="nextRecurrence", default=None)
    """The next time the grant will recurr."""

    priority: Optional[int] = None
    """The priority of the grant.

    Grants with higher priority are applied first. Priority is a positive decimal
    numbers. With lower numbers indicating higher importance. For example, a
    priority of 1 is more urgent than a priority of 2. When there are several grants
    available for the same subject, the system selects the grant with the highest
    priority. In cases where grants share the same priority level, the grant closest
    to its expiration will be used first. In the case of two grants have identical
    priorities and expiration dates, the system will use the grant that was created
    first.
    """

    recurrence: Optional[Recurrence] = None
    """Recurring period with an interval and an anchor."""

    voided_at: Optional[datetime] = FieldInfo(alias="voidedAt", default=None)
    """The time the grant was voided."""
