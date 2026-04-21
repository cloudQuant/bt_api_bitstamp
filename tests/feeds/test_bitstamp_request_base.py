from unittest.mock import AsyncMock
import pytest
from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_bitstamp.feeds.live_bitstamp import BitstampRequestData


def test_bitstamp_request_allows_missing_extra_data(monkeypatch) -> None:
    request_data = BitstampRequestData(
        public_key="public-key",
        private_key="secret-key",
        exchange_name="BITSTAMP___SPOT",
    )

    monkeypatch.setattr(
        request_data,
        "http_request",
        lambda method, url, headers, body, timeout: {"server_time": 1710000000},
    )

    result = request_data.request("GET /api/v2/timestamp/")

    assert isinstance(result, RequestData)
    assert result.get_extra_data() == {}
    assert result.get_input_data() == {"server_time": 1710000000}
