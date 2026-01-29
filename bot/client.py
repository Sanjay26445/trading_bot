import os
import logging
from binance.client import Client

logger = logging.getLogger(__name__)


class BinanceClient:
    def __init__(self):
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            raise ValueError("Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables")
        
        self.client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=True
        )
        
        self.client.API_URL = 'https://testnet.binancefuture.com'
        logger.info("Binance Futures Testnet client initialized")
    
    def get_client(self):
        return self.client