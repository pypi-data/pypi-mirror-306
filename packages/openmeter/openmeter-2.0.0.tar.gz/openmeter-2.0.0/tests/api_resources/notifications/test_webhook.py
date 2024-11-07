# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWebhook:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_svix(self, client: OpenMeter) -> None:
        webhook = client.notifications.webhook.svix(
            data={"foo": "string"},
            type="endpoint.created",
        )
        assert webhook is None

    @parametrize
    def test_raw_response_svix(self, client: OpenMeter) -> None:
        response = client.notifications.webhook.with_raw_response.svix(
            data={"foo": "string"},
            type="endpoint.created",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert webhook is None

    @parametrize
    def test_streaming_response_svix(self, client: OpenMeter) -> None:
        with client.notifications.webhook.with_streaming_response.svix(
            data={"foo": "string"},
            type="endpoint.created",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert webhook is None

        assert cast(Any, response.is_closed) is True


class TestAsyncWebhook:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_svix(self, async_client: AsyncOpenMeter) -> None:
        webhook = await async_client.notifications.webhook.svix(
            data={"foo": "string"},
            type="endpoint.created",
        )
        assert webhook is None

    @parametrize
    async def test_raw_response_svix(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.webhook.with_raw_response.svix(
            data={"foo": "string"},
            type="endpoint.created",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert webhook is None

    @parametrize
    async def test_streaming_response_svix(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.webhook.with_streaming_response.svix(
            data={"foo": "string"},
            type="endpoint.created",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert webhook is None

        assert cast(Any, response.is_closed) is True
