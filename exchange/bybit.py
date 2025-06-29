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
        endpoint = f"/v5/market/kline"
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": timeframe,
            "limit": limit
        }
        res = requests.get(self.base_url + endpoint, params=params)
        data = res.json()

        # ✅ SAFETY CHECK
        if data["retCode"] != 0:
            raise Exception(f"Failed OHLCV fetch: {data['retMsg']}")

        # ✅ RETURN CLEANED CANDLE DATA
        return [
            {
                "timestamp": int(c[0]),
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
                "volume": float(c[5])
            }
            for c in data["result"]["list"]
        ]


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
