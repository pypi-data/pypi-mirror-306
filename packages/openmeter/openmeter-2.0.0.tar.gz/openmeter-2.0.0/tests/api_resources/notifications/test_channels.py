# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types.notifications import (
    ChannelListResponse,
    NotificationChannel,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChannels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: OpenMeter) -> None:
        channel = client.notifications.channels.create(
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: OpenMeter) -> None:
        channel = client.notifications.channels.create(
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
            custom_headers={"foo": "string"},
            disabled=True,
            signing_secret="whsec_S6g2HLnTwd9AhHwUIMFggVS9OfoPafN8",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: OpenMeter) -> None:
        response = client.notifications.channels.with_raw_response.create(
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = response.parse()
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: OpenMeter) -> None:
        with client.notifications.channels.with_streaming_response.create(
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = response.parse()
            assert_matches_type(NotificationChannel, channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: OpenMeter) -> None:
        channel = client.notifications.channels.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: OpenMeter) -> None:
        response = client.notifications.channels.with_raw_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = response.parse()
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: OpenMeter) -> None:
        with client.notifications.channels.with_streaming_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = response.parse()
            assert_matches_type(NotificationChannel, channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `channel_id` but received ''"):
            client.notifications.channels.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: OpenMeter) -> None:
        channel = client.notifications.channels.update(
            channel_id="01G65Z755AFWAKHE12NY0CQ9FH",
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: OpenMeter) -> None:
        channel = client.notifications.channels.update(
            channel_id="01G65Z755AFWAKHE12NY0CQ9FH",
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
            custom_headers={"foo": "string"},
            disabled=True,
            signing_secret="whsec_S6g2HLnTwd9AhHwUIMFggVS9OfoPafN8",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: OpenMeter) -> None:
        response = client.notifications.channels.with_raw_response.update(
            channel_id="01G65Z755AFWAKHE12NY0CQ9FH",
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = response.parse()
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: OpenMeter) -> None:
        with client.notifications.channels.with_streaming_response.update(
            channel_id="01G65Z755AFWAKHE12NY0CQ9FH",
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = response.parse()
            assert_matches_type(NotificationChannel, channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `channel_id` but received ''"):
            client.notifications.channels.with_raw_response.update(
                channel_id="",
                name="customer-webhook",
                type="WEBHOOK",
                url="https://example.com/webhook",
            )

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        channel = client.notifications.channels.list()
        assert_matches_type(ChannelListResponse, channel, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        channel = client.notifications.channels.list(
            include_deleted=True,
            include_disabled=True,
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
        )
        assert_matches_type(ChannelListResponse, channel, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.notifications.channels.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = response.parse()
        assert_matches_type(ChannelListResponse, channel, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.notifications.channels.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = response.parse()
            assert_matches_type(ChannelListResponse, channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: OpenMeter) -> None:
        channel = client.notifications.channels.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert channel is None

    @parametrize
    def test_raw_response_delete(self, client: OpenMeter) -> None:
        response = client.notifications.channels.with_raw_response.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = response.parse()
        assert channel is None

    @parametrize
    def test_streaming_response_delete(self, client: OpenMeter) -> None:
        with client.notifications.channels.with_streaming_response.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = response.parse()
            assert channel is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `channel_id` but received ''"):
            client.notifications.channels.with_raw_response.delete(
                "",
            )


class TestAsyncChannels:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOpenMeter) -> None:
        channel = await async_client.notifications.channels.create(
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        channel = await async_client.notifications.channels.create(
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
            custom_headers={"foo": "string"},
            disabled=True,
            signing_secret="whsec_S6g2HLnTwd9AhHwUIMFggVS9OfoPafN8",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.channels.with_raw_response.create(
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = await response.parse()
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.channels.with_streaming_response.create(
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = await response.parse()
            assert_matches_type(NotificationChannel, channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOpenMeter) -> None:
        channel = await async_client.notifications.channels.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.channels.with_raw_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = await response.parse()
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.channels.with_streaming_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = await response.parse()
            assert_matches_type(NotificationChannel, channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `channel_id` but received ''"):
            await async_client.notifications.channels.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncOpenMeter) -> None:
        channel = await async_client.notifications.channels.update(
            channel_id="01G65Z755AFWAKHE12NY0CQ9FH",
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        channel = await async_client.notifications.channels.update(
            channel_id="01G65Z755AFWAKHE12NY0CQ9FH",
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
            custom_headers={"foo": "string"},
            disabled=True,
            signing_secret="whsec_S6g2HLnTwd9AhHwUIMFggVS9OfoPafN8",
        )
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.channels.with_raw_response.update(
            channel_id="01G65Z755AFWAKHE12NY0CQ9FH",
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = await response.parse()
        assert_matches_type(NotificationChannel, channel, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.channels.with_streaming_response.update(
            channel_id="01G65Z755AFWAKHE12NY0CQ9FH",
            name="customer-webhook",
            type="WEBHOOK",
            url="https://example.com/webhook",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = await response.parse()
            assert_matches_type(NotificationChannel, channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `channel_id` but received ''"):
            await async_client.notifications.channels.with_raw_response.update(
                channel_id="",
                name="customer-webhook",
                type="WEBHOOK",
                url="https://example.com/webhook",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        channel = await async_client.notifications.channels.list()
        assert_matches_type(ChannelListResponse, channel, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        channel = await async_client.notifications.channels.list(
            include_deleted=True,
            include_disabled=True,
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
        )
        assert_matches_type(ChannelListResponse, channel, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.channels.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = await response.parse()
        assert_matches_type(ChannelListResponse, channel, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.channels.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = await response.parse()
            assert_matches_type(ChannelListResponse, channel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncOpenMeter) -> None:
        channel = await async_client.notifications.channels.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert channel is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.channels.with_raw_response.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        channel = await response.parse()
        assert channel is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.channels.with_streaming_response.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            channel = await response.parse()
            assert channel is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `channel_id` but received ''"):
            await async_client.notifications.channels.with_raw_response.delete(
                "",
            )
