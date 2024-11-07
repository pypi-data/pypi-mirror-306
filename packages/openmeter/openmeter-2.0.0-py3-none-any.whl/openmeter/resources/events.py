# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime

import httpx

from ..types import event_list_params, event_ingest_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.event_list_response import EventListResponse
from ..types.event_ingest_response import EventIngestResponse

__all__ = ["EventsResource", "AsyncEventsResource"]


class EventsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return EventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return EventsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        id: str | NotGiven = NOT_GIVEN,
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        has_error: bool | NotGiven = NOT_GIVEN,
        ingested_at_from: Union[str, datetime] | NotGiven = NOT_GIVEN,
        ingested_at_to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        subject: str | NotGiven = NOT_GIVEN,
        to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventListResponse:
        """
        List ingested events within a time range.

        If the from query param is not provided it defaults to last 72 hours.

        Args:
          id: The event ID.

              Accepts partial ID.

          from_: Start date-time in RFC 3339 format.

              Inclusive.

          has_error: If not provided lists all events.

              If provided with true, only list events with processing error.

              If provided with false, only list events without processing error.

          ingested_at_from: Start date-time in RFC 3339 format.

              Inclusive.

          ingested_at_to: End date-time in RFC 3339 format.

              Inclusive.

          limit: Number of events to return.

          subject: The event subject.

              Accepts partial subject.

          to: End date-time in RFC 3339 format.

              Inclusive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v1/events",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "from_": from_,
                        "has_error": has_error,
                        "ingested_at_from": ingested_at_from,
                        "ingested_at_to": ingested_at_to,
                        "limit": limit,
                        "subject": subject,
                        "to": to,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            cast_to=EventListResponse,
        )

    def ingest(
        self,
        *,
        id: str,
        source: str,
        specversion: str,
        subject: str,
        type: str,
        data: Union[str, object, None] | NotGiven = NOT_GIVEN,
        datacontenttype: Optional[str] | NotGiven = NOT_GIVEN,
        dataschema: Optional[str] | NotGiven = NOT_GIVEN,
        time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventIngestResponse:
        """
        Ingests an event or batch of events following the CloudEvents specification.

        Args:
          id: Identifies the event.

          source: Identifies the context in which an event happened.

          specversion: The version of the CloudEvents specification which the event uses.

          subject: Describes the subject of the event in the context of the event producer
              (identified by source).

          type: Contains a value describing the type of event related to the originating
              occurrence.

          data: The event payload.

          datacontenttype: Content type of the data value. Must adhere to RFC 2046 format.

          dataschema: Identifies the schema that data adheres to.

          time: Timestamp of when the occurrence happened. Must adhere to RFC 3339.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/cloudevents+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/events",
            body=maybe_transform(
                {
                    "id": id,
                    "source": source,
                    "specversion": specversion,
                    "subject": subject,
                    "type": type,
                    "data": data,
                    "datacontenttype": datacontenttype,
                    "dataschema": dataschema,
                    "time": time,
                },
                event_ingest_params.EventIngestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventIngestResponse,
        )


class AsyncEventsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/openmeterio/openmeter-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/openmeterio/openmeter-python#with_streaming_response
        """
        return AsyncEventsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        id: str | NotGiven = NOT_GIVEN,
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        has_error: bool | NotGiven = NOT_GIVEN,
        ingested_at_from: Union[str, datetime] | NotGiven = NOT_GIVEN,
        ingested_at_to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        subject: str | NotGiven = NOT_GIVEN,
        to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventListResponse:
        """
        List ingested events within a time range.

        If the from query param is not provided it defaults to last 72 hours.

        Args:
          id: The event ID.

              Accepts partial ID.

          from_: Start date-time in RFC 3339 format.

              Inclusive.

          has_error: If not provided lists all events.

              If provided with true, only list events with processing error.

              If provided with false, only list events without processing error.

          ingested_at_from: Start date-time in RFC 3339 format.

              Inclusive.

          ingested_at_to: End date-time in RFC 3339 format.

              Inclusive.

          limit: Number of events to return.

          subject: The event subject.

              Accepts partial subject.

          to: End date-time in RFC 3339 format.

              Inclusive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v1/events",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "id": id,
                        "from_": from_,
                        "has_error": has_error,
                        "ingested_at_from": ingested_at_from,
                        "ingested_at_to": ingested_at_to,
                        "limit": limit,
                        "subject": subject,
                        "to": to,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            cast_to=EventListResponse,
        )

    async def ingest(
        self,
        *,
        id: str,
        source: str,
        specversion: str,
        subject: str,
        type: str,
        data: Union[str, object, None] | NotGiven = NOT_GIVEN,
        datacontenttype: Optional[str] | NotGiven = NOT_GIVEN,
        dataschema: Optional[str] | NotGiven = NOT_GIVEN,
        time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventIngestResponse:
        """
        Ingests an event or batch of events following the CloudEvents specification.

        Args:
          id: Identifies the event.

          source: Identifies the context in which an event happened.

          specversion: The version of the CloudEvents specification which the event uses.

          subject: Describes the subject of the event in the context of the event producer
              (identified by source).

          type: Contains a value describing the type of event related to the originating
              occurrence.

          data: The event payload.

          datacontenttype: Content type of the data value. Must adhere to RFC 2046 format.

          dataschema: Identifies the schema that data adheres to.

          time: Timestamp of when the occurrence happened. Must adhere to RFC 3339.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/cloudevents+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/events",
            body=await async_maybe_transform(
                {
                    "id": id,
                    "source": source,
                    "specversion": specversion,
                    "subject": subject,
                    "type": type,
                    "data": data,
                    "datacontenttype": datacontenttype,
                    "dataschema": dataschema,
                    "time": time,
                },
                event_ingest_params.EventIngestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventIngestResponse,
        )


class EventsResourceWithRawResponse:
    def __init__(self, events: EventsResource) -> None:
        self._events = events

        self.list = to_raw_response_wrapper(
            events.list,
        )
        self.ingest = to_raw_response_wrapper(
            events.ingest,
        )


class AsyncEventsResourceWithRawResponse:
    def __init__(self, events: AsyncEventsResource) -> None:
        self._events = events

        self.list = async_to_raw_response_wrapper(
            events.list,
        )
        self.ingest = async_to_raw_response_wrapper(
            events.ingest,
        )


class EventsResourceWithStreamingResponse:
    def __init__(self, events: EventsResource) -> None:
        self._events = events

        self.list = to_streamed_response_wrapper(
            events.list,
        )
        self.ingest = to_streamed_response_wrapper(
            events.ingest,
        )


class AsyncEventsResourceWithStreamingResponse:
    def __init__(self, events: AsyncEventsResource) -> None:
        self._events = events

        self.list = async_to_streamed_response_wrapper(
            events.list,
        )
        self.ingest = async_to_streamed_response_wrapper(
            events.ingest,
        )
