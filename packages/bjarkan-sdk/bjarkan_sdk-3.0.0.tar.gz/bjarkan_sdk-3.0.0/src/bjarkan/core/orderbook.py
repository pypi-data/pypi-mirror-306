import asyncio
from typing import Dict, List, Optional, Callable
import ccxt.pro as ccxt
from loguru import logger

from bjarkan.models import OrderbookConfig
from bjarkan.exceptions import BjarkanError


class OrderbookManager:
    """Manages orderbook data collection and processing."""

    def __init__(self, config: OrderbookConfig):
        self.config = config
        self.exchanges = {}
        self.orderbooks = {}
        self._callbacks = []
        self._running = True
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Initialize exchange connections and validate setup."""
        for exchange_id in self.config.exchanges:
            try:
                exchange_class = getattr(ccxt, exchange_id)
                exchange = exchange_class({'enableRateLimit': True})

                is_sandbox = self.config.sandbox_mode.get(exchange_id, False)
                exchange.set_sandbox_mode(is_sandbox)

                await exchange.load_markets()
                self.exchanges[exchange_id] = exchange

            except Exception as e:
                logger.error(f"Failed to initialize {exchange_id}: {str(e)}")
                raise BjarkanError(f"Exchange initialization failed: {str(e)}")

    async def _process_orderbook(self, exchange_id: str, orderbook: Dict) -> Dict:
        """Process raw orderbook data with fees and VWAP if configured."""
        processed = orderbook.copy()

        # Apply fees if configured
        if self.config.fees_bps:
            fee = self.config.fees_bps.get(exchange_id, 0)
            if isinstance(fee, dict):
                fee = fee.get(processed['symbol'], 0)

            fee_multiplier = 1 + (fee / 10000)
            processed['asks'] = [(price * fee_multiplier, amount)
                                 for price, amount in processed['asks']]
            processed['bids'] = [(price / fee_multiplier, amount)
                                 for price, amount in processed['bids']]

        # Apply VWAP if weighting is configured
        if self.config.weighting and processed['symbol'] in self.config.weighting:
            weight = self.config.weighting[processed['symbol']]
            processed = self._calculate_vwap(processed, weight)

        return processed

    def _calculate_vwap(self, orderbook: Dict, weight: Dict) -> Dict:
        """Calculate VWAP prices for given target size."""
        # VWAP calculation implementation
        return orderbook  # Simplified for brevity - actual implementation would calculate VWAP

    async def get_latest(self) -> Dict:
        """Get the latest processed orderbook data."""
        async with self._lock:
            return self.orderbooks.copy()

    def add_callback(self, callback: Callable):
        """Add callback for orderbook updates."""
        self._callbacks.append(callback)

    async def _collect_orderbook(self, exchange_id: str, symbol: str):
        """Collect and process orderbook data for a single exchange and symbol."""
        exchange = self.exchanges[exchange_id]

        while self._running:
            try:
                orderbook = await exchange.watch_order_book(symbol, self.config.depth)
                processed = await self._process_orderbook(exchange_id, orderbook)

                async with self._lock:
                    self.orderbooks[symbol] = processed

                for callback in self._callbacks:
                    await callback(processed)

            except Exception as e:
                if self._running:
                    logger.error(f"Error collecting orderbook from {exchange_id}: {str(e)}")
                await asyncio.sleep(5)

    async def start(self):
        """Start orderbook data collection."""
        tasks = [
            self._collect_orderbook(exchange_id, symbol)
            for exchange_id in self.exchanges
            for symbol in self.config.symbols
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def stop(self):
        """Stop orderbook data collection."""
        self._running = False
        await asyncio.gather(*[
            exchange.close()
            for exchange in self.exchanges.values()
        ], return_exceptions=True)
        self._callbacks.clear()
