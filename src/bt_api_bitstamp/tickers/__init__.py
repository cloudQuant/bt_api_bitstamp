from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float


class BitstampRequestTickerData(TickerData):
    def __init__(
        self,
        ticker_info: Any,
        symbol_name: str,
        asset_type: str = "SPOT",
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.exchange_name = "BITSTAMP"
        self.local_update_time = time.time()
        self.ticker_data: dict[str, Any] | None = ticker_info if has_been_json_encoded else None
        self.ticker_symbol_name: str | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.volume_24h: float | None = None
        self.high_24h: float | None = None
        self.low_24h: float | None = None
        self.open_24h: float | None = None
        self.has_been_init_data = False

    def init_data(self) -> BitstampRequestTickerData:
        if not self.has_been_json_encoded:
            self.ticker_data = (
                json.loads(self.ticker_info)
                if isinstance(self.ticker_info, str)
                else self.ticker_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = self.ticker_data or {}
        if data:
            self.ticker_symbol_name = self.symbol_name
            self.last_price = from_dict_get_float(data, "last")
            self.bid_price = from_dict_get_float(data, "bid")
            self.ask_price = from_dict_get_float(data, "ask")
            self.volume_24h = from_dict_get_float(data, "volume")
            self.high_24h = from_dict_get_float(data, "high")
            self.low_24h = from_dict_get_float(data, "low")
            self.open_24h = from_dict_get_float(data, "open")

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return str(self.exchange_name)

    def get_symbol_name(self) -> str:
        return str(self.symbol_name)

    def get_ticker_symbol_name(self) -> str | None:
        return self.ticker_symbol_name

    def get_asset_type(self) -> str:
        return str(self.asset_type)

    def get_local_update_time(self) -> float:
        return float(self.local_update_time)

    def get_server_time(self) -> float | None:
        return None

    def get_bid_price(self) -> float | None:
        return self.bid_price

    def get_ask_price(self) -> float | None:
        return self.ask_price

    def get_bid_volume(self) -> float | None:
        return None

    def get_ask_volume(self) -> float | None:
        return None

    def get_last_price(self) -> float | None:
        return self.last_price

    def get_last_volume(self) -> float | None:
        return None

    def get_all_data(self) -> dict[str, Any]:
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "asset_type": self.asset_type,
            "local_update_time": self.local_update_time,
            "ticker_symbol_name": self.ticker_symbol_name,
            "last_price": self.last_price,
            "bid_price": self.bid_price,
            "ask_price": self.ask_price,
            "volume_24h": self.volume_24h,
            "high_24h": self.high_24h,
            "low_24h": self.low_24h,
            "open_24h": self.open_24h,
        }

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()
