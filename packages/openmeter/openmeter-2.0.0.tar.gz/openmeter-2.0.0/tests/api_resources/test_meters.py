# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types import Meter, MeterQueryResult, MeterListResponse
from openmeter._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMeters:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: OpenMeter) -> None:
        meter = client.meters.create(
            aggregation="SUM",
            event_type="prompt",
            slug="tokens_total",
            window_size="MINUTE",
        )
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: OpenMeter) -> None:
        meter = client.meters.create(
            aggregation="SUM",
            event_type="prompt",
            slug="tokens_total",
            window_size="MINUTE",
            description="AI Token Usage",
            group_by={
                "model": "$.model",
                "type": "$.type",
            },
            value_property="$.tokens",
        )
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: OpenMeter) -> None:
        response = client.meters.with_raw_response.create(
            aggregation="SUM",
            event_type="prompt",
            slug="tokens_total",
            window_size="MINUTE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = response.parse()
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: OpenMeter) -> None:
        with client.meters.with_streaming_response.create(
            aggregation="SUM",
            event_type="prompt",
            slug="tokens_total",
            window_size="MINUTE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = response.parse()
            assert_matches_type(Meter, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: OpenMeter) -> None:
        meter = client.meters.retrieve(
            "x",
        )
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: OpenMeter) -> None:
        response = client.meters.with_raw_response.retrieve(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = response.parse()
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: OpenMeter) -> None:
        with client.meters.with_streaming_response.retrieve(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = response.parse()
            assert_matches_type(Meter, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meter_id_or_slug` but received ''"):
            client.meters.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        meter = client.meters.list()
        assert_matches_type(MeterListResponse, meter, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.meters.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = response.parse()
        assert_matches_type(MeterListResponse, meter, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.meters.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = response.parse()
            assert_matches_type(MeterListResponse, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: OpenMeter) -> None:
        meter = client.meters.delete(
            "x",
        )
        assert meter is None

    @parametrize
    def test_raw_response_delete(self, client: OpenMeter) -> None:
        response = client.meters.with_raw_response.delete(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = response.parse()
        assert meter is None

    @parametrize
    def test_streaming_response_delete(self, client: OpenMeter) -> None:
        with client.meters.with_streaming_response.delete(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = response.parse()
            assert meter is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meter_id_or_slug` but received ''"):
            client.meters.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_query(self, client: OpenMeter) -> None:
        meter = client.meters.query(
            meter_id_or_slug="x",
        )
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    def test_method_query_with_all_params(self, client: OpenMeter) -> None:
        meter = client.meters.query(
            meter_id_or_slug="x",
            filter_group_by={"foo": "string"},
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            group_by=["string", "string", "string"],
            subject=["string", "string", "string"],
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="MINUTE",
            window_time_zone="windowTimeZone",
        )
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    def test_raw_response_query(self, client: OpenMeter) -> None:
        response = client.meters.with_raw_response.query(
            meter_id_or_slug="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = response.parse()
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    def test_streaming_response_query(self, client: OpenMeter) -> None:
        with client.meters.with_streaming_response.query(
            meter_id_or_slug="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = response.parse()
            assert_matches_type(MeterQueryResult, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meter_id_or_slug` but received ''"):
            client.meters.with_raw_response.query(
                meter_id_or_slug="",
            )


class TestAsyncMeters:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOpenMeter) -> None:
        meter = await async_client.meters.create(
            aggregation="SUM",
            event_type="prompt",
            slug="tokens_total",
            window_size="MINUTE",
        )
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        meter = await async_client.meters.create(
            aggregation="SUM",
            event_type="prompt",
            slug="tokens_total",
            window_size="MINUTE",
            description="AI Token Usage",
            group_by={
                "model": "$.model",
                "type": "$.type",
            },
            value_property="$.tokens",
        )
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.meters.with_raw_response.create(
            aggregation="SUM",
            event_type="prompt",
            slug="tokens_total",
            window_size="MINUTE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = await response.parse()
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.meters.with_streaming_response.create(
            aggregation="SUM",
            event_type="prompt",
            slug="tokens_total",
            window_size="MINUTE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = await response.parse()
            assert_matches_type(Meter, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOpenMeter) -> None:
        meter = await async_client.meters.retrieve(
            "x",
        )
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.meters.with_raw_response.retrieve(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = await response.parse()
        assert_matches_type(Meter, meter, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.meters.with_streaming_response.retrieve(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = await response.parse()
            assert_matches_type(Meter, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meter_id_or_slug` but received ''"):
            await async_client.meters.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        meter = await async_client.meters.list()
        assert_matches_type(MeterListResponse, meter, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.meters.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = await response.parse()
        assert_matches_type(MeterListResponse, meter, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.meters.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = await response.parse()
            assert_matches_type(MeterListResponse, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncOpenMeter) -> None:
        meter = await async_client.meters.delete(
            "x",
        )
        assert meter is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.meters.with_raw_response.delete(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = await response.parse()
        assert meter is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.meters.with_streaming_response.delete(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = await response.parse()
            assert meter is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meter_id_or_slug` but received ''"):
            await async_client.meters.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_query(self, async_client: AsyncOpenMeter) -> None:
        meter = await async_client.meters.query(
            meter_id_or_slug="x",
        )
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        meter = await async_client.meters.query(
            meter_id_or_slug="x",
            filter_group_by={"foo": "string"},
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            group_by=["string", "string", "string"],
            subject=["string", "string", "string"],
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_size="MINUTE",
            window_time_zone="windowTimeZone",
        )
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.meters.with_raw_response.query(
            meter_id_or_slug="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = await response.parse()
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.meters.with_streaming_response.query(
            meter_id_or_slug="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = await response.parse()
            assert_matches_type(MeterQueryResult, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meter_id_or_slug` but received ''"):
            await async_client.meters.with_raw_response.query(
                meter_id_or_slug="",
            )
