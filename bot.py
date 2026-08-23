import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# تنظیم لاگ‌ها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توکن ربات
TOKEN = os.getenv("BOT_TOKEN")

# لیست فیلم ها
VIDEOS = {
    "1": {
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "title": "فیلم اول"
    },
    "2": {
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "title": "فیلم دوم"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("فیلم 1", callback_data="film_1")],
        [InlineKeyboardButton("فیلم 2", callback_data="film_2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("یک فیلم را انتخاب کنید:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    film_id = query.data.split("_")[1]
    video = VIDEOS.get(film_id)
    
    if video:
        await query.message.reply_video(video=video["url"], caption=video["title"])

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
