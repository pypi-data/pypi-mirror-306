# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, List, cast
from typing_extensions import Literal

import httpx

from .grants import (
    GrantsResource,
    AsyncGrantsResource,
    GrantsResourceWithRawResponse,
    AsyncGrantsResourceWithRawResponse,
    GrantsResourceWithStreamingResponse,
    AsyncGrantsResourceWithStreamingResponse,
)
from ...types import entitlement_list_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .features import (
    FeaturesResource,
    AsyncFeaturesResource,
    FeaturesResourceWithRawResponse,
    AsyncFeaturesResourceWithRawResponse,
    FeaturesResourceWithStreamingResponse,
    AsyncFeaturesResourceWithStreamingResponse,
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
from ...types.entitlement import Entitlement
from ...types.list_entitlements_result import ListEntitlementsResult

__all__ = ["EntitlementsResource", "AsyncEntitlementsResource"]


class EntitlementsResource(SyncAPIResource):
    @cached_property
    def features(self) -> FeaturesResource:
        return FeaturesResource(self._client)

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

    def retrieve(
        self,
        entitlement_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """
        Get entitlement by id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        return cast(
            Entitlement,
            self._get(
                f"/api/v1/entitlements/{entitlement_id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Entitlement),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        entitlement_type: List[Literal["metered", "boolean", "static"]] | NotGiven = NOT_GIVEN,
        feature: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        order_by: Literal["createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        subject: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListEntitlementsResult:
        """List all entitlements for all the subjects and features.

        This endpoint is
        intended for administrative purposes only. To fetch the entitlements of a
        specific subject please use the /api/v1/subjects/{subjectKeyOrID}/entitlements
        endpoint. If page is provided that takes precedence and the paginated response
        is returned.

        Args:
          entitlement_type: Filtering by multiple entitlement types.

              Usage: `?entitlementType=metered&entitlementType=boolean`

          feature: Filtering by multiple features.

              Usage: `?feature=feature-1&feature=feature-2`

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
            ListEntitlementsResult,
            self._get(
                "/api/v1/entitlements",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {
                            "entitlement_type": entitlement_type,
                            "feature": feature,
                            "limit": limit,
                            "offset": offset,
                            "order": order,
                            "order_by": order_by,
                            "page": page,
                            "page_size": page_size,
                            "subject": subject,
                        },
                        entitlement_list_params.EntitlementListParams,
                    ),
                ),
                cast_to=cast(
                    Any, ListEntitlementsResult
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncEntitlementsResource(AsyncAPIResource):
    @cached_property
    def features(self) -> AsyncFeaturesResource:
        return AsyncFeaturesResource(self._client)

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

    async def retrieve(
        self,
        entitlement_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Entitlement:
        """
        Get entitlement by id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not entitlement_id:
            raise ValueError(f"Expected a non-empty value for `entitlement_id` but received {entitlement_id!r}")
        return cast(
            Entitlement,
            await self._get(
                f"/api/v1/entitlements/{entitlement_id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Entitlement),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def list(
        self,
        *,
        entitlement_type: List[Literal["metered", "boolean", "static"]] | NotGiven = NOT_GIVEN,
        feature: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        order_by: Literal["createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        subject: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListEntitlementsResult:
        """List all entitlements for all the subjects and features.

        This endpoint is
        intended for administrative purposes only. To fetch the entitlements of a
        specific subject please use the /api/v1/subjects/{subjectKeyOrID}/entitlements
        endpoint. If page is provided that takes precedence and the paginated response
        is returned.

        Args:
          entitlement_type: Filtering by multiple entitlement types.

              Usage: `?entitlementType=metered&entitlementType=boolean`

          feature: Filtering by multiple features.

              Usage: `?feature=feature-1&feature=feature-2`

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
            ListEntitlementsResult,
            await self._get(
                "/api/v1/entitlements",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {
                            "entitlement_type": entitlement_type,
                            "feature": feature,
                            "limit": limit,
                            "offset": offset,
                            "order": order,
                            "order_by": order_by,
                            "page": page,
                            "page_size": page_size,
                            "subject": subject,
                        },
                        entitlement_list_params.EntitlementListParams,
                    ),
                ),
                cast_to=cast(
                    Any, ListEntitlementsResult
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class EntitlementsResourceWithRawResponse:
    def __init__(self, entitlements: EntitlementsResource) -> None:
        self._entitlements = entitlements

        self.retrieve = to_raw_response_wrapper(
            entitlements.retrieve,
        )
        self.list = to_raw_response_wrapper(
            entitlements.list,
        )

    @cached_property
    def features(self) -> FeaturesResourceWithRawResponse:
        return FeaturesResourceWithRawResponse(self._entitlements.features)

    @cached_property
    def grants(self) -> GrantsResourceWithRawResponse:
        return GrantsResourceWithRawResponse(self._entitlements.grants)


class AsyncEntitlementsResourceWithRawResponse:
    def __init__(self, entitlements: AsyncEntitlementsResource) -> None:
        self._entitlements = entitlements

        self.retrieve = async_to_raw_response_wrapper(
            entitlements.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            entitlements.list,
        )

    @cached_property
    def features(self) -> AsyncFeaturesResourceWithRawResponse:
        return AsyncFeaturesResourceWithRawResponse(self._entitlements.features)

    @cached_property
    def grants(self) -> AsyncGrantsResourceWithRawResponse:
        return AsyncGrantsResourceWithRawResponse(self._entitlements.grants)


class EntitlementsResourceWithStreamingResponse:
    def __init__(self, entitlements: EntitlementsResource) -> None:
        self._entitlements = entitlements

        self.retrieve = to_streamed_response_wrapper(
            entitlements.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            entitlements.list,
        )

    @cached_property
    def features(self) -> FeaturesResourceWithStreamingResponse:
        return FeaturesResourceWithStreamingResponse(self._entitlements.features)

    @cached_property
    def grants(self) -> GrantsResourceWithStreamingResponse:
        return GrantsResourceWithStreamingResponse(self._entitlements.grants)


class AsyncEntitlementsResourceWithStreamingResponse:
    def __init__(self, entitlements: AsyncEntitlementsResource) -> None:
        self._entitlements = entitlements

        self.retrieve = async_to_streamed_response_wrapper(
            entitlements.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            entitlements.list,
        )

    @cached_property
    def features(self) -> AsyncFeaturesResourceWithStreamingResponse:
        return AsyncFeaturesResourceWithStreamingResponse(self._entitlements.features)

    @cached_property
    def grants(self) -> AsyncGrantsResourceWithStreamingResponse:
        return AsyncGrantsResourceWithStreamingResponse(self._entitlements.grants)
