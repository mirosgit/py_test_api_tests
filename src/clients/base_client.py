from __future__ import annotations
from typing import Any, Dict, Optional
import json as _json

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.utils.config import settings
from src.utils.allure_helpers import attach_json, attach_text, as_curl


class BaseAPIClient:
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = (base_url or str(settings.base_url)).rstrip('/')
        self.timeout = timeout or settings.timeout
        self._headers: Dict[str, str] = {"Accept": "application/json"}
        if settings.x_api_key:
            self._headers["x-api-key"] = settings.x_api_key
        if settings.bearer_token:
            self._headers["Authorization"] = f"Bearer {settings.bearer_token}"
        self._client = httpx.Client(base_url=self.base_url, timeout=self.timeout, follow_redirects=True)

    def _attach(self, method: str, url: str, headers: Dict[str, str], json_data: Any | None, resp: httpx.Response) -> None:
        body = ""
        try:
            body = resp.request.content.decode() if resp.request.content else ""
        except Exception:
            pass
        attach_text("Request CURL", as_curl(method, url, headers=headers, body=body))
        if json_data is not None:
            attach_json("Request JSON", json_data)
        attach_text("Response Status", f"{resp.status_code}")
        try:
            attach_json("Response JSON", resp.json())
        except Exception:
            attach_text("Response Body", resp.text)

    @retry(stop=stop_after_attempt(settings.retries), wait=wait_exponential(multiplier=0.5, min=0.5, max=3))
    def _request(self, method: str, path: str, *, params: Dict[str, Any] | None = None, json: Any | None = None) -> httpx.Response:
        url = f"{self.base_url}{path}"
        headers = dict(self._headers)
        if method in {"POST", "PUT", "PATCH"}:
            headers["Content-Type"] = "application/json"
        resp = self._client.request(method, url, headers=headers, params=params, json=json)
        self._attach(method, url, headers, json, resp)
        return resp

    # convenience
    def get(self, path: str, *, params: Dict[str, Any] | None = None) -> httpx.Response:
        return self._request("GET", path, params=params)

    def post(self, path: str, *, json: Any | None = None) -> httpx.Response:
        return self._request("POST", path, json=json)

    def put(self, path: str, *, json: Any | None = None) -> httpx.Response:
        return self._request("PUT", path, json=json)

    def patch(self, path: str, *, json: Any | None = None) -> httpx.Response:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str, *, params: Dict[str, Any] | None = None) -> httpx.Response:
        return self._request("DELETE", path, params=params)

    def close(self) -> None:
        self._client.close()
