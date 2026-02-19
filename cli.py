import argparse
import os
from typing import Any, Dict

from dotenv import load_dotenv

from bot.client import BinanceFuturesTestnetClient
from bot.logging_config import setup_logging
from bot.orders import place_market_or_limit_order
from bot.validators import validate_inputs
from bot.symbol_info import get_symbol_filters_cached, normalize_order



def _print_order_summary(order_in) -> None:
    print("\n=== ORDER REQUEST SUMMARY ===")
    print(f"Symbol     : {order_in.symbol}")
    print(f"Side       : {order_in.side}")
    print(f"Type       : {order_in.order_type}")
    print(f"Quantity   : {order_in.quantity}")
    if order_in.order_type == "LIMIT":
        print(f"Price      : {order_in.price}")
    print("=============================\n")


def _print_order_response(data: Dict[str, Any]) -> None:
    print("=== ORDER RESPONSE ===")
    # Different responses may include different fields; print key ones if present
    for k in ["orderId", "status", "symbol", "side", "type", "executedQty", "avgPrice", "price"]:
        if k in data:
            print(f"{k:11}: {data.get(k)}")
    # Useful extra:
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
    logger = setup_logging("logs/bot.log")

    parser = build_parser()
    args = parser.parse_args()

    try:
        order_in = validate_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )
        symbol_filters = get_symbol_filters_cached(
            base_url=base_url,
            api_key=api_key,
            api_secret=api_secret,
            symbol=order_in.symbol
        )

        qty_norm, price_norm = normalize_order(symbol_filters, order_in.quantity, order_in.price)

        logger.info(f"Normalized qty/price: qty={qty_norm}, price={price_norm} (filters={symbol_filters})")


        _print_order_summary(order_in)

        api_key = os.getenv("BINANCE_API_KEY", "")
        api_secret = os.getenv("BINANCE_API_SECRET", "")
        base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

        client = BinanceFuturesTestnetClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
        )

        logger.info(f"Placing order: {order_in}")
        resp = place_market_or_limit_order(
            client=client,
            symbol=order_in.symbol,
            side=order_in.side,
            order_type=order_in.order_type,
            quantity=qty_norm,
            price=price_norm,
        )
        logger.info(f"Order response: {resp}")

        _print_order_response(resp)
        print("✅ SUCCESS: Order placed successfully.\n")

    except Exception as e:
        logger.exception(f"❌ FAILED: {e}")
        print("\n❌ FAILED:", str(e))
        print("Check logs/bot.log for details.\n")


if __name__ == "__main__":
    main()
