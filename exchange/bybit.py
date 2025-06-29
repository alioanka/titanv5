# exchange/bybit.py

import requests
import time
import hmac
import hashlib
import uuid

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
        endpoint = "/v5/order/create"
        url = self.base_url + endpoint
        order_id = str(uuid.uuid4())[:18]

        side_bybit = "Buy" if side == "LONG" else "Sell"

        payload = {
            "category": "linear",
            "symbol": symbol,
            "side": side_bybit,
            "orderType": "Market",
            "qty": str(qty),
            "timeInForce": "GoodTillCancel",
            "orderLinkId": order_id,
            "reduceOnly": False,
            "takeProfit": str(tp),
            "stopLoss": str(sl),
            "leverage": leverage
        }

        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            res = requests.post(url, json=payload, headers=headers)
            data = res.json()

            if data.get("retCode") == 0:
                print(f"✅ Order placed: {symbol} {side}")
                return {
                    "success": True,
                    "entry_price": float(tp if side == "LONG" else sl),
                    "symbol": symbol
                }
            else:
                print(f"❌ Failed to place order: {data}")
                return {"success": False}
        except Exception as e:
            print(f"❌ API Error placing order: {e}")
            return {"success": False}


    def _mock_price(self, symbol):
        # Simulate a price for dev
        return 10000.0 + hash(symbol) % 1000
