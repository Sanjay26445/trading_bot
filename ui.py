import streamlit as st
import sys
import os
sys.path.append('src')

from advanced import (
    BinanceClient,
    place_market_order,
    place_limit_order,
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
    get_logger,
    log_exception
)

logger = get_logger(__name__)

st.title("Trading Bot")

if 'order_response' not in st.session_state:
    st.session_state.order_response = None
if 'order_error' not in st.session_state:
    st.session_state.order_error = None

with st.form("order_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        symbol = st.text_input("Symbol", value="BTCUSDT")
        side = st.selectbox("Side", ["BUY", "SELL"])
        
    with col2:
        order_type = st.selectbox("Type", ["MARKET", "LIMIT"])
        quantity = st.number_input("Quantity", min_value=0.0, value=0.01, step=0.001, format="%.6f")
    
    price = None
    if order_type == "LIMIT":
        price = st.number_input("Price", min_value=0.0, value=85000.0, step=100.0, format="%.2f")
    
    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        st.session_state.order_response = None
        st.session_state.order_error = None
        
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(quantity)
        if order_type == "LIMIT":
            validate_price(price)
        
        logger.info(f"UI {order_type} order request: {symbol} {side} {quantity}" + 
                   (f" @ {price}" if price else ""))
        
        client = BinanceClient()
        
        if order_type == 'MARKET':
            response = place_market_order(client, symbol, side, quantity)
        else:
            response = place_limit_order(client, symbol, side, quantity, price)
        
        logger.info(f"UI {order_type} order response: orderId={response.get('orderId')}, status={response.get('status')}")
        st.session_state.order_response = response
        
    except ValueError as e:
        logger.error(f"UI validation failed: {e}")
        st.session_state.order_error = str(e)
        
    except Exception as e:
        log_exception(logger, f"UI {order_type} order failed")
        st.session_state.order_error = str(e)

if st.session_state.order_response:
    response = st.session_state.order_response
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"Order ID: {response.get('orderId')}")
        st.write(f"Status: {response.get('status')}")
    
    with col2:
        st.write(f"Executed Qty: {response.get('executedQty')}")
        
        avg_price = response.get('avgPrice')
        if avg_price and str(avg_price) != '0':
            st.write(f"Avg Price: {avg_price}")

elif st.session_state.order_error:
    st.error(st.session_state.order_error)