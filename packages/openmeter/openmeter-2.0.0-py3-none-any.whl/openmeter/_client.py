# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Dict, Union, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "OpenMeter",
    "AsyncOpenMeter",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "production": "https://openmeter.cloud",
    "local": "https://127.0.0.1:8888",
}


class OpenMeter(SyncAPIClient):
    events: resources.EventsResource
    meters: resources.MetersResource
    subjects: resources.SubjectsResource
    entitlements: resources.EntitlementsResource
    notifications: resources.NotificationsResource
    portal: resources.PortalResource
    debug: resources.DebugResource
    with_raw_response: OpenMeterWithRawResponse
    with_streaming_response: OpenMeterWithStreamedResponse

    # client options
    cloud_api_token: str | None

    _environment: Literal["production", "local"] | NotGiven

    def __init__(
        self,
        *,
        cloud_api_token: str | None = None,
        environment: Literal["production", "local"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous OpenMeter client instance.

        This automatically infers the `cloud_api_token` argument from the `CLOUD_API_TOKEN` environment variable if it is not provided.
        """
        if cloud_api_token is None:
            cloud_api_token = os.environ.get("CLOUD_API_TOKEN")
        self.cloud_api_token = cloud_api_token

        self._environment = environment

        base_url_env = os.environ.get("OPEN_METER_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `OPEN_METER_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.events = resources.EventsResource(self)
        self.meters = resources.MetersResource(self)
        self.subjects = resources.SubjectsResource(self)
        self.entitlements = resources.EntitlementsResource(self)
        self.notifications = resources.NotificationsResource(self)
        self.portal = resources.PortalResource(self)
        self.debug = resources.DebugResource(self)
        self.with_raw_response = OpenMeterWithRawResponse(self)
        self.with_streaming_response = OpenMeterWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        cloud_api_token = self.cloud_api_token
        if cloud_api_token is None:
            return {}
        return {"Authorization": f"Bearer {cloud_api_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.cloud_api_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the cloud_api_token to be set. Or for the `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        cloud_api_token: str | None = None,
        environment: Literal["production", "local"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            cloud_api_token=cloud_api_token or self.cloud_api_token,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncOpenMeter(AsyncAPIClient):
    events: resources.AsyncEventsResource
    meters: resources.AsyncMetersResource
    subjects: resources.AsyncSubjectsResource
    entitlements: resources.AsyncEntitlementsResource
    notifications: resources.AsyncNotificationsResource
    portal: resources.AsyncPortalResource
    debug: resources.AsyncDebugResource
    with_raw_response: AsyncOpenMeterWithRawResponse
    with_streaming_response: AsyncOpenMeterWithStreamedResponse

    # client options
    cloud_api_token: str | None

    _environment: Literal["production", "local"] | NotGiven

    def __init__(
        self,
        *,
        cloud_api_token: str | None = None,
        environment: Literal["production", "local"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async OpenMeter client instance.

        This automatically infers the `cloud_api_token` argument from the `CLOUD_API_TOKEN` environment variable if it is not provided.
        """
        if cloud_api_token is None:
            cloud_api_token = os.environ.get("CLOUD_API_TOKEN")
        self.cloud_api_token = cloud_api_token

        self._environment = environment

        base_url_env = os.environ.get("OPEN_METER_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `OPEN_METER_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.events = resources.AsyncEventsResource(self)
        self.meters = resources.AsyncMetersResource(self)
        self.subjects = resources.AsyncSubjectsResource(self)
        self.entitlements = resources.AsyncEntitlementsResource(self)
        self.notifications = resources.AsyncNotificationsResource(self)
        self.portal = resources.AsyncPortalResource(self)
        self.debug = resources.AsyncDebugResource(self)
        self.with_raw_response = AsyncOpenMeterWithRawResponse(self)
        self.with_streaming_response = AsyncOpenMeterWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        cloud_api_token = self.cloud_api_token
        if cloud_api_token is None:
            return {}
        return {"Authorization": f"Bearer {cloud_api_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.cloud_api_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the cloud_api_token to be set. Or for the `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        cloud_api_token: str | None = None,
        environment: Literal["production", "local"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            cloud_api_token=cloud_api_token or self.cloud_api_token,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class OpenMeterWithRawResponse:
    def __init__(self, client: OpenMeter) -> None:
        self.events = resources.EventsResourceWithRawResponse(client.events)
        self.meters = resources.MetersResourceWithRawResponse(client.meters)
        self.subjects = resources.SubjectsResourceWithRawResponse(client.subjects)
        self.entitlements = resources.EntitlementsResourceWithRawResponse(client.entitlements)
        self.notifications = resources.NotificationsResourceWithRawResponse(client.notifications)
        self.portal = resources.PortalResourceWithRawResponse(client.portal)
        self.debug = resources.DebugResourceWithRawResponse(client.debug)


class AsyncOpenMeterWithRawResponse:
    def __init__(self, client: AsyncOpenMeter) -> None:
        self.events = resources.AsyncEventsResourceWithRawResponse(client.events)
        self.meters = resources.AsyncMetersResourceWithRawResponse(client.meters)
        self.subjects = resources.AsyncSubjectsResourceWithRawResponse(client.subjects)
        self.entitlements = resources.AsyncEntitlementsResourceWithRawResponse(client.entitlements)
        self.notifications = resources.AsyncNotificationsResourceWithRawResponse(client.notifications)
        self.portal = resources.AsyncPortalResourceWithRawResponse(client.portal)
        self.debug = resources.AsyncDebugResourceWithRawResponse(client.debug)


class OpenMeterWithStreamedResponse:
    def __init__(self, client: OpenMeter) -> None:
        self.events = resources.EventsResourceWithStreamingResponse(client.events)
        self.meters = resources.MetersResourceWithStreamingResponse(client.meters)
        self.subjects = resources.SubjectsResourceWithStreamingResponse(client.subjects)
        self.entitlements = resources.EntitlementsResourceWithStreamingResponse(client.entitlements)
        self.notifications = resources.NotificationsResourceWithStreamingResponse(client.notifications)
        self.portal = resources.PortalResourceWithStreamingResponse(client.portal)
        self.debug = resources.DebugResourceWithStreamingResponse(client.debug)


class AsyncOpenMeterWithStreamedResponse:
    def __init__(self, client: AsyncOpenMeter) -> None:
        self.events = resources.AsyncEventsResourceWithStreamingResponse(client.events)
        self.meters = resources.AsyncMetersResourceWithStreamingResponse(client.meters)
        self.subjects = resources.AsyncSubjectsResourceWithStreamingResponse(client.subjects)
        self.entitlements = resources.AsyncEntitlementsResourceWithStreamingResponse(client.entitlements)
        self.notifications = resources.AsyncNotificationsResourceWithStreamingResponse(client.notifications)
        self.portal = resources.AsyncPortalResourceWithStreamingResponse(client.portal)
        self.debug = resources.AsyncDebugResourceWithStreamingResponse(client.debug)


Client = OpenMeter

AsyncClient = AsyncOpenMeter
