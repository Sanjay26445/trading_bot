import argparse
import sys
from advanced import (
    BinanceClient, 
    place_limit_order, 
    validate_symbol, 
    validate_side, 
    validate_quantity,
    validate_price,
    get_logger,
    log_exception
)

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol')
    parser.add_argument('side', choices=['BUY', 'SELL'])
    parser.add_argument('quantity', type=float)
    parser.add_argument('price', type=float)
    
    args = parser.parse_args()
    
    try:
        validate_symbol(args.symbol)
        validate_side(args.side)
        validate_quantity(args.quantity)
        validate_price(args.price)
        
        logger.info(f"Limit order request: {args.symbol} {args.side} {args.quantity} @ {args.price}")
        
        client = BinanceClient()
        response = place_limit_order(client, args.symbol, args.side, args.quantity, args.price)
        
        logger.info(f"Limit order response: orderId={response.get('orderId')}, status={response.get('status')}, executedQty={response.get('executedQty')}")
        
        print(f"Order ID: {response.get('orderId')}")
        print(f"Status: {response.get('status')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        
        avg_price = response.get('avgPrice')
        if avg_price and str(avg_price) != '0':
            print(f"Avg Price: {avg_price}")
        
    except ValueError as e:
        logger.error(f"Validation failed: {e}")
        print(f"Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        log_exception(logger, "Limit order failed")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()