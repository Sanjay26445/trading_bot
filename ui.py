import streamlit as st
from bot.client import BinanceClient
from bot.orders import place_market_order, place_limit_order
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.logging_config import get_logger, log_exception

logger = get_logger(__name__)

st.title("Binance Futures Trading Bot")

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
        order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
        quantity = st.number_input("Quantity", min_value=0.0, value=0.01, step=0.001, format="%.6f")
    
    price = None
    if order_type == "LIMIT":
        price = st.number_input("Price", min_value=0.0, value=85000.0, step=100.0, format="%.2f")
    
    submitted = st.form_submit_button("Place Order")

if submitted:
    try:
        st.session_state.order_response = None
        st.session_state.order_error = None
        
        validate_symbol(symbol)
        validate_side(side)
        validate_order_type(order_type)
        validate_quantity(quantity)
        validate_price(price, order_type)
        
        logger.info(f"UI Order request: symbol={symbol}, side={side}, type={order_type}, quantity={quantity}" + 
                   (f", price={price}" if price else ""))
        
        st.subheader("Order Request Summary")
        st.write(f"**Symbol:** {symbol}")
        st.write(f"**Side:** {side}")
        st.write(f"**Type:** {order_type}")
        st.write(f"**Quantity:** {quantity}")
        if price:
            st.write(f"**Price:** {price}")
        
        try:
            client = BinanceClient()
            logger.info("UI: Binance client initialized successfully")
        except ValueError as e:
            logger.error(f"UI: Client initialization failed: {e}")
            st.session_state.order_error = f"Client initialization failed: {e}"
            st.error(st.session_state.order_error)
            st.stop()
        except Exception as e:
            log_exception(logger, "UI: Unexpected error during client initialization")
            st.session_state.order_error = f"Unexpected error: {e}"
            st.error(st.session_state.order_error)
            st.stop()
        
        try:
            if order_type == 'MARKET':
                logger.info(f"UI: Placing market order: {symbol} {side} {quantity}")
                response = place_market_order(client, symbol, side, quantity)
            else:
                logger.info(f"UI: Placing limit order: {symbol} {side} {quantity} @ {price}")
                response = place_limit_order(client, symbol, side, quantity, price)
            
            logger.info(f"UI: Order placed successfully. Response: orderId={response.get('orderId')}, status={response.get('status')}, executedQty={response.get('executedQty')}, avgPrice={response.get('avgPrice', '0.00')}")
            st.session_state.order_response = response
            
        except Exception as e:
            log_exception(logger, "UI: Order placement failed")
            st.session_state.order_error = str(e)
            
    except ValueError as e:
        logger.error(f"UI: Input validation failed: {e}")
        st.session_state.order_error = f"Invalid input: {e}"
        
    except Exception as e:
        log_exception(logger, "UI: Unexpected error")
        st.session_state.order_error = f"Unexpected error: {e}"

if st.session_state.order_response:
    st.subheader("Order Response")
    response = st.session_state.order_response
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Order ID:** {response.get('orderId', 'N/A')}")
        st.write(f"**Status:** {response.get('status', 'N/A')}")
    
    with col2:
        st.write(f"**Executed Qty:** {response.get('executedQty', 'N/A')}")
        
        avg_price = response.get('avgPrice')
        if avg_price and str(avg_price) != '0' and str(avg_price) != '0.00':
            st.write(f"**Avg Price:** {avg_price}")
    
    st.success("✓ Order placed successfully")

elif st.session_state.order_error:
    st.subheader("Order Failed")
    st.error(f"✗ {st.session_state.order_error}")