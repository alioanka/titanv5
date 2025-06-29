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

    def get_ohlcv(self, symbol, timeframe="1h", limit=100):
        now = int(time.time() * 1000)
        candles = []
        for i in range(limit):
            base = 101800 + (i * 10)  # aligned with Bybit testnet price
            candles.append({
                "timestamp": now - ((limit - i) * 3600 * 1000),
                "open": base,
                "high": base + 50,
                "low": base - 50,
                "close": base + 25,
                "volume": 100 + i * 2
            })
        return candles

    def get_balance(self):
        return 10000.0

    def get_open_positions(self):
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
            "qty": f"{qty:.4f}",
            "timeInForce": "GoodTillCancel",
            "orderLinkId": order_id,
            "reduceOnly": False,
            "leverage": str(leverage)
        }

        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        body_str = json.dumps(payload)
        signature_payload = timestamp + self.api_key + recv_window + body_str
        signature = hmac.new(
            self.api_secret.encode(),
            msg=signature_payload.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
            "X-BAPI-SIGN": signature,
            "Content-Type": "application/json"
        }

        try:
            print(f"📦 Sending Order Payload:\n{json.dumps(payload, indent=2)}")
            response = requests.post(url, headers=headers, data=body_str)
            data = response.json()

            if data.get("retCode") == 0:
                print(f"✅ Order placed: {symbol} {side}")
                self.place_tp_sl(symbol, side_bybit, sl, tp)
                return {
                    "success": True,
                    "entry_price": 0.0,
                    "symbol": symbol
                }
            else:
                print(f"❌ Failed to place order: {data}")
                return {"success": False}
        except Exception as e:
            print(f"❌ Error placing order: {e}")
            return {"success": False}

    def place_tp_sl(self, symbol, side, sl, tp):
        endpoint = "/v5/position/trading-stop"
        url = self.base_url + endpoint

        payload = {
            "category": "linear",
            "symbol": symbol,
            "takeProfit": f"{tp:.2f}",
            "stopLoss": f"{sl:.2f}"
        }

        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        body_str = json.dumps(payload)

        signature_payload = timestamp + self.api_key + recv_window + body_str
        signature = hmac.new(
            self.api_secret.encode(),
            msg=signature_payload.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
            "X-BAPI-SIGN": signature,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, data=body_str)
            data = response.json()
            if data.get("retCode") == 0:
                print(f"✅ SL/TP applied: SL={sl} | TP={tp}")
            else:
                print(f"❌ Failed to apply SL/TP: {data}")
        except Exception as e:
            print(f"❌ Error applying SL/TP: {e}")
