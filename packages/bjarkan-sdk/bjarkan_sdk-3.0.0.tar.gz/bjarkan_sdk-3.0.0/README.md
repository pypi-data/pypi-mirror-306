# Bjarkan SDK

A powerful cryptocurrency trading SDK with smart order routing capabilities.

## Features

- Real-time market data aggregation from multiple exchanges
- Fee-aware orderbook processing
- VWAP calculations
- Smart order routing and execution
- Trade monitoring and filtering

## Installation

```bash
pip install bjarkan-sdk
```

## Quick Start

```python
import asyncio
from bjarkan import BjarkanSDK, OrderbookConfig

async def main():
    # Initialize SDK
    sdk = BjarkanSDK()
    
    # Configure orderbook data
    config = OrderbookConfig(
        aggregated=True,
        exchanges=["binance", "okx"],
        symbols=["BTC/USDT"],
        depth=10
    )
    
    # Setup and start
    await sdk.setup_orderbook(config)
    await sdk.start_orderbook()
    
    # Get real-time orderbook data
    orderbook = await sdk.get_latest_orderbook()
    print(orderbook)
    
    # Cleanup
    await sdk.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

For complete documentation, examples, and API reference, visit our [documentation](https://docs.bjarkan.io).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
