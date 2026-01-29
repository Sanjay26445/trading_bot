import argparse
import sys
from bot.client import BinanceClient
from bot.orders import place_market_order, place_limit_order
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.logging_config import get_logger, log_exception

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Binance Futures Testnet Trading Bot')
    parser.add_argument('--symbol', required=True, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--type', required=True, choices=['MARKET', 'LIMIT'], help='Order type')
    parser.add_argument('--quantity', required=True, type=float, help='Order quantity')
    parser.add_argument('--price', type=float, help='Order price (required for LIMIT orders)')
    
    args = parser.parse_args()
    
    try:
        validate_symbol(args.symbol)
        validate_side(args.side)
        validate_order_type(args.type)
        validate_quantity(args.quantity)
        validate_price(args.price, args.type)
        
        logger.info(f"Order request: symbol={args.symbol}, side={args.side}, type={args.type}, quantity={args.quantity}" + 
                   (f", price={args.price}" if args.price else ""))
        
        print("Order Request Summary:")
        print(f"  Symbol: {args.symbol}")
        print(f"  Side: {args.side}")
        print(f"  Type: {args.type}")
        print(f"  Quantity: {args.quantity}")
        if args.price:
            print(f"  Price: {args.price}")
        print()
        
        try:
            client = BinanceClient()
            logger.info("Binance client initialized successfully")
        except ValueError as e:
            logger.error(f"Client initialization failed: {e}")
            print(f"✗ Client initialization failed: {e}")
            sys.exit(1)
        except Exception as e:
            log_exception(logger, "Unexpected error during client initialization")
            print(f"✗ Unexpected error: {e}")
            sys.exit(1)
        
        try:
            if args.type == 'MARKET':
                logger.info(f"Placing market order: {args.symbol} {args.side} {args.quantity}")
                response = place_market_order(client, args.symbol, args.side, args.quantity)
            else:
                logger.info(f"Placing limit order: {args.symbol} {args.side} {args.quantity} @ {args.price}")
                response = place_limit_order(client, args.symbol, args.side, args.quantity, args.price)
            
            logger.info(f"Order placed successfully. Response: orderId={response.get('orderId')}, status={response.get('status')}, executedQty={response.get('executedQty')}, avgPrice={response.get('avgPrice', '0.00')}")
            
            print("Order Response:")
            print(f"  Order ID: {response.get('orderId', 'N/A')}")
            print(f"  Status: {response.get('status', 'N/A')}")
            print(f"  Executed Qty: {response.get('executedQty', 'N/A')}")
            
            avg_price = response.get('avgPrice')
            if avg_price and str(avg_price) != '0' and str(avg_price) != '0.00':
                print(f"  Avg Price: {avg_price}")
            
            print()
            print("✓ Order placed successfully")
            
        except Exception as e:
            log_exception(logger, "Order placement failed")
            print(f"✗ Order failed: {e}")
            sys.exit(1)
            
    except ValueError as e:
        logger.error(f"Input validation failed: {e}")
        print(f"✗ Invalid input: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\n✗ Operation cancelled")
        sys.exit(1)
        
    except Exception as e:
        log_exception(logger, "Unexpected error in main")
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()