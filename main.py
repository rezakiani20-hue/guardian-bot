# ==========================================
# فایل اصلی اجرای ربات تلگرام (main.py)
# ==========================================
import os
import time
import requests
import config
from news_engine import NewsEngine
from trading_engine import TradingEngine

TOKEN = config.TELEGRAM_TOKEN
news_bot = NewsEngine()
trader = TradingEngine()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": "@YOUR_CHANNEL_OR_CHAT_ID", # یا می‌توانید با getUpdates آیدی پیام دهید
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        # ارسال پیام به تلگرام از طریق API مستقیم
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")

def run_bot():
    print("🤖 سیستم معاملاتی گاردین فعال شد...")
    
    while True:
        try:
            # ۱. بررسی فیلتر اخبار
            is_news, news_title = news_bot.is_news_time()
            if is_news:
                print(f"⚠️ انتشار خبر مهم: {news_title} - تحلیل بازار متوقف شد.")
                time.sleep(300)
                continue

            # ۲. اسکن جفت‌ارزها
            for symbol in config.TOP_PAIRS:
                signal = trader.analyze_symbol(symbol)
                if signal:
                    msg = (
                        f"🛡 **سیگنال سیستم معاملاتی گاردین**\n\n"
                        f"📌 **نماد:** `{signal['symbol']}`\n"
                        f"📊 **جهت:** {signal['signal']}\n"
                        f"🎯 **نقطه ورود:** `{signal['entry']}`\n"
                        f"🛑 **حد زیان (SL):** `{signal['stop_loss']}`\n"
                        f"🟢 **حد سود (TP):** `{signal['take_profit']}`\n"
                        f"⚖️ **نسبت R/R:** `{signal['rr_ratio']}`\n"
                        f"⭐ **امتیاز همگرایی:** `{signal['score']}`\n"
                    )
                    send_telegram_message(msg)
                    print(f"✅ سیگنال برای {symbol} ارسال شد.")
            
            # اسکن بعدی بعد از ۵ دقیقه
            time.sleep(300)

        except Exception as e:
            print(f"خطا در اجرای ربات: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()
