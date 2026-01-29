from binance.exceptions import BinanceAPIException, BinanceOrderException
from .client import BinanceClient


def place_market_order(client, symbol, side, quantity):
    try:
        return client.get_client().futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
    except (BinanceAPIException, BinanceOrderException) as e:
        raise Exception(f"Failed to place market order: {e}")


def place_limit_order(client, symbol, side, quantity, price):
    try:
        return client.get_client().futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=price
        )
    except (BinanceAPIException, BinanceOrderException) as e:
        raise Exception(f"Failed to place limit order: {e}")