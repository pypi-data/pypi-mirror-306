# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types.portal import (
    PortalToken,
    TokenListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTokens:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: OpenMeter) -> None:
        token = client.portal.tokens.create(
            subject="customer-id",
        )
        assert_matches_type(PortalToken, token, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: OpenMeter) -> None:
        token = client.portal.tokens.create(
            subject="customer-id",
            allowed_meter_slugs=["tokens_total"],
        )
        assert_matches_type(PortalToken, token, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: OpenMeter) -> None:
        response = client.portal.tokens.with_raw_response.create(
            subject="customer-id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = response.parse()
        assert_matches_type(PortalToken, token, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: OpenMeter) -> None:
        with client.portal.tokens.with_streaming_response.create(
            subject="customer-id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = response.parse()
            assert_matches_type(PortalToken, token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        token = client.portal.tokens.list()
        assert_matches_type(TokenListResponse, token, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        token = client.portal.tokens.list(
            limit=25,
        )
        assert_matches_type(TokenListResponse, token, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.portal.tokens.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = response.parse()
        assert_matches_type(TokenListResponse, token, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.portal.tokens.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = response.parse()
            assert_matches_type(TokenListResponse, token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_invalidate(self, client: OpenMeter) -> None:
        token = client.portal.tokens.invalidate()
        assert token is None

    @parametrize
    def test_method_invalidate_with_all_params(self, client: OpenMeter) -> None:
        token = client.portal.tokens.invalidate(
            id="01G65Z755AFWAKHE12NY0CQ9FH",
            subject="subject",
        )
        assert token is None

    @parametrize
    def test_raw_response_invalidate(self, client: OpenMeter) -> None:
        response = client.portal.tokens.with_raw_response.invalidate()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = response.parse()
        assert token is None

    @parametrize
    def test_streaming_response_invalidate(self, client: OpenMeter) -> None:
        with client.portal.tokens.with_streaming_response.invalidate() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = response.parse()
            assert token is None

        assert cast(Any, response.is_closed) is True


class TestAsyncTokens:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOpenMeter) -> None:
        token = await async_client.portal.tokens.create(
            subject="customer-id",
        )
        assert_matches_type(PortalToken, token, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        token = await async_client.portal.tokens.create(
            subject="customer-id",
            allowed_meter_slugs=["tokens_total"],
        )
        assert_matches_type(PortalToken, token, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.portal.tokens.with_raw_response.create(
            subject="customer-id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = await response.parse()
        assert_matches_type(PortalToken, token, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.portal.tokens.with_streaming_response.create(
            subject="customer-id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = await response.parse()
            assert_matches_type(PortalToken, token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        token = await async_client.portal.tokens.list()
        assert_matches_type(TokenListResponse, token, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        token = await async_client.portal.tokens.list(
            limit=25,
        )
        assert_matches_type(TokenListResponse, token, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.portal.tokens.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = await response.parse()
        assert_matches_type(TokenListResponse, token, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.portal.tokens.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = await response.parse()
            assert_matches_type(TokenListResponse, token, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_invalidate(self, async_client: AsyncOpenMeter) -> None:
        token = await async_client.portal.tokens.invalidate()
        assert token is None

    @parametrize
    async def test_method_invalidate_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        token = await async_client.portal.tokens.invalidate(
            id="01G65Z755AFWAKHE12NY0CQ9FH",
            subject="subject",
        )
        assert token is None

    @parametrize
    async def test_raw_response_invalidate(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.portal.tokens.with_raw_response.invalidate()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        token = await response.parse()
        assert token is None

    @parametrize
    async def test_streaming_response_invalidate(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.portal.tokens.with_streaming_response.invalidate() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            token = await response.parse()
            assert token is None

        assert cast(Any, response.is_closed) is True
