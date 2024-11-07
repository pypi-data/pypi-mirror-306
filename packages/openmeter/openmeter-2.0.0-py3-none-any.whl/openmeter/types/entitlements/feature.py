# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["Feature"]


class Feature(BaseModel):
    id: str
    """Readonly unique ULID identifier."""

    created_at: datetime = FieldInfo(alias="createdAt")
    """The date and time the resource was created."""

    key: str
    """
    The key is an immutable unique identifier of the feature used throughout the
    API, for example when interacting with a subject's entitlements. The key has to
    be unique across all active features, but archived features can share the same
    key. The key should consist of lowercase alphanumeric characters and dashes.
    """

    name: str
    """The name of the feature."""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """The date and time the resource was last updated.

    The initial value is the same as createdAt.
    """

    archived_at: Optional[datetime] = FieldInfo(alias="archivedAt", default=None)
    """If the feature is archived, no new entitlements can be created for it."""

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)
    """The date and time the resource was deleted."""

    metadata: Optional[Dict[str, str]] = None
    """
    Additional metadata for the feature, useful for syncing with external systems
    and annotating custom fields.
    """

    meter_group_by_filters: Optional[Dict[str, str]] = FieldInfo(alias="meterGroupByFilters", default=None)
    """Optional meter group by filters.

    Useful if the meter scope is broader than what feature tracks. Example scenario
    would be a meter tracking all token use with groupBy fields for the model, then
    the feature could filter for model=gpt-4.
    """

    meter_slug: Optional[str] = FieldInfo(alias="meterSlug", default=None)
    """
    The meter that the feature is associated with and and based on which usage is
    calculated. The meter selected must have SUM or COUNT aggregation.
    """
