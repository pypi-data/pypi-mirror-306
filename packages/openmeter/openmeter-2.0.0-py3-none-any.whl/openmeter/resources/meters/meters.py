# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union
from datetime import datetime
from typing_extensions import Literal

import httpx

from ...types import meter_query_params, meter_create_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .subjects import (
    SubjectsResource,
    AsyncSubjectsResource,
    SubjectsResourceWithRawResponse,
    AsyncSubjectsResourceWithRawResponse,
    SubjectsResourceWithStreamingResponse,
    AsyncSubjectsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.meter import Meter
from ..._base_client import make_request_options
from ...types.meter_query_result import MeterQueryResult
from ...types.meter_list_response import MeterListResponse

__all__ = ["MetersResource", "AsyncMetersResource"]


class MetersResource(SyncAPIResource):
    @cached_property
    def subjects(self) -> SubjectsResource:
        return SubjectsResource(self._client)

    @cached_property
    def with_raw_response(self) -> MetersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return MetersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MetersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return MetersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        aggregation: Literal["SUM", "COUNT", "UNIQUE_COUNT", "AVG", "MIN", "MAX"],
        event_type: str,
        slug: str,
        window_size: Literal["MINUTE", "HOUR", "DAY"],
        description: str | NotGiven = NOT_GIVEN,
        group_by: Dict[str, str] | NotGiven = NOT_GIVEN,
        value_property: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Meter:
        """
        Create a meter.

        Args:
          aggregation: The aggregation type to use for the meter.

          event_type: The event type to aggregate.

          slug: A unique, human-readable identifier for the meter. Must consist only
              alphanumeric and underscore characters.

          window_size: Aggregation window size.

          description: A description of the meter.

          group_by: Named JSONPath expressions to extract the group by values from the event data.

              Keys must be unique and consist only alphanumeric and underscore characters.

              TODO: add key format enforcement

          value_property: JSONPath expression to extract the value from the ingested event's data
              property.

              The ingested value for SUM, AVG, MIN, and MAX aggregations is a number or a
              string that can be parsed to a number.

              For UNIQUE_COUNT aggregation, the ingested value must be a string. For COUNT
              aggregation the valueProperty is ignored.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/meters",
            body=maybe_transform(
                {
                    "aggregation": aggregation,
                    "event_type": event_type,
                    "slug": slug,
                    "window_size": window_size,
                    "description": description,
                    "group_by": group_by,
                    "value_property": value_property,
                },
                meter_create_params.MeterCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Meter,
        )

    def retrieve(
        self,
        meter_id_or_slug: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Meter:
        """
        Get a meter by ID or slug.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meter_id_or_slug:
            raise ValueError(f"Expected a non-empty value for `meter_id_or_slug` but received {meter_id_or_slug!r}")
        return self._get(
            f"/api/v1/meters/{meter_id_or_slug}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Meter,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MeterListResponse:
        """List meters."""
        return self._get(
            "/api/v1/meters",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MeterListResponse,
        )

    def delete(
        self,
        meter_id_or_slug: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a meter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meter_id_or_slug:
            raise ValueError(f"Expected a non-empty value for `meter_id_or_slug` but received {meter_id_or_slug!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v1/meters/{meter_id_or_slug}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def query(
        self,
        meter_id_or_slug: str,
        *,
        filter_group_by: Dict[str, str] | NotGiven = NOT_GIVEN,
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        group_by: List[str] | NotGiven = NOT_GIVEN,
        subject: List[str] | NotGiven = NOT_GIVEN,
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
        """Query meter for usage.

        Query meter for usage.

        Args:
          filter_group_by: Simple filter for group bys with exact match.

          from_: Start date-time in RFC 3339 format.

              Inclusive.

          group_by: If not specified a single aggregate will be returned for each subject and time
              window. `subject` is a reserved group by value.

          subject: Filtering by multiple subjects.

          to: End date-time in RFC 3339 format.

              Inclusive.

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
        if not meter_id_or_slug:
            raise ValueError(f"Expected a non-empty value for `meter_id_or_slug` but received {meter_id_or_slug!r}")
        return self._get(
            f"/api/v1/meters/{meter_id_or_slug}/query",
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
                        "subject": subject,
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
    def subjects(self) -> AsyncSubjectsResource:
        return AsyncSubjectsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMetersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMetersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMetersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return AsyncMetersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        aggregation: Literal["SUM", "COUNT", "UNIQUE_COUNT", "AVG", "MIN", "MAX"],
        event_type: str,
        slug: str,
        window_size: Literal["MINUTE", "HOUR", "DAY"],
        description: str | NotGiven = NOT_GIVEN,
        group_by: Dict[str, str] | NotGiven = NOT_GIVEN,
        value_property: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Meter:
        """
        Create a meter.

        Args:
          aggregation: The aggregation type to use for the meter.

          event_type: The event type to aggregate.

          slug: A unique, human-readable identifier for the meter. Must consist only
              alphanumeric and underscore characters.

          window_size: Aggregation window size.

          description: A description of the meter.

          group_by: Named JSONPath expressions to extract the group by values from the event data.

              Keys must be unique and consist only alphanumeric and underscore characters.

              TODO: add key format enforcement

          value_property: JSONPath expression to extract the value from the ingested event's data
              property.

              The ingested value for SUM, AVG, MIN, and MAX aggregations is a number or a
              string that can be parsed to a number.

              For UNIQUE_COUNT aggregation, the ingested value must be a string. For COUNT
              aggregation the valueProperty is ignored.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/meters",
            body=await async_maybe_transform(
                {
                    "aggregation": aggregation,
                    "event_type": event_type,
                    "slug": slug,
                    "window_size": window_size,
                    "description": description,
                    "group_by": group_by,
                    "value_property": value_property,
                },
                meter_create_params.MeterCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Meter,
        )

    async def retrieve(
        self,
        meter_id_or_slug: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Meter:
        """
        Get a meter by ID or slug.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meter_id_or_slug:
            raise ValueError(f"Expected a non-empty value for `meter_id_or_slug` but received {meter_id_or_slug!r}")
        return await self._get(
            f"/api/v1/meters/{meter_id_or_slug}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Meter,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MeterListResponse:
        """List meters."""
        return await self._get(
            "/api/v1/meters",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MeterListResponse,
        )

    async def delete(
        self,
        meter_id_or_slug: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a meter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not meter_id_or_slug:
            raise ValueError(f"Expected a non-empty value for `meter_id_or_slug` but received {meter_id_or_slug!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v1/meters/{meter_id_or_slug}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def query(
        self,
        meter_id_or_slug: str,
        *,
        filter_group_by: Dict[str, str] | NotGiven = NOT_GIVEN,
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        group_by: List[str] | NotGiven = NOT_GIVEN,
        subject: List[str] | NotGiven = NOT_GIVEN,
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
        """Query meter for usage.

        Query meter for usage.

        Args:
          filter_group_by: Simple filter for group bys with exact match.

          from_: Start date-time in RFC 3339 format.

              Inclusive.

          group_by: If not specified a single aggregate will be returned for each subject and time
              window. `subject` is a reserved group by value.

          subject: Filtering by multiple subjects.

          to: End date-time in RFC 3339 format.

              Inclusive.

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
        if not meter_id_or_slug:
            raise ValueError(f"Expected a non-empty value for `meter_id_or_slug` but received {meter_id_or_slug!r}")
        return await self._get(
            f"/api/v1/meters/{meter_id_or_slug}/query",
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
                        "subject": subject,
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

        self.create = to_raw_response_wrapper(
            meters.create,
        )
        self.retrieve = to_raw_response_wrapper(
            meters.retrieve,
        )
        self.list = to_raw_response_wrapper(
            meters.list,
        )
        self.delete = to_raw_response_wrapper(
            meters.delete,
        )
        self.query = to_raw_response_wrapper(
            meters.query,
        )

    @cached_property
    def subjects(self) -> SubjectsResourceWithRawResponse:
        return SubjectsResourceWithRawResponse(self._meters.subjects)


class AsyncMetersResourceWithRawResponse:
    def __init__(self, meters: AsyncMetersResource) -> None:
        self._meters = meters

        self.create = async_to_raw_response_wrapper(
            meters.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            meters.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            meters.list,
        )
        self.delete = async_to_raw_response_wrapper(
            meters.delete,
        )
        self.query = async_to_raw_response_wrapper(
            meters.query,
        )

    @cached_property
    def subjects(self) -> AsyncSubjectsResourceWithRawResponse:
        return AsyncSubjectsResourceWithRawResponse(self._meters.subjects)


class MetersResourceWithStreamingResponse:
    def __init__(self, meters: MetersResource) -> None:
        self._meters = meters

        self.create = to_streamed_response_wrapper(
            meters.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            meters.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            meters.list,
        )
        self.delete = to_streamed_response_wrapper(
            meters.delete,
        )
        self.query = to_streamed_response_wrapper(
            meters.query,
        )

    @cached_property
    def subjects(self) -> SubjectsResourceWithStreamingResponse:
        return SubjectsResourceWithStreamingResponse(self._meters.subjects)


class AsyncMetersResourceWithStreamingResponse:
    def __init__(self, meters: AsyncMetersResource) -> None:
        self._meters = meters

        self.create = async_to_streamed_response_wrapper(
            meters.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            meters.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            meters.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            meters.delete,
        )
        self.query = async_to_streamed_response_wrapper(
            meters.query,
        )

    @cached_property
    def subjects(self) -> AsyncSubjectsResourceWithStreamingResponse:
        return AsyncSubjectsResourceWithStreamingResponse(self._meters.subjects)
