# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types import MeterQueryResult
from openmeter._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMeters:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_query(self, client: OpenMeter) -> None:
        meter = client.portal.meters.query(
            meter_slug="tokens_total",
        )
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    def test_method_query_with_all_params(self, client: OpenMeter) -> None:
        meter = client.portal.meters.query(
            meter_slug="tokens_total",
            filter_group_by={
                "model": "gpt-4",
                "type": "input",
            },
            from_=parse_datetime("2023-01-01T00:00:00Z"),
            group_by=["model", "type"],
            to=parse_datetime("2023-01-02T00:00:00Z"),
            window_size="MINUTE",
            window_time_zone="America/New_York",
        )
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    def test_raw_response_query(self, client: OpenMeter) -> None:
        response = client.portal.meters.with_raw_response.query(
            meter_slug="tokens_total",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = response.parse()
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    def test_streaming_response_query(self, client: OpenMeter) -> None:
        with client.portal.meters.with_streaming_response.query(
            meter_slug="tokens_total",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = response.parse()
            assert_matches_type(MeterQueryResult, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meter_slug` but received ''"):
            client.portal.meters.with_raw_response.query(
                meter_slug="",
            )


class TestAsyncMeters:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_query(self, async_client: AsyncOpenMeter) -> None:
        meter = await async_client.portal.meters.query(
            meter_slug="tokens_total",
        )
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        meter = await async_client.portal.meters.query(
            meter_slug="tokens_total",
            filter_group_by={
                "model": "gpt-4",
                "type": "input",
            },
            from_=parse_datetime("2023-01-01T00:00:00Z"),
            group_by=["model", "type"],
            to=parse_datetime("2023-01-02T00:00:00Z"),
            window_size="MINUTE",
            window_time_zone="America/New_York",
        )
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.portal.meters.with_raw_response.query(
            meter_slug="tokens_total",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        meter = await response.parse()
        assert_matches_type(MeterQueryResult, meter, path=["response"])

    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.portal.meters.with_streaming_response.query(
            meter_slug="tokens_total",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            meter = await response.parse()
            assert_matches_type(MeterQueryResult, meter, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `meter_slug` but received ''"):
            await async_client.portal.meters.with_raw_response.query(
                meter_slug="",
            )
