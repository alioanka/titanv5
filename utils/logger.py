# utils/logger.py

import csv
import os
import time
from config import TRADE_LOG_PATH, BALANCE_LOG_PATH

def log_trade(symbol, side, qty, sl, tp, entry_price, balance):
    row = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol,
        "side": side,
        "qty": qty,
        "entry_price": entry_price,
        "sl": sl,
        "tp": tp,
        "balance_before": balance
    }
    _write_row(TRADE_LOG_PATH, row, header=[
        "timestamp", "symbol", "side", "qty", "entry_price", "sl", "tp", "balance_before"
    ])

def log_balance(balance):
    row = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "balance": balance
    }
    _write_row(BALANCE_LOG_PATH, row, header=["timestamp", "balance"])

def _write_row(file_path, row, header):
    new_file = not os.path.exists(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if new_file:
            writer.writeheader()
        writer.writerow(row)
