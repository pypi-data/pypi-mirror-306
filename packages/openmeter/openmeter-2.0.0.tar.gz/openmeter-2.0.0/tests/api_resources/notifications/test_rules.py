# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types.notifications import (
    NotificationRule,
    RuleListResponse,
    NotificationEvent,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRules:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: OpenMeter) -> None:
        rule = client.notifications.rules.create(
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: OpenMeter) -> None:
        rule = client.notifications.rules.create(
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
            disabled=True,
            features=["x"],
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: OpenMeter) -> None:
        response = client.notifications.rules.with_raw_response.create(
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: OpenMeter) -> None:
        with client.notifications.rules.with_streaming_response.create(
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(NotificationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: OpenMeter) -> None:
        rule = client.notifications.rules.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: OpenMeter) -> None:
        response = client.notifications.rules.with_raw_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: OpenMeter) -> None:
        with client.notifications.rules.with_streaming_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(NotificationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rule_id` but received ''"):
            client.notifications.rules.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: OpenMeter) -> None:
        rule = client.notifications.rules.update(
            rule_id="01G65Z755AFWAKHE12NY0CQ9FH",
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: OpenMeter) -> None:
        rule = client.notifications.rules.update(
            rule_id="01G65Z755AFWAKHE12NY0CQ9FH",
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
            disabled=True,
            features=["x"],
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: OpenMeter) -> None:
        response = client.notifications.rules.with_raw_response.update(
            rule_id="01G65Z755AFWAKHE12NY0CQ9FH",
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: OpenMeter) -> None:
        with client.notifications.rules.with_streaming_response.update(
            rule_id="01G65Z755AFWAKHE12NY0CQ9FH",
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(NotificationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rule_id` but received ''"):
            client.notifications.rules.with_raw_response.update(
                rule_id="",
                channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
                name="Balance threshold reached",
                thresholds=[
                    {
                        "type": "PERCENT",
                        "value": 100,
                    }
                ],
                type="entitlements.balance.threshold",
            )

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        rule = client.notifications.rules.list()
        assert_matches_type(RuleListResponse, rule, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        rule = client.notifications.rules.list(
            channel=["string", "string", "string"],
            feature=["x", "x", "x"],
            include_deleted=True,
            include_disabled=True,
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
        )
        assert_matches_type(RuleListResponse, rule, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.notifications.rules.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(RuleListResponse, rule, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.notifications.rules.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(RuleListResponse, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: OpenMeter) -> None:
        rule = client.notifications.rules.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert rule is None

    @parametrize
    def test_raw_response_delete(self, client: OpenMeter) -> None:
        response = client.notifications.rules.with_raw_response.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert rule is None

    @parametrize
    def test_streaming_response_delete(self, client: OpenMeter) -> None:
        with client.notifications.rules.with_streaming_response.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert rule is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rule_id` but received ''"):
            client.notifications.rules.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_test(self, client: OpenMeter) -> None:
        rule = client.notifications.rules.test(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert_matches_type(NotificationEvent, rule, path=["response"])

    @parametrize
    def test_raw_response_test(self, client: OpenMeter) -> None:
        response = client.notifications.rules.with_raw_response.test(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = response.parse()
        assert_matches_type(NotificationEvent, rule, path=["response"])

    @parametrize
    def test_streaming_response_test(self, client: OpenMeter) -> None:
        with client.notifications.rules.with_streaming_response.test(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = response.parse()
            assert_matches_type(NotificationEvent, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_test(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rule_id` but received ''"):
            client.notifications.rules.with_raw_response.test(
                "",
            )


class TestAsyncRules:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOpenMeter) -> None:
        rule = await async_client.notifications.rules.create(
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        rule = await async_client.notifications.rules.create(
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
            disabled=True,
            features=["x"],
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.rules.with_raw_response.create(
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.rules.with_streaming_response.create(
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(NotificationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOpenMeter) -> None:
        rule = await async_client.notifications.rules.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.rules.with_raw_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.rules.with_streaming_response.retrieve(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(NotificationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rule_id` but received ''"):
            await async_client.notifications.rules.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncOpenMeter) -> None:
        rule = await async_client.notifications.rules.update(
            rule_id="01G65Z755AFWAKHE12NY0CQ9FH",
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        rule = await async_client.notifications.rules.update(
            rule_id="01G65Z755AFWAKHE12NY0CQ9FH",
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
            disabled=True,
            features=["x"],
        )
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.rules.with_raw_response.update(
            rule_id="01G65Z755AFWAKHE12NY0CQ9FH",
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(NotificationRule, rule, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.rules.with_streaming_response.update(
            rule_id="01G65Z755AFWAKHE12NY0CQ9FH",
            channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
            name="Balance threshold reached",
            thresholds=[
                {
                    "type": "PERCENT",
                    "value": 100,
                }
            ],
            type="entitlements.balance.threshold",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(NotificationRule, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rule_id` but received ''"):
            await async_client.notifications.rules.with_raw_response.update(
                rule_id="",
                channels=["01G65Z755AFWAKHE12NY0CQ9FH"],
                name="Balance threshold reached",
                thresholds=[
                    {
                        "type": "PERCENT",
                        "value": 100,
                    }
                ],
                type="entitlements.balance.threshold",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        rule = await async_client.notifications.rules.list()
        assert_matches_type(RuleListResponse, rule, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        rule = await async_client.notifications.rules.list(
            channel=["string", "string", "string"],
            feature=["x", "x", "x"],
            include_deleted=True,
            include_disabled=True,
            order="ASC",
            order_by="id",
            page=1,
            page_size=1,
        )
        assert_matches_type(RuleListResponse, rule, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.rules.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(RuleListResponse, rule, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.rules.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(RuleListResponse, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncOpenMeter) -> None:
        rule = await async_client.notifications.rules.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert rule is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.rules.with_raw_response.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert rule is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.rules.with_streaming_response.delete(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert rule is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rule_id` but received ''"):
            await async_client.notifications.rules.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_test(self, async_client: AsyncOpenMeter) -> None:
        rule = await async_client.notifications.rules.test(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )
        assert_matches_type(NotificationEvent, rule, path=["response"])

    @parametrize
    async def test_raw_response_test(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.notifications.rules.with_raw_response.test(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rule = await response.parse()
        assert_matches_type(NotificationEvent, rule, path=["response"])

    @parametrize
    async def test_streaming_response_test(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.notifications.rules.with_streaming_response.test(
            "01G65Z755AFWAKHE12NY0CQ9FH",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rule = await response.parse()
            assert_matches_type(NotificationEvent, rule, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_test(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `rule_id` but received ''"):
            await async_client.notifications.rules.with_raw_response.test(
                "",
            )
