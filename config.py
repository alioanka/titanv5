# config.py

### === GENERAL SETTINGS === ###
BOT_NAME = "TitanBot Reforged"
EXCHANGE = "bybit"  # "binance" for production later
MODE = "futures"    # or "spot" in the future
USE_TESTNET = True

### === SYMBOLS TO TRADE === ###
SYMBOLS = [
    "BTCUSDT"#,
#    "ETHUSDT",
#    "SOLUSDT",
#    "BNBUSDT",
#    "XRPUSDT"
]

### === RISK MANAGEMENT === ###
MAX_RISK_PER_TRADE = 0.03       # 3% of balance per trade
MAX_OPEN_POSITIONS = 3          # Limit concurrent trades
DYNAMIC_LEVERAGE = True         # Adjust leverage based on volatility/confidence

### === SL/TP SETTINGS (ATR-based) === ###
ATR_PERIOD = 14
TP_MULTIPLIER = 2.0             # Take Profit = 2x ATR
SL_MULTIPLIER = 1.0             # Stop Loss = 1x ATR
TRAILING_START = 1.5            # Start trailing after 1.5x ATR in profit
TRAILING_GAP = 0.5              # Trail by 0.5x ATR

### === STRATEGY SETTINGS === ###
MIN_TREND_STRENGTH = 0.6        # Only trade strong trends (0–1 score)
MIN_VOLATILITY = 0.005          # Minimum daily % movement to enter trade
TIMEFRAME = "1h"                # Chart timeframe for decision making

### === TELEGRAM BOT === ###
TELEGRAM_ENABLED = True
TELEGRAM_TOKEN = "7678357905:AAEe0MfHa4ZYhFnDhlUPL2oDaNXSoLo-YaM"
TELEGRAM_CHAT_ID = "462007586"

### === LOGGING === ###
TRADE_LOG_PATH = "logs/trade_log.csv"
BALANCE_LOG_PATH = "logs/balance_log.csv"
LOG_LEVEL = "INFO"
