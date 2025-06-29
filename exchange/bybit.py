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
        # Choose correct category based on symbol suffix
        category = "linear" if symbol.endswith("USDT") else "inverse"

        endpoint = "/v5/market/kline"
        params = {
            "category": category,
            "symbol": symbol,
            "interval": timeframe,
            "limit": limit
        }

        try:
            res = requests.get(self.base_url + endpoint, params=params)
            data = res.json()

            if data["retCode"] != 0 or "result" not in data or not data["result"]["list"]:
                print(f"⚠️ No data returned for {symbol}: {data}")
                return []

            # Clean and return formatted candle data
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

        except Exception as e:
            print(f"❌ Error fetching OHLCV for {symbol}: {e}")
            return []



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
