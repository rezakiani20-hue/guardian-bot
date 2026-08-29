=====================
​فایل تنظیمات سیستم معاملاتی گاردین (config.py)
​==========================================
​import os
​توکن ربات تلگرام
​TELEGRAM_TOKEN = 8869758028:AAHtKdxdzNTJabCZAFYyynLoLj4pDppJvMM
Iran
TELEGRAM_CHAT_ID = "آیدی_چت_یا_کانال_شما"
​فیلتر ارزهای معتبر (حذف ارزهای کم‌حجم و اسکام)
​MIN_24H_VOLUME_USD = 20_000_000
​TOP_PAIRS = [
"BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT",
"ADA/USDT", "AVAX/USDT", "LINK/USDT", "DOT/USDT",
"SUI/USDT", "APT/USDT", "LTC/USDT", "MATIC/USDT"
]
​پارامترهای استراتژی معاملاتی
​TIMEFRAME = "1h"               # فریم ۱ ساعته #
MIN_RR_RATIO = 2.0             # به زبان ۱ به ۲ #
REQUIRED_CONFLUENCE_SCORE = 4  # از ۵ شرط اصلی #
​تنظیمات اندیکاتورها و پرایس اکشن
​RSI_PERIOD = 14
EMA_FAST = 50
EMA_SLOW = 200
ATR_PERIOD = 14
​کافی است همین متن بالا را کپی کنید، در صفحه ویرایش گیت‌هاب جایگزین کنید، توکن خود را در خط ۷ قرار دهید و تغییرات را ذخیره (Commit) کنید.
