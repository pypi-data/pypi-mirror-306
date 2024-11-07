# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.notifications import rule_list_params, rule_create_params, rule_update_params
from ...types.notifications.notification_rule import NotificationRule
from ...types.notifications.notification_event import NotificationEvent
from ...types.notifications.rule_list_response import RuleListResponse

__all__ = ["RulesResource", "AsyncRulesResource"]


class RulesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RulesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return RulesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RulesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return RulesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        channels: List[str],
        name: str,
        thresholds: Iterable[rule_create_params.Threshold],
        type: Literal["entitlements.balance.threshold"],
        disabled: bool | NotGiven = NOT_GIVEN,
        features: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationRule:
        """
        Create a new notification rule.

        Args:
          channels: List of notification channels the rule is applied to.

          name: The user friendly name of the notification rule.

          thresholds: List of thresholds the rule suppose to be triggered.

          type: Notification rule type.

          disabled: Whether the rule is disabled or not.

          features: Optional field for defining the scope of notification by feature. It may contain
              features by id or key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/notification/rules",
            body=maybe_transform(
                {
                    "channels": channels,
                    "name": name,
                    "thresholds": thresholds,
                    "type": type,
                    "disabled": disabled,
                    "features": features,
                },
                rule_create_params.RuleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationRule,
        )

    def retrieve(
        self,
        rule_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationRule:
        """
        Get a notification rule by id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rule_id:
            raise ValueError(f"Expected a non-empty value for `rule_id` but received {rule_id!r}")
        return self._get(
            f"/api/v1/notification/rules/{rule_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationRule,
        )

    def update(
        self,
        rule_id: str,
        *,
        channels: List[str],
        name: str,
        thresholds: Iterable[rule_update_params.Threshold],
        type: Literal["entitlements.balance.threshold"],
        disabled: bool | NotGiven = NOT_GIVEN,
        features: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationRule:
        """
        Update notification rule.

        Args:
          channels: List of notification channels the rule is applied to.

          name: The user friendly name of the notification rule.

          thresholds: List of thresholds the rule suppose to be triggered.

          type: Notification rule type.

          disabled: Whether the rule is disabled or not.

          features: Optional field for defining the scope of notification by feature. It may contain
              features by id or key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rule_id:
            raise ValueError(f"Expected a non-empty value for `rule_id` but received {rule_id!r}")
        return self._put(
            f"/api/v1/notification/rules/{rule_id}",
            body=maybe_transform(
                {
                    "channels": channels,
                    "name": name,
                    "thresholds": thresholds,
                    "type": type,
                    "disabled": disabled,
                    "features": features,
                },
                rule_update_params.RuleUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationRule,
        )

    def list(
        self,
        *,
        channel: List[str] | NotGiven = NOT_GIVEN,
        feature: List[str] | NotGiven = NOT_GIVEN,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        include_disabled: bool | NotGiven = NOT_GIVEN,
        order: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        order_by: Literal["id", "type", "createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RuleListResponse:
        """
        List all notification rules.

        Args:
          channel: Filtering by multiple notifiaction channel ids.

              Usage: `?channel=01ARZ3NDEKTSV4RRFFQ69G5FAV&channel=01J8J2Y5X4NNGQS32CF81W95E3`

          feature: Filtering by multiple feature ids/keys.

              Usage: `?feature=feature-1&feature=feature-2`

          include_deleted: Include deleted notification rules in response.

              Usage: `?includeDeleted=true`

          include_disabled: Include disabled notification rules in response.

              Usage: `?includeDisabled=false`

          order: The order direction.

          order_by: The order by field.

          page: Start date-time in RFC 3339 format.

              Inclusive.

          page_size: Number of items per page.

              Default is 100.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v1/notification/rules",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "channel": channel,
                        "feature": feature,
                        "include_deleted": include_deleted,
                        "include_disabled": include_disabled,
                        "order": order,
                        "order_by": order_by,
                        "page": page,
                        "page_size": page_size,
                    },
                    rule_list_params.RuleListParams,
                ),
            ),
            cast_to=RuleListResponse,
        )

    def delete(
        self,
        rule_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Soft delete notification rule by id.

        Once a notification rule is deleted it cannot be undeleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rule_id:
            raise ValueError(f"Expected a non-empty value for `rule_id` but received {rule_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v1/notification/rules/{rule_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def test(
        self,
        rule_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationEvent:
        """
        Test a notification rule by sending a test event with random data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rule_id:
            raise ValueError(f"Expected a non-empty value for `rule_id` but received {rule_id!r}")
        return self._post(
            f"/api/v1/notification/rules/{rule_id}/test",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationEvent,
        )


class AsyncRulesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRulesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRulesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRulesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return AsyncRulesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        channels: List[str],
        name: str,
        thresholds: Iterable[rule_create_params.Threshold],
        type: Literal["entitlements.balance.threshold"],
        disabled: bool | NotGiven = NOT_GIVEN,
        features: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationRule:
        """
        Create a new notification rule.

        Args:
          channels: List of notification channels the rule is applied to.

          name: The user friendly name of the notification rule.

          thresholds: List of thresholds the rule suppose to be triggered.

          type: Notification rule type.

          disabled: Whether the rule is disabled or not.

          features: Optional field for defining the scope of notification by feature. It may contain
              features by id or key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/notification/rules",
            body=await async_maybe_transform(
                {
                    "channels": channels,
                    "name": name,
                    "thresholds": thresholds,
                    "type": type,
                    "disabled": disabled,
                    "features": features,
                },
                rule_create_params.RuleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationRule,
        )

    async def retrieve(
        self,
        rule_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationRule:
        """
        Get a notification rule by id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rule_id:
            raise ValueError(f"Expected a non-empty value for `rule_id` but received {rule_id!r}")
        return await self._get(
            f"/api/v1/notification/rules/{rule_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationRule,
        )

    async def update(
        self,
        rule_id: str,
        *,
        channels: List[str],
        name: str,
        thresholds: Iterable[rule_update_params.Threshold],
        type: Literal["entitlements.balance.threshold"],
        disabled: bool | NotGiven = NOT_GIVEN,
        features: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationRule:
        """
        Update notification rule.

        Args:
          channels: List of notification channels the rule is applied to.

          name: The user friendly name of the notification rule.

          thresholds: List of thresholds the rule suppose to be triggered.

          type: Notification rule type.

          disabled: Whether the rule is disabled or not.

          features: Optional field for defining the scope of notification by feature. It may contain
              features by id or key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rule_id:
            raise ValueError(f"Expected a non-empty value for `rule_id` but received {rule_id!r}")
        return await self._put(
            f"/api/v1/notification/rules/{rule_id}",
            body=await async_maybe_transform(
                {
                    "channels": channels,
                    "name": name,
                    "thresholds": thresholds,
                    "type": type,
                    "disabled": disabled,
                    "features": features,
                },
                rule_update_params.RuleUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationRule,
        )

    async def list(
        self,
        *,
        channel: List[str] | NotGiven = NOT_GIVEN,
        feature: List[str] | NotGiven = NOT_GIVEN,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        include_disabled: bool | NotGiven = NOT_GIVEN,
        order: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        order_by: Literal["id", "type", "createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RuleListResponse:
        """
        List all notification rules.

        Args:
          channel: Filtering by multiple notifiaction channel ids.

              Usage: `?channel=01ARZ3NDEKTSV4RRFFQ69G5FAV&channel=01J8J2Y5X4NNGQS32CF81W95E3`

          feature: Filtering by multiple feature ids/keys.

              Usage: `?feature=feature-1&feature=feature-2`

          include_deleted: Include deleted notification rules in response.

              Usage: `?includeDeleted=true`

          include_disabled: Include disabled notification rules in response.

              Usage: `?includeDisabled=false`

          order: The order direction.

          order_by: The order by field.

          page: Start date-time in RFC 3339 format.

              Inclusive.

          page_size: Number of items per page.

              Default is 100.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v1/notification/rules",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "channel": channel,
                        "feature": feature,
                        "include_deleted": include_deleted,
                        "include_disabled": include_disabled,
                        "order": order,
                        "order_by": order_by,
                        "page": page,
                        "page_size": page_size,
                    },
                    rule_list_params.RuleListParams,
                ),
            ),
            cast_to=RuleListResponse,
        )

    async def delete(
        self,
        rule_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Soft delete notification rule by id.

        Once a notification rule is deleted it cannot be undeleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rule_id:
            raise ValueError(f"Expected a non-empty value for `rule_id` but received {rule_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v1/notification/rules/{rule_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def test(
        self,
        rule_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationEvent:
        """
        Test a notification rule by sending a test event with random data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rule_id:
            raise ValueError(f"Expected a non-empty value for `rule_id` but received {rule_id!r}")
        return await self._post(
            f"/api/v1/notification/rules/{rule_id}/test",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationEvent,
        )


class RulesResourceWithRawResponse:
    def __init__(self, rules: RulesResource) -> None:
        self._rules = rules

        self.create = to_raw_response_wrapper(
            rules.create,
        )
        self.retrieve = to_raw_response_wrapper(
            rules.retrieve,
        )
        self.update = to_raw_response_wrapper(
            rules.update,
        )
        self.list = to_raw_response_wrapper(
            rules.list,
        )
        self.delete = to_raw_response_wrapper(
            rules.delete,
        )
        self.test = to_raw_response_wrapper(
            rules.test,
        )


class AsyncRulesResourceWithRawResponse:
    def __init__(self, rules: AsyncRulesResource) -> None:
        self._rules = rules

        self.create = async_to_raw_response_wrapper(
            rules.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            rules.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            rules.update,
        )
        self.list = async_to_raw_response_wrapper(
            rules.list,
        )
        self.delete = async_to_raw_response_wrapper(
            rules.delete,
        )
        self.test = async_to_raw_response_wrapper(
            rules.test,
        )


class RulesResourceWithStreamingResponse:
    def __init__(self, rules: RulesResource) -> None:
        self._rules = rules

        self.create = to_streamed_response_wrapper(
            rules.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            rules.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            rules.update,
        )
        self.list = to_streamed_response_wrapper(
            rules.list,
        )
        self.delete = to_streamed_response_wrapper(
            rules.delete,
        )
        self.test = to_streamed_response_wrapper(
            rules.test,
        )


class AsyncRulesResourceWithStreamingResponse:
    def __init__(self, rules: AsyncRulesResource) -> None:
        self._rules = rules

        self.create = async_to_streamed_response_wrapper(
            rules.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            rules.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            rules.update,
        )
        self.list = async_to_streamed_response_wrapper(
            rules.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            rules.delete,
        )
        self.test = async_to_streamed_response_wrapper(
            rules.test,
        )
