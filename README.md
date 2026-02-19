Binance Futures Testnet Trading Bot (Python)

This project is a simple, robust trading bot built for the Binance Futures USDT-M Testnet. It allows users to place MARKET and LIMIT orders using a command-line interface, emphasizing proper validation, logging, and error handling.

The primary goal of this project is to demonstrate clean backend architecture, secure API integration, and reliable order execution.

🚀 Features

Order Types: Place MARKET and LIMIT orders on the Binance Futures Testnet.

Trade Sides: Supports both BUY (Long) and SELL (Short) positions.

CLI Interface: Easy-to-use command-line interface powered by argparse.

Strict Validation: Robust input validation for symbols, trade sides, order types, quantities, and pricing.

Modular Design: Structured and modular code for maintainability and scalability.

Comprehensive Logging: Tracks all API requests, responses, and errors.

Error Handling: Graceful failure management for invalid inputs and API rate limits/errors.

⭐ Bonus: Lightweight web UI built with Streamlit for a visual trading experience.

🛠️ Tech Stack

Python 3.x: Core programming language.

Requests: For making REST API calls to Binance.

python-dotenv: For secure environment variable management.

Streamlit: For the optional web-based user interface.

⚙️ Setup Instructions

Follow these steps to get the bot running on your local machine.

1. Clone the repository

git clone <your-repo-link>
cd trading_bot


2. Create and activate a virtual environment

# Create the virtual environment
python -m venv .venv

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activate on Mac/Linux
source .venv/bin/activate


3. Install dependencies

pip install -r requirements.txt


4. Setup environment variables

Create a .env file based on the provided example template:

# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env


Open the newly created .env file and update it with your Binance Futures Testnet credentials:

BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_BASE_URL=[https://testnet.binancefuture.com](https://testnet.binancefuture.com)


💻 How to Run

Using the CLI (Required)

You can place orders directly from your terminal using cli.py.

Place a MARKET Order:

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01


Place a LIMIT Order:

python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 65000


📝 Trading Note for Limit Orders:

BUY: Ensure you set the price below the current market price.

SELL: Ensure you set the price above the current market price.

Using the UI (Optional Bonus)

If you prefer a visual interface, you can launch the Streamlit dashboard:

streamlit run ui.py


This will open a browser-based application where you can enter order details and execute trades.

📜 Logging

All API requests, execution responses, and system errors are securely logged for debugging and auditing purposes.

Main Log File: logs/bot.log

Sample Logs (For reference):

logs/market_order.log

logs/limit_order.log

📁 Project Structure

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


📌 Assumptions

The bot is strictly configured to use the Binance Futures Testnet (USDT-M). Do not use this with mainnet keys without modifying the base URL.

Provided API keys are valid and have the necessary "Futures Trading" permissions enabled.

Quantity and price inputs will be properly normalized by the bot to match Binance's strict precision and tick size rules.

Users will provide valid, tradable ticker symbols (e.g., BTCUSDT, ETHUSDT).