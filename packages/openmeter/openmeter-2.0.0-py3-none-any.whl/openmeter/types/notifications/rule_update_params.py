# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["RuleUpdateParams", "Threshold"]


class RuleUpdateParams(TypedDict, total=False):
    channels: Required[List[str]]
    """List of notification channels the rule is applied to."""

    name: Required[str]
    """The user friendly name of the notification rule."""

    thresholds: Required[Iterable[Threshold]]
    """List of thresholds the rule suppose to be triggered."""

    type: Required[Literal["entitlements.balance.threshold"]]
    """Notification rule type."""

    disabled: bool
    """Whether the rule is disabled or not."""

    features: List[str]
    """Optional field for defining the scope of notification by feature.

    It may contain features by id or key.
    """


class Threshold(TypedDict, total=False):
    type: Required[Literal["PERCENT", "NUMBER"]]
    """Type of the rule in the balance threshold specification."""

    value: Required[float]
    """Value of the threshold."""
