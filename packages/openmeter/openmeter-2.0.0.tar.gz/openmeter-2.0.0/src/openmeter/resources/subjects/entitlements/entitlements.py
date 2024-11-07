# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, Union, cast
from datetime import datetime
from typing_extensions import Literal, overload

import httpx

from .grants import (
    GrantsResource,
    AsyncGrantsResource,
    GrantsResourceWithRawResponse,
    AsyncGrantsResourceWithRawResponse,
    GrantsResourceWithStreamingResponse,
    AsyncGrantsResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ...._utils import (
    required_args,
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.subjects import (
    entitlement_list_params,
    entitlement_reset_params,
    entitlement_value_params,
    entitlement_create_params,
    entitlement_history_params,
    entitlement_override_params,
)
from ....types.entitlement import Entitlement
from ....types.subjects.entitlement_value import EntitlementValue
from ....types.subjects.entitlement_list_response import EntitlementListResponse
from ....types.subjects.entitlement_history_response import EntitlementHistoryResponse

__all__ = ["EntitlementsResource", "AsyncEntitlementsResource"]


class EntitlementsResource(SyncAPIResource):
    @cached_property
    def grants(self) -> GrantsResource:
        return GrantsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EntitlementsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return EntitlementsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EntitlementsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return EntitlementsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        subject_id_or_key: str,
        *,
        type: Literal["metered"],
        usage_period: entitlement_create_params.EntitlementMeteredCreateInputsUsagePeriod,
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        is_soft_limit: bool | NotGiven = NOT_GIVEN,
        issue_after_reset: float | NotGiven = NOT_GIVEN,
        issue_after_reset_priority: int | NotGiven = NOT_GIVEN,
        is_unlimited: bool | NotGiven = NOT_GIVEN,
        measure_usage_from: Union[Literal["CURRENT_PERIOD_START", "NOW"], Union[str, datetime]] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        preserve_overage_at_reset: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """OpenMeter has three types of entitlements: metered, boolean, and static.

        The
        type property determines the type of entitlement. The underlying feature has to
        be compatible with the entitlement type specified in the request (e.g., a
        metered entitlement needs a feature associated with a meter).

        - Boolean entitlements define static feature access, e.g. "Can use SSO
          authentication".
        - Static entitlements let you pass along a configuration while granting access,
          e.g. "Using this feature with X Y settings" (passed in the config).
        - Metered entitlements have many use cases, from setting up usage-based access
          to implementing complex credit systems. Example: The customer can use 10000 AI
          tokens during the usage period of the entitlement.

        A given subject can only have one active (non-deleted) entitlement per
        featureKey. If you try to create a new entitlement for a featureKey that already
        has an active entitlement, the request will fail with a 409 error.

        Once an entitlement is created you cannot modify it, only delete it.

        Args:
          usage_period: Recurring period with an interval and an anchor.

          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          is_soft_limit: If softLimit=true the subject can use the feature even if the entitlement is
              exhausted, hasAccess will always be true.

          issue_after_reset: You can grant usage automatically alongside the entitlement, the example
              scenario would be creating a starting balance. If an amount is specified here, a
              grant will be created alongside the entitlement with the specified amount. That
              grant will have it's rollover settings configured in a way that after each reset
              operation, the balance will return the original amount specified here. Manually
              creating such a grant would mean having the "amount", "minRolloverAmount", and
              "maxRolloverAmount" fields all be the same.

          issue_after_reset_priority: Defines the grant priority for the default grant.

          is_unlimited: Deprecated, ignored by the backend. Please use isSoftLimit instead; this field
              will be removed in the future.

          measure_usage_from: Measure usage from

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          preserve_overage_at_reset: If true, the overage is preserved at reset. If false, the usage is reset to 0.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        subject_id_or_key: str,
        *,
        config: str,
        type: Literal["static"],
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        usage_period: entitlement_create_params.EntitlementStaticCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """OpenMeter has three types of entitlements: metered, boolean, and static.

        The
        type property determines the type of entitlement. The underlying feature has to
        be compatible with the entitlement type specified in the request (e.g., a
        metered entitlement needs a feature associated with a meter).

        - Boolean entitlements define static feature access, e.g. "Can use SSO
          authentication".
        - Static entitlements let you pass along a configuration while granting access,
          e.g. "Using this feature with X Y settings" (passed in the config).
        - Metered entitlements have many use cases, from setting up usage-based access
          to implementing complex credit systems. Example: The customer can use 10000 AI
          tokens during the usage period of the entitlement.

        A given subject can only have one active (non-deleted) entitlement per
        featureKey. If you try to create a new entitlement for a featureKey that already
        has an active entitlement, the request will fail with a 409 error.

        Once an entitlement is created you cannot modify it, only delete it.

        Args:
          config: The JSON parsable config of the entitlement. This value is also returned when
              checking entitlement access and it is useful for configuring fine-grained access
              settings to the feature, implemented in your own system. Has to be an object.

          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          usage_period: Recurring period with an interval and an anchor.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        subject_id_or_key: str,
        *,
        type: Literal["boolean"],
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        usage_period: entitlement_create_params.EntitlementBooleanCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """OpenMeter has three types of entitlements: metered, boolean, and static.

        The
        type property determines the type of entitlement. The underlying feature has to
        be compatible with the entitlement type specified in the request (e.g., a
        metered entitlement needs a feature associated with a meter).

        - Boolean entitlements define static feature access, e.g. "Can use SSO
          authentication".
        - Static entitlements let you pass along a configuration while granting access,
          e.g. "Using this feature with X Y settings" (passed in the config).
        - Metered entitlements have many use cases, from setting up usage-based access
          to implementing complex credit systems. Example: The customer can use 10000 AI
          tokens during the usage period of the entitlement.

        A given subject can only have one active (non-deleted) entitlement per
        featureKey. If you try to create a new entitlement for a featureKey that already
        has an active entitlement, the request will fail with a 409 error.

        Once an entitlement is created you cannot modify it, only delete it.

        Args:
          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          usage_period: Recurring period with an interval and an anchor.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["type", "usage_period"], ["config", "type"], ["type"])
    def create(
        self,
        subject_id_or_key: str,
        *,
        type: Literal["metered"] | Literal["static"] | Literal["boolean"],
        usage_period: entitlement_create_params.EntitlementMeteredCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        is_soft_limit: bool | NotGiven = NOT_GIVEN,
        issue_after_reset: float | NotGiven = NOT_GIVEN,
        issue_after_reset_priority: int | NotGiven = NOT_GIVEN,
        is_unlimited: bool | NotGiven = NOT_GIVEN,
        measure_usage_from: Union[Literal["CURRENT_PERIOD_START", "NOW"], Union[str, datetime]] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        preserve_overage_at_reset: bool | NotGiven = NOT_GIVEN,
        config: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        return cast(
            Entitlement,
            self._post(
                f"/api/v1/subjects/{subject_id_or_key}/entitlements",
                body=maybe_transform(
                    {
                        "type": type,
                        "usage_period": usage_period,
                        "feature_id": feature_id,
                        "feature_key": feature_key,
                        "is_soft_limit": is_soft_limit,
                        "issue_after_reset": issue_after_reset,
                        "issue_after_reset_priority": issue_after_reset_priority,
                        "is_unlimited": is_unlimited,
                        "measure_usage_from": measure_usage_from,
                        "metadata": metadata,
                        "preserve_overage_at_reset": preserve_overage_at_reset,
                        "config": config,
                    },
                    entitlement_create_params.EntitlementCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Entitlement),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        entitlement_id: str,
        *,
        subject_id_or_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """Get entitlement by id.

        For checking entitlement access, use the /value endpoint
        instead.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        return cast(
            Entitlement,
            self._get(
                f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Entitlement),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        subject_id_or_key: str,
        *,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EntitlementListResponse:
        """List all entitlements for a subject.

        For checking entitlement access, use the
        /value endpoint instead.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        return self._get(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_deleted": include_deleted}, entitlement_list_params.EntitlementListParams
                ),
            ),
            cast_to=EntitlementListResponse,
        )

    def delete(
        self,
        entitlement_id: str,
        *,
        subject_id_or_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Deleting an entitlement revokes access to the associated feature.

        As a single
        subject can only have one entitlement per featureKey, when "migrating" features
        you have to delete the old entitlements as well. As access and status checks can
        be historical queries, deleting an entitlement populates the deletedAt
        timestamp. When queried for a time before that, the entitlement is still
        considered active, you cannot have retroactive changes to access, which is
        important for, among other things, auditing.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def history(
        self,
        entitlement_id: str,
        *,
        subject_id_or_key: str,
        window_size: Literal["MINUTE", "HOUR", "DAY"],
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        window_time_zone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EntitlementHistoryResponse:
        """Returns historical balance and usage data for the entitlement.

        The queried
        history can span accross multiple reset events.

        BurndownHistory returns a continous history of segments, where the segments are
        seperated by events that changed either the grant burndown priority or the usage
        period.

        WindowedHistory returns windowed usage data for the period enriched with balance
        information and the list of grants that were being burnt down in that window.

        Args:
          window_size: Windowsize

          from_: Start of time range to query entitlement: date-time in RFC 3339 format. Defaults
              to the last reset. Gets truncated to the granularity of the underlying meter.

          to: End of time range to query entitlement: date-time in RFC 3339 format. Defaults
              to now. If not now then gets truncated to the granularity of the underlying
              meter.

          window_time_zone: The timezone used when calculating the windows.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        return self._get(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id}/history",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "window_size": window_size,
                        "from_": from_,
                        "to": to,
                        "window_time_zone": window_time_zone,
                    },
                    entitlement_history_params.EntitlementHistoryParams,
                ),
            ),
            cast_to=EntitlementHistoryResponse,
        )

    @overload
    def override(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        type: Literal["metered"],
        usage_period: entitlement_override_params.EntitlementMeteredCreateInputsUsagePeriod,
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        is_soft_limit: bool | NotGiven = NOT_GIVEN,
        issue_after_reset: float | NotGiven = NOT_GIVEN,
        issue_after_reset_priority: int | NotGiven = NOT_GIVEN,
        is_unlimited: bool | NotGiven = NOT_GIVEN,
        measure_usage_from: Union[Literal["CURRENT_PERIOD_START", "NOW"], Union[str, datetime]] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        preserve_overage_at_reset: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """
        Overriding an entitlement creates a new entitlement from the provided inputs and
        soft deletes the previous entitlement for the provided subject-feature pair. If
        the previous entitlement is already deleted or otherwise doesnt exist, the
        override will fail.

        This endpoint is useful for upgrades, downgrades, or other changes to
        entitlements that require a new entitlement to be created with zero downtime.

        Args:
          usage_period: Recurring period with an interval and an anchor.

          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          is_soft_limit: If softLimit=true the subject can use the feature even if the entitlement is
              exhausted, hasAccess will always be true.

          issue_after_reset: You can grant usage automatically alongside the entitlement, the example
              scenario would be creating a starting balance. If an amount is specified here, a
              grant will be created alongside the entitlement with the specified amount. That
              grant will have it's rollover settings configured in a way that after each reset
              operation, the balance will return the original amount specified here. Manually
              creating such a grant would mean having the "amount", "minRolloverAmount", and
              "maxRolloverAmount" fields all be the same.

          issue_after_reset_priority: Defines the grant priority for the default grant.

          is_unlimited: Deprecated, ignored by the backend. Please use isSoftLimit instead; this field
              will be removed in the future.

          measure_usage_from: Measure usage from

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          preserve_overage_at_reset: If true, the overage is preserved at reset. If false, the usage is reset to 0.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def override(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        config: str,
        type: Literal["static"],
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        usage_period: entitlement_override_params.EntitlementStaticCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """
        Overriding an entitlement creates a new entitlement from the provided inputs and
        soft deletes the previous entitlement for the provided subject-feature pair. If
        the previous entitlement is already deleted or otherwise doesnt exist, the
        override will fail.

        This endpoint is useful for upgrades, downgrades, or other changes to
        entitlements that require a new entitlement to be created with zero downtime.

        Args:
          config: The JSON parsable config of the entitlement. This value is also returned when
              checking entitlement access and it is useful for configuring fine-grained access
              settings to the feature, implemented in your own system. Has to be an object.

          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          usage_period: Recurring period with an interval and an anchor.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def override(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        type: Literal["boolean"],
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        usage_period: entitlement_override_params.EntitlementBooleanCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """
        Overriding an entitlement creates a new entitlement from the provided inputs and
        soft deletes the previous entitlement for the provided subject-feature pair. If
        the previous entitlement is already deleted or otherwise doesnt exist, the
        override will fail.

        This endpoint is useful for upgrades, downgrades, or other changes to
        entitlements that require a new entitlement to be created with zero downtime.

        Args:
          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          usage_period: Recurring period with an interval and an anchor.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["subject_id_or_key", "type", "usage_period"],
        ["subject_id_or_key", "config", "type"],
        ["subject_id_or_key", "type"],
    )
    def override(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        type: Literal["metered"] | Literal["static"] | Literal["boolean"],
        usage_period: entitlement_override_params.EntitlementMeteredCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        is_soft_limit: bool | NotGiven = NOT_GIVEN,
        issue_after_reset: float | NotGiven = NOT_GIVEN,
        issue_after_reset_priority: int | NotGiven = NOT_GIVEN,
        is_unlimited: bool | NotGiven = NOT_GIVEN,
        measure_usage_from: Union[Literal["CURRENT_PERIOD_START", "NOW"], Union[str, datetime]] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        preserve_overage_at_reset: bool | NotGiven = NOT_GIVEN,
        config: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id_or_feature_key:
            raise ValueError(
                f"Expected a non-empty value for `entitlement_id_or_feature_key` but received {entitlement_id_or_feature_key!r}"
            )
        return cast(
            Entitlement,
            self._put(
                f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id_or_feature_key}/override",
                body=maybe_transform(
                    {
                        "type": type,
                        "usage_period": usage_period,
                        "feature_id": feature_id,
                        "feature_key": feature_key,
                        "is_soft_limit": is_soft_limit,
                        "issue_after_reset": issue_after_reset,
                        "issue_after_reset_priority": issue_after_reset_priority,
                        "is_unlimited": is_unlimited,
                        "measure_usage_from": measure_usage_from,
                        "metadata": metadata,
                        "preserve_overage_at_reset": preserve_overage_at_reset,
                        "config": config,
                    },
                    entitlement_override_params.EntitlementOverrideParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Entitlement),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def reset(
        self,
        entitlement_id: str,
        *,
        subject_id_or_key: str,
        effective_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        preserve_overage: bool | NotGiven = NOT_GIVEN,
        retain_anchor: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Reset marks the start of a new usage period for the entitlement and initiates
        grant rollover. At the start of a period usage is zerod out and grants are
        rolled over based on their rollover settings. It would typically be synced with
        the subjects billing period to enforce usage based on their subscription.

        Usage is automatically reset for metered entitlements based on their usage
        period, but this endpoint allows to manually reset it at any time. When doing so
        the period anchor of the entitlement can be changed if needed.

        Args:
          effective_at: The time at which the reset takes effect, defaults to now. The reset cannot be
              in the future. The provided value is truncated to the minute due to how
              historical meter data is stored.

          preserve_overage: Determines whether the overage is preserved or forgiven, overriding the
              entitlement's default behavior.

              - If true, the overage is preserved.
              - If false, the overage is forgiven.

          retain_anchor: Determines whether the usage period anchor is retained or reset to the
              effectiveAt time.

              - If true, the usage period anchor is retained.
              - If false, the usage period anchor is reset to the effectiveAt time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id}/reset",
            body=maybe_transform(
                {
                    "effective_at": effective_at,
                    "preserve_overage": preserve_overage,
                    "retain_anchor": retain_anchor,
                },
                entitlement_reset_params.EntitlementResetParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def value(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        time: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EntitlementValue:
        """This endpoint should be used for access checks and enforcement.

        All entitlement
        types share the hasAccess property in their value response, but multiple other
        properties are returned based on the entitlement type.

        For convenience reasons, /value works with both entitlementId and featureKey.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id_or_feature_key:
            raise ValueError(
                f"Expected a non-empty value for `entitlement_id_or_feature_key` but received {entitlement_id_or_feature_key!r}"
            )
        return self._get(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id_or_feature_key}/value",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"time": time}, entitlement_value_params.EntitlementValueParams),
            ),
            cast_to=EntitlementValue,
        )


class AsyncEntitlementsResource(AsyncAPIResource):
    @cached_property
    def grants(self) -> AsyncGrantsResource:
        return AsyncGrantsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEntitlementsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEntitlementsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEntitlementsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return AsyncEntitlementsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        subject_id_or_key: str,
        *,
        type: Literal["metered"],
        usage_period: entitlement_create_params.EntitlementMeteredCreateInputsUsagePeriod,
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        is_soft_limit: bool | NotGiven = NOT_GIVEN,
        issue_after_reset: float | NotGiven = NOT_GIVEN,
        issue_after_reset_priority: int | NotGiven = NOT_GIVEN,
        is_unlimited: bool | NotGiven = NOT_GIVEN,
        measure_usage_from: Union[Literal["CURRENT_PERIOD_START", "NOW"], Union[str, datetime]] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        preserve_overage_at_reset: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """OpenMeter has three types of entitlements: metered, boolean, and static.

        The
        type property determines the type of entitlement. The underlying feature has to
        be compatible with the entitlement type specified in the request (e.g., a
        metered entitlement needs a feature associated with a meter).

        - Boolean entitlements define static feature access, e.g. "Can use SSO
          authentication".
        - Static entitlements let you pass along a configuration while granting access,
          e.g. "Using this feature with X Y settings" (passed in the config).
        - Metered entitlements have many use cases, from setting up usage-based access
          to implementing complex credit systems. Example: The customer can use 10000 AI
          tokens during the usage period of the entitlement.

        A given subject can only have one active (non-deleted) entitlement per
        featureKey. If you try to create a new entitlement for a featureKey that already
        has an active entitlement, the request will fail with a 409 error.

        Once an entitlement is created you cannot modify it, only delete it.

        Args:
          usage_period: Recurring period with an interval and an anchor.

          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          is_soft_limit: If softLimit=true the subject can use the feature even if the entitlement is
              exhausted, hasAccess will always be true.

          issue_after_reset: You can grant usage automatically alongside the entitlement, the example
              scenario would be creating a starting balance. If an amount is specified here, a
              grant will be created alongside the entitlement with the specified amount. That
              grant will have it's rollover settings configured in a way that after each reset
              operation, the balance will return the original amount specified here. Manually
              creating such a grant would mean having the "amount", "minRolloverAmount", and
              "maxRolloverAmount" fields all be the same.

          issue_after_reset_priority: Defines the grant priority for the default grant.

          is_unlimited: Deprecated, ignored by the backend. Please use isSoftLimit instead; this field
              will be removed in the future.

          measure_usage_from: Measure usage from

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          preserve_overage_at_reset: If true, the overage is preserved at reset. If false, the usage is reset to 0.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        subject_id_or_key: str,
        *,
        config: str,
        type: Literal["static"],
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        usage_period: entitlement_create_params.EntitlementStaticCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """OpenMeter has three types of entitlements: metered, boolean, and static.

        The
        type property determines the type of entitlement. The underlying feature has to
        be compatible with the entitlement type specified in the request (e.g., a
        metered entitlement needs a feature associated with a meter).

        - Boolean entitlements define static feature access, e.g. "Can use SSO
          authentication".
        - Static entitlements let you pass along a configuration while granting access,
          e.g. "Using this feature with X Y settings" (passed in the config).
        - Metered entitlements have many use cases, from setting up usage-based access
          to implementing complex credit systems. Example: The customer can use 10000 AI
          tokens during the usage period of the entitlement.

        A given subject can only have one active (non-deleted) entitlement per
        featureKey. If you try to create a new entitlement for a featureKey that already
        has an active entitlement, the request will fail with a 409 error.

        Once an entitlement is created you cannot modify it, only delete it.

        Args:
          config: The JSON parsable config of the entitlement. This value is also returned when
              checking entitlement access and it is useful for configuring fine-grained access
              settings to the feature, implemented in your own system. Has to be an object.

          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          usage_period: Recurring period with an interval and an anchor.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        subject_id_or_key: str,
        *,
        type: Literal["boolean"],
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        usage_period: entitlement_create_params.EntitlementBooleanCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """OpenMeter has three types of entitlements: metered, boolean, and static.

        The
        type property determines the type of entitlement. The underlying feature has to
        be compatible with the entitlement type specified in the request (e.g., a
        metered entitlement needs a feature associated with a meter).

        - Boolean entitlements define static feature access, e.g. "Can use SSO
          authentication".
        - Static entitlements let you pass along a configuration while granting access,
          e.g. "Using this feature with X Y settings" (passed in the config).
        - Metered entitlements have many use cases, from setting up usage-based access
          to implementing complex credit systems. Example: The customer can use 10000 AI
          tokens during the usage period of the entitlement.

        A given subject can only have one active (non-deleted) entitlement per
        featureKey. If you try to create a new entitlement for a featureKey that already
        has an active entitlement, the request will fail with a 409 error.

        Once an entitlement is created you cannot modify it, only delete it.

        Args:
          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          usage_period: Recurring period with an interval and an anchor.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["type", "usage_period"], ["config", "type"], ["type"])
    async def create(
        self,
        subject_id_or_key: str,
        *,
        type: Literal["metered"] | Literal["static"] | Literal["boolean"],
        usage_period: entitlement_create_params.EntitlementMeteredCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        is_soft_limit: bool | NotGiven = NOT_GIVEN,
        issue_after_reset: float | NotGiven = NOT_GIVEN,
        issue_after_reset_priority: int | NotGiven = NOT_GIVEN,
        is_unlimited: bool | NotGiven = NOT_GIVEN,
        measure_usage_from: Union[Literal["CURRENT_PERIOD_START", "NOW"], Union[str, datetime]] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        preserve_overage_at_reset: bool | NotGiven = NOT_GIVEN,
        config: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        return cast(
            Entitlement,
            await self._post(
                f"/api/v1/subjects/{subject_id_or_key}/entitlements",
                body=await async_maybe_transform(
                    {
                        "type": type,
                        "usage_period": usage_period,
                        "feature_id": feature_id,
                        "feature_key": feature_key,
                        "is_soft_limit": is_soft_limit,
                        "issue_after_reset": issue_after_reset,
                        "issue_after_reset_priority": issue_after_reset_priority,
                        "is_unlimited": is_unlimited,
                        "measure_usage_from": measure_usage_from,
                        "metadata": metadata,
                        "preserve_overage_at_reset": preserve_overage_at_reset,
                        "config": config,
                    },
                    entitlement_create_params.EntitlementCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Entitlement),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        entitlement_id: str,
        *,
        subject_id_or_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """Get entitlement by id.

        For checking entitlement access, use the /value endpoint
        instead.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        return cast(
            Entitlement,
            await self._get(
                f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Entitlement),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def list(
        self,
        subject_id_or_key: str,
        *,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EntitlementListResponse:
        """List all entitlements for a subject.

        For checking entitlement access, use the
        /value endpoint instead.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        return await self._get(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_deleted": include_deleted}, entitlement_list_params.EntitlementListParams
                ),
            ),
            cast_to=EntitlementListResponse,
        )

    async def delete(
        self,
        entitlement_id: str,
        *,
        subject_id_or_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Deleting an entitlement revokes access to the associated feature.

        As a single
        subject can only have one entitlement per featureKey, when "migrating" features
        you have to delete the old entitlements as well. As access and status checks can
        be historical queries, deleting an entitlement populates the deletedAt
        timestamp. When queried for a time before that, the entitlement is still
        considered active, you cannot have retroactive changes to access, which is
        important for, among other things, auditing.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def history(
        self,
        entitlement_id: str,
        *,
        subject_id_or_key: str,
        window_size: Literal["MINUTE", "HOUR", "DAY"],
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        window_time_zone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EntitlementHistoryResponse:
        """Returns historical balance and usage data for the entitlement.

        The queried
        history can span accross multiple reset events.

        BurndownHistory returns a continous history of segments, where the segments are
        seperated by events that changed either the grant burndown priority or the usage
        period.

        WindowedHistory returns windowed usage data for the period enriched with balance
        information and the list of grants that were being burnt down in that window.

        Args:
          window_size: Windowsize

          from_: Start of time range to query entitlement: date-time in RFC 3339 format. Defaults
              to the last reset. Gets truncated to the granularity of the underlying meter.

          to: End of time range to query entitlement: date-time in RFC 3339 format. Defaults
              to now. If not now then gets truncated to the granularity of the underlying
              meter.

          window_time_zone: The timezone used when calculating the windows.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        return await self._get(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id}/history",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "window_size": window_size,
                        "from_": from_,
                        "to": to,
                        "window_time_zone": window_time_zone,
                    },
                    entitlement_history_params.EntitlementHistoryParams,
                ),
            ),
            cast_to=EntitlementHistoryResponse,
        )

    @overload
    async def override(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        type: Literal["metered"],
        usage_period: entitlement_override_params.EntitlementMeteredCreateInputsUsagePeriod,
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        is_soft_limit: bool | NotGiven = NOT_GIVEN,
        issue_after_reset: float | NotGiven = NOT_GIVEN,
        issue_after_reset_priority: int | NotGiven = NOT_GIVEN,
        is_unlimited: bool | NotGiven = NOT_GIVEN,
        measure_usage_from: Union[Literal["CURRENT_PERIOD_START", "NOW"], Union[str, datetime]] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        preserve_overage_at_reset: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """
        Overriding an entitlement creates a new entitlement from the provided inputs and
        soft deletes the previous entitlement for the provided subject-feature pair. If
        the previous entitlement is already deleted or otherwise doesnt exist, the
        override will fail.

        This endpoint is useful for upgrades, downgrades, or other changes to
        entitlements that require a new entitlement to be created with zero downtime.

        Args:
          usage_period: Recurring period with an interval and an anchor.

          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          is_soft_limit: If softLimit=true the subject can use the feature even if the entitlement is
              exhausted, hasAccess will always be true.

          issue_after_reset: You can grant usage automatically alongside the entitlement, the example
              scenario would be creating a starting balance. If an amount is specified here, a
              grant will be created alongside the entitlement with the specified amount. That
              grant will have it's rollover settings configured in a way that after each reset
              operation, the balance will return the original amount specified here. Manually
              creating such a grant would mean having the "amount", "minRolloverAmount", and
              "maxRolloverAmount" fields all be the same.

          issue_after_reset_priority: Defines the grant priority for the default grant.

          is_unlimited: Deprecated, ignored by the backend. Please use isSoftLimit instead; this field
              will be removed in the future.

          measure_usage_from: Measure usage from

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          preserve_overage_at_reset: If true, the overage is preserved at reset. If false, the usage is reset to 0.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def override(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        config: str,
        type: Literal["static"],
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        usage_period: entitlement_override_params.EntitlementStaticCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """
        Overriding an entitlement creates a new entitlement from the provided inputs and
        soft deletes the previous entitlement for the provided subject-feature pair. If
        the previous entitlement is already deleted or otherwise doesnt exist, the
        override will fail.

        This endpoint is useful for upgrades, downgrades, or other changes to
        entitlements that require a new entitlement to be created with zero downtime.

        Args:
          config: The JSON parsable config of the entitlement. This value is also returned when
              checking entitlement access and it is useful for configuring fine-grained access
              settings to the feature, implemented in your own system. Has to be an object.

          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          usage_period: Recurring period with an interval and an anchor.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def override(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        type: Literal["boolean"],
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        usage_period: entitlement_override_params.EntitlementBooleanCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """
        Overriding an entitlement creates a new entitlement from the provided inputs and
        soft deletes the previous entitlement for the provided subject-feature pair. If
        the previous entitlement is already deleted or otherwise doesnt exist, the
        override will fail.

        This endpoint is useful for upgrades, downgrades, or other changes to
        entitlements that require a new entitlement to be created with zero downtime.

        Args:
          feature_id: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          feature_key: The feature the subject is entitled to use. Either featureKey or featureId is
              required.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          usage_period: Recurring period with an interval and an anchor.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["subject_id_or_key", "type", "usage_period"],
        ["subject_id_or_key", "config", "type"],
        ["subject_id_or_key", "type"],
    )
    async def override(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        type: Literal["metered"] | Literal["static"] | Literal["boolean"],
        usage_period: entitlement_override_params.EntitlementMeteredCreateInputsUsagePeriod | NotGiven = NOT_GIVEN,
        feature_id: str | NotGiven = NOT_GIVEN,
        feature_key: str | NotGiven = NOT_GIVEN,
        is_soft_limit: bool | NotGiven = NOT_GIVEN,
        issue_after_reset: float | NotGiven = NOT_GIVEN,
        issue_after_reset_priority: int | NotGiven = NOT_GIVEN,
        is_unlimited: bool | NotGiven = NOT_GIVEN,
        measure_usage_from: Union[Literal["CURRENT_PERIOD_START", "NOW"], Union[str, datetime]] | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        preserve_overage_at_reset: bool | NotGiven = NOT_GIVEN,
        config: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id_or_feature_key:
            raise ValueError(
                f"Expected a non-empty value for `entitlement_id_or_feature_key` but received {entitlement_id_or_feature_key!r}"
            )
        return cast(
            Entitlement,
            await self._put(
                f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id_or_feature_key}/override",
                body=await async_maybe_transform(
                    {
                        "type": type,
                        "usage_period": usage_period,
                        "feature_id": feature_id,
                        "feature_key": feature_key,
                        "is_soft_limit": is_soft_limit,
                        "issue_after_reset": issue_after_reset,
                        "issue_after_reset_priority": issue_after_reset_priority,
                        "is_unlimited": is_unlimited,
                        "measure_usage_from": measure_usage_from,
                        "metadata": metadata,
                        "preserve_overage_at_reset": preserve_overage_at_reset,
                        "config": config,
                    },
                    entitlement_override_params.EntitlementOverrideParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Entitlement),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def reset(
        self,
        entitlement_id: str,
        *,
        subject_id_or_key: str,
        effective_at: Union[str, datetime] | NotGiven = NOT_GIVEN,
        preserve_overage: bool | NotGiven = NOT_GIVEN,
        retain_anchor: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Reset marks the start of a new usage period for the entitlement and initiates
        grant rollover. At the start of a period usage is zerod out and grants are
        rolled over based on their rollover settings. It would typically be synced with
        the subjects billing period to enforce usage based on their subscription.

        Usage is automatically reset for metered entitlements based on their usage
        period, but this endpoint allows to manually reset it at any time. When doing so
        the period anchor of the entitlement can be changed if needed.

        Args:
          effective_at: The time at which the reset takes effect, defaults to now. The reset cannot be
              in the future. The provided value is truncated to the minute due to how
              historical meter data is stored.

          preserve_overage: Determines whether the overage is preserved or forgiven, overriding the
              entitlement's default behavior.

              - If true, the overage is preserved.
              - If false, the overage is forgiven.

          retain_anchor: Determines whether the usage period anchor is retained or reset to the
              effectiveAt time.

              - If true, the usage period anchor is retained.
              - If false, the usage period anchor is reset to the effectiveAt time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id}/reset",
            body=await async_maybe_transform(
                {
                    "effective_at": effective_at,
                    "preserve_overage": preserve_overage,
                    "retain_anchor": retain_anchor,
                },
                entitlement_reset_params.EntitlementResetParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def value(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        time: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EntitlementValue:
        """This endpoint should be used for access checks and enforcement.

        All entitlement
        types share the hasAccess property in their value response, but multiple other
        properties are returned based on the entitlement type.

        For convenience reasons, /value works with both entitlementId and featureKey.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        if not entitlement_id_or_feature_key:
            raise ValueError(
                f"Expected a non-empty value for `entitlement_id_or_feature_key` but received {entitlement_id_or_feature_key!r}"
            )
        return await self._get(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id_or_feature_key}/value",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"time": time}, entitlement_value_params.EntitlementValueParams),
            ),
            cast_to=EntitlementValue,
        )


class EntitlementsResourceWithRawResponse:
    def __init__(self, entitlements: EntitlementsResource) -> None:
        self._entitlements = entitlements

        self.create = to_raw_response_wrapper(
            entitlements.create,
        )
        self.retrieve = to_raw_response_wrapper(
            entitlements.retrieve,
        )
        self.list = to_raw_response_wrapper(
            entitlements.list,
        )
        self.delete = to_raw_response_wrapper(
            entitlements.delete,
        )
        self.history = to_raw_response_wrapper(
            entitlements.history,
        )
        self.override = to_raw_response_wrapper(
            entitlements.override,
        )
        self.reset = to_raw_response_wrapper(
            entitlements.reset,
        )
        self.value = to_raw_response_wrapper(
            entitlements.value,
        )

    @cached_property
    def grants(self) -> GrantsResourceWithRawResponse:
        return GrantsResourceWithRawResponse(self._entitlements.grants)


class AsyncEntitlementsResourceWithRawResponse:
    def __init__(self, entitlements: AsyncEntitlementsResource) -> None:
        self._entitlements = entitlements

        self.create = async_to_raw_response_wrapper(
            entitlements.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            entitlements.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            entitlements.list,
        )
        self.delete = async_to_raw_response_wrapper(
            entitlements.delete,
        )
        self.history = async_to_raw_response_wrapper(
            entitlements.history,
        )
        self.override = async_to_raw_response_wrapper(
            entitlements.override,
        )
        self.reset = async_to_raw_response_wrapper(
            entitlements.reset,
        )
        self.value = async_to_raw_response_wrapper(
            entitlements.value,
        )

    @cached_property
    def grants(self) -> AsyncGrantsResourceWithRawResponse:
        return AsyncGrantsResourceWithRawResponse(self._entitlements.grants)


class EntitlementsResourceWithStreamingResponse:
    def __init__(self, entitlements: EntitlementsResource) -> None:
        self._entitlements = entitlements

        self.create = to_streamed_response_wrapper(
            entitlements.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            entitlements.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            entitlements.list,
        )
        self.delete = to_streamed_response_wrapper(
            entitlements.delete,
        )
        self.history = to_streamed_response_wrapper(
            entitlements.history,
        )
        self.override = to_streamed_response_wrapper(
            entitlements.override,
        )
        self.reset = to_streamed_response_wrapper(
            entitlements.reset,
        )
        self.value = to_streamed_response_wrapper(
            entitlements.value,
        )

    @cached_property
    def grants(self) -> GrantsResourceWithStreamingResponse:
        return GrantsResourceWithStreamingResponse(self._entitlements.grants)


class AsyncEntitlementsResourceWithStreamingResponse:
    def __init__(self, entitlements: AsyncEntitlementsResource) -> None:
        self._entitlements = entitlements

        self.create = async_to_streamed_response_wrapper(
            entitlements.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            entitlements.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            entitlements.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            entitlements.delete,
        )
        self.history = async_to_streamed_response_wrapper(
            entitlements.history,
        )
        self.override = async_to_streamed_response_wrapper(
            entitlements.override,
        )
        self.reset = async_to_streamed_response_wrapper(
            entitlements.reset,
        )
        self.value = async_to_streamed_response_wrapper(
            entitlements.value,
        )

    @cached_property
    def grants(self) -> AsyncGrantsResourceWithStreamingResponse:
        return AsyncGrantsResourceWithStreamingResponse(self._entitlements.grants)
