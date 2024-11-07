# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types import Entitlement
from openmeter._utils import parse_datetime
from openmeter.types.subjects import (
    EntitlementValue,
    EntitlementListResponse,
    EntitlementHistoryResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEntitlements:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            is_soft_limit=True,
            issue_after_reset=0,
            issue_after_reset_priority=1,
            is_unlimited=True,
            measure_usage_from="CURRENT_PERIOD_START",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            preserve_overage_at_reset=True,
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.create(
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.create(
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_overload_1(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.create(
                subject_id_or_key="",
                type="metered",
                usage_period={"interval": "DAY"},
            )

    @parametrize
    def test_method_create_overload_2(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_raw_response_create_overload_2(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.create(
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_2(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.create(
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_overload_2(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.create(
                subject_id_or_key="",
                config='{ "integrations": ["github"] }',
                type="static",
            )

    @parametrize
    def test_method_create_overload_3(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_3(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_raw_response_create_overload_3(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.create(
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_3(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.create(
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_overload_3(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.create(
                subject_id_or_key="",
                type="boolean",
            )

    @parametrize
    def test_method_retrieve(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.retrieve(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.retrieve(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.retrieve(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.retrieve(
                entitlement_id="entitlementId",
                subject_id_or_key="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            client.subjects.entitlements.with_raw_response.retrieve(
                entitlement_id="",
                subject_id_or_key="subjectIdOrKey",
            )

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.list(
            subject_id_or_key="subjectIdOrKey",
        )
        assert_matches_type(EntitlementListResponse, entitlement, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.list(
            subject_id_or_key="subjectIdOrKey",
            include_deleted=True,
        )
        assert_matches_type(EntitlementListResponse, entitlement, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.list(
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(EntitlementListResponse, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.list(
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(EntitlementListResponse, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.list(
                subject_id_or_key="",
            )

    @parametrize
    def test_method_delete(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.delete(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )
        assert entitlement is None

    @parametrize
    def test_raw_response_delete(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.delete(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert entitlement is None

    @parametrize
    def test_streaming_response_delete(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.delete(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert entitlement is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.delete(
                entitlement_id="entitlementId",
                subject_id_or_key="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            client.subjects.entitlements.with_raw_response.delete(
                entitlement_id="",
                subject_id_or_key="subjectIdOrKey",
            )

    @parametrize
    def test_method_history(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.history(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            window_size="MINUTE",
        )
        assert_matches_type(EntitlementHistoryResponse, entitlement, path=["response"])

    @parametrize
    def test_method_history_with_all_params(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.history(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            window_size="MINUTE",
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_time_zone="windowTimeZone",
        )
        assert_matches_type(EntitlementHistoryResponse, entitlement, path=["response"])

    @parametrize
    def test_raw_response_history(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.history(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            window_size="MINUTE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(EntitlementHistoryResponse, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_history(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.history(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            window_size="MINUTE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(EntitlementHistoryResponse, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_history(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.history(
                entitlement_id="entitlementId",
                subject_id_or_key="",
                window_size="MINUTE",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            client.subjects.entitlements.with_raw_response.history(
                entitlement_id="",
                subject_id_or_key="subjectIdOrKey",
                window_size="MINUTE",
            )

    @parametrize
    def test_method_override_overload_1(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_method_override_with_all_params_overload_1(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            is_soft_limit=True,
            issue_after_reset=0,
            issue_after_reset_priority=1,
            is_unlimited=True,
            measure_usage_from="CURRENT_PERIOD_START",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            preserve_overage_at_reset=True,
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_raw_response_override_overload_1(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_override_overload_1(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_override_overload_1(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
                type="metered",
                usage_period={"interval": "DAY"},
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
                type="metered",
                usage_period={"interval": "DAY"},
            )

    @parametrize
    def test_method_override_overload_2(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_method_override_with_all_params_overload_2(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_raw_response_override_overload_2(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_override_overload_2(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_override_overload_2(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
                config='{ "integrations": ["github"] }',
                type="static",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
                config='{ "integrations": ["github"] }',
                type="static",
            )

    @parametrize
    def test_method_override_overload_3(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_method_override_with_all_params_overload_3(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_raw_response_override_overload_3(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_override_overload_3(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_override_overload_3(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
                type="boolean",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
                type="boolean",
            )

    @parametrize
    def test_method_reset(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.reset(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )
        assert entitlement is None

    @parametrize
    def test_method_reset_with_all_params(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.reset(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            preserve_overage=True,
            retain_anchor=True,
        )
        assert entitlement is None

    @parametrize
    def test_raw_response_reset(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.reset(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert entitlement is None

    @parametrize
    def test_streaming_response_reset(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.reset(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert entitlement is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_reset(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.reset(
                entitlement_id="entitlementId",
                subject_id_or_key="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            client.subjects.entitlements.with_raw_response.reset(
                entitlement_id="",
                subject_id_or_key="subjectIdOrKey",
            )

    @parametrize
    def test_method_value(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.value(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        )
        assert_matches_type(EntitlementValue, entitlement, path=["response"])

    @parametrize
    def test_method_value_with_all_params(self, client: OpenMeter) -> None:
        entitlement = client.subjects.entitlements.value(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EntitlementValue, entitlement, path=["response"])

    @parametrize
    def test_raw_response_value(self, client: OpenMeter) -> None:
        response = client.subjects.entitlements.with_raw_response.value(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = response.parse()
        assert_matches_type(EntitlementValue, entitlement, path=["response"])

    @parametrize
    def test_streaming_response_value(self, client: OpenMeter) -> None:
        with client.subjects.entitlements.with_streaming_response.value(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = response.parse()
            assert_matches_type(EntitlementValue, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_value(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.entitlements.with_raw_response.value(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            client.subjects.entitlements.with_raw_response.value(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
            )


class TestAsyncEntitlements:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            is_soft_limit=True,
            issue_after_reset=0,
            issue_after_reset_priority=1,
            is_unlimited=True,
            measure_usage_from="CURRENT_PERIOD_START",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            preserve_overage_at_reset=True,
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.create(
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.create(
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_overload_1(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.create(
                subject_id_or_key="",
                type="metered",
                usage_period={"interval": "DAY"},
            )

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.create(
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.create(
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_overload_2(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.create(
                subject_id_or_key="",
                config='{ "integrations": ["github"] }',
                type="static",
            )

    @parametrize
    async def test_method_create_overload_3(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_3(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.create(
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_3(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.create(
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_3(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.create(
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_overload_3(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.create(
                subject_id_or_key="",
                type="boolean",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.retrieve(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.retrieve(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.retrieve(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.retrieve(
                entitlement_id="entitlementId",
                subject_id_or_key="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.retrieve(
                entitlement_id="",
                subject_id_or_key="subjectIdOrKey",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.list(
            subject_id_or_key="subjectIdOrKey",
        )
        assert_matches_type(EntitlementListResponse, entitlement, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.list(
            subject_id_or_key="subjectIdOrKey",
            include_deleted=True,
        )
        assert_matches_type(EntitlementListResponse, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.list(
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(EntitlementListResponse, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.list(
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(EntitlementListResponse, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.list(
                subject_id_or_key="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.delete(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )
        assert entitlement is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.delete(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert entitlement is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.delete(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert entitlement is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.delete(
                entitlement_id="entitlementId",
                subject_id_or_key="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.delete(
                entitlement_id="",
                subject_id_or_key="subjectIdOrKey",
            )

    @parametrize
    async def test_method_history(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.history(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            window_size="MINUTE",
        )
        assert_matches_type(EntitlementHistoryResponse, entitlement, path=["response"])

    @parametrize
    async def test_method_history_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.history(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            window_size="MINUTE",
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
            window_time_zone="windowTimeZone",
        )
        assert_matches_type(EntitlementHistoryResponse, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_history(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.history(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            window_size="MINUTE",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(EntitlementHistoryResponse, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_history(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.history(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            window_size="MINUTE",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(EntitlementHistoryResponse, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_history(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.history(
                entitlement_id="entitlementId",
                subject_id_or_key="",
                window_size="MINUTE",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.history(
                entitlement_id="",
                subject_id_or_key="subjectIdOrKey",
                window_size="MINUTE",
            )

    @parametrize
    async def test_method_override_overload_1(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_method_override_with_all_params_overload_1(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            is_soft_limit=True,
            issue_after_reset=0,
            issue_after_reset_priority=1,
            is_unlimited=True,
            measure_usage_from="CURRENT_PERIOD_START",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            preserve_overage_at_reset=True,
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_override_overload_1(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_override_overload_1(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="metered",
            usage_period={"interval": "DAY"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_override_overload_1(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
                type="metered",
                usage_period={"interval": "DAY"},
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            await async_client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
                type="metered",
                usage_period={"interval": "DAY"},
            )

    @parametrize
    async def test_method_override_overload_2(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_method_override_with_all_params_overload_2(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_override_overload_2(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_override_overload_2(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            config='{ "integrations": ["github"] }',
            type="static",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_override_overload_2(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
                config='{ "integrations": ["github"] }',
                type="static",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            await async_client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
                config='{ "integrations": ["github"] }',
                type="static",
            )

    @parametrize
    async def test_method_override_overload_3(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_method_override_with_all_params_overload_3(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
            feature_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            feature_key="x",
            metadata={"externalId": "019142cc-a016-796a-8113-1a942fecd26d"},
            usage_period={
                "interval": "DAY",
                "anchor": parse_datetime("2019-12-27T18:11:19.117Z"),
            },
        )
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_override_overload_3(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(Entitlement, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_override_overload_3(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.override(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            type="boolean",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(Entitlement, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_override_overload_3(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
                type="boolean",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            await async_client.subjects.entitlements.with_raw_response.override(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
                type="boolean",
            )

    @parametrize
    async def test_method_reset(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.reset(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )
        assert entitlement is None

    @parametrize
    async def test_method_reset_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.reset(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
            effective_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            preserve_overage=True,
            retain_anchor=True,
        )
        assert entitlement is None

    @parametrize
    async def test_raw_response_reset(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.reset(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert entitlement is None

    @parametrize
    async def test_streaming_response_reset(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.reset(
            entitlement_id="entitlementId",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert entitlement is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_reset(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.reset(
                entitlement_id="entitlementId",
                subject_id_or_key="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entitlement_id` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.reset(
                entitlement_id="",
                subject_id_or_key="subjectIdOrKey",
            )

    @parametrize
    async def test_method_value(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.value(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        )
        assert_matches_type(EntitlementValue, entitlement, path=["response"])

    @parametrize
    async def test_method_value_with_all_params(self, async_client: AsyncOpenMeter) -> None:
        entitlement = await async_client.subjects.entitlements.value(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
            time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(EntitlementValue, entitlement, path=["response"])

    @parametrize
    async def test_raw_response_value(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.entitlements.with_raw_response.value(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        entitlement = await response.parse()
        assert_matches_type(EntitlementValue, entitlement, path=["response"])

    @parametrize
    async def test_streaming_response_value(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.entitlements.with_streaming_response.value(
            entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
            subject_id_or_key="subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            entitlement = await response.parse()
            assert_matches_type(EntitlementValue, entitlement, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_value(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.entitlements.with_raw_response.value(
                entitlement_id_or_feature_key="entitlementIdOrFeatureKey",
                subject_id_or_key="",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `entitlement_id_or_feature_key` but received ''"
        ):
            await async_client.subjects.entitlements.with_raw_response.value(
                entitlement_id_or_feature_key="",
                subject_id_or_key="subjectIdOrKey",
            )
