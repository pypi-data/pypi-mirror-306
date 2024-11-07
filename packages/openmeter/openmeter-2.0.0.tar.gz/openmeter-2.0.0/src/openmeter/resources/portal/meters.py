# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union
from datetime import datetime
from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ...types.portal import meter_query_params
from ...types.meter_query_result import MeterQueryResult

__all__ = ["MetersResource", "AsyncMetersResource"]


class MetersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MetersResourceWithRawResponse:
        return MetersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MetersResourceWithStreamingResponse:
        return MetersResourceWithStreamingResponse(self)

    def query(
        self,
        meter_slug: str,
        *,
        filter_group_by: Dict[str, str] | NotGiven = NOT_GIVEN,
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        group_by: List[str] | NotGiven = NOT_GIVEN,
        to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        window_size: Literal["MINUTE", "HOUR", "DAY"] | NotGiven = NOT_GIVEN,
        window_time_zone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MeterQueryResult:
        """Query meter for consumer portal.

        This endpoint is publicly exposable to
        consumers.

        Args:
          filter_group_by: Simple filter for group bys with exact match.

              Usage: `?filterGroupBy[type]=input&filterGroupBy[model]=gpt-4`

          from_: Start date-time in RFC 3339 format. Inclusive.

          group_by: If not specified a single aggregate will be returned for each subject and time
              window. `subject` is a reserved group by value.

          to: End date-time in RFC 3339 format. Inclusive.

          window_size: If not specified, a single usage aggregate will be returned for the entirety of
              the specified period for each subject and group.

          window_time_zone: The value is the name of the time zone as defined in the IANA Time Zone Database
              (http://www.iana.org/time-zones). If not specified, the UTC timezone will be
              used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meter_slug:
            raise ValueError(f"Expected a non-empty value for `meter_slug` but received {meter_slug!r}")
        return self._get(
            f"/api/v1/portal/meters/{meter_slug}/query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "filter_group_by": filter_group_by,
                        "from_": from_,
                        "group_by": group_by,
                        "to": to,
                        "window_size": window_size,
                        "window_time_zone": window_time_zone,
                    },
                    meter_query_params.MeterQueryParams,
                ),
            ),
            cast_to=MeterQueryResult,
        )


class AsyncMetersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMetersResourceWithRawResponse:
        return AsyncMetersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMetersResourceWithStreamingResponse:
        return AsyncMetersResourceWithStreamingResponse(self)

    async def query(
        self,
        meter_slug: str,
        *,
        filter_group_by: Dict[str, str] | NotGiven = NOT_GIVEN,
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        group_by: List[str] | NotGiven = NOT_GIVEN,
        to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        window_size: Literal["MINUTE", "HOUR", "DAY"] | NotGiven = NOT_GIVEN,
        window_time_zone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MeterQueryResult:
        """Query meter for consumer portal.

        This endpoint is publicly exposable to
        consumers.

        Args:
          filter_group_by: Simple filter for group bys with exact match.

              Usage: `?filterGroupBy[type]=input&filterGroupBy[model]=gpt-4`

          from_: Start date-time in RFC 3339 format. Inclusive.

          group_by: If not specified a single aggregate will be returned for each subject and time
              window. `subject` is a reserved group by value.

          to: End date-time in RFC 3339 format. Inclusive.

          window_size: If not specified, a single usage aggregate will be returned for the entirety of
              the specified period for each subject and group.

          window_time_zone: The value is the name of the time zone as defined in the IANA Time Zone Database
              (http://www.iana.org/time-zones). If not specified, the UTC timezone will be
              used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meter_slug:
            raise ValueError(f"Expected a non-empty value for `meter_slug` but received {meter_slug!r}")
        return await self._get(
            f"/api/v1/portal/meters/{meter_slug}/query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "filter_group_by": filter_group_by,
                        "from_": from_,
                        "group_by": group_by,
                        "to": to,
                        "window_size": window_size,
                        "window_time_zone": window_time_zone,
                    },
                    meter_query_params.MeterQueryParams,
                ),
            ),
            cast_to=MeterQueryResult,
        )


class MetersResourceWithRawResponse:
    def __init__(self, meters: MetersResource) -> None:
        self._meters = meters

        self.query = to_raw_response_wrapper(
            meters.query,
        )


class AsyncMetersResourceWithRawResponse:
    def __init__(self, meters: AsyncMetersResource) -> None:
        self._meters = meters

        self.query = async_to_raw_response_wrapper(
            meters.query,
        )


class MetersResourceWithStreamingResponse:
    def __init__(self, meters: MetersResource) -> None:
        self._meters = meters

        self.query = to_streamed_response_wrapper(
            meters.query,
        )


class AsyncMetersResourceWithStreamingResponse:
    def __init__(self, meters: AsyncMetersResource) -> None:
        self._meters = meters

        self.query = async_to_streamed_response_wrapper(
            meters.query,
        )
