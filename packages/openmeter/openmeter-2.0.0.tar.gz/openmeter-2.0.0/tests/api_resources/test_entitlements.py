# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types import Entitlement, ListEntitlementsResult

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEntitlements:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: OpenMeter) -> None:
        entitlement = client.entitlements.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: OpenMeter) -> None:
        response = client.entitlements.with_raw_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: OpenMeter) -> None:
        with client.entitlements.with_streaming_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            client.entitlements.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        entitlement = client.entitlements.list()
        assert_matches_type(ListEntitlementsResult, entitlement, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        entitlement = client.entitlements.list(
            entitlement_type=["metered", "boolean", "static"],
            feature=["string", "string", "string"],
            limit=1,
            offset=0,
            order="ASC",
            order_by="createdAt",
            page=1,
            page_size=1,
            subject=["string", "string", "string"],
        )
        assert_matches_type(ListEntitlementsResult, entitlement, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.entitlements.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(ListEntitlementsResult, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.entitlements.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(ListEntitlementsResult, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEntitlements:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.entitlements.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.entitlements.with_raw_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.entitlements.with_streaming_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            await async_client.entitlements.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.entitlements.list()
        assert_matches_type(ListEntitlementsResult, entitlement, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.entitlements.list(
            entitlement_type=["metered", "boolean", "static"],
            feature=["string", "string", "string"],
            limit=1,
            offset=0,
            order="ASC",
            order_by="createdAt",
            page=1,
            page_size=1,
            subject=["string", "string", "string"],
        )
        assert_matches_type(ListEntitlementsResult, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.entitlements.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(ListEntitlementsResult, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.entitlements.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(ListEntitlementsResult, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True
