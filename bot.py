import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()
TOKEN = "8152105369:AAENG2ZwpHDIaT5lgXogL2fpKBeBNmg6pJo"

logging.basicConfig(level=logging.INFO)

VIDEOS = {
    "1": {
        "url": "https://example.com/film1.mp4",
        "title": "فیلم اول 🎬"
    },
    "2": {
        "url": "https.example.com/film2.mp4",
        "title": "فیلم دوم 🎥"
    },
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args and args[0] in VIDEOS:
        video = VIDEOS[args[0]]
        await update.message.reply_video(
            video=video["url"],
            caption=video["title"]
        )
    else:
        keyboard = [
            [InlineKeyboardButton("فیلم 1", callback_data="film_1")],
            [InlineKeyboardButton("فیلم 2", callback_data="film_2")],
        ]
        await update.message.reply_text(
            "سلام! 🎬\nیه فیلم انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    film_id = query.data.split("_")[1]
    video = VIDEOS.get(film_id)
    if video:
        await query.message.reply_video(video=video["url"], caption=video["title"])

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
