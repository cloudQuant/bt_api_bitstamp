# Bitstamp Exchange Plugin for bt_api

## Bitstamp | 比特戳

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bitstamp.svg)](https://pypi.org/project/bt_api_bitstamp/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bitstamp.svg)](https://pypi.org/project/bt_api_bitstamp/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bitstamp/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bitstamp/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bitstamp/badge/?version=latest)](https://bt-api-bitstamp.readthedocs.io/)

---

## English | [中文](#中文)

### Overview

This package provides **Bitstamp exchange plugin** for the [bt_api](https://github.com/cloudQuant/bt_api_py) framework. It offers a unified interface for interacting with **Bitstamp**, one of the oldest and most trusted cryptocurrency exchanges in Europe.

Bitstamp provides trading in USD, EUR, GBP, and various cryptocurrencies. This plugin integrates Bitstamp's REST API v2 into the bt_api unified trading framework.

### Key Features

- **Complete REST API Coverage**: Ticker, order book, klines, trades, orders, balances
- **Basic Authentication**: Secure API key and secret key authentication via Base64 encoding
- **Rate Limit Protection**: Built-in rate limiter (200 requests/second per IP)
- **Unified Interface**: Compatible with bt_api's BtApi, EventBus, and data containers
- **Async Support**: Full async/await support for concurrent operations

### Exchange Information

| Item | Value |
|------|-------|
| Exchange Name | Bitstamp |
| Trading Code | `BITSTAMP___SPOT` |
| REST API URL | `https://www.bitstamp.net/api/v2` |
| WebSocket URL | `wss://ws.bitstamp.net` |
| Asset Type | SPOT |
| Supported Currencies | USD, EUR, GBP, USDC |
| Rate Limit | 200 requests/second per IP |
| Authentication | Basic Auth (Base64) |

### Installation

#### From PyPI (Recommended)

```bash
pip install bt_api_bitstamp
```

#### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bitstamp
cd bt_api_bitstamp
pip install -e .
```

### Quick Start

#### Initialize the Exchange

```python
from bt_api_py import BtApi

# Configure Bitstamp exchange
exchange_config = {
    "BITSTAMP___SPOT": {
        "api_key": "your_api_key",
        "secret_key": "your_secret_key",
    }
}

# Initialize BtApi
api = BtApi(exchange_kwargs=exchange_config)
```

#### Get Market Data

```python
# Get ticker
ticker = api.get_tick("BITSTAMP___SPOT", "BTCUSD")
print(ticker)

# Get order book depth
depth = api.get_depth("BITSTAMP___SPOT", "BTCUSD", limit=20)
print(depth)

# Get kline/candlestick data
klines = api.get_kline("BITSTAMP___SPOT", "BTCUSD", period="1h", count=100)
print(klines)

# Get recent trades
trades = api.get_trades("BITSTAMP___SPOT", "BTCUSD")
print(trades)
```

#### Trading Operations

```python
# Place an order (buy limit)
order = api.make_order(
    exchange_name="BITSTAMP___SPOT",
    symbol="BTCUSD",
    volume=0.01,
    price=50000,
    order_type="buy-limit",
)
print(order)

# Place an order (sell limit)
order = api.make_order(
    exchange_name="BITSTAMP___SPOT",
    symbol="BTCUSD",
    volume=0.01,
    price=60000,
    order_type="sell-limit",
)
print(order)

# Cancel an order
cancel_result = api.cancel_order(
    exchange_name="BITSTAMP___SPOT",
    symbol="BTCUSD",
    order_id="your_order_id",
)
print(cancel_result)

# Query order status
order_info = api.query_order(
    exchange_name="BITSTAMP___SPOT",
    symbol="BTCUSD",
    order_id="your_order_id",
)
print(order_info)

# Get open orders
open_orders = api.get_open_orders("BITSTAMP___SPOT", "BTCUSD")
print(open_orders)

# Get account balance
balance = api.get_balance("BITSTAMP___SPOT")
print(balance)
```

#### Asynchronous Operations

```python
import asyncio
from bt_api_py import BtApi

async def main():
    api = BtApi(exchange_kwargs={
        "BITSTAMP___SPOT": {
            "api_key": "your_api_key",
            "secret_key": "your_secret_key",
        }
    })

    # Async get ticker
    ticker = await api.async_get_tick("BITSTAMP___SPOT", "BTCUSD")
    print(ticker)

    # Async place order
    order = await api.async_make_order(
        exchange_name="BITSTAMP___SPOT",
        symbol="BTCUSD",
        volume=0.01,
        price=50000,
        order_type="buy-limit",
    )
    print(order)

asyncio.run(main())
```

### Supported Operations

| Operation | REST API | Description |
|-----------|----------|-------------|
| `get_tick` | GET /ticker/{symbol} | Get ticker data (last price, volume, etc.) |
| `get_depth` | GET /order_book/{symbol} | Get order book depth |
| `get_kline` | GET /ohlc/{symbol} | Get candlestick/kline data |
| `get_trades` | GET /transactions/{symbol} | Get recent trades |
| `make_order` | POST /buy, POST /sell | Place a new order |
| `cancel_order` | POST /cancel_order | Cancel an order |
| `query_order` | POST /order_status | Query order status |
| `get_open_orders` | POST /open_orders/all | Get all open orders |
| `get_deals` | POST /user_transactions | Get user transaction history |
| `get_balance` | POST /balance | Get account balance |
| `get_account` | POST /balance | Get account information |
| `get_server_time` | GET /server_time_utc | Get server time |
| `get_exchange_info` | GET /trading-pairs-info | Get available trading pairs |

### Symbol Format

Bitstamp uses lowercase symbols with no separator:

| bt_api Symbol | Bitstamp Symbol |
|---------------|----------------|
| `BTCUSD` | `btcusd` |
| `ETHUSD` | `ethusd` |
| `EURUSD` | `eurusd` |
| `XRPUSD` | `xrpusd` |
| `BTCGBP` | `btcgbp` |

The plugin automatically converts between formats.

### Order Types

Bitstamp supports the following order types:

| Order Type | Description |
|------------|-------------|
| `buy-limit` | Buy limit order |
| `sell-limit` | Sell limit order |
| `buy-market` | Buy market order |
| `sell-market` | Sell market order |

### Rate Limiting

Bitstamp implements a rate limit of **200 requests per second** per IP address. This plugin includes a built-in rate limiter using sliding window algorithm to prevent exceeding the limit.

### Error Handling

All API errors are translated to bt_api's standard error types:

```python
from bt_api_py.errors import (
    RateLimitError,
    AuthenticationError,
    OrderNotFoundError,
    InsufficientBalanceError,
)
```

### Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bitstamp.readthedocs.io/ |
| Chinese Docs | https://bt-api-bitstamp.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_bitstamp |
| Bitstamp API Docs | https://www.bitstamp.net/api/ |
| Issue Tracker | https://github.com/cloudQuant/bt_api_bitstamp/issues |

### Architecture

```
bt_api_bitstamp/
├── src/bt_api_bitstamp/           # Source code
│   ├── containers/                # Data containers
│   │   ├── balances/              # Balance data containers
│   │   └── orders/              # Order data containers
│   ├── exchange_data/            # Exchange configuration
│   │   └── __init__.py          # BitstampExchangeData class
│   ├── feeds/                   # API feeds
│   │   └── live_bitstamp/       # Live trading feed
│   │       ├── __init__.py      # BitstampRequestData base class
│   │       └── spot.py          # Spot trading feed
│   ├── tickers/                 # Ticker data containers
│   ├── errors/                   # Error translations
│   └── plugin.py                # Plugin registration
├── tests/                       # Unit tests
└── docs/                       # Documentation
```

### Requirements

| Dependency | Version | Description |
|------------|---------|-------------|
| Python | >= 3.9 | Programming language |
| bt_api_base | >= 0.15 | Core framework |

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

MIT License - see [LICENSE](LICENSE) for details.

### Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_bitstamp/issues)
- Email: yunjinqi@gmail.com

---

## 中文

### 概述

本包为 [bt_api](https://github.com/cloudQuant/bt_api_py) 框架提供 **Bitstamp（比特戳）交易所插件**。Bitstamp 是欧洲最古老、最可信赖的加密货币交易所之一，提供美元（USD）、欧元（EUR）、英镑（GBP）和各种加密货币的交易服务。

本插件将 Bitstamp 的 REST API v2 集成到 bt_api 统一交易框架中，提供标准化的行情查询、订单管理和账户查询接口。

### 核心功能

- **完整 REST API 覆盖**：行情、订单簿、K线、交易、订单、余额
- **Basic 认证**：通过 Base64 编码的安全 API Key 和 Secret Key 认证
- **速率限制保护**：内置限流器（每秒 200 请求/IP）
- **统一接口**：与 bt_api 的 BtApi、EventBus 和数据容器完全兼容
- **异步支持**：完整的 async/await 支持并发操作

### 交易所信息

| 项目 | 值 |
|------|-------|
| 交易所名称 | Bitstamp（比特戳） |
| 交易代码 | `BITSTAMP___SPOT` |
| REST API 地址 | `https://www.bitstamp.net/api/v2` |
| WebSocket 地址 | `wss://ws.bitstamp.net` |
| 资产类型 | 现货（SPOT） |
| 支持法币 | USD, EUR, GBP, USDC |
| 速率限制 | 每秒 200 请求/IP |
| 认证方式 | Basic Auth（Base64） |

### 安装

#### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bitstamp
```

#### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bitstamp
cd bt_api_bitstamp
pip install -e .
```

### 快速开始

#### 初始化交易所

```python
from bt_api_py import BtApi

# 配置 Bitstamp 交易所
exchange_config = {
    "BITSTAMP___SPOT": {
        "api_key": "your_api_key",
        "secret_key": "your_secret_key",
    }
}

# 初始化 BtApi
api = BtApi(exchange_kwargs=exchange_config)
```

#### 获取市场数据

```python
# 获取行情
ticker = api.get_tick("BITSTAMP___SPOT", "BTCUSD")
print(ticker)

# 获取订单簿深度
depth = api.get_depth("BITSTAMP___SPOT", "BTCUSD", limit=20)
print(depth)

# 获取 K 线数据
klines = api.get_kline("BITSTAMP___SPOT", "BTCUSD", period="1h", count=100)
print(klines)

# 获取最近交易
trades = api.get_trades("BITSTAMP___SPOT", "BTCUSD")
print(trades)
```

#### 交易操作

```python
# 下单（买入限价单）
order = api.make_order(
    exchange_name="BITSTAMP___SPOT",
    symbol="BTCUSD",
    volume=0.01,
    price=50000,
    order_type="buy-limit",
)
print(order)

# 下单（卖出限价单）
order = api.make_order(
    exchange_name="BITSTAMP___SPOT",
    symbol="BTCUSD",
    volume=0.01,
    price=60000,
    order_type="sell-limit",
)
print(order)

# 取消订单
cancel_result = api.cancel_order(
    exchange_name="BITSTAMP___SPOT",
    symbol="BTCUSD",
    order_id="your_order_id",
)
print(cancel_result)

# 查询订单状态
order_info = api.query_order(
    exchange_name="BITSTAMP___SPOT",
    symbol="BTCUSD",
    order_id="your_order_id",
)
print(order_info)

# 获取挂单
open_orders = api.get_open_orders("BITSTAMP___SPOT", "BTCUSD")
print(open_orders)

# 获取账户余额
balance = api.get_balance("BITSTAMP___SPOT")
print(balance)
```

#### 异步操作

```python
import asyncio
from bt_api_py import BtApi

async def main():
    api = BtApi(exchange_kwargs={
        "BITSTAMP___SPOT": {
            "api_key": "your_api_key",
            "secret_key": "your_secret_key",
        }
    })

    # 异步获取行情
    ticker = await api.async_get_tick("BITSTAMP___SPOT", "BTCUSD")
    print(ticker)

    # 异步下单
    order = await api.async_make_order(
        exchange_name="BITSTAMP___SPOT",
        symbol="BTCUSD",
        volume=0.01,
        price=50000,
        order_type="buy-limit",
    )
    print(order)

asyncio.run(main())
```

### 支持的操作

| 操作 | REST API | 说明 |
|------|----------|------|
| `get_tick` | GET /ticker/{symbol} | 获取行情数据（最新价格、成交量等） |
| `get_depth` | GET /order_book/{symbol} | 获取订单簿深度 |
| `get_kline` | GET /ohlc/{symbol} | 获取 K 线/蜡烛图数据 |
| `get_trades` | GET /transactions/{symbol} | 获取最近交易 |
| `make_order` | POST /buy, POST /sell | 下新订单 |
| `cancel_order` | POST /cancel_order | 取消订单 |
| `query_order` | POST /order_status | 查询订单状态 |
| `get_open_orders` | POST /open_orders/all | 获取所有挂单 |
| `get_deals` | POST /user_transactions | 获取用户交易历史 |
| `get_balance` | POST /balance | 获取账户余额 |
| `get_account` | POST /balance | 获取账户信息 |
| `get_server_time` | GET /server_time_utc | 获取服务器时间 |
| `get_exchange_info` | GET /trading-pairs-info | 获取可交易交易对 |

### 交易对格式

Bitstamp 使用小写字母无分隔符的格式：

| bt_api 交易对 | Bitstamp 交易对 |
|----------------|-----------------|
| `BTCUSD` | `btcusd` |
| `ETHUSD` | `ethusd` |
| `EURUSD` | `eurusd` |
| `XRPUSD` | `xrpusd` |
| `BTCGBP` | `btcgbp` |

插件会自动转换格式。

### 订单类型

Bitstamp 支持以下订单类型：

| 订单类型 | 说明 |
|----------|------|
| `buy-limit` | 买入限价单 |
| `sell-limit` | 卖出限价单 |
| `buy-market` | 买入市价单 |
| `sell-market` | 卖出市价单 |

### 速率限制

Bitstamp 的速率限制为 **每秒 200 请求**（每个 IP 地址）。本插件内置了滑动窗口算法的限流器，防止超出限制。

### 错误处理

所有 API 错误都会转换为 bt_api 的标准错误类型：

```python
from bt_api_py.errors import (
    RateLimitError,          # 速率限制错误
    AuthenticationError,     # 认证错误
    OrderNotFoundError,      # 订单未找到
    InsufficientBalanceError,  # 余额不足
)
```

### 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bitstamp.readthedocs.io/ |
| 中文文档 | https://bt-api-bitstamp.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_bitstamp |
| Bitstamp API 文档 | https://www.bitstamp.net/api/ |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bitstamp/issues |

### 系统要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | >= 3.9 | 编程语言 |
| bt_api_base | >= 0.15 | 核心框架 |

### 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

### 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_bitstamp/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com

---

如果这个项目对您有帮助，请给我们一个 Star！

[![Star History Chart](https://api.star-history.com/svg?repos=cloudQuant/bt_api_bitstamp&type=Date)](https://star-history.com/#cloudQuant/bt_api_bitstamp&Type=Date)
