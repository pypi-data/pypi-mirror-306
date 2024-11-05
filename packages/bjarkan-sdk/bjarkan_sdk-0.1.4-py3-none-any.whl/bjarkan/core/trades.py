import asyncio
from typing import Dict, List, Optional, Callable
import ccxt.pro as ccxt
from loguru import logger

from bjarkan.models import TradesConfig
from bjarkan.exceptions import BjarkanError


class TradesManager:
    """Manages trade data collection and processing."""

    def __init__(self, config: TradesConfig):
        self.config = config
        self.exchanges = {}
        self.trades = {}
        self._callbacks = []
        self._running = True
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Initialize exchange connections."""
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

    async def _process_trade(self, exchange_id: str, trade: Dict) -> Dict:
        """Process raw trade data with fees if configured."""
        processed = trade.copy()

        if self.config.fees_bps:
            fee = self.config.fees_bps.get(exchange_id, 0)
            if isinstance(fee, dict):
                fee = fee.get(processed['symbol'], 0)

            fee_multiplier = 1 + (fee / 10000)
            processed['price'] = processed['price'] * fee_multiplier

        return processed

    async def get_latest(self) -> Dict:
        """Get the latest processed trade data."""
        async with self._lock:
            return self.trades.copy()

    def add_callback(self, callback: Callable):
        """Add callback for trade updates."""
        self._callbacks.append(callback)

    async def _collect_trades(self, exchange_id: str, symbol: str):
        """Collect and process trade data for a single exchange and symbol."""
        exchange = self.exchanges[exchange_id]

        while self._running:
            try:
                trades = await exchange.watch_trades(symbol)
                processed = await self._process_trade(exchange_id, trades[-1])

                async with self._lock:
                    if symbol not in self.trades:
                        self.trades[symbol] = []
                    self.trades[symbol].append(processed)

                for callback in self._callbacks:
                    await callback(processed)

            except Exception as e:
                if self._running:
                    logger.error(f"Error collecting trades from {exchange_id}: {str(e)}")
                await asyncio.sleep(5)

    async def start(self):
        """Start trade data collection."""
        tasks = [
            self._collect_trades(exchange_id, symbol)
            for exchange_id in self.exchanges
            for symbol in self.config.symbols
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def stop(self):
        """Stop trade data collection."""
        self._running = False
        await asyncio.gather(*[
            exchange.close()
            for exchange in self.exchanges.values()
        ], return_exceptions=True)
        self._callbacks.clear()
