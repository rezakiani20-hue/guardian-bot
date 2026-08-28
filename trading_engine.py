# ==========================================
# موتور تحلیل ۵ شرطی و استراتژی معاملاتی (trading_engine.py)
# ==========================================
import ccxt
import pandas as pd
import pandas_ta as ta
import config

class TradingEngine:
    def __init__(self):
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })

    def fetch_data(self, symbol, timeframe=config.TIMEFRAME, limit=250):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception:
            return None

    def analyze_symbol(self, symbol):
        df = self.fetch_data(symbol)
        if df is None or len(df) < 200:
            return None

        # ۱. محاسبه اندیکاتورها
        df['EMA_FAST'] = ta.ema(df['close'], length=config.EMA_FAST)
        df['EMA_SLOW'] = ta.ema(df['close'], length=config.EMA_SLOW)
        df['RSI'] = ta.rsi(df['close'], length=config.RSI_PERIOD)
        df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=config.ATR_PERIOD)

        curr = df.iloc[-1]
        prev = df.iloc[-2]

        score = 0
        signal_type = None

        # ۲. بررسی ۵ شرط اصلی (Confluence Score)
        # شرط ۱: روند EMA
        ema_bullish = curr['EMA_FAST'] > curr['EMA_SLOW']
        ema_bearish = curr['EMA_FAST'] < curr['EMA_SLOW']
        
        # شرط ۲: RSI وضعیت اشباع
        rsi_bullish = curr['RSI'] < 40 and curr['RSI'] > prev['RSI']
        rsi_bearish = curr['RSI'] > 60 and curr['RSI'] < prev['RSI']

        # شرط ۳: پرایس اکشن (شکست کندل قبلی)
        price_bullish = curr['close'] > prev['high']
        price_bearish = curr['close'] < prev['low']

        # شرط ۴: مومنتوم کندلی (کندل قدرتمند)
        candle_body = abs(curr['close'] - curr['open'])
        avg_body = abs(df['close'] - df['open']).tail(20).mean()
        momentum = candle_body > avg_body

        # شرط ۵: حجم معاملات تاییدکننده
        volume_confirm = curr['volume'] > df['volume'].tail(20).mean()

        # محاسبه امتیاز خرید (LONG)
        long_score = sum([ema_bullish, rsi_bullish, price_bullish, momentum, volume_confirm])
        # محاسبه امتیاز فروش (SHORT)
        short_score = sum([ema_bearish, rsi_bearish, price_bearish, momentum, volume_confirm])

        if long_score >= config.REQUIRED_CONFLUENCE_SCORE:
            signal_type = "BUY (LONG) 🟢"
            score = long_score
            stop_loss = curr['close'] - (curr['ATR'] * 1.5)
            take_profit = curr['close'] + (abs(curr['close'] - stop_loss) * config.MIN_RR_RATIO)
        elif short_score >= config.REQUIRED_CONFLUENCE_SCORE:
            signal_type = "SELL (SHORT) 🔴"
            score = short_score
            stop_loss = curr['close'] + (curr['ATR'] * 1.5)
            take_profit = curr['close'] - (abs(stop_loss - curr['close']) * config.MIN_RR_RATIO)
        else:
            return None

        # محاسبه نسبت سود به زیان (R/R)
        risk = abs(curr['close'] - stop_loss)
        reward = abs(take_profit - curr['close'])
        rr_ratio = reward / risk if risk > 0 else 0

        if rr_ratio < config.MIN_RR_RATIO:
            return None

        return {
            "symbol": symbol,
            "signal": signal_type,
            "entry": round(curr['close'], 4),
            "stop_loss": round(stop_loss, 4),
            "take_profit": round(take_profit, 4),
            "rr_ratio": round(rr_ratio, 2),
            "score": f"{score}/5"
        }
