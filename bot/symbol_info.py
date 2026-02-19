import math
from functools import lru_cache
from typing import Dict, Any

from .client import BinanceFuturesTestnetClient


def _to_float(x: str) -> float:
    return float(x)


def _decimals_from_step(step: float) -> int:
    # step like 0.001 -> 3 decimals
    s = f"{step:.18f}".rstrip("0")
    if "." not in s:
        return 0
    return len(s.split(".")[1])


def _floor_to_step(value: float, step: float) -> float:
    if step <= 0:
        return value
    return math.floor(value / step) * step


@lru_cache(maxsize=256)
def get_symbol_filters_cached(base_url: str, api_key: str, api_secret: str, symbol: str) -> Dict[str, Any]:
    client = BinanceFuturesTestnetClient(api_key=api_key, api_secret=api_secret, base_url=base_url)
    info = client.get_exchange_info()
    for s in info.get("symbols", []):
        if s.get("symbol") == symbol:
            filters = {f["filterType"]: f for f in s.get("filters", [])}
            return {
                "price_tick": _to_float(filters["PRICE_FILTER"]["tickSize"]),
                "qty_step": _to_float(filters["LOT_SIZE"]["stepSize"]),
                "min_qty": _to_float(filters["LOT_SIZE"]["minQty"]),
                "max_qty": _to_float(filters["LOT_SIZE"]["maxQty"]),
                "min_price": _to_float(filters["PRICE_FILTER"]["minPrice"]),
                "max_price": _to_float(filters["PRICE_FILTER"]["maxPrice"]),
            }
    raise ValueError(f"Symbol not found in exchangeInfo: {symbol}")


def normalize_order(symbol_filters: Dict[str, Any], quantity: float, price: float | None):
    qty_step = symbol_filters["qty_step"]
    price_tick = symbol_filters["price_tick"]

    qty_norm = _floor_to_step(quantity, qty_step)
    qty_decimals = _decimals_from_step(qty_step)
    qty_norm = round(qty_norm, qty_decimals)

    price_norm = None
    if price is not None:
        price_norm = _floor_to_step(price, price_tick)
        price_decimals = _decimals_from_step(price_tick)
        price_norm = round(price_norm, price_decimals)

    if qty_norm <= 0:
        raise ValueError(f"Quantity too small after rounding. Step size={qty_step}")

    return qty_norm, price_norm
