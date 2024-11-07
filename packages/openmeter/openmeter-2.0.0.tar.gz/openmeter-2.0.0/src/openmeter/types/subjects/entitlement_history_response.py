# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "EntitlementHistoryResponse",
    "BurndownHistory",
    "BurndownHistoryGrantUsage",
    "BurndownHistoryPeriod",
    "WindowedHistory",
    "WindowedHistoryPeriod",
]


class BurndownHistoryGrantUsage(BaseModel):
    grant_id: str = FieldInfo(alias="grantId")
    """The id of the grant"""

    usage: float
    """The usage in the period"""


class BurndownHistoryPeriod(BaseModel):
    from_: datetime = FieldInfo(alias="from")
    """Period start time."""

    to: datetime
    """Period end time."""


class BurndownHistory(BaseModel):
    balance_at_end: float = FieldInfo(alias="balanceAtEnd")
    """The entitlement balance at the end of the period."""

    balance_at_start: float = FieldInfo(alias="balanceAtStart")
    """entitlement balance at the start of the period."""

    grant_balances_at_end: Dict[str, float] = FieldInfo(alias="grantBalancesAtEnd")
    """
    The balance breakdown of each active grant at the end of the period: GrantID:
    Balance
    """

    grant_balances_at_start: Dict[str, float] = FieldInfo(alias="grantBalancesAtStart")
    """
    The balance breakdown of each active grant at the start of the period: GrantID:
    Balance
    """

    grant_usages: List[BurndownHistoryGrantUsage] = FieldInfo(alias="grantUsages")
    """Which grants were actually burnt down in the period and by what amount."""

    overage: float
    """Overuse that wasn't covered by grants."""

    period: BurndownHistoryPeriod
    """A period with a start and end time."""

    usage: float
    """The total usage of the grant in the period."""


class WindowedHistoryPeriod(BaseModel):
    from_: datetime = FieldInfo(alias="from")
    """Period start time."""

    to: datetime
    """Period end time."""


class WindowedHistory(BaseModel):
    balance_at_start: float = FieldInfo(alias="balanceAtStart")
    """The entitlement balance at the start of the period."""

    period: WindowedHistoryPeriod
    """A period with a start and end time."""

    usage: float
    """The total usage of the feature in the period."""


class EntitlementHistoryResponse(BaseModel):
    burndown_history: List[BurndownHistory] = FieldInfo(alias="burndownHistory")
    """Grant burndown history."""

    windowed_history: List[WindowedHistory] = FieldInfo(alias="windowedHistory")
    """The windowed balance history.

    - It only returns rows for windows where there was usage.
    - The windows are inclusive at their start and exclusive at their end.
    - The last window may be smaller than the window size and is inclusive at both
      ends.
    """
