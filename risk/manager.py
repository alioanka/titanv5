# risk/manager.py

from config import *
from telegram.bot import send_alert

def calculate_position_size(balance, candles, signal, symbol):
    atr_value = signal['atr']
    if atr_value == 0:
        return 0, 0, 0, 1

    max_loss = balance * MAX_RISK_PER_TRADE
    sl_distance = atr_value * SL_MULTIPLIER
    raw_size = max_loss / sl_distance

    # Final leverage
    leverage = 1
    if DYNAMIC_LEVERAGE:
        leverage = min(int((TP_MULTIPLIER / SL_MULTIPLIER) * 2), 10)

    # ✅ Cap size so cost doesn't exceed margin
    current_price = candles[-1]['close']
    max_allowed_qty = (balance * leverage) / current_price
    capped_size = min(raw_size * leverage, max_allowed_qty * 0.90)

    # ✅ Enforce 0.001 min size, rounded to 3 digits
    final_qty = max(round(capped_size, 3), 0.001)

    # SL/TP
    if signal['side'] == "LONG":
        sl = current_price - sl_distance
        tp = current_price + (atr_value * TP_MULTIPLIER)
    else:
        sl = current_price + sl_distance
        tp = current_price - (atr_value * TP_MULTIPLIER)

    print(f"💡 Final qty: {final_qty}, Max allowed: {max_allowed_qty:.3f}, Price: {current_price}, Leverage: {leverage}")


    return final_qty, round(sl, 2), round(tp, 2), leverage



def place_trade(exchange, symbol, side, qty, sl, tp, leverage):
    try:
        return exchange.place_order(symbol, side, qty, sl, tp, leverage)
    except Exception as e:
        send_alert(f"❌ Trade Failed: {symbol} {side} - {str(e)}")
        return {"success": False}
