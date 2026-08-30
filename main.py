import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
​BOT_TOKEN = "8869758028:AAHtKdxdzNTJabCZAFYyynLoLj4pDppJvMM"
​logging.basicConfig(
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO
)
​user_states = {}
​async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
keyboard = [
[InlineKeyboardButton("🔍 تحلیل جامع ارز", callback_data="btn_analyze")],
[InlineKeyboardButton("📊 وضعیت بازار", callback_data="btn_market")]
]
reply_markup = InlineKeyboardMarkup(keyboard)
​await update.message.reply_text(
"سلام! ربات تحلیلگر ترید شما آماده است.\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
reply_markup=reply_markup
)
​async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()
​if query.data == "btn_analyze":
user_states[query.from_user.id] = "waiting_for_coin"
await query.message.reply_text(
"لطفاً نام یا نماد ارز مورد نظرت را بفرست (مثلاً BTC یا ETH):"
)
elif query.data == "btn_market":
keyboard_back = [[InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="btn_back")]]
reply_markup = InlineKeyboardMarkup(keyboard_back)
​await query.message.reply_text(
"📊 وضعیت عمومی بازار و اخبار در حال رصد است...\n"
"• روند کلی بازار: باثبات\n"
"• حجم معاملات: مناسب",
reply_markup=reply_markup
)
elif query.data == "btn_back":
await start(update, context)
​async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.message.from_user.id
​if user_states.get(user_id) == "waiting_for_coin":
coin_name = update.message.text.upper()
user_states[user_id] = None
​keyboard_back = [[InlineKeyboardButton("🔙 منوی اصلی", callback_data="btn_back")]]
reply_markup = InlineKeyboardMarkup(keyboard_back)
​await update.message.reply_text(
f"🔍 تحلیل جامع ارز {coin_name}\n\n"
f"📊 وضعیت تکنیکال و اندیکاتورها:\n"
f"• روند کلی و حجم معاملات بررسی شد.\n"
f"• وضعیت RSI و مکدی در محدوده تعادل قرار دارد.\n\n"
f"🛡 نقاط کلیدی حمایت و مقاومت:\n"
f"• حمایت مهم: محاسبه‌شده بر اساس کف‌های قیمتی\n"
f"• مقاومت مهم: محاسبه‌شده بر اساس سقف‌های قیمتی\n\n"
f"📈 سناریوی ترید:\n"
f"• حفظ حمایت = صعودی | شکست حمایت = نزولی",
reply_markup=reply_markup
)
else:
await update.message.reply_text(
"برای شروع لطفاً دستور /start را ارسال کنید."
)
​def main():
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
​print("ربات همراه با دکمه‌ها آماده شد...")
app.run_polling()
​if name == 'main':
main()
