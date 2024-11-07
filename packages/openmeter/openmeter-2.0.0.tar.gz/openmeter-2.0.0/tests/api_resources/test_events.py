# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types import EventListResponse, EventIngestResponse
from openmeter._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        event = client.events.list()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        event = client.events.list(
            id="id",
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            has_error=True,
            ingested_at_from=parse_datetime("2019-12-27T18:11:19.117Z"),
            ingested_at_to=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=1,
            subject="subject",
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.events.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.events.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventListResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_ingest(self, client: OpenMeter) -> None:
        event = client.events.ingest(
            id="5c10fade-1c9e-4d6c-8275-c52c36731d3c",
            source="service-name",
            specversion="1.0",
            subject="customer-id",
            type="prompt",
        )
        assert_matches_type(EventIngestResponse, event, path=["response"])

    @parametrize
    def test_method_ingest_with_all_params(self, client: OpenMeter) -> None:
        event = client.events.ingest(
            id="5c10fade-1c9e-4d6c-8275-c52c36731d3c",
            source="service-name",
            specversion="1.0",
            subject="customer-id",
            type="prompt",
            data="string",
            datacontenttype="application/json",
            dataschema="https://example.com",
            time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EventIngestResponse, event, path=["response"])

    @parametrize
    def test_raw_response_ingest(self, client: OpenMeter) -> None:
        response = client.events.with_raw_response.ingest(
            id="5c10fade-1c9e-4d6c-8275-c52c36731d3c",
            source="service-name",
            specversion="1.0",
            subject="customer-id",
            type="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventIngestResponse, event, path=["response"])

    @parametrize
    def test_streaming_response_ingest(self, client: OpenMeter) -> None:
        with client.events.with_streaming_response.ingest(
            id="5c10fade-1c9e-4d6c-8275-c52c36731d3c",
            source="service-name",
            specversion="1.0",
            subject="customer-id",
            type="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventIngestResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEvents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        event = await async_client.events.list()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        event = await async_client.events.list(
            id="id",
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            has_error=True,
            ingested_at_from=parse_datetime("2019-12-27T18:11:19.117Z"),
            ingested_at_to=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=1,
            subject="subject",
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.events.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.events.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventListResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_ingest(self, async_client: AsyncOpenMeter) -> None:
        event = await async_client.events.ingest(
            id="5c10fade-1c9e-4d6c-8275-c52c36731d3c",
            source="service-name",
            specversion="1.0",
            subject="customer-id",
            type="prompt",
        )
        assert_matches_type(EventIngestResponse, event, path=["response"])

    @parametrize
    async def test_method_ingest_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        event = await async_client.events.ingest(
            id="5c10fade-1c9e-4d6c-8275-c52c36731d3c",
            source="service-name",
            specversion="1.0",
            subject="customer-id",
            type="prompt",
            data="string",
            datacontenttype="application/json",
            dataschema="https://example.com",
            time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EventIngestResponse, event, path=["response"])

    @parametrize
    async def test_raw_response_ingest(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.events.with_raw_response.ingest(
            id="5c10fade-1c9e-4d6c-8275-c52c36731d3c",
            source="service-name",
            specversion="1.0",
            subject="customer-id",
            type="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventIngestResponse, event, path=["response"])

    @parametrize
    async def test_streaming_response_ingest(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.events.with_streaming_response.ingest(
            id="5c10fade-1c9e-4d6c-8275-c52c36731d3c",
            source="service-name",
            specversion="1.0",
            subject="customer-id",
            type="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventIngestResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True
