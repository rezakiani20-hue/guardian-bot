# ==========================================
# فایل تنظیمات سیستم معاملاتی گاردین (config.py)
# ==========================================
import os

# توکن ربات تلگرام
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")

# فیلتر ارزهای معتبر (حذف ارزهای کم‌حجم و اسکام)
MIN_24H_VOLUME_USD = 20_000_000

TOP_PAIRS = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT",
    "ADA/USDT", "AVAX/USDT", "LINK/USDT", "DOT/USDT", "NEAR/USDT",
    "SUI/USDT", "APT/USDT", "LTC/USDT", "MATIC/USDT", "ATOM/USDT"
]

# پارامترهای استراتژی معاملاتی
TIMEFRAME = "1h"               # تایم‌فریم ۱ ساعته
MIN_RR_RATIO = 2.0             # حداقل نسبت سود به زیان ۱ به ۲
REQUIRED_CONFLUENCE_SCORE = 4  # حداقل ۴ شرط از ۵ شرط اصلی

# تنظیمات اندیکاتورها و پرایس اکشن
RSI_PERIOD = 14
EMA_FAST = 50
EMA_SLOW = 200
ATR_PERIOD = 14
