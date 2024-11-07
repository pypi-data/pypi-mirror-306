# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types.entitlements import Feature, ListFeaturesResult

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFeatures:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: OpenMeter) -> None:
        feature = client.entitlements.features.create(
            key="x",
            name="name",
        )
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: OpenMeter) -> None:
        feature = client.entitlements.features.create(
            key="x",
            name="name",
            metadata={"key": "value"},
            meter_group_by_filters={
                "model": "gpt-4",
                "type": "input",
            },
            meter_slug="tokens_total",
        )
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: OpenMeter) -> None:
        response = client.entitlements.features.with_raw_response.create(
            key="x",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feature = response.parse()
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: OpenMeter) -> None:
        with client.entitlements.features.with_streaming_response.create(
            key="x",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feature = response.parse()
            assert_matches_type(Feature, feature, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: OpenMeter) -> None:
        feature = client.entitlements.features.retrieve(
            "featureId",
        )
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: OpenMeter) -> None:
        response = client.entitlements.features.with_raw_response.retrieve(
            "featureId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feature = response.parse()
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: OpenMeter) -> None:
        with client.entitlements.features.with_streaming_response.retrieve(
            "featureId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feature = response.parse()
            assert_matches_type(Feature, feature, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `feature_id` but received ''"):
            client.entitlements.features.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        feature = client.entitlements.features.list()
        assert_matches_type(ListFeaturesResult, feature, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        feature = client.entitlements.features.list(
            include_archived=True,
            limit=1,
            meter_slug=["string", "string", "string"],
            offset=0,
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
        )
        assert_matches_type(ListFeaturesResult, feature, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.entitlements.features.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feature = response.parse()
        assert_matches_type(ListFeaturesResult, feature, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.entitlements.features.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feature = response.parse()
            assert_matches_type(ListFeaturesResult, feature, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: OpenMeter) -> None:
        feature = client.entitlements.features.archive(
            "featureId",
        )
        assert feature is None

    @parametrize
    def test_raw_response_archive(self, client: OpenMeter) -> None:
        response = client.entitlements.features.with_raw_response.archive(
            "featureId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feature = response.parse()
        assert feature is None

    @parametrize
    def test_streaming_response_archive(self, client: OpenMeter) -> None:
        with client.entitlements.features.with_streaming_response.archive(
            "featureId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feature = response.parse()
            assert feature is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `feature_id` but received ''"):
            client.entitlements.features.with_raw_response.archive(
                "",
            )


class TestAsyncFeatures:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOpenMeter) -> None:
        feature = await async_client.entitlements.features.create(
            key="x",
            name="name",
        )
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        feature = await async_client.entitlements.features.create(
            key="x",
            name="name",
            metadata={"key": "value"},
            meter_group_by_filters={
                "model": "gpt-4",
                "type": "input",
            },
            meter_slug="tokens_total",
        )
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.entitlements.features.with_raw_response.create(
            key="x",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feature = await response.parse()
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.entitlements.features.with_streaming_response.create(
            key="x",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feature = await response.parse()
            assert_matches_type(Feature, feature, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOpenMeter) -> None:
        feature = await async_client.entitlements.features.retrieve(
            "featureId",
        )
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.entitlements.features.with_raw_response.retrieve(
            "featureId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feature = await response.parse()
        assert_matches_type(Feature, feature, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.entitlements.features.with_streaming_response.retrieve(
            "featureId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feature = await response.parse()
            assert_matches_type(Feature, feature, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `feature_id` but received ''"):
            await async_client.entitlements.features.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        feature = await async_client.entitlements.features.list()
        assert_matches_type(ListFeaturesResult, feature, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        feature = await async_client.entitlements.features.list(
            include_archived=True,
            limit=1,
            meter_slug=["string", "string", "string"],
            offset=0,
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
        )
        assert_matches_type(ListFeaturesResult, feature, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.entitlements.features.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feature = await response.parse()
        assert_matches_type(ListFeaturesResult, feature, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.entitlements.features.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feature = await response.parse()
            assert_matches_type(ListFeaturesResult, feature, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncOpenMeter) -> None:
        feature = await async_client.entitlements.features.archive(
            "featureId",
        )
        assert feature is None

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.entitlements.features.with_raw_response.archive(
            "featureId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        feature = await response.parse()
        assert feature is None

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.entitlements.features.with_streaming_response.archive(
            "featureId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            feature = await response.parse()
            assert feature is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `feature_id` but received ''"):
            await async_client.entitlements.features.with_raw_response.archive(
                "",
            )
