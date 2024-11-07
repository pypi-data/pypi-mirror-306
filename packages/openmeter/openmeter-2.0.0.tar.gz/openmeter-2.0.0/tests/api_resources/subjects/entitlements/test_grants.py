# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter._utils import parse_datetime
from openmeter.types.subjects.entitlements import (
    EntitlementGrant,
    GrantListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGrants:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: OpenMeter) -> None:
        grant = client.subjects.entitlements.grants.create(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            amount=100,
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            expiration={
                "count": 12,
                "duration": "HOUR",
            },
        )
        assert_matches_type(EntitlementGrant, grant, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: OpenMeter) -> None:
        grant = client.subjects.entitlements.grants.create(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            amount=100,
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            expiration={
                "count": 12,
                "duration": "HOUR",
            },
            max_rollover_amount=100,
            metadata={"stripePaymentId": "pi_4OrAkhLvyihio9p51h9iiFnB"},
            min_rollover_amount=100,
            priority=1,
            recurrence={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(EntitlementGrant, grant, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.grants.with_raw_response.create(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            amount=100,
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            expiration={
                "count": 12,
                "duration": "HOUR",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        grant = response.parse()
        assert_matches_type(EntitlementGrant, grant, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.grants.with_streaming_response.create(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            amount=100,
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            expiration={
                "count": 12,
                "duration": "HOUR",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            grant = response.parse()
            assert_matches_type(EntitlementGrant, grant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.grants.with_raw_response.create(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
                amount=100,
                effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                expiration={
                    "count": 12,
                    "duration": "HOUR",
                },
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            client.subjects.entitlements.grants.with_raw_response.create(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
                amount=100,
                effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                expiration={
                    "count": 12,
                    "duration": "HOUR",
                },
            )

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        grant = client.subjects.entitlements.grants.list(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        )
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        grant = client.subjects.entitlements.grants.list(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            include_deleted=True,
            order_by="id",
        )
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.grants.with_raw_response.list(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        grant = response.parse()
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.grants.with_streaming_response.list(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            grant = response.parse()
            assert_matches_type(GrantListResponse, grant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.grants.with_raw_response.list(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            client.subjects.entitlements.grants.with_raw_response.list(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
            )


class TestAsyncGrants:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncOpenMeter) -> None:
        grant = await async_client.subjects.entitlements.grants.create(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            amount=100,
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            expiration={
                "count": 12,
                "duration": "HOUR",
            },
        )
        assert_matches_type(EntitlementGrant, grant, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        grant = await async_client.subjects.entitlements.grants.create(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            amount=100,
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            expiration={
                "count": 12,
                "duration": "HOUR",
            },
            max_rollover_amount=100,
            metadata={"stripePaymentId": "pi_4OrAkhLvyihio9p51h9iiFnB"},
            min_rollover_amount=100,
            priority=1,
            recurrence={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(EntitlementGrant, grant, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.grants.with_raw_response.create(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            amount=100,
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            expiration={
                "count": 12,
                "duration": "HOUR",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        grant = await response.parse()
        assert_matches_type(EntitlementGrant, grant, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.grants.with_streaming_response.create(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            amount=100,
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            expiration={
                "count": 12,
                "duration": "HOUR",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            grant = await response.parse()
            assert_matches_type(EntitlementGrant, grant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.grants.with_raw_response.create(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
                amount=100,
                effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                expiration={
                    "count": 12,
                    "duration": "HOUR",
                },
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            await async_client.subjects.entitlements.grants.with_raw_response.create(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
                amount=100,
                effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                expiration={
                    "count": 12,
                    "duration": "HOUR",
                },
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        grant = await async_client.subjects.entitlements.grants.list(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        )
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        grant = await async_client.subjects.entitlements.grants.list(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            include_deleted=True,
            order_by="id",
        )
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.grants.with_raw_response.list(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        grant = await response.parse()
        assert_matches_type(GrantListResponse, grant, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.grants.with_streaming_response.list(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            grant = await response.parse()
            assert_matches_type(GrantListResponse, grant, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.grants.with_raw_response.list(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            await async_client.subjects.entitlements.grants.with_raw_response.list(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
            )
