# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["FeatureCreateParams"]


class FeatureCreateParams(TypedDict, total=False):
    key: Required[str]
    """
    The key is an immutable unique identifier of the feature used throughout the
    API, for example when interacting with a subject's entitlements. The key has to
    be unique across all active features, but archived features can share the same
    key. The key should consist of lowercase alphanumeric characters and dashes.
    """

    name: Required[str]
    """The name of the feature."""

    metadata: Dict[str, str]
    """
    Additional metadata for the feature, useful for syncing with external systems
    and annotating custom fields.
    """

    meter_group_by_filters: Annotated[Dict[str, str], PropertyInfo(alias="meterGroupByFilters")]
    """Optional meter group by filters.

    Useful if the meter scope is broader than what feature tracks. Example scenario
    would be a meter tracking all token use with groupBy fields for the model, then
    the feature could filter for model=gpt-4.
    """

    meter_slug: Annotated[str, PropertyInfo(alias="meterSlug")]
    """
    The meter that the feature is associated with and and based on which usage is
    calculated. The meter selected must have SUM or COUNT aggregation.
    """
