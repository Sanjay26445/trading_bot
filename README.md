# Binance Futures Testnet Trading Bot

A Python trading bot for placing orders on Binance Futures USDT-M Testnet.

## Project Overview

This trading bot provides both CLI and optional web UI interfaces for placing MARKET and LIMIT orders on Binance Futures Testnet. It focuses on order placement functionality with proper validation, logging, and error handling.

## Setup Steps

### 1. Python Version
Requires Python 3.7+

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Set your Binance Testnet API credentials:

**Windows:**
```cmd
set BINANCE_API_KEY=your_testnet_api_key
set BINANCE_API_SECRET=your_testnet_secret_key
```

**Linux/Mac:**
```bash
export BINANCE_API_KEY="your_testnet_api_key"
export BINANCE_API_SECRET="your_testnet_secret_key"
```

## How to Run

### CLI (Primary Interface)

**MARKET Order Example:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**LIMIT Order Example:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 85000
```

### UI (Optional)

**Run Streamlit UI:**
```bash
streamlit run ui.py
```

Access at http://localhost:8501

## Assumptions

- **Futures Testnet Only**: Uses Binance Futures Testnet environment
- **USDT-M Contracts**: Designed for USDT-Margined futures contracts  
- **No Strategy Logic**: Pure order placement tool without trading algorithms
- **Manual Execution**: Each order requires manual execution
- **Minimum Order Size**: Orders must meet Binance minimum notional value requirements (~100 USDT)

## Getting Testnet Credentials

1. Visit https://testnet.binancefuture.com/
2. Create account or login
3. Go to API Management
4. Create new API key pair
5. Use these credentials with the bot