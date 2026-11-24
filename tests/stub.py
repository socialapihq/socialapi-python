"""A client whose requests never leave: each is recorded and answered by a stub."""

from __future__ import annotations

import json
from typing import Any

import urllib3

from socialapihq import SocialAPI


class _Pool:
    def __init__(self, status: int, body: Any, headers: dict[str, str]) -> None:
        self.status = status
        self.body = body
        self.headers = headers
        self.requests: list[tuple[str, str, dict[str, str]]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> urllib3.HTTPResponse:
        self.requests.append((method, url, dict(kwargs.get("headers") or {})))
        return urllib3.HTTPResponse(
            body=json.dumps(self.body).encode(),
            status=self.status,
            headers={"content-type": "application/json", **self.headers},
            preload_content=False,
        )

    def clear(self) -> None:
        pass


def stubbed(status: int, body: Any, headers: dict[str, str] | None = None, **options: Any):
    client = SocialAPI(api_key="sapi_test", **options)
    pool = _Pool(status, body, headers or {})
    client._client.rest_client.pool_manager = pool  # noqa: SLF001 - the seam for tests
    return client, pool.requests
