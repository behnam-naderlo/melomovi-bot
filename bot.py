import os
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("فیلم 1", callback_data="film_1")],
        [InlineKeyboardButton("فیلم 2", callback_data="film_2")]
    ]
    await update.message.reply_text("یک فیلم را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    film_id = query.data.split("_")[1]
    if film_id == "1":
        await query.message.reply_video("https://www.w3schools.com/html/mov_bbb.mp4", caption="فیلم اول")
    elif film_id == "2":
        await query.message.reply_video("https://www.w3schools.com/html/mov_bbb.mp4", caption="فیلم دوم")

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # تعریف کردن متغیر RENDER_EXTERNAL_HOSTNAME از روی پورت
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TOKEN,
        webhook_url="https://" + os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost") + "/" + TOKEN
    )
    
    app.run(host="0.0.0.0", port=10000)
