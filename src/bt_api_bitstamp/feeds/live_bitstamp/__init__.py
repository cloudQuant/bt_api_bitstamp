from __future__ import annotations

import base64
import json
import time
from typing import Any
from urllib.parse import urlencode

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.logging_factory import get_logger
from bt_api_base.rate_limiter import RateLimiter, RateLimitRule

from bt_api_bitstamp.exchange_data import BitstampExchangeData
from bt_api_bitstamp.tickers import BitstampRequestTickerData


class BitstampRequestData(Feed, RequestData):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
            Capability.QUERY_ORDER,
            Capability.QUERY_OPEN_ORDERS,
            Capability.GET_DEALS,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_SERVER_TIME,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.public_key = kwargs.get("public_key") or kwargs.get("api_key")
        self.private_key = (
            kwargs.get("private_key") or kwargs.get("secret_key") or kwargs.get("api_secret")
        )
        self.asset_type = kwargs.get("asset_type", "spot")
        self.exchange_name = "BITSTAMP"
        self.logger_name = kwargs.get("logger_name", "bitstamp_feed.log")
        self._params = BitstampExchangeData()
        self.request_logger = get_logger("request")
        self.async_logger = get_logger("async_request")
        self._rate_limiter = kwargs.get("rate_limiter", self._create_default_rate_limiter())

    @staticmethod
    def _create_default_rate_limiter():
        return RateLimiter(
            rules=[
                RateLimitRule(
                    name="bitstamp_public",
                    type="request_count",
                    interval=1,
                    limit=200,
                    scope="ip",
                ),
            ],
        )

    def _build_auth_headers(self, path: str, params: dict = None) -> dict:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if self.public_key is not None and self.private_key is not None:
            credentials = f"{self.public_key}:{self.private_key}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        return headers

    @staticmethod
    def _extract_data_normalize_function(input_data, extra_data):
        if input_data is None:
            return [], False
        if isinstance(input_data, dict):
            return [input_data], True
        if isinstance(input_data, list):
            return input_data, True
        return [], False

    def request(self, path, params=None, body=None, extra_data=None, timeout=10):
        if params is None:
            params = {}
        headers = self._build_auth_headers(path, params)
        url = f"{self._params.rest_url}{path}"
        return self._http_client.request(
            "POST" if body or "POST" in path else "GET",
            url,
            params=params,
            data=body,
            headers=headers,
            timeout=timeout,
            rate_limiter=self._rate_limiter,
        )

    def async_request(self, path, params=None, body=None, extra_data=None, timeout=10):
        if params is None:
            params = {}
        headers = self._build_auth_headers(path, params)
        url = f"{self._params.rest_url}{path}"
        return self._http_client.async_request(
            "POST" if body or "POST" in path else "GET",
            url,
            params=params,
            data=body,
            headers=headers,
            timeout=timeout,
            rate_limiter=self._rate_limiter,
        )

    def async_callback(self, response, extra_data=None):
        return response
