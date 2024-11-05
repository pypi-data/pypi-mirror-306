import asyncio
from typing import Dict, List
import ccxt.pro as ccxt
from loguru import logger

from bjarkan.models import OrderbookConfig, OrderConfig, APIConfig
from bjarkan.exceptions import BjarkanError


class OrderExecutor:
    """Handles order execution and smart order routing."""

    def __init__(self, api_configs: List[APIConfig], orderbook_config: OrderbookConfig):
        self.api_configs = {config.exchange: config for config in api_configs}
        self.orderbook_config = orderbook_config
        self.exchanges = {}
        self._running = True

    async def initialize(self):
        """Initialize exchange connections with API keys."""
        for exchange_id, config in self.api_configs.items():
            try:
                exchange_class = getattr(ccxt, exchange_id)
                exchange = exchange_class({
                    'apiKey': config.api_key,
                    'secret': config.secret,
                    'password': config.password,
                    'enableRateLimit': True
                })

                is_sandbox = self.orderbook_config.sandbox_mode.get(exchange_id, False)
                exchange.set_sandbox_mode(is_sandbox)

                await exchange.load_markets()
                self.exchanges[exchange_id] = exchange

            except Exception as e:
                logger.error(f"Failed to initialize {exchange_id}: {str(e)}")
                raise BjarkanError(f"Exchange initialization failed: {str(e)}")

    async def execute(self, order: OrderConfig, orderbook: Dict) -> Dict:
        """Execute an order using smart order routing."""
        if not orderbook:
            raise BjarkanError("No orderbook data available")

        execution_plan = self._create_execution_plan(order, orderbook)
        results = []

        for exchange_id, amount, price in execution_plan:
            try:
                exchange = self.exchanges[exchange_id]
                result = await exchange.create_order(
                    symbol=order.symbol,
                    type=order.type,
                    side=order.side,
                    amount=amount,price=price if order.type == 'limit' else None,
                    params={'timeInForce': order.time_in_force} if order.type == 'limit' else {}
                )

                results.append({
                    'exchange': exchange_id,
                    'order_id': result['id'],
                    'amount': amount,
                    'price': price,
                    'status': result['status'],
                    'filled': result.get('filled', 0)
                })

            except Exception as e:
                logger.error(f"Order execution failed on {exchange_id}: {str(e)}")
                results.append({
                    'exchange': exchange_id,
                    'error': str(e),
                    'amount': amount,
                    'price': price,
                    'status': 'failed'
                })

        return {
            'status': 'completed' if any(r.get('status') == 'filled' for r in results) else 'partial',
            'results': results,
            'execution_plan': execution_plan
        }

    @staticmethod
    def _create_execution_plan(order: OrderConfig, orderbook: Dict) -> List[tuple]:
        """Create an execution plan based on available liquidity."""
        execution_plan = []
        remaining_amount = order.amount

        # Sort venues by best price
        venues = []
        if order.side == 'buy':
            for symbol, data in orderbook.items():
                for price, amount, exchange in data['asks']:
                    venues.append((exchange, price, amount))
            venues.sort(key=lambda x: x[1])  # Sort by lowest ask price
        else:
            for symbol, data in orderbook.items():
                for price, amount, exchange in data['bids']:
                    venues.append((exchange, price, amount))
            venues.sort(key=lambda x: x[1], reverse=True)  # Sort by highest bid price

        # Create execution plan
        for exchange, price, available in venues:
            if remaining_amount <= 0:
                break
            executable = min(remaining_amount, available)
            execution_plan.append((exchange, executable, price))
            remaining_amount -= executable

        return execution_plan

    async def get_balances(self) -> Dict:
        """Get current balances across all configured exchanges."""
        balances = {}

        for exchange_id, exchange in self.exchanges.items():
            try:
                balance = await exchange.fetch_balance()
                balances[exchange_id] = {
                    currency: {
                        'free': data['free'],
                        'used': data['used'],
                        'total': data['total']
                    }
                    for currency, data in balance.items()
                    if currency not in ['info', 'timestamp', 'datetime']
                }
            except Exception as e:
                logger.error(f"Failed to fetch balance from {exchange_id}: {str(e)}")
                balances[exchange_id] = {'error': str(e)}

        return balances

    async def stop(self):
        """Clean up resources."""
        self._running = False
        await asyncio.gather(*[
            exchange.close()
            for exchange in self.exchanges.values()
        ], return_exceptions=True)
