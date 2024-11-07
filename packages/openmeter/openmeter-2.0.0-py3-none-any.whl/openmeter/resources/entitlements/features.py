# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, List, cast
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
from ...types.entitlements import feature_list_params, feature_create_params
from ...types.entitlements.feature import Feature
from ...types.entitlements.list_features_result import ListFeaturesResult

__all__ = ["FeaturesResource", "AsyncFeaturesResource"]


class FeaturesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FeaturesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return FeaturesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FeaturesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return FeaturesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        key: str,
        name: str,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        meter_group_by_filters: Dict[str, str] | NotGiven = NOT_GIVEN,
        meter_slug: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Feature:
        """Features are either metered or static.

        A feature is metered if meterSlug is
        provided at creation. For metered features you can pass additional filters that
        will be applied when calculating feature usage, based on the meter's groupBy
        fields. Only meters with SUM and COUNT aggregation are supported for features.
        Features cannot be updated later, only archived.

        Args:
          key: A key is a unique string that is used to identify a resource.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          meter_group_by_filters: Optional meter group by filters. Useful if the meter scope is broader than what
              feature tracks. Example scenario would be a meter tracking all token use with
              groupBy fields for the model, then the feature could filter for model=gpt-4.

          meter_slug: A key is a unique string that is used to identify a resource.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/features",
            body=maybe_transform(
                {
                    "key": key,
                    "name": name,
                    "metadata": metadata,
                    "meter_group_by_filters": meter_group_by_filters,
                    "meter_slug": meter_slug,
                },
                feature_create_params.FeatureCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Feature,
        )

    def retrieve(
        self,
        feature_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Feature:
        """
        Get a feature by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not feature_id:
            raise ValueError(f"Expected a non-empty value for `feature_id` but received {feature_id!r}")
        return self._get(
            f"/api/v1/features/{feature_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Feature,
        )

    def list(
        self,
        *,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        meter_slug: List[str] | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        order_by: Literal["id", "createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListFeaturesResult:
        """
        List features.

        Args:
          include_archived: Filter by meterGroupByFilters

          limit: Number of items to return.

              Default is 100.

          meter_slug: Filter by meterSlug

          offset: Number of items to skip.

              Default is 0.

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
        return cast(
            ListFeaturesResult,
            self._get(
                "/api/v1/features",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {
                            "include_archived": include_archived,
                            "limit": limit,
                            "meter_slug": meter_slug,
                            "offset": offset,
                            "order": order,
                            "order_by": order_by,
                            "page": page,
                            "page_size": page_size,
                        },
                        feature_list_params.FeatureListParams,
                    ),
                ),
                cast_to=cast(
                    Any, ListFeaturesResult
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def archive(
        self,
        feature_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Archive a feature by ID.

        Once a feature is archived it cannot be unarchived.

        If a feature is archived,
        new entitlements cannot be created for it, but archiving the feature does not
        affect existing entitlements. This means, if you want to create a new feature
        with the same key, and then create entitlements for it, the previous
        entitlements have to be deleted first on a per subject basis.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not feature_id:
            raise ValueError(f"Expected a non-empty value for `feature_id` but received {feature_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v1/features/{feature_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncFeaturesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFeaturesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFeaturesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFeaturesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return AsyncFeaturesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        key: str,
        name: str,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        meter_group_by_filters: Dict[str, str] | NotGiven = NOT_GIVEN,
        meter_slug: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Feature:
        """Features are either metered or static.

        A feature is metered if meterSlug is
        provided at creation. For metered features you can pass additional filters that
        will be applied when calculating feature usage, based on the meter's groupBy
        fields. Only meters with SUM and COUNT aggregation are supported for features.
        Features cannot be updated later, only archived.

        Args:
          key: A key is a unique string that is used to identify a resource.

          metadata: Set of key-value pairs. Metadata can be used to store additional information
              about a resource.

          meter_group_by_filters: Optional meter group by filters. Useful if the meter scope is broader than what
              feature tracks. Example scenario would be a meter tracking all token use with
              groupBy fields for the model, then the feature could filter for model=gpt-4.

          meter_slug: A key is a unique string that is used to identify a resource.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/features",
            body=await async_maybe_transform(
                {
                    "key": key,
                    "name": name,
                    "metadata": metadata,
                    "meter_group_by_filters": meter_group_by_filters,
                    "meter_slug": meter_slug,
                },
                feature_create_params.FeatureCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Feature,
        )

    async def retrieve(
        self,
        feature_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Feature:
        """
        Get a feature by ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not feature_id:
            raise ValueError(f"Expected a non-empty value for `feature_id` but received {feature_id!r}")
        return await self._get(
            f"/api/v1/features/{feature_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Feature,
        )

    async def list(
        self,
        *,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        meter_slug: List[str] | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["ASC", "DESC"] | NotGiven = NOT_GIVEN,
        order_by: Literal["id", "createdAt", "updatedAt"] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListFeaturesResult:
        """
        List features.

        Args:
          include_archived: Filter by meterGroupByFilters

          limit: Number of items to return.

              Default is 100.

          meter_slug: Filter by meterSlug

          offset: Number of items to skip.

              Default is 0.

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
        return cast(
            ListFeaturesResult,
            await self._get(
                "/api/v1/features",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {
                            "include_archived": include_archived,
                            "limit": limit,
                            "meter_slug": meter_slug,
                            "offset": offset,
                            "order": order,
                            "order_by": order_by,
                            "page": page,
                            "page_size": page_size,
                        },
                        feature_list_params.FeatureListParams,
                    ),
                ),
                cast_to=cast(
                    Any, ListFeaturesResult
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def archive(
        self,
        feature_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Archive a feature by ID.

        Once a feature is archived it cannot be unarchived.

        If a feature is archived,
        new entitlements cannot be created for it, but archiving the feature does not
        affect existing entitlements. This means, if you want to create a new feature
        with the same key, and then create entitlements for it, the previous
        entitlements have to be deleted first on a per subject basis.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not feature_id:
            raise ValueError(f"Expected a non-empty value for `feature_id` but received {feature_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v1/features/{feature_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class FeaturesResourceWithRawResponse:
    def __init__(self, features: FeaturesResource) -> None:
        self._features = features

        self.create = to_raw_response_wrapper(
            features.create,
        )
        self.retrieve = to_raw_response_wrapper(
            features.retrieve,
        )
        self.list = to_raw_response_wrapper(
            features.list,
        )
        self.archive = to_raw_response_wrapper(
            features.archive,
        )


class AsyncFeaturesResourceWithRawResponse:
    def __init__(self, features: AsyncFeaturesResource) -> None:
        self._features = features

        self.create = async_to_raw_response_wrapper(
            features.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            features.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            features.list,
        )
        self.archive = async_to_raw_response_wrapper(
            features.archive,
        )


class FeaturesResourceWithStreamingResponse:
    def __init__(self, features: FeaturesResource) -> None:
        self._features = features

        self.create = to_streamed_response_wrapper(
            features.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            features.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            features.list,
        )
        self.archive = to_streamed_response_wrapper(
            features.archive,
        )


class AsyncFeaturesResourceWithStreamingResponse:
    def __init__(self, features: AsyncFeaturesResource) -> None:
        self._features = features

        self.create = async_to_streamed_response_wrapper(
            features.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            features.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            features.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            features.archive,
        )
