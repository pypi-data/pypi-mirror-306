# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime
from typing_extensions import Literal

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
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
from ....types.subjects.entitlements import grant_list_params, grant_create_params
from ....types.subjects.entitlements.entitlement_grant import EntitlementGrant
from ....types.subjects.entitlements.grant_list_response import GrantListResponse

__all__ = ["GrantsResource", "AsyncGrantsResource"]


class GrantsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GrantsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return GrantsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GrantsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return GrantsResourceWithStreamingResponse(self)

    def create(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        amount: float,
        effective_at: Union[str, datetime],
        expiration: grant_create_params.Expiration,
        max_rollover_amount: float | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        min_rollover_amount: float | NotGiven = NOT_GIVEN,
        priority: int | NotGiven = NOT_GIVEN,
        recurrence: grant_create_params.Recurrence | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EntitlementGrant:
        """Grants define a behavior of granting usage for a metered entitlement.

        They can
        have complicated recurrence and rollover rules, thanks to which you can define a
        wide range of access patterns with a single grant, in most cases you don't have
        to periodically create new grants. You can only issue grants for active metered
        entitlements.

        A grant defines a given amount of usage that can be consumed for the
        entitlement. The grant is in effect between its effective date and its
        expiration date. Specifying both is mandatory for new grants.

        Grants have a priority setting that determines their order of use. Lower numbers
        have higher priority, with 0 being the highest priority.

        Grants can have a recurrence setting intended to automate the manual reissuing
        of grants. For example, a daily recurrence is equal to reissuing that same grant
        every day (ignoring rollover settings).

        Rollover settings define what happens to the remaining balance of a grant at a
        reset. Balance_After_Reset = MIN(MaxRolloverAmount, MAX(Balance_Before_Reset,
        MinRolloverAmount))

        Grants cannot be changed once created, only deleted. This is to ensure that
        balance is deterministic regardless of when it is queried.

        Args:
          amount: The amount to grant. Should be a positive number.

          effective_at: Effective date for grants and anchor for recurring grants. Provided value will
              be ceiled to metering windowSize (minute).

          expiration: The grant expiration definition

          max_rollover_amount: Grants are rolled over at reset, after which they can have a different balance
              compared to what they had before the reset. Balance after the reset is
              calculated as: Balance_After_Reset = MIN(MaxRolloverAmount,
              MAX(Balance_Before_Reset, MinRolloverAmount))

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          min_rollover_amount: Grants are rolled over at reset, after which they can have a different balance
              compared to what they had before the reset. Balance after the reset is
              calculated as: Balance_After_Reset = MIN(MaxRolloverAmount,
              MAX(Balance_Before_Reset, MinRolloverAmount))

          priority: The priority of the grant. Grants with higher priority are applied first.
              Priority is a positive decimal numbers. With lower numbers indicating higher
              importance. For example, a priority of 1 is more urgent than a priority of 2.
              When there are several grants available for the same subject, the system selects
              the grant with the highest priority. In cases where grants share the same
              priority level, the grant closest to its expiration will be used first. In the
              case of two grants have identical priorities and expiration dates, the system
              will use the grant that was created first.

          recurrence: Recurring period with an interval and an anchor.

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
        return self._post(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id_or_feature_key}/grants",
            body=maybe_transform(
                {
                    "amount": amount,
                    "effective_at": effective_at,
                    "expiration": expiration,
                    "max_rollover_amount": max_rollover_amount,
                    "metadata": metadata,
                    "min_rollover_amount": min_rollover_amount,
                    "priority": priority,
                    "recurrence": recurrence,
                },
                grant_create_params.GrantCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EntitlementGrant,
        )

    def list(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        order_by: Literal["id", "createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GrantListResponse:
        """List all grants issued for an entitlement.

        The entitlement can be defined either
        by its id or featureKey.

        Args:
          order_by: Order by options for grants.

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
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id_or_feature_key}/grants",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_deleted": include_deleted,
                        "order_by": order_by,
                    },
                    grant_list_params.GrantListParams,
                ),
            ),
            cast_to=GrantListResponse,
        )


class AsyncGrantsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGrantsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return AsyncGrantsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGrantsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return AsyncGrantsResourceWithStreamingResponse(self)

    async def create(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        amount: float,
        effective_at: Union[str, datetime],
        expiration: grant_create_params.Expiration,
        max_rollover_amount: float | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        min_rollover_amount: float | NotGiven = NOT_GIVEN,
        priority: int | NotGiven = NOT_GIVEN,
        recurrence: grant_create_params.Recurrence | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EntitlementGrant:
        """Grants define a behavior of granting usage for a metered entitlement.

        They can
        have complicated recurrence and rollover rules, thanks to which you can define a
        wide range of access patterns with a single grant, in most cases you don't have
        to periodically create new grants. You can only issue grants for active metered
        entitlements.

        A grant defines a given amount of usage that can be consumed for the
        entitlement. The grant is in effect between its effective date and its
        expiration date. Specifying both is mandatory for new grants.

        Grants have a priority setting that determines their order of use. Lower numbers
        have higher priority, with 0 being the highest priority.

        Grants can have a recurrence setting intended to automate the manual reissuing
        of grants. For example, a daily recurrence is equal to reissuing that same grant
        every day (ignoring rollover settings).

        Rollover settings define what happens to the remaining balance of a grant at a
        reset. Balance_After_Reset = MIN(MaxRolloverAmount, MAX(Balance_Before_Reset,
        MinRolloverAmount))

        Grants cannot be changed once created, only deleted. This is to ensure that
        balance is deterministic regardless of when it is queried.

        Args:
          amount: The amount to grant. Should be a positive number.

          effective_at: Effective date for grants and anchor for recurring grants. Provided value will
              be ceiled to metering windowSize (minute).

          expiration: The grant expiration definition

          max_rollover_amount: Grants are rolled over at reset, after which they can have a different balance
              compared to what they had before the reset. Balance after the reset is
              calculated as: Balance_After_Reset = MIN(MaxRolloverAmount,
              MAX(Balance_Before_Reset, MinRolloverAmount))

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          min_rollover_amount: Grants are rolled over at reset, after which they can have a different balance
              compared to what they had before the reset. Balance after the reset is
              calculated as: Balance_After_Reset = MIN(MaxRolloverAmount,
              MAX(Balance_Before_Reset, MinRolloverAmount))

          priority: The priority of the grant. Grants with higher priority are applied first.
              Priority is a positive decimal numbers. With lower numbers indicating higher
              importance. For example, a priority of 1 is more urgent than a priority of 2.
              When there are several grants available for the same subject, the system selects
              the grant with the highest priority. In cases where grants share the same
              priority level, the grant closest to its expiration will be used first. In the
              case of two grants have identical priorities and expiration dates, the system
              will use the grant that was created first.

          recurrence: Recurring period with an interval and an anchor.

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
        return await self._post(
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id_or_feature_key}/grants",
            body=await async_maybe_transform(
                {
                    "amount": amount,
                    "effective_at": effective_at,
                    "expiration": expiration,
                    "max_rollover_amount": max_rollover_amount,
                    "metadata": metadata,
                    "min_rollover_amount": min_rollover_amount,
                    "priority": priority,
                    "recurrence": recurrence,
                },
                grant_create_params.GrantCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EntitlementGrant,
        )

    async def list(
        self,
        entitlement_id_or_feature_key: str,
        *,
        subject_id_or_key: str,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        order_by: Literal["id", "createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GrantListResponse:
        """List all grants issued for an entitlement.

        The entitlement can be defined either
        by its id or featureKey.

        Args:
          order_by: Order by options for grants.

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
            f"/api/v1/subjects/{subject_id_or_key}/entitlements/{entitlement_id_or_feature_key}/grants",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "include_deleted": include_deleted,
                        "order_by": order_by,
                    },
                    grant_list_params.GrantListParams,
                ),
            ),
            cast_to=GrantListResponse,
        )


class GrantsResourceWithRawResponse:
    def __init__(self, grants: GrantsResource) -> None:
        self._grants = grants

        self.create = to_raw_response_wrapper(
            grants.create,
        )
        self.list = to_raw_response_wrapper(
            grants.list,
        )


class AsyncGrantsResourceWithRawResponse:
    def __init__(self, grants: AsyncGrantsResource) -> None:
        self._grants = grants

        self.create = async_to_raw_response_wrapper(
            grants.create,
        )
        self.list = async_to_raw_response_wrapper(
            grants.list,
        )


class GrantsResourceWithStreamingResponse:
    def __init__(self, grants: GrantsResource) -> None:
        self._grants = grants

        self.create = to_streamed_response_wrapper(
            grants.create,
        )
        self.list = to_streamed_response_wrapper(
            grants.list,
        )


class AsyncGrantsResourceWithStreamingResponse:
    def __init__(self, grants: AsyncGrantsResource) -> None:
        self._grants = grants

        self.create = async_to_streamed_response_wrapper(
            grants.create,
        )
        self.list = async_to_streamed_response_wrapper(
            grants.list,
        )
