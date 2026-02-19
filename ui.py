# ui.py  (FINAL — with mark price, smart limit defaults, normalized summary, and cleaner logging)

import os
import streamlit as st
from dotenv import load_dotenv

from bot.client import BinanceFuturesTestnetClient
from bot.logging_config import setup_logging
from bot.orders import place_market_or_limit_order
from bot.validators import validate_inputs
from bot.symbol_info import get_symbol_filters_cached, normalize_order

load_dotenv()
logger = setup_logging("logs/bot.log")

st.set_page_config(page_title="Binance Futures Testnet Bot", page_icon="📈", layout="centered")

st.title("📈 Binance Futures Testnet Trading Bot (Simple UI)")
st.caption("Places MARKET/LIMIT orders on USDT-M Futures Testnet with validation + logging.")

# --- API Config ---
api_key = os.getenv("BINANCE_API_KEY", "")
api_secret = os.getenv("BINANCE_API_SECRET", "")
base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

with st.expander("⚙️ Connection Settings", expanded=False):
    st.write("Base URL:", base_url)
    st.write("API Key loaded:", "✅ Yes" if api_key else "❌ No")
    st.write("API Secret loaded:", "✅ Yes" if api_secret else "❌ No")
    st.info("Tip: Create a .env file from .env.example and add your keys.")

st.divider()

# --- UI Inputs ---
col1, col2 = st.columns(2)
with col1:
    symbol = st.text_input("Symbol", value="BTCUSDT").strip().upper()
    side = st.selectbox("Side", ["BUY", "SELL"])
with col2:
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
    quantity = st.number_input("Quantity", min_value=0.0, value=0.01, step=0.01)

# --- Show Mark Price + smart default for LIMIT ---
mark_price = None
if symbol and api_key and api_secret:
    try:
        tmp_client = BinanceFuturesTestnetClient(api_key, api_secret, base_url)
        mp = tmp_client.get_mark_price(symbol)  # requires get_mark_price() method in client.py
        mark_price = float(mp.get("markPrice", 0.0))
        if mark_price > 0:
            st.write(f"📌 Current Mark Price: **{mark_price:.2f}**")
    except Exception:
        st.warning("Could not fetch mark price (check symbol / network / API keys).")

price = None
if order_type == "LIMIT":
    default_price = 60000.0
    if mark_price and mark_price > 0:
        # Good practical defaults: BUY below mark, SELL above mark
        default_price = (mark_price * 0.99) if side == "BUY" else (mark_price * 1.01)

    price = st.number_input(
        "Price (required for LIMIT)",
        min_value=0.0,
        value=float(default_price),
        step=10.0
    )

st.divider()

# --- Action ---
if st.button("🚀 Place Order", use_container_width=True):
    if not api_key or not api_secret:
        st.error("Missing API credentials. Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.")
        st.stop()

    try:
        # 1) Validate raw inputs
        order_in = validate_inputs(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=float(quantity),
            price=float(price) if price is not None else None,
        )

        # 2) Fetch filters + normalize qty/price to stepSize/tickSize
        symbol_filters = get_symbol_filters_cached(
            base_url=base_url,
            api_key=api_key,
            api_secret=api_secret,
            symbol=order_in.symbol
        )
        qty_norm, price_norm = normalize_order(symbol_filters, order_in.quantity, order_in.price)

        st.info(f"Normalized: quantity={qty_norm}, price={price_norm}")
        logger.info(f"[UI] Normalized qty/price: qty={qty_norm}, price={price_norm} (filters={symbol_filters})")

        # 3) Print request summary (normalized)
        st.subheader("✅ Order Request Summary (Normalized)")
        summary = {
            "symbol": order_in.symbol,
            "side": order_in.side,
            "type": order_in.order_type,
            "quantity": qty_norm,
            "price": price_norm,
        }
        st.json(summary)

        # 4) Place order
        client = BinanceFuturesTestnetClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
        )

        logger.info(
            f"[UI] Placing order: symbol={order_in.symbol}, side={order_in.side}, "
            f"type={order_in.order_type}, qty={qty_norm}, price={price_norm}"
        )

        resp = place_market_or_limit_order(
            client=client,
            symbol=order_in.symbol,
            side=order_in.side,
            order_type=order_in.order_type,
            quantity=qty_norm,
            price=price_norm,
        )

        logger.info(f"[UI] Order response: {resp}")

        # 5) Show response
        st.subheader("📩 Order Response")
        st.json(resp)

        key_fields = {
            "orderId": resp.get("orderId"),
            "status": resp.get("status"),
            "executedQty": resp.get("executedQty"),
            "avgPrice": resp.get("avgPrice"),
            "price": resp.get("price"),
        }
        st.subheader("🔎 Key Fields")
        st.json(key_fields)

        st.success("✅ Order placed successfully! Check logs/bot.log for full request/response logs.")

    except Exception as e:
        logger.exception(f"[UI] FAILED: {e}")
        st.error(f"❌ FAILED: {e}")

        # Helpful hint for common LIMIT constraint error
        msg = str(e)
        if "Limit price can't be lower than" in msg and order_type == "LIMIT":
            st.info("Tip: For LIMIT SELL, set price ABOVE mark price. For LIMIT BUY, set price BELOW mark price.")
        st.info("Check logs/bot.log for details.")
