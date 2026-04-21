# bt_api_bitstamp

Bitstamp exchange plugin for `bt_api`.

## Installation

```bash
pip install bt_api_bitstamp
```

## Usage

```python
from bt_api_bitstamp import BitstampRequestDataSpot

feed = BitstampRequestDataSpot(public_key="your_key", private_key="your_secret")
ticker = feed.get_ticker("BTCUSD")
```