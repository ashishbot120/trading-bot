# 🤖 Binance Futures Testnet Trading Bot

A simple, robust trading bot built for the **Binance Futures USDT-M Testnet**. Place MARKET and LIMIT orders via a clean CLI — with optional Streamlit web UI as a bonus.

---

## 🚀 Features

- **Order Types:** MARKET and LIMIT orders on the Binance Futures Testnet
- **Trade Sides:** Supports BUY (Long) and SELL (Short) positions
- **CLI Interface:** Easy-to-use command-line interface powered by `argparse`
- **Strict Validation:** Robust input validation for symbols, sides, order types, quantities, and pricing
- **Modular Design:** Structured and maintainable codebase
- **Comprehensive Logging:** Tracks all API requests, responses, and errors
- **Error Handling:** Graceful failure management for invalid inputs and API rate limits
- ⭐ **Bonus:** Lightweight web UI built with Streamlit for a visual trading experience

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Core programming language |
| Requests | REST API calls to Binance |
| python-dotenv | Secure environment variable management |
| Streamlit | Optional web-based user interface |

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── client.py          # Binance API wrapper (handles request signing)
│   ├── orders.py          # Core order placement logic
│   ├── validators.py      # Input validation logic
│   ├── logging_config.py  # Centralized logging setup
│   └── symbol_info.py     # Handles Binance symbol precision & step size rules
├── logs/                  # Directory containing runtime logs
├── cli.py                 # Command-line interface entry point
├── ui.py                  # Optional Streamlit web interface
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd trading_bot
```

### 2. Create and Activate a Virtual Environment

```bash
# Create the virtual environment
python -m venv .venv

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activate on Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file from the provided template:

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Open the `.env` file and fill in your Binance Futures Testnet credentials:

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

---

## 💻 How to Run

### Using the CLI (Required)

Place a **MARKET** order:

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

Place a **LIMIT** order:

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 65000
```

> **📝 Note for Limit Orders:**
> - **BUY:** Set the price *below* the current market price
> - **SELL:** Set the price *above* the current market price

### Using the Web UI (Optional Bonus)

```bash
streamlit run ui.py
```

This opens a browser-based dashboard where you can enter order details and execute trades visually.

---

## 📜 Logging

All API requests, execution responses, and system errors are logged for debugging and auditing.

| Log File | Description |
|---|---|
| `logs/bot.log` | Main runtime log |
| `logs/market_order.log` | Sample market order logs |
| `logs/limit_order.log` | Sample limit order logs |

---

## 📌 Assumptions

- The bot is strictly configured for the **Binance Futures Testnet (USDT-M)**. Do **not** use mainnet keys without changing the base URL.
- Provided API keys must have **Futures Trading** permissions enabled.
- Quantity and price inputs are automatically normalized by the bot to match Binance's precision and tick size rules.
- Users should provide valid, tradable ticker symbols (e.g., `BTCUSDT`, `ETHUSDT`).