import os
import logging
import traceback
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

_logger_initialized = False


def setup_logging():
    global _logger_initialized
    
    if _logger_initialized:
        return
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    if not root_logger.handlers:
        file_handler = logging.FileHandler('bot.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    _logger_initialized = True


def get_logger(name):
    setup_logging()
    return logging.getLogger(name)


def log_exception(logger, message):
    logger.error(f"{message}: {traceback.format_exc()}")


class BinanceClient:
    def __init__(self):
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            raise ValueError("Missing API credentials")
        
        self.client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
        self.client.API_URL = 'https://testnet.binancefuture.com'
        
        logger = get_logger(__name__)
        logger.info("Binance client initialized")
    
    def get_client(self):
        return self.client


def validate_symbol(symbol):
    if not isinstance(symbol, str) or not symbol:
        raise ValueError("Invalid symbol")


def validate_side(side):
    if side.upper() not in ['BUY', 'SELL']:
        raise ValueError("Side must be BUY or SELL")


def validate_quantity(quantity):
    if not isinstance(quantity, (int, float)) or quantity <= 0:
        raise ValueError("Quantity must be positive")


def validate_price(price):
    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError("Price must be positive")


def place_market_order(client, symbol, side, quantity):
    try:
        return client.get_client().futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
    except (BinanceAPIException, BinanceOrderException) as e:
        raise Exception(f"Market order failed: {e}")


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
        raise Exception(f"Limit order failed: {e}")