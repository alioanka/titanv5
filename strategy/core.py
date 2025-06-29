# strategy/core.py

import pandas as pd
import numpy as np
from config import ATR_PERIOD, MIN_TREND_STRENGTH, MIN_VOLATILITY

def generate_signal(candles):
    df = pd.DataFrame(candles)
    df['close'] = df['close'].astype(float)

    # === Calculate indicators === #
    df['returns'] = df['close'].pct_change()
    df['trend'] = df['close'].rolling(3).mean() - df['close'].rolling(12).mean()
    df['volatility'] = df['returns'].rolling(14).std()
    df['atr'] = atr(df, ATR_PERIOD)

    # === Calculate trend strength === #
    trend_strength = df['trend'].iloc[-1] / df['close'].iloc[-1]
    volatility = df['volatility'].iloc[-1]

#    if abs(trend_strength) < MIN_TREND_STRENGTH:
#        return None  # No strong trend
#    if volatility < MIN_VOLATILITY:
#        return None  # Too flat
    # FORCE signal for testing
    print(f"🔍 Forcing entry for testing | Trend: {trend_strength:.4f} | Vol: {volatility:.4f}")

    # === Decide direction === #
    direction = "LONG" if trend_strength > 0 else "SHORT"
    print(f"DEBUG → Trend strength: {trend_strength}, ATR: {df['atr'].iloc[-1]}")

    return {
        "side": direction,
        "atr": df['atr'].iloc[-1]
    }

def atr(df, period):
    df['H-L'] = df['high'] - df['low']
    df['H-C'] = abs(df['high'] - df['close'].shift())
    df['L-C'] = abs(df['low'] - df['close'].shift())
    tr = df[['H-L', 'H-C', 'L-C']].max(axis=1)
    return tr.rolling(period).mean()
