import asyncio
from typing import Dict, List
import ccxt.pro as ccxt
import time
from bjarkan.models import OrderbookConfig, OrderConfig, APIConfig
from bjarkan.utils.logger import logger, catch_exception


class OrderExecutor:
    @catch_exception
    def __init__(self, orderbook_config: OrderbookConfig, api_configs: List[APIConfig]):
        if not orderbook_config.aggregated or len(orderbook_config.symbols) != 1:
            raise ValueError("OrderExecutor requires aggregated data and exactly one symbol in orderbook_config")

        self.orderbook_config = orderbook_config
        self.api_configs = {config.exchange: config for config in api_configs}
        self.exchanges = {}
        self.symbol = orderbook_config.symbols[0]
        self.latest_orderbook = None

        self._initialize_exchanges()

    @catch_exception
    def _initialize_exchanges(self):
        for exchange_id in self.orderbook_config.exchanges:
            if exchange_id not in self.api_configs:
                raise ValueError(f"No API configuration found for exchange: {exchange_id}")

            config = self.api_configs[exchange_id]
            exchange_class = getattr(ccxt, exchange_id)

            self.exchanges[exchange_id] = exchange_class({
                'apiKey': config.api_key,
                'secret': config.secret,
                'password': config.password,
                'enableRateLimit': True,
            })

            is_sandbox = self.orderbook_config.sandbox_mode.get(exchange_id, False)
            self.exchanges[exchange_id].set_sandbox_mode(is_sandbox)

    @catch_exception
    async def update_orderbook(self, orderbook: Dict):
        self.latest_orderbook = orderbook[self.symbol]

    @catch_exception
    async def execute_order(self, order: OrderConfig) -> Dict:
        if not self.latest_orderbook:
            raise ValueError("No orderbook data available")

        execution_plan = self.create_execution_plan(order)
        execution_results = []
        remaining_amount = order.amount
        total_filled_amount = 0
        start_time = time.time()

        for exchange_id, amount, price in execution_plan:
            try:
                exchange = self.exchanges[exchange_id]
                params = {}
                if order.type == 'limit':
                    params['timeInForce'] = order.time_in_force

                executed_order = await exchange.createOrder(
                    self.symbol,
                    order.type,
                    order.side,
                    amount,
                    price if order.type == 'limit' else None,
                    params
                )

                filled_amount = executed_order.get('filled', 0)
                if filled_amount is None:
                    filled_amount = 0
                    logger.warning(f"Filled amount is None for order on {exchange_id}. Using 0 as default.")

                total_filled_amount += filled_amount
                remaining_amount -= filled_amount

                execution_results.append({
                    "exchange": exchange_id,
                    "order": executed_order,
                    "status": "success",
                    "planned_amount": amount,
                    "filled_amount": filled_amount,
                    "planned_price": price,
                    "actual_price": executed_order.get('price'),
                })

            except Exception as e:
                logger.error(f"Error executing order on {exchange_id}: {str(e)}")
                execution_results.append({
                    "exchange": exchange_id,
                    "error": str(e),
                    "status": "failed",
                    "planned_amount": amount,
                    "planned_price": price
                })

        total_time = time.time() - start_time

        return {
            "status": "completed" if remaining_amount <= 1e-8 else "partially_filled",
            "original_amount": order.amount,
            "filled_amount": total_filled_amount,
            "remaining_amount": remaining_amount,
            "execution_results": execution_results,
            "execution_plan": execution_plan,
            "total_execution_time": total_time * 1000,  # Convert to milliseconds
        }

    @catch_exception
    def create_execution_plan(self, order: OrderConfig) -> List[tuple]:
        execution_plan = []
        remaining_amount = order.amount
        book_side = self.latest_orderbook['bids'] if order.side == 'sell' else self.latest_orderbook['asks']

        for price, size, exchange in book_side:
            if remaining_amount <= 0:
                break
            executable_amount = min(remaining_amount, size)
            execution_plan.append((exchange, executable_amount, price))
            remaining_amount -= executable_amount

        return execution_plan

    @catch_exception
    async def close(self):
        await asyncio.gather(*[
            exchange.close()
            for exchange in self.exchanges.values()
        ], return_exceptions=True)
