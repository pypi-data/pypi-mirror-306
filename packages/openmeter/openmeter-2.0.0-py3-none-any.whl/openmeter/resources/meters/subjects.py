# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.meters.subject_list_response import SubjectListResponse

__all__ = ["SubjectsResource", "AsyncSubjectsResource"]


class SubjectsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SubjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return SubjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SubjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return SubjectsResourceWithStreamingResponse(self)

    def list(
        self,
        meter_id_or_slug: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubjectListResponse:
        """
        List subjects for a meter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meter_id_or_slug:
            raise ValueError(f"Expected a non-empty value for `meter_id_or_slug` but received {meter_id_or_slug!r}")
        return self._get(
            f"/api/v1/meters/{meter_id_or_slug}/subjects",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectListResponse,
        )


class AsyncSubjectsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSubjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSubjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSubjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return AsyncSubjectsResourceWithStreamingResponse(self)

    async def list(
        self,
        meter_id_or_slug: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubjectListResponse:
        """
        List subjects for a meter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meter_id_or_slug:
            raise ValueError(f"Expected a non-empty value for `meter_id_or_slug` but received {meter_id_or_slug!r}")
        return await self._get(
            f"/api/v1/meters/{meter_id_or_slug}/subjects",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectListResponse,
        )


class SubjectsResourceWithRawResponse:
    def __init__(self, subjects: SubjectsResource) -> None:
        self._subjects = subjects

        self.list = to_raw_response_wrapper(
            subjects.list,
        )


class AsyncSubjectsResourceWithRawResponse:
    def __init__(self, subjects: AsyncSubjectsResource) -> None:
        self._subjects = subjects

        self.list = async_to_raw_response_wrapper(
            subjects.list,
        )


class SubjectsResourceWithStreamingResponse:
    def __init__(self, subjects: SubjectsResource) -> None:
        self._subjects = subjects

        self.list = to_streamed_response_wrapper(
            subjects.list,
        )


class AsyncSubjectsResourceWithStreamingResponse:
    def __init__(self, subjects: AsyncSubjectsResource) -> None:
        self._subjects = subjects

        self.list = async_to_streamed_response_wrapper(
            subjects.list,
        )
