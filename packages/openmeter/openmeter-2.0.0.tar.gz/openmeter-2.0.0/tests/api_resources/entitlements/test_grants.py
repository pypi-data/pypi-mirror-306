# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types.entitlements import GrantListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGrants:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        grant = client.entitlements.grants.list()
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        grant = client.entitlements.grants.list(
            feature=["string", "string", "string"],
            include_deleted=True,
            limit=1,
            offset=0,
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
            subject=["string", "string", "string"],
        )
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.entitlements.grants.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        grant = response.parse()
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.entitlements.grants.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            grant = response.parse()
            assert_matches_type(GrantListResponse, grant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_void(self, client: OpenMeter) -> None:
        grant = client.entitlements.grants.void(
            "grantId",
        )
        assert grant is None

    @parametrize
    def test_raw_response_void(self, client: OpenMeter) -> None:
        response = client.entitlements.grants.with_raw_response.void(
            "grantId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        grant = response.parse()
        assert grant is None

    @parametrize
    def test_streaming_response_void(self, client: OpenMeter) -> None:
        with client.entitlements.grants.with_streaming_response.void(
            "grantId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            grant = response.parse()
            assert grant is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_void(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `grant_id` but received ''"):
            client.entitlements.grants.with_raw_response.void(
                "",
            )


class TestAsyncGrants:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        grant = await async_client.entitlements.grants.list()
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        grant = await async_client.entitlements.grants.list(
            feature=["string", "string", "string"],
            include_deleted=True,
            limit=1,
            offset=0,
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
            subject=["string", "string", "string"],
        )
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.entitlements.grants.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        grant = await response.parse()
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.entitlements.grants.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            grant = await response.parse()
            assert_matches_type(GrantListResponse, grant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_void(self, async_client: AsyncOpenMeter) -> None:
        grant = await async_client.entitlements.grants.void(
            "grantId",
        )
        assert grant is None

    @parametrize
    async def test_raw_response_void(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.entitlements.grants.with_raw_response.void(
            "grantId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        grant = await response.parse()
        assert grant is None

    @parametrize
    async def test_streaming_response_void(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.entitlements.grants.with_streaming_response.void(
            "grantId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            grant = await response.parse()
            assert grant is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_void(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `grant_id` but received ''"):
            await async_client.entitlements.grants.with_raw_response.void(
                "",
            )
