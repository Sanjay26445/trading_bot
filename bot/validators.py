from typing import Union, Optional


def validate_symbol(symbol):
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string")
    
    if not symbol:
        raise ValueError("Symbol cannot be empty")


def validate_side(side):
    if not isinstance(side, str):
        raise ValueError("Side must be a string")
    
    if side.upper() not in ['BUY', 'SELL']:
        raise ValueError("Side must be 'BUY' or 'SELL'")


def validate_order_type(order_type):
    if not isinstance(order_type, str):
        raise ValueError("Order type must be a string")
    
    if order_type.upper() not in ['MARKET', 'LIMIT']:
        raise ValueError("Order type must be 'MARKET' or 'LIMIT'")


def validate_quantity(quantity):
    if not isinstance(quantity, (int, float)):
        raise ValueError("Quantity must be a number")
    
    if quantity <= 0:
        raise ValueError("Quantity must be positive")


def validate_price(price, order_type):
    if order_type.upper() == 'LIMIT':
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        
        if price <= 0:
            raise ValueError("Price must be positive")