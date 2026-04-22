from __future__ import annotations

from typing import Any

from bt_api_base.balance_utils import nested_balance_handler as _bitstamp_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_bitstamp.exchange_data import BitstampExchangeData
from bt_api_bitstamp.feeds.live_bitstamp.spot import BitstampRequestDataSpot


def _bitstamp_spot_subscribe_handler(
    data_queue: Any, exchange_params: Any, topics: Any, bt_api: Any,
) -> None:
    topic_list = [i["topic"] for i in topics]
    bt_api.log(f"Bitstamp Spot topics requested: {topic_list}")


def register_bitstamp(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("BITSTAMP___SPOT", BitstampRequestDataSpot)
    registry.register_exchange_data("BITSTAMP___SPOT", BitstampExchangeData)
    registry.register_balance_handler("BITSTAMP___SPOT", _bitstamp_balance_handler)
    registry.register_stream("BITSTAMP___SPOT", "subscribe", _bitstamp_spot_subscribe_handler)
