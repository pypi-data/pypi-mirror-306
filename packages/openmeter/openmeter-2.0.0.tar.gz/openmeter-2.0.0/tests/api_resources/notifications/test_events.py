# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter._utils import parse_datetime
from openmeter.types.notifications import EventListResponse, NotificationEvent

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: OpenMeter) -> None:
        event = client.notifications.events.retrieve(
            "eventId",
        )
        assert_matches_type(NotificationEvent, event, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: OpenMeter) -> None:
        response = client.notifications.events.with_raw_response.retrieve(
            "eventId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(NotificationEvent, event, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: OpenMeter) -> None:
        with client.notifications.events.with_streaming_response.retrieve(
            "eventId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(NotificationEvent, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_id` but received ''"):
            client.notifications.events.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        event = client.notifications.events.list()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        event = client.notifications.events.list(
            channel=["01G65Z755AFWAKHE12NY0CQ9FH", "01G65Z755AFWAKHE12NY0CQ9FH", "01G65Z755AFWAKHE12NY0CQ9FH"],
            feature=["string", "string", "string"],
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
            rule=["01G65Z755AFWAKHE12NY0CQ9FH", "01G65Z755AFWAKHE12NY0CQ9FH", "01G65Z755AFWAKHE12NY0CQ9FH"],
            subject=["string", "string", "string"],
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.notifications.events.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.notifications.events.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventListResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEvents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOpenMeter) -> None:
        event = await async_client.notifications.events.retrieve(
            "eventId",
        )
        assert_matches_type(NotificationEvent, event, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.events.with_raw_response.retrieve(
            "eventId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(NotificationEvent, event, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.events.with_streaming_response.retrieve(
            "eventId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(NotificationEvent, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_id` but received ''"):
            await async_client.notifications.events.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        event = await async_client.notifications.events.list()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        event = await async_client.notifications.events.list(
            channel=["01G65Z755AFWAKHE12NY0CQ9FH", "01G65Z755AFWAKHE12NY0CQ9FH", "01G65Z755AFWAKHE12NY0CQ9FH"],
            feature=["string", "string", "string"],
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
            rule=["01G65Z755AFWAKHE12NY0CQ9FH", "01G65Z755AFWAKHE12NY0CQ9FH", "01G65Z755AFWAKHE12NY0CQ9FH"],
            subject=["string", "string", "string"],
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.events.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.events.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventListResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True
