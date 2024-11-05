import asyncio
from typing import Dict, List, Optional, Callable
from loguru import logger
import ccxt.pro as ccxt

from bjarkan.models import OrderbookConfig, TradesConfig, APIConfig, OrderConfig
from bjarkan.core.orderbook import OrderbookManager
from bjarkan.core.trades import TradesManager
from bjarkan.core.executor import OrderExecutor
from bjarkan.exceptions import BjarkanError


class BjarkanSDK:
    """Main SDK client for interacting with cryptocurrency exchanges."""

    def __init__(self):
        self._orderbook_manager = None
        self._trades_manager = None
        self._order_executor = None
        self._running = True
        logger.info("Initialized Bjarkan SDK")

    async def setup_orderbook(self, config: OrderbookConfig) -> Dict:
        """Configure and initialize orderbook data collection."""
        try:
            self._orderbook_manager = OrderbookManager(config)
            await self._orderbook_manager.initialize()
            return {"status": "success", "message": "Orderbook configuration set"}
        except Exception as e:
            raise BjarkanError(f"Failed to setup orderbook: {str(e)}")

    async def setup_trades(self, config: TradesConfig) -> Dict:
        """Configure and initialize trades data collection."""
        try:
            self._trades_manager = TradesManager(config)
            await self._trades_manager.initialize()
            return {"status": "success", "message": "Trades configuration set"}
        except Exception as e:
            raise BjarkanError(f"Failed to setup trades: {str(e)}")

    async def setup_api_keys(self, api_configs: List[APIConfig]) -> Dict:
        """Set up API keys for trading."""
        if not self._orderbook_manager:
            raise BjarkanError("Orderbook must be configured before setting API keys")

        try:
            self._order_executor = OrderExecutor(
                api_configs,
                self._orderbook_manager.config
            )
            await self._order_executor.initialize()
            return {"status": "success", "message": "API keys configured"}
        except Exception as e:
            raise BjarkanError(f"Failed to setup API keys: {str(e)}")

    async def start_orderbook(self, callback: Optional[Callable] = None):
        """Start orderbook data stream."""
        if not self._orderbook_manager:
            raise BjarkanError("Orderbook not configured")
        if callback:
            self._orderbook_manager.add_callback(callback)
        await self._orderbook_manager.start()

    async def start_trades(self, callback: Optional[Callable] = None):
        """Start trades data stream."""
        if not self._trades_manager:
            raise BjarkanError("Trades not configured")
        if callback:
            self._trades_manager.add_callback(callback)
        await self._trades_manager.start()

    async def stop_orderbook(self):
        """Stop orderbook data stream."""
        if self._orderbook_manager:
            await self._orderbook_manager.stop()

    async def stop_trades(self):
        """Stop trades data stream."""
        if self._trades_manager:
            await self._trades_manager.stop()

    async def get_latest_orderbook(self) -> Dict:
        """Get the latest orderbook data."""
        if not self._orderbook_manager:
            raise BjarkanError("Orderbook not configured")
        return await self._orderbook_manager.get_latest()

    async def get_latest_trades(self) -> Dict:
        """Get the latest trades data."""
        if not self._trades_manager:
            raise BjarkanError("Trades not configured")
        return await self._trades_manager.get_latest()

    async def execute_order(self, order: OrderConfig) -> Dict:
        """Execute an order using smart order routing."""
        if not self._order_executor:
            raise BjarkanError("API keys not configured")
        if not self._orderbook_manager:
            raise BjarkanError("Orderbook not configured")

        orderbook = await self.get_latest_orderbook()
        return await self._order_executor.execute(order, orderbook)

    async def get_balances(self) -> Dict:
        """Get current balances across configured exchanges."""
        if not self._order_executor:
            raise BjarkanError("API keys not configured")
        return await self._order_executor.get_balances()

    async def close(self):
        """Clean up resources and close connections."""
        self._running = False
        tasks = []

        if self._orderbook_manager:
            tasks.append(self._orderbook_manager.stop())
        if self._trades_manager:
            tasks.append(self._trades_manager.stop())
        if self._order_executor:
            tasks.append(self._order_executor.stop())

        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("SDK closed")
