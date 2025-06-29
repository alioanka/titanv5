# exchange/bybit.py

import requests
import time
import hmac
import hashlib

class BybitFutures:
    def __init__(self, testnet=True):
        self.api_key = "x8kcsHYirixoBKCJpb"
        self.api_secret = "V6M8daqATSvaUAnxl4WuD75uX4NMsq4fseB1"
        self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"

    def _headers(self):
        return {"X-BAPI-API-KEY": self.api_key}

    def get_ohlcv(self, symbol, timeframe="1h", limit=100):
        # ✅ MOCK OHLCV GENERATOR (1-hour candles)
        now = int(time.time() * 1000)
        candles = []

        for i in range(limit):
            base = 30000 + (i * 10)  # Simulate a rising trend
            candles.append({
                "timestamp": now - ((limit - i) * 3600 * 1000),  # backdate each candle
                "open": base,
                "high": base + 50,
                "low": base - 50,
                "close": base + 25,
                "volume": 100 + i * 2
            })

        return candles




    def get_balance(self):
        # Simulated for now — replace with real call in prod
        return 5000.0

    def get_open_positions(self):
        # Simulated — can connect to Bybit `/position` endpoint
        return []

    def place_order(self, symbol, side, qty, sl, tp, leverage):
        print(f"📤 Placing {side} on {symbol} | Qty: {qty} | SL: {sl} | TP: {tp}")
        entry_price = self._mock_price(symbol)
        return {
            "success": True,
            "entry_price": entry_price,
            "symbol": symbol
        }

    def _mock_price(self, symbol):
        # Simulate a price for dev
        return 10000.0 + hash(symbol) % 1000
