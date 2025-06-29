# main.py

import time
from config import *
from exchange.bybit import BybitFutures
from strategy.core import generate_signal
from risk.manager import calculate_position_size, place_trade
from utils.logger import log_trade, log_balance
from telegram.bot import send_alert

print(f"🚀 Starting {BOT_NAME} on {EXCHANGE.upper()} - Mode: {MODE} | Testnet: {USE_TESTNET}")
send_alert(f"🚀 Starting {BOT_NAME} on {EXCHANGE.upper()} - Mode: {MODE} | Testnet: {USE_TESTNET}")

# Initialize exchange interface
exchange = BybitFutures(testnet=USE_TESTNET)

def run_bot():
    while True:
        try:
            balance = exchange.get_balance()
            log_balance(balance)

            open_positions = exchange.get_open_positions()
            active_symbols = set([pos['symbol'] for pos in open_positions])

            for symbol in SYMBOLS:
                if symbol in active_symbols:
                    continue  # Skip if already in a trade

                data = exchange.get_ohlcv(symbol, TIMEFRAME)

                # 🛡️ Add this line right here:
                if not data or 'close' not in data[-1]:
                    print(f"⚠️ Skipping {symbol}: invalid OHLCV data → {data}")
                    continue
                signal = generate_signal(data)

                if signal is None:
                    continue  # No valid signal

                position_size, sl, tp, leverage = calculate_position_size(
                    balance, data, signal, symbol
                )

                if position_size <= 0:
                    continue  # Risk limit reached

                order_result = place_trade(
                    exchange=exchange,
                    symbol=symbol,
                    side=signal['side'],
                    qty=position_size,
                    sl=sl,
                    tp=tp,
                    leverage=leverage
                )

                if order_result['success']:
                    log_trade(symbol, signal['side'], position_size, sl, tp, order_result['entry_price'], balance)
                    send_alert(f"🚀 New {signal['side']} Position\n{symbol} @ {order_result['entry_price']}\nSL: {sl} | TP: {tp}\nLeverage: {leverage}x")

        except Exception as e:
            print(f"❌ Error in bot loop: {e}")
            send_alert(f"⚠️ Bot Error: {str(e)}")

        time.sleep(60)  # Run every minute

if __name__ == "__main__":
    run_bot()
