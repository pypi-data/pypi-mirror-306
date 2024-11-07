# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, List, cast
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
from ...types.entitlements import grant_list_params
from ...types.entitlements.grant_list_response import GrantListResponse

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

    def list(
        self,
        *,
        feature: List[str] | NotGiven = NOT_GIVEN,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        order_by: Literal["id", "createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        subject: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GrantListResponse:
        """List all grants for all the subjects and entitlements.

        This endpoint is intended
        for administrative purposes only. To fetch the grants of a specific entitlement
        please use the
        /api/v1/subjects/{subjectKeyOrID}/entitlements/{entitlementOrFeatureID}/grants
        endpoint. If page is provided that takes precedence and the paginated response
        is returned.

        Args:
          feature: Filtering by multiple features.

              Usage: `?feature=feature-1&feature=feature-2`

          include_deleted: Include deleted

          limit: Number of items to return.

              Default is 100.

          offset: Number of items to skip.

              Default is 0.

          order: The order direction.

          order_by: The order by field.

          page: Start date-time in RFC 3339 format.

              Inclusive.

          page_size: Number of items per page.

              Default is 100.

          subject: Filtering by multiple subjects.

              Usage: `?subject=customer-1&subject=customer-2`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            GrantListResponse,
            self._get(
                "/api/v1/grants",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {
                            "feature": feature,
                            "include_deleted": include_deleted,
                            "limit": limit,
                            "offset": offset,
                            "order": order,
                            "order_by": order_by,
                            "page": page,
                            "page_size": page_size,
                            "subject": subject,
                        },
                        grant_list_params.GrantListParams,
                    ),
                ),
                cast_to=cast(Any, GrantListResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def void(
        self,
        grant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Voiding a grant means it is no longer valid, it doesn't take part in further
        balance calculations. Voiding a grant does not retroactively take effect,
        meaning any usage that has already been attributed to the grant will remain, but
        future usage cannot be burnt down from the grant. For example, if you have a
        single grant for your metered entitlement with an initial amount of 100, and so
        far 60 usage has been metered, the grant (and the entitlement itself) would have
        a balance of 40. If you then void that grant, balance becomes 0, but the 60
        previous usage will not be affected.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not grant_id:
            raise ValueError(f"Expected a non-empty value for `grant_id` but received {grant_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v1/grants/{grant_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
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

    async def list(
        self,
        *,
        feature: List[str] | NotGiven = NOT_GIVEN,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        order_by: Literal["id", "createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        subject: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GrantListResponse:
        """List all grants for all the subjects and entitlements.

        This endpoint is intended
        for administrative purposes only. To fetch the grants of a specific entitlement
        please use the
        /api/v1/subjects/{subjectKeyOrID}/entitlements/{entitlementOrFeatureID}/grants
        endpoint. If page is provided that takes precedence and the paginated response
        is returned.

        Args:
          feature: Filtering by multiple features.

              Usage: `?feature=feature-1&feature=feature-2`

          include_deleted: Include deleted

          limit: Number of items to return.

              Default is 100.

          offset: Number of items to skip.

              Default is 0.

          order: The order direction.

          order_by: The order by field.

          page: Start date-time in RFC 3339 format.

              Inclusive.

          page_size: Number of items per page.

              Default is 100.

          subject: Filtering by multiple subjects.

              Usage: `?subject=customer-1&subject=customer-2`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            GrantListResponse,
            await self._get(
                "/api/v1/grants",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {
                            "feature": feature,
                            "include_deleted": include_deleted,
                            "limit": limit,
                            "offset": offset,
                            "order": order,
                            "order_by": order_by,
                            "page": page,
                            "page_size": page_size,
                            "subject": subject,
                        },
                        grant_list_params.GrantListParams,
                    ),
                ),
                cast_to=cast(Any, GrantListResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def void(
        self,
        grant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Voiding a grant means it is no longer valid, it doesn't take part in further
        balance calculations. Voiding a grant does not retroactively take effect,
        meaning any usage that has already been attributed to the grant will remain, but
        future usage cannot be burnt down from the grant. For example, if you have a
        single grant for your metered entitlement with an initial amount of 100, and so
        far 60 usage has been metered, the grant (and the entitlement itself) would have
        a balance of 40. If you then void that grant, balance becomes 0, but the 60
        previous usage will not be affected.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not grant_id:
            raise ValueError(f"Expected a non-empty value for `grant_id` but received {grant_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v1/grants/{grant_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class GrantsResourceWithRawResponse:
    def __init__(self, grants: GrantsResource) -> None:
        self._grants = grants

        self.list = to_raw_response_wrapper(
            grants.list,
        )
        self.void = to_raw_response_wrapper(
            grants.void,
        )


class AsyncGrantsResourceWithRawResponse:
    def __init__(self, grants: AsyncGrantsResource) -> None:
        self._grants = grants

        self.list = async_to_raw_response_wrapper(
            grants.list,
        )
        self.void = async_to_raw_response_wrapper(
            grants.void,
        )


class GrantsResourceWithStreamingResponse:
    def __init__(self, grants: GrantsResource) -> None:
        self._grants = grants

        self.list = to_streamed_response_wrapper(
            grants.list,
        )
        self.void = to_streamed_response_wrapper(
            grants.void,
        )


class AsyncGrantsResourceWithStreamingResponse:
    def __init__(self, grants: AsyncGrantsResource) -> None:
        self._grants = grants

        self.list = async_to_streamed_response_wrapper(
            grants.list,
        )
        self.void = async_to_streamed_response_wrapper(
            grants.void,
        )
