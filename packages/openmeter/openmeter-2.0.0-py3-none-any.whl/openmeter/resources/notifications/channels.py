# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
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
from ...types.notifications import channel_list_params, channel_create_params, channel_update_params
from ...types.notifications.notification_channel import NotificationChannel
from ...types.notifications.channel_list_response import ChannelListResponse

__all__ = ["ChannelsResource", "AsyncChannelsResource"]


class ChannelsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChannelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return ChannelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChannelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return ChannelsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        type: Literal["WEBHOOK"],
        url: str,
        custom_headers: Dict[str, str] | NotGiven = NOT_GIVEN,
        disabled: bool | NotGiven = NOT_GIVEN,
        signing_secret: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationChannel:
        """
        Create a new notification channel.

        Args:
          name: User friendly name of the channel.

          type: Notification channel type.

          url: Webhook URL where the notification is sent.

          custom_headers: Custom HTTP headers sent as part of the webhook request.

          disabled: Whether the channel is disabled or not.

          signing_secret: Signing secret used for webhook request validation on the receiving end.

              Format: `base64` encoded random bytes optionally prefixed with `whsec_`.
              Recommended size: 24

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/notification/channels",
            body=maybe_transform(
                {
                    "name": name,
                    "type": type,
                    "url": url,
                    "custom_headers": custom_headers,
                    "disabled": disabled,
                    "signing_secret": signing_secret,
                },
                channel_create_params.ChannelCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationChannel,
        )

    def retrieve(
        self,
        channel_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationChannel:
        """
        Get a notification channel by id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not channel_id:
            raise ValueError(f"Expected a non-empty value for `channel_id` but received {channel_id!r}")
        return self._get(
            f"/api/v1/notification/channels/{channel_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationChannel,
        )

    def update(
        self,
        channel_id: str,
        *,
        name: str,
        type: Literal["WEBHOOK"],
        url: str,
        custom_headers: Dict[str, str] | NotGiven = NOT_GIVEN,
        disabled: bool | NotGiven = NOT_GIVEN,
        signing_secret: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationChannel:
        """
        Update notification channel.

        Args:
          name: User friendly name of the channel.

          type: Notification channel type.

          url: Webhook URL where the notification is sent.

          custom_headers: Custom HTTP headers sent as part of the webhook request.

          disabled: Whether the channel is disabled or not.

          signing_secret: Signing secret used for webhook request validation on the receiving end.

              Format: `base64` encoded random bytes optionally prefixed with `whsec_`.
              Recommended size: 24

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not channel_id:
            raise ValueError(f"Expected a non-empty value for `channel_id` but received {channel_id!r}")
        return self._put(
            f"/api/v1/notification/channels/{channel_id}",
            body=maybe_transform(
                {
                    "name": name,
                    "type": type,
                    "url": url,
                    "custom_headers": custom_headers,
                    "disabled": disabled,
                    "signing_secret": signing_secret,
                },
                channel_update_params.ChannelUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationChannel,
        )

    def list(
        self,
        *,
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
    ) -> ChannelListResponse:
        """
        List all notification channels.

        Args:
          include_deleted: Include deleted notification channels in response.

              Usage: `?includeDeleted=true`

          include_disabled: Include disabled notification channels in response.

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
            "/api/v1/notification/channels",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_deleted": include_deleted,
                        "include_disabled": include_disabled,
                        "order": order,
                        "order_by": order_by,
                        "page": page,
                        "page_size": page_size,
                    },
                    channel_list_params.ChannelListParams,
                ),
            ),
            cast_to=ChannelListResponse,
        )

    def delete(
        self,
        channel_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Soft delete notification channel by id.

        Once a notification channel is deleted it cannot be undeleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not channel_id:
            raise ValueError(f"Expected a non-empty value for `channel_id` but received {channel_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v1/notification/channels/{channel_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncChannelsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChannelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChannelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChannelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return AsyncChannelsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        type: Literal["WEBHOOK"],
        url: str,
        custom_headers: Dict[str, str] | NotGiven = NOT_GIVEN,
        disabled: bool | NotGiven = NOT_GIVEN,
        signing_secret: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationChannel:
        """
        Create a new notification channel.

        Args:
          name: User friendly name of the channel.

          type: Notification channel type.

          url: Webhook URL where the notification is sent.

          custom_headers: Custom HTTP headers sent as part of the webhook request.

          disabled: Whether the channel is disabled or not.

          signing_secret: Signing secret used for webhook request validation on the receiving end.

              Format: `base64` encoded random bytes optionally prefixed with `whsec_`.
              Recommended size: 24

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/notification/channels",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "type": type,
                    "url": url,
                    "custom_headers": custom_headers,
                    "disabled": disabled,
                    "signing_secret": signing_secret,
                },
                channel_create_params.ChannelCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationChannel,
        )

    async def retrieve(
        self,
        channel_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationChannel:
        """
        Get a notification channel by id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not channel_id:
            raise ValueError(f"Expected a non-empty value for `channel_id` but received {channel_id!r}")
        return await self._get(
            f"/api/v1/notification/channels/{channel_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationChannel,
        )

    async def update(
        self,
        channel_id: str,
        *,
        name: str,
        type: Literal["WEBHOOK"],
        url: str,
        custom_headers: Dict[str, str] | NotGiven = NOT_GIVEN,
        disabled: bool | NotGiven = NOT_GIVEN,
        signing_secret: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotificationChannel:
        """
        Update notification channel.

        Args:
          name: User friendly name of the channel.

          type: Notification channel type.

          url: Webhook URL where the notification is sent.

          custom_headers: Custom HTTP headers sent as part of the webhook request.

          disabled: Whether the channel is disabled or not.

          signing_secret: Signing secret used for webhook request validation on the receiving end.

              Format: `base64` encoded random bytes optionally prefixed with `whsec_`.
              Recommended size: 24

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not channel_id:
            raise ValueError(f"Expected a non-empty value for `channel_id` but received {channel_id!r}")
        return await self._put(
            f"/api/v1/notification/channels/{channel_id}",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "type": type,
                    "url": url,
                    "custom_headers": custom_headers,
                    "disabled": disabled,
                    "signing_secret": signing_secret,
                },
                channel_update_params.ChannelUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NotificationChannel,
        )

    async def list(
        self,
        *,
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
    ) -> ChannelListResponse:
        """
        List all notification channels.

        Args:
          include_deleted: Include deleted notification channels in response.

              Usage: `?includeDeleted=true`

          include_disabled: Include disabled notification channels in response.

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
            "/api/v1/notification/channels",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "include_deleted": include_deleted,
                        "include_disabled": include_disabled,
                        "order": order,
                        "order_by": order_by,
                        "page": page,
                        "page_size": page_size,
                    },
                    channel_list_params.ChannelListParams,
                ),
            ),
            cast_to=ChannelListResponse,
        )

    async def delete(
        self,
        channel_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Soft delete notification channel by id.

        Once a notification channel is deleted it cannot be undeleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not channel_id:
            raise ValueError(f"Expected a non-empty value for `channel_id` but received {channel_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v1/notification/channels/{channel_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ChannelsResourceWithRawResponse:
    def __init__(self, channels: ChannelsResource) -> None:
        self._channels = channels

        self.create = to_raw_response_wrapper(
            channels.create,
        )
        self.retrieve = to_raw_response_wrapper(
            channels.retrieve,
        )
        self.update = to_raw_response_wrapper(
            channels.update,
        )
        self.list = to_raw_response_wrapper(
            channels.list,
        )
        self.delete = to_raw_response_wrapper(
            channels.delete,
        )


class AsyncChannelsResourceWithRawResponse:
    def __init__(self, channels: AsyncChannelsResource) -> None:
        self._channels = channels

        self.create = async_to_raw_response_wrapper(
            channels.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            channels.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            channels.update,
        )
        self.list = async_to_raw_response_wrapper(
            channels.list,
        )
        self.delete = async_to_raw_response_wrapper(
            channels.delete,
        )


class ChannelsResourceWithStreamingResponse:
    def __init__(self, channels: ChannelsResource) -> None:
        self._channels = channels

        self.create = to_streamed_response_wrapper(
            channels.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            channels.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            channels.update,
        )
        self.list = to_streamed_response_wrapper(
            channels.list,
        )
        self.delete = to_streamed_response_wrapper(
            channels.delete,
        )


class AsyncChannelsResourceWithStreamingResponse:
    def __init__(self, channels: AsyncChannelsResource) -> None:
        self._channels = channels

        self.create = async_to_streamed_response_wrapper(
            channels.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            channels.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            channels.update,
        )
        self.list = async_to_streamed_response_wrapper(
            channels.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            channels.delete,
        )
