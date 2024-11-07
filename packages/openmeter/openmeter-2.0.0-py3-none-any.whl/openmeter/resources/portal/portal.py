# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .meters import (
    MetersResource,
    AsyncMetersResource,
    MetersResourceWithRawResponse,
    AsyncMetersResourceWithRawResponse,
    MetersResourceWithStreamingResponse,
    AsyncMetersResourceWithStreamingResponse,
)
from .tokens import (
    TokensResource,
    AsyncTokensResource,
    TokensResourceWithRawResponse,
    AsyncTokensResourceWithRawResponse,
    TokensResourceWithStreamingResponse,
    AsyncTokensResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["PortalResource", "AsyncPortalResource"]


class PortalResource(SyncAPIResource):
    @cached_property
    def meters(self) -> MetersResource:
        return MetersResource(self._client)

    @cached_property
    def tokens(self) -> TokensResource:
        return TokensResource(self._client)

    @cached_property
    def with_raw_response(self) -> PortalResourceWithRawResponse:
        return PortalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PortalResourceWithStreamingResponse:
        return PortalResourceWithStreamingResponse(self)


class AsyncPortalResource(AsyncAPIResource):
    @cached_property
    def meters(self) -> AsyncMetersResource:
        return AsyncMetersResource(self._client)

    @cached_property
    def tokens(self) -> AsyncTokensResource:
        return AsyncTokensResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPortalResourceWithRawResponse:
        return AsyncPortalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPortalResourceWithStreamingResponse:
        return AsyncPortalResourceWithStreamingResponse(self)


class PortalResourceWithRawResponse:
    def __init__(self, portal: PortalResource) -> None:
        self._portal = portal

    @cached_property
    def meters(self) -> MetersResourceWithRawResponse:
        return MetersResourceWithRawResponse(self._portal.meters)

    @cached_property
    def tokens(self) -> TokensResourceWithRawResponse:
        return TokensResourceWithRawResponse(self._portal.tokens)


class AsyncPortalResourceWithRawResponse:
    def __init__(self, portal: AsyncPortalResource) -> None:
        self._portal = portal

    @cached_property
    def meters(self) -> AsyncMetersResourceWithRawResponse:
        return AsyncMetersResourceWithRawResponse(self._portal.meters)

    @cached_property
    def tokens(self) -> AsyncTokensResourceWithRawResponse:
        return AsyncTokensResourceWithRawResponse(self._portal.tokens)


class PortalResourceWithStreamingResponse:
    def __init__(self, portal: PortalResource) -> None:
        self._portal = portal

    @cached_property
    def meters(self) -> MetersResourceWithStreamingResponse:
        return MetersResourceWithStreamingResponse(self._portal.meters)

    @cached_property
    def tokens(self) -> TokensResourceWithStreamingResponse:
        return TokensResourceWithStreamingResponse(self._portal.tokens)


class AsyncPortalResourceWithStreamingResponse:
    def __init__(self, portal: AsyncPortalResource) -> None:
        self._portal = portal

    @cached_property
    def meters(self) -> AsyncMetersResourceWithStreamingResponse:
        return AsyncMetersResourceWithStreamingResponse(self._portal.meters)

    @cached_property
    def tokens(self) -> AsyncTokensResourceWithStreamingResponse:
        return AsyncTokensResourceWithStreamingResponse(self._portal.tokens)
