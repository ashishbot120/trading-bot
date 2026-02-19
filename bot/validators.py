from dataclasses import dataclass


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


@dataclass(frozen=True)
class OrderInput:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: float | None


def _is_valid_symbol(symbol: str) -> bool:
    # Simple format check: uppercase alphanumerics, common like BTCUSDT
    return symbol.isalnum() and symbol.upper() == symbol and 6 <= len(symbol) <= 20


def validate_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
) -> OrderInput:
    symbol = (symbol or "").strip().upper()
    side = (side or "").strip().upper()
    order_type = (order_type or "").strip().upper()

    if not _is_valid_symbol(symbol):
        raise ValueError("Invalid symbol. Example: BTCUSDT")

    if side not in VALID_SIDES:
        raise ValueError("Invalid side. Must be BUY or SELL.")

    if order_type not in VALID_ORDER_TYPES:
        raise ValueError("Invalid order type. Must be MARKET or LIMIT.")

    if quantity is None or quantity <= 0:
        raise ValueError("Invalid quantity. Must be > 0.")

    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price is required for LIMIT orders and must be > 0.")
    else:
        # MARKET: ignore any provided price
        price = None

    return OrderInput(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=float(quantity),
        price=float(price) if price is not None else None,
    )
