# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "Entitlement",
    "EntitlementMetered",
    "EntitlementMeteredCurrentUsagePeriod",
    "EntitlementMeteredUsagePeriod",
    "EntitlementStatic",
    "EntitlementStaticCurrentUsagePeriod",
    "EntitlementStaticUsagePeriod",
    "EntitlementBaseTemplate",
    "EntitlementBaseTemplateCurrentUsagePeriod",
    "EntitlementBaseTemplateUsagePeriod",
]


class EntitlementMeteredCurrentUsagePeriod(BaseModel):
    from_: datetime = FieldInfo(alias="from")
    """Period start time."""

    to: datetime
    """Period end time."""


class EntitlementMeteredUsagePeriod(BaseModel):
    anchor: datetime
    """A date-time anchor to base the recurring period on."""

    interval: Literal["DAY", "WEEK", "MONTH", "YEAR"]
    """The unit of time for the interval. One of: `day`, `week`, `month`, or `year`."""


class EntitlementMetered(BaseModel):
    id: str
    """Readonly unique ULID identifier."""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Timestamp of when the resource was created."""

    current_usage_period: EntitlementMeteredCurrentUsagePeriod = FieldInfo(alias="currentUsagePeriod")
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

    usage_period: EntitlementMeteredUsagePeriod = FieldInfo(alias="usagePeriod")
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


class EntitlementStaticCurrentUsagePeriod(BaseModel):
    from_: datetime = FieldInfo(alias="from")
    """Period start time."""

    to: datetime
    """Period end time."""


class EntitlementStaticUsagePeriod(BaseModel):
    anchor: datetime
    """A date-time anchor to base the recurring period on."""

    interval: Literal["DAY", "WEEK", "MONTH", "YEAR"]
    """The unit of time for the interval. One of: `day`, `week`, `month`, or `year`."""


class EntitlementStatic(BaseModel):
    id: str
    """Readonly unique ULID identifier."""

    config: str
    """The JSON parsable config of the entitlement.

    This value is also returned when checking entitlement access and it is useful
    for configuring fine-grained access settings to the feature, implemented in your
    own system. Has to be an object.
    """

    created_at: datetime = FieldInfo(alias="createdAt")
    """Timestamp of when the resource was created."""

    feature_id: str = FieldInfo(alias="featureId")
    """The feature the subject is entitled to use."""

    feature_key: str = FieldInfo(alias="featureKey")
    """The feature the subject is entitled to use."""

    subject_key: str = FieldInfo(alias="subjectKey")
    """The identifier key unique to the subject"""

    type: Literal["static"]

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Timestamp of when the resource was last updated."""

    current_usage_period: Optional[EntitlementStaticCurrentUsagePeriod] = FieldInfo(
        alias="currentUsagePeriod", default=None
    )
    """A period with a start and end time."""

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)
    """Timestamp of when the resource was permanently deleted."""

    metadata: Optional[Dict[str, str]] = None
    """
    Set of key-value pairs. Metadata can be used to store additional information
    about a resource.
    """

    usage_period: Optional[EntitlementStaticUsagePeriod] = FieldInfo(alias="usagePeriod", default=None)
    """Recurring period with an interval and an anchor."""


class EntitlementBaseTemplateCurrentUsagePeriod(BaseModel):
    from_: datetime = FieldInfo(alias="from")
    """Period start time."""

    to: datetime
    """Period end time."""


class EntitlementBaseTemplateUsagePeriod(BaseModel):
    anchor: datetime
    """A date-time anchor to base the recurring period on."""

    interval: Literal["DAY", "WEEK", "MONTH", "YEAR"]
    """The unit of time for the interval. One of: `day`, `week`, `month`, or `year`."""


class EntitlementBaseTemplate(BaseModel):
    id: str
    """Readonly unique ULID identifier."""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Timestamp of when the resource was created."""

    feature_id: str = FieldInfo(alias="featureId")
    """The feature the subject is entitled to use."""

    feature_key: str = FieldInfo(alias="featureKey")
    """The feature the subject is entitled to use."""

    subject_key: str = FieldInfo(alias="subjectKey")
    """The identifier key unique to the subject"""

    type: Literal["metered", "boolean", "static"]
    """Type of the entitlement."""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Timestamp of when the resource was last updated."""

    current_usage_period: Optional[EntitlementBaseTemplateCurrentUsagePeriod] = FieldInfo(
        alias="currentUsagePeriod", default=None
    )
    """A period with a start and end time."""

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)
    """Timestamp of when the resource was permanently deleted."""

    metadata: Optional[Dict[str, str]] = None
    """
    Set of key-value pairs. Metadata can be used to store additional information
    about a resource.
    """

    usage_period: Optional[EntitlementBaseTemplateUsagePeriod] = FieldInfo(alias="usagePeriod", default=None)
    """Recurring period with an interval and an anchor."""


Entitlement: TypeAlias = Annotated[
    Union[EntitlementMetered, EntitlementStatic, EntitlementBaseTemplate], PropertyInfo(discriminator="type")
]
