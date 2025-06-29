# risk/manager.py

from config import *
from telegram.bot import send_alert

def calculate_position_size(balance, candles, signal, symbol):
    atr_value = signal['atr']
    if atr_value == 0:
        return 0, 0, 0, 1  # Safety fallback

    # === Risk per trade ===
    max_loss = balance * MAX_RISK_PER_TRADE

    # === Raw position size based on ATR stop ===
    sl_distance = atr_value * SL_MULTIPLIER
    position_size = max_loss / sl_distance

    # === Adaptive leverage ===
    leverage = 1
    if DYNAMIC_LEVERAGE:
        leverage = min(int((TP_MULTIPLIER / SL_MULTIPLIER) * 2), 10)

    position_size *= leverage

    # After position_size *= leverage:
    max_qty = (balance * leverage) / candles[-1]["close"]
    position_size = min(position_size, max_qty * 0.95)  # 95% buffer


    # === Final SL/TP levels ===
    last_close = candles[-1]['close']
    if signal['side'] == "LONG":
        sl = last_close - sl_distance
        tp = last_close + (atr_value * TP_MULTIPLIER)
    else:
        sl = last_close + sl_distance
        tp = last_close - (atr_value * TP_MULTIPLIER)

    print(f"DEBUG → close: {last_close}, sl: {sl}, tp: {tp}, atr: {atr_value}")


    position_size = max(round(position_size, 3), 0.001)
    return position_size, round(sl, 2), round(tp, 2), leverage


def place_trade(exchange, symbol, side, qty, sl, tp, leverage):
    try:
        return exchange.place_order(symbol, side, qty, sl, tp, leverage)
    except Exception as e:
        send_alert(f"❌ Trade Failed: {symbol} {side} - {str(e)}")
        return {"success": False}
