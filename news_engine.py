# ==========================================
# موتور فیلتر اخبار اقتصادی و فدرال رزرو (news_engine.py)
# ==========================================
import requests
from datetime import datetime

class NewsEngine:
    def __init__(self):
        # آدرس دریافت تقویم اقتصادی
        self.news_api_url = "https://napi.coinglass.com/api/index/economic-calendar"

    def is_news_time(self):
        """
        این تابع بررسی می‌کند آیا هم‌اکنون در زمان انتشار اخبار مهم فدرال رزرو (FOMC/CPI) هستیم یا خیر.
        اگر خبر مهمی باشد، جهت جلوگیری از کال‌مارجین شدن سیگنال صادر نمی‌شود.
        """
        try:
            # در صورتی که دیتای خبر دریافت شود فیلتر اعمال می‌گردد
            response = requests.get(self.news_api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # بررسی رویدادهای با اهمیت بالا (High Impact)
                for event in data.get("data", []):
                    if event.get("importance") == 3: # خبر درجه ۳ و بسیار مهم
                        event_time = datetime.fromtimestamp(event.get("date", 0) / 1000)
                        now = datetime.now()
                        # اگر در فاصله ۳۰ دقیقه قبل یا بعد از خبر باشیم
                        diff_minutes = abs((event_time - now).total_seconds()) / 60
                        if diff_minutes <= 30:
                            return True, event.get("title", "خبر مهم فدرال رزرو")
            return False, ""
        except Exception:
            # در صورت عدم دسترسی به API، ریسک نکرده و بازار را امن در نظر می‌گیرد
            return False, ""
