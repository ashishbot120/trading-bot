import argparse
import os
from typing import Any, Dict

from dotenv import load_dotenv

from bot.client import BinanceFuturesTestnetClient
from bot.logging_config import setup_logging
from bot.orders import place_market_or_limit_order
from bot.validators import validate_inputs
from bot.symbol_info import get_symbol_filters_cached, normalize_order


def _print_order_response(data: Dict[str, Any]) -> None:
    print("=== ORDER RESPONSE ===")
    for k in ["orderId", "status", "symbol", "side", "type", "executedQty", "avgPrice", "price"]:
        if k in data:
            print(f"{k:11}: {data.get(k)}")
    if "updateTime" in data:
        print(f"{'updateTime':11}: {data.get('updateTime')}")
    print("======================\n")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot (Market/Limit)")
    p.add_argument("--symbol", required=True, help="Trading symbol e.g. BTCUSDT")
    p.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    p.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order type")
    p.add_argument("--quantity", required=True, type=float, help="Order quantity (positive number)")
    p.add_argument("--price", type=float, default=None, help="Required for LIMIT orders")
    return p


def main():
    load_dotenv()

    # Main log (always)
    main_logger = setup_logging("logs/bot.log")

    parser = build_parser()
    args = parser.parse_args()

    try:
        # Load env
        api_key = os.getenv("BINANCE_API_KEY", "")
        api_secret = os.getenv("BINANCE_API_SECRET", "")
        base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

        # Validate inputs
        order_in = validate_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )

        # Select per-order log file (for submission deliverables)
        order_log_file = "logs/market_order.log" if order_in.order_type == "MARKET" else "logs/limit_order.log"

        # IMPORTANT: Use a unique logger name per file to avoid handler duplication
        order_logger = setup_logging(order_log_file)

        # Normalize quantity/price based on exchange filters
        symbol_filters = get_symbol_filters_cached(
            base_url=base_url,
            api_key=api_key,
            api_secret=api_secret,
            symbol=order_in.symbol,
        )
        qty_norm, price_norm = normalize_order(symbol_filters, order_in.quantity, order_in.price)

        # Print request summary (normalized)
        print("\n=== ORDER REQUEST SUMMARY (Normalized) ===")
        print(f"Symbol     : {order_in.symbol}")
        print(f"Side       : {order_in.side}")
        print(f"Type       : {order_in.order_type}")
        print(f"Quantity   : {qty_norm}")
        if order_in.order_type == "LIMIT":
            print(f"Price      : {price_norm}")
        print("=========================================\n")

        # Create API client
        client = BinanceFuturesTestnetClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
        )

        # Log request
        msg_req = (
            f"Placing order: symbol={order_in.symbol}, side={order_in.side}, "
            f"type={order_in.order_type}, qty={qty_norm}, price={price_norm}"
        )
        main_logger.info(msg_req)
        order_logger.info(msg_req)

        # Place order
        resp = place_market_or_limit_order(
            client=client,
            symbol=order_in.symbol,
            side=order_in.side,
            order_type=order_in.order_type,
            quantity=qty_norm,
            price=price_norm,
        )

        # Log response
        main_logger.info(f"Order response: {resp}")
        order_logger.info(f"Order response: {resp}")

        # Print response
        _print_order_response(resp)
        print("✅ SUCCESS: Order placed successfully.\n")

    except Exception as e:
        # Log errors to main log always
        main_logger.exception(f"❌ FAILED: {e}")

        # Also log to order-specific file if possible
        try:
            # If order_in exists, choose correct file; else fallback to bot.log only
            order_type = getattr(locals().get("order_in", None), "order_type", None)
            if order_type in ("MARKET", "LIMIT"):
                order_log_file = "logs/market_order.log" if order_type == "MARKET" else "logs/limit_order.log"
                setup_logging(order_log_file).exception(f"❌ FAILED: {e}")
        except Exception:
            pass

        print("\n❌ FAILED:", str(e))
        print("Check logs/bot.log for details.\n")


if __name__ == "__main__":
    main()
