# Binance Futures Testnet Trading Bot (Python)

This project is a simple trading bot built for the Binance Futures **USDT-M Testnet**.  
It allows users to place **MARKET** and **LIMIT** orders using a command-line interface, with proper validation, logging, and error handling.

The goal of this project is to demonstrate clean backend structure, API integration, and reliable order execution.

---

## Features

- Place **MARKET** and **LIMIT** orders on Binance Futures Testnet
- Supports both **BUY** and **SELL** sides
- CLI-based input using `argparse`
- Input validation (symbol, side, order type, quantity, price)
- Structured and modular code design
- Logging of all requests, responses, and errors
- Graceful error handling for invalid inputs and API failures

**Bonus:**
- Lightweight UI built with Streamlit for easier interaction

---

## Tech Stack

- Python 3
- Requests (REST API calls)
- python-dotenv (environment variables)
- Streamlit (optional UI)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd trading_bot
2. Create and activate virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Mac/Linux
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Setup environment variables
Create a .env file:

copy .env.example .env   # Windows
# OR
cp .env.example .env     # Mac/Linux
Update .env with your Binance Testnet credentials:

BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
BINANCE_BASE_URL=https://testnet.binancefuture.com


How to Run
Using CLI (Required)
MARKET order example
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
LIMIT order example
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 65000
Note:

BUY → set price below market

SELL → set price above market

Using UI (Optional Bonus)
streamlit run ui.py
This will open a browser-based interface to place orders.

Logging
All API requests, responses, and errors are logged in:

logs/bot.log
For submission, sample logs are provided:

logs/market_order.log

logs/limit_order.log

Project Structure
trading_bot/
  bot/
    client.py          # Binance API wrapper (request signing)
    orders.py          # Order placement logic
    validators.py      # Input validation
    logging_config.py  # Logging setup
    symbol_info.py     # Precision handling
  cli.py               # CLI entry point
  ui.py                # Optional UI
  requirements.txt
  README.md
Assumptions
Uses Binance Futures Testnet (USDT-M)

API keys are valid and have trading permissions

Quantity and price are normalized to match Binance precision rules

Users provide valid symbols (e.g., BTCUSDT)