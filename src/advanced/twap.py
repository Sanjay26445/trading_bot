import argparse
import sys
import time
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from advanced import (
    BinanceClient,
    place_market_order,
    validate_symbol,
    validate_side,
    validate_quantity,
    get_logger,
    log_exception
)

logger = get_logger(__name__)


def execute_twap(symbol, side, total_quantity, chunks, interval_seconds):
    chunk_size = total_quantity / chunks
    client = BinanceClient()
    
    orders_placed = 0
    total_executed = 0.0
    
    logger.info(f"TWAP execution started: {symbol} {side} {total_quantity} in {chunks} chunks every {interval_seconds}s")
    
    for i in range(chunks):
        try:
            logger.info(f"Placing TWAP chunk {i+1}/{chunks}: {chunk_size}")
            response = place_market_order(client, symbol, side, chunk_size)
            
            orders_placed += 1
            executed_qty = float(response.get('executedQty', 0))
            total_executed += executed_qty
            
            logger.info(f"TWAP chunk {i+1} executed: orderId={response.get('orderId')}, executedQty={executed_qty}")
            print(f"Chunk {i+1}: Order {response.get('orderId')} executed {executed_qty}")
            
            if i < chunks - 1:
                time.sleep(interval_seconds)
                
        except Exception as e:
            log_exception(logger, f"TWAP chunk {i+1} failed")
            print(f"Chunk {i+1} failed: {e}")
    
    logger.info(f"TWAP execution completed: {orders_placed} orders placed, {total_executed} total executed")
    return orders_placed, total_executed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol')
    parser.add_argument('side', choices=['BUY', 'SELL'])
    parser.add_argument('total_quantity', type=float)
    parser.add_argument('chunks', type=int)
    parser.add_argument('interval_seconds', type=int)
    
    args = parser.parse_args()
    
    try:
        validate_symbol(args.symbol)
        validate_side(args.side)
        validate_quantity(args.total_quantity)
        
        if args.chunks <= 0:
            raise ValueError("Chunks must be positive")
        if args.interval_seconds < 0:
            raise ValueError("Interval must be non-negative")
        
        orders_placed, total_executed = execute_twap(
            args.symbol, 
            args.side, 
            args.total_quantity, 
            args.chunks, 
            args.interval_seconds
        )
        
        print(f"TWAP completed: {orders_placed} orders, {total_executed} total executed")
        
    except ValueError as e:
        logger.error(f"TWAP validation failed: {e}")
        print(f"Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        log_exception(logger, "TWAP execution failed")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()