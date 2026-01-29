# Binance Futures Trading Bot

Python trading bot for Binance USDT-M Futures Testnet with market orders, limit orders, and TWAP execution.

## Setup

### Requirements
Python 3.7+

### Installation
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```


### API Keys
Set environment variables:
```bash
export BINANCE_API_KEY="your_testnet_api_key"
export BINANCE_API_SECRET="your_testnet_secret_key"
```

Get testnet keys from https://testnet.binancefuture.com/

### Getting Testnet Credentials
Visit https://testnet.binancefuture.com/
Create account or login
Go to API Management
Create new API key pair
Use these credentials with the bot
### Market Orders
```bash
python src/market_orders.py BTCUSDT BUY 0.01
```

### Limit Orders
```bash
python src/limit_orders.py BTCUSDT SELL 0.01 30000
```

### TWAP Orders
```bash
python src/advanced/twap.py BTCUSDT BUY 0.1 5 10
```

### UI 
```bash
streamlit run ui.py
```

## Logging

All activity logged to `bot.log` at project root:
- Order requests and responses
- Execution results
- Errors with stack traces

## Assumptions

- Binance USDT-M Futures Testnet only
- Educational and demo purposes
- Manual execution required
- Minimum order sizes apply