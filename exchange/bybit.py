# exchange/bybit.py

import requests
import time
import hmac
import hashlib
import uuid
import json

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
            base = 10200 + (i * 1.5)  # Simulate a rising trend
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

        # === Construct Payload ===
        payload = {
            "category": "linear",
            "symbol": symbol,
            "side": side_bybit,
            "orderType": "Market",
            "qty": f"{qty:.4f}",
            "timeInForce": "GoodTillCancel",
            "orderLinkId": order_id,
            "reduceOnly": False,
            "takeProfit": f"{tp:.2f}",
            "stopLoss": f"{sl:.2f}",
            "leverage": str(leverage)
        }

        # === Auth Headers ===
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        body_str = json.dumps(payload)

        signature_payload = timestamp + self.api_key + recv_window + body_str
        signature = hmac.new(
            bytes(self.api_secret, "utf-8"),
            msg=bytes(signature_payload, "utf-8"),
            digestmod=hashlib.sha256
        ).hexdigest()

        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
            "X-BAPI-SIGN": signature,
            "Content-Type": "application/json"
        }

        print(f"📦 Sending Order Payload:\n{json.dumps(payload, indent=2)}")


        try:
            response = requests.post(url, headers=headers, data=body_str)
            data = response.json()

            if data.get("retCode") == 0:
                print(f"✅ Order placed: {symbol} {side}")
                return {
                    "success": True,
                    "entry_price": float(data["result"]["orderPrice"]) if "result" in data and "orderPrice" in data["result"] else 0.0,
                    "symbol": symbol
                }
            else:
                print(f"❌ Failed to place order: {data}")
                return {"success": False}
        except Exception as e:
            print(f"❌ Error placing order: {e}")
            return {"success": False}

    def _mock_price(self, symbol):
        # Simulate a price for dev
        return 10000.0 + hash(symbol) % 1000
