# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openmeter import OpenMeter, AsyncOpenMeter
from tests.utils import assert_matches_type
from openmeter.types import Subject, SubjectListResponse, SubjectUpsertResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSubjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: OpenMeter) -> None:
        subject = client.subjects.retrieve(
            "subjectIdOrKey",
        )
        assert_matches_type(Subject, subject, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: OpenMeter) -> None:
        response = client.subjects.with_raw_response.retrieve(
            "subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = response.parse()
        assert_matches_type(Subject, subject, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: OpenMeter) -> None:
        with client.subjects.with_streaming_response.retrieve(
            "subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = response.parse()
            assert_matches_type(Subject, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: OpenMeter) -> None:
        subject = client.subjects.list()
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: OpenMeter) -> None:
        response = client.subjects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = response.parse()
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: OpenMeter) -> None:
        with client.subjects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = response.parse()
            assert_matches_type(SubjectListResponse, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: OpenMeter) -> None:
        subject = client.subjects.delete(
            "subjectIdOrKey",
        )
        assert subject is None

    @parametrize
    def test_raw_response_delete(self, client: OpenMeter) -> None:
        response = client.subjects.with_raw_response.delete(
            "subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = response.parse()
        assert subject is None

    @parametrize
    def test_streaming_response_delete(self, client: OpenMeter) -> None:
        with client.subjects.with_streaming_response.delete(
            "subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = response.parse()
            assert subject is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: OpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            client.subjects.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_upsert(self, client: OpenMeter) -> None:
        subject = client.subjects.upsert(
            body=[{"key": "customer-id"}, {"key": "customer-id"}, {"key": "customer-id"}],
        )
        assert_matches_type(SubjectUpsertResponse, subject, path=["response"])

    @parametrize
    def test_raw_response_upsert(self, client: OpenMeter) -> None:
        response = client.subjects.with_raw_response.upsert(
            body=[{"key": "customer-id"}, {"key": "customer-id"}, {"key": "customer-id"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = response.parse()
        assert_matches_type(SubjectUpsertResponse, subject, path=["response"])

    @parametrize
    def test_streaming_response_upsert(self, client: OpenMeter) -> None:
        with client.subjects.with_streaming_response.upsert(
            body=[{"key": "customer-id"}, {"key": "customer-id"}, {"key": "customer-id"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = response.parse()
            assert_matches_type(SubjectUpsertResponse, subject, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSubjects:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncOpenMeter) -> None:
        subject = await async_client.subjects.retrieve(
            "subjectIdOrKey",
        )
        assert_matches_type(Subject, subject, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.with_raw_response.retrieve(
            "subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = await response.parse()
        assert_matches_type(Subject, subject, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.with_streaming_response.retrieve(
            "subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = await response.parse()
            assert_matches_type(Subject, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncOpenMeter) -> None:
        subject = await async_client.subjects.list()
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = await response.parse()
        assert_matches_type(SubjectListResponse, subject, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = await response.parse()
            assert_matches_type(SubjectListResponse, subject, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncOpenMeter) -> None:
        subject = await async_client.subjects.delete(
            "subjectIdOrKey",
        )
        assert subject is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.with_raw_response.delete(
            "subjectIdOrKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = await response.parse()
        assert subject is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.with_streaming_response.delete(
            "subjectIdOrKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = await response.parse()
            assert subject is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncOpenMeter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `subject_id_or_key` but received ''"):
            await async_client.subjects.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_upsert(self, async_client: AsyncOpenMeter) -> None:
        subject = await async_client.subjects.upsert(
            body=[{"key": "customer-id"}, {"key": "customer-id"}, {"key": "customer-id"}],
        )
        assert_matches_type(SubjectUpsertResponse, subject, path=["response"])

    @parametrize
    async def test_raw_response_upsert(self, async_client: AsyncOpenMeter) -> None:
        response = await async_client.subjects.with_raw_response.upsert(
            body=[{"key": "customer-id"}, {"key": "customer-id"}, {"key": "customer-id"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subject = await response.parse()
        assert_matches_type(SubjectUpsertResponse, subject, path=["response"])

    @parametrize
    async def test_streaming_response_upsert(self, async_client: AsyncOpenMeter) -> None:
        async with async_client.subjects.with_streaming_response.upsert(
            body=[{"key": "customer-id"}, {"key": "customer-id"}, {"key": "customer-id"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subject = await response.parse()
            assert_matches_type(SubjectUpsertResponse, subject, path=["response"])

        assert cast(Any, response.is_closed) is True
