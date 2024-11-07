# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..subject import Subject
from ..._models import BaseModel
from .notification_rule import NotificationRule
from ..entitlements.feature import Feature
from ..subjects.entitlement_value import EntitlementValue

__all__ = [
    "NotificationEvent",
    "DeliveryStatus",
    "DeliveryStatusChannel",
    "Payload",
    "PayloadData",
    "PayloadDataEntitlement",
    "PayloadDataEntitlementCurrentUsagePeriod",
    "PayloadDataEntitlementUsagePeriod",
    "PayloadDataThreshold",
]


class DeliveryStatusChannel(BaseModel):
    id: str
    """Identifies the notification channel."""

    type: Literal["WEBHOOK"]
    """Type of the notification channel."""


class DeliveryStatus(BaseModel):
    channel: DeliveryStatusChannel
    """Metadata only fields of a notification channel."""

    reason: str
    """The reason of the last deliverry state update."""

    state: Literal["SUCCESS", "FAILED", "SENDING", "PENDING"]
    """The delivery state of the notification event to the channel."""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Timestamp of when the status was last updated in RFC 3339 format."""


class PayloadDataEntitlementCurrentUsagePeriod(BaseModel):
    from_: datetime = FieldInfo(alias="from")
    """Period start time."""

    to: datetime
    """Period end time."""


class PayloadDataEntitlementUsagePeriod(BaseModel):
    anchor: datetime
    """A date-time anchor to base the recurring period on."""

    interval: Literal["DAY", "WEEK", "MONTH", "YEAR"]
    """The unit of time for the interval. One of: `day`, `week`, `month`, or `year`."""


class PayloadDataEntitlement(BaseModel):
    id: str
    """Readonly unique ULID identifier."""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Timestamp of when the resource was created."""

    current_usage_period: PayloadDataEntitlementCurrentUsagePeriod = FieldInfo(alias="currentUsagePeriod")
    """A period with a start and end time."""

    feature_id: str = FieldInfo(alias="featureId")
    """The feature the subject is entitled to use."""

    feature_key: str = FieldInfo(alias="featureKey")
    """The feature the subject is entitled to use."""

    last_reset: datetime = FieldInfo(alias="lastReset")
    """The time the last reset happened."""

    measure_usage_from: datetime = FieldInfo(alias="measureUsageFrom")
    """The time from which usage is measured.

    If not specified on creation, defaults to entitlement creation time.
    """

    subject_key: str = FieldInfo(alias="subjectKey")
    """The identifier key unique to the subject"""

    type: Literal["metered"]

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Timestamp of when the resource was last updated."""

    usage_period: PayloadDataEntitlementUsagePeriod = FieldInfo(alias="usagePeriod")
    """Recurring period with an interval and an anchor."""

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)
    """Timestamp of when the resource was permanently deleted."""

    is_soft_limit: Optional[bool] = FieldInfo(alias="isSoftLimit", default=None)
    """
    If softLimit=true the subject can use the feature even if the entitlement is
    exhausted, hasAccess will always be true.
    """

    issue_after_reset: Optional[float] = FieldInfo(alias="issueAfterReset", default=None)
    """
    You can grant usage automatically alongside the entitlement, the example
    scenario would be creating a starting balance. If an amount is specified here, a
    grant will be created alongside the entitlement with the specified amount. That
    grant will have it's rollover settings configured in a way that after each reset
    operation, the balance will return the original amount specified here. Manually
    creating such a grant would mean having the "amount", "minRolloverAmount", and
    "maxRolloverAmount" fields all be the same.
    """

    issue_after_reset_priority: Optional[int] = FieldInfo(alias="issueAfterResetPriority", default=None)
    """Defines the grant priority for the default grant."""

    is_unlimited: Optional[bool] = FieldInfo(alias="isUnlimited", default=None)
    """Deprecated, ignored by the backend.

    Please use isSoftLimit instead; this field will be removed in the future.
    """

    metadata: Optional[Dict[str, str]] = None
    """
    Set of key-value pairs. Metadata can be used to store additional information
    about a resource.
    """

    preserve_overage_at_reset: Optional[bool] = FieldInfo(alias="preserveOverageAtReset", default=None)
    """If true, the overage is preserved at reset. If false, the usage is reset to 0."""


class PayloadDataThreshold(BaseModel):
    type: Literal["PERCENT", "NUMBER"]
    """Type of the rule in the balance threshold specification."""

    value: float
    """Value of the threshold."""


class PayloadData(BaseModel):
    entitlement: PayloadDataEntitlement
    """
    Metered entitlements are useful for many different use cases, from setting up
    usage based access to implementing complex credit systems. Access is determined
    based on feature usage using a balance calculation (the "usage allowance"
    provided by the issued grants is "burnt down" by the usage).
    """

    feature: Feature
    """
    Represents a feature that can be enabled or disabled for a plan. Used both for
    product catalog and entitlements.
    """

    subject: Subject
    """A subject is a unique identifier for a user or entity."""

    threshold: PayloadDataThreshold
    """Threshold value with multiple supported types."""

    value: EntitlementValue
    """Entitlements are the core of OpenMeter access management.

    They define access to features for subjects. Entitlements can be metered,
    boolean, or static.
    """


class Payload(BaseModel):
    id: str
    """A unique identifier for the notification event the payload belongs to."""

    data: PayloadData
    """
    Data of the payload for notification event with `entitlements.balance.threshold`
    type.
    """

    timestamp: datetime
    """Timestamp when the notification event was created in RFC 3339 format."""

    type: Literal["entitlements.balance.threshold"]
    """Type of the notification event."""


class NotificationEvent(BaseModel):
    id: str
    """A unique identifier of the notification event."""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Timestamp when the notification event was created in RFC 3339 format."""

    delivery_status: List[DeliveryStatus] = FieldInfo(alias="deliveryStatus")
    """The delivery status of the notification event."""

    payload: Payload
    """Payload for notification event with `entitlements.balance.threshold` type."""

    rule: NotificationRule
    """Notification rule with entitlements.balance.threshold type."""

    type: Literal["entitlements.balance.threshold"]
    """Type of the notification event."""

    annotations: Optional[Dict[str, object]] = None
    """Set of key-value pairs managed by the system. Cannot be modified by user."""
