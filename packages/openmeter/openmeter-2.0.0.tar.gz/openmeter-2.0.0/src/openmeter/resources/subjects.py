# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ...types import subject_upsert_params
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
from .entitlements import (
    EntitlementsResource,
    AsyncEntitlementsResource,
    EntitlementsResourceWithRawResponse,
    AsyncEntitlementsResourceWithRawResponse,
    EntitlementsResourceWithStreamingResponse,
    AsyncEntitlementsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from ...types.subject import Subject
from .entitlements.entitlements import EntitlementsResource, AsyncEntitlementsResource
from ...types.subject_list_response import SubjectListResponse
from ...types.subject_upsert_response import SubjectUpsertResponse

__all__ = ["SubjectsResource", "AsyncSubjectsResource"]


class SubjectsResource(SyncAPIResource):
    @cached_property
    def entitlements(self) -> EntitlementsResource:
        return EntitlementsResource(self._client)

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

    def retrieve(
        self,
        subject_id_or_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Subject:
        """
        Get subject by ID or key.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        return self._get(
            f"/api/v1/subjects/{subject_id_or_key}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Subject,
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
    ) -> SubjectListResponse:
        """List subjects."""
        return self._get(
            "/api/v1/subjects",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectListResponse,
        )

    def delete(
        self,
        subject_id_or_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete subject by ID or key.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v1/subjects/{subject_id_or_key}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def upsert(
        self,
        *,
        body: Iterable[subject_upsert_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubjectUpsertResponse:
        """Upserts a subject.

        Creates or updates subject.

        If the subject doesn't exist, it will be created. If the subject exists, it will
        be partially updated with the provided fields.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/subjects",
            body=maybe_transform(body, Iterable[subject_upsert_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectUpsertResponse,
        )


class AsyncSubjectsResource(AsyncAPIResource):
    @cached_property
    def entitlements(self) -> AsyncEntitlementsResource:
        return AsyncEntitlementsResource(self._client)

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

    async def retrieve(
        self,
        subject_id_or_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Subject:
        """
        Get subject by ID or key.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        return await self._get(
            f"/api/v1/subjects/{subject_id_or_key}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Subject,
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
    ) -> SubjectListResponse:
        """List subjects."""
        return await self._get(
            "/api/v1/subjects",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectListResponse,
        )

    async def delete(
        self,
        subject_id_or_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete subject by ID or key.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not subject_id_or_key:
            raise ValueError(f"Expected a non-empty value for `subject_id_or_key` but received {subject_id_or_key!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v1/subjects/{subject_id_or_key}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def upsert(
        self,
        *,
        body: Iterable[subject_upsert_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubjectUpsertResponse:
        """Upserts a subject.

        Creates or updates subject.

        If the subject doesn't exist, it will be created. If the subject exists, it will
        be partially updated with the provided fields.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/subjects",
            body=await async_maybe_transform(body, Iterable[subject_upsert_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubjectUpsertResponse,
        )


class SubjectsResourceWithRawResponse:
    def __init__(self, subjects: SubjectsResource) -> None:
        self._subjects = subjects

        self.retrieve = to_raw_response_wrapper(
            subjects.retrieve,
        )
        self.list = to_raw_response_wrapper(
            subjects.list,
        )
        self.delete = to_raw_response_wrapper(
            subjects.delete,
        )
        self.upsert = to_raw_response_wrapper(
            subjects.upsert,
        )

    @cached_property
    def entitlements(self) -> EntitlementsResourceWithRawResponse:
        return EntitlementsResourceWithRawResponse(self._subjects.entitlements)


class AsyncSubjectsResourceWithRawResponse:
    def __init__(self, subjects: AsyncSubjectsResource) -> None:
        self._subjects = subjects

        self.retrieve = async_to_raw_response_wrapper(
            subjects.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            subjects.list,
        )
        self.delete = async_to_raw_response_wrapper(
            subjects.delete,
        )
        self.upsert = async_to_raw_response_wrapper(
            subjects.upsert,
        )

    @cached_property
    def entitlements(self) -> AsyncEntitlementsResourceWithRawResponse:
        return AsyncEntitlementsResourceWithRawResponse(self._subjects.entitlements)


class SubjectsResourceWithStreamingResponse:
    def __init__(self, subjects: SubjectsResource) -> None:
        self._subjects = subjects

        self.retrieve = to_streamed_response_wrapper(
            subjects.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            subjects.list,
        )
        self.delete = to_streamed_response_wrapper(
            subjects.delete,
        )
        self.upsert = to_streamed_response_wrapper(
            subjects.upsert,
        )

    @cached_property
    def entitlements(self) -> EntitlementsResourceWithStreamingResponse:
        return EntitlementsResourceWithStreamingResponse(self._subjects.entitlements)


class AsyncSubjectsResourceWithStreamingResponse:
    def __init__(self, subjects: AsyncSubjectsResource) -> None:
        self._subjects = subjects

        self.retrieve = async_to_streamed_response_wrapper(
            subjects.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            subjects.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            subjects.delete,
        )
        self.upsert = async_to_streamed_response_wrapper(
            subjects.upsert,
        )

    @cached_property
    def entitlements(self) -> AsyncEntitlementsResourceWithStreamingResponse:
        return AsyncEntitlementsResourceWithStreamingResponse(self._subjects.entitlements)
