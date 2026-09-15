import os
import threading
import logging
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token
BOT_TOKEN = "8017205070:AAFgbCv6bPfLb-CWCelBW2_S50NYDOIAh2Q"

# Flask Server (For UptimeRobot 24/7 Hosting)
server = Flask(__name__)

@server.route('/')
def home():
    return "Bot is active 24/7!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)

def get_id_keyboard(user_id: int):
    """
    Screenshot jaisa Button Design:
    - 1st Button (Blue UI Tint): ID Copy button format
    - 2nd Button (Red UI Tint): Direct Share ID inline action
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"📋 {user_id}",
                callback_data=f"copy_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Share ID",
                switch_inline_query=f"{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Jab bhi koi user /start bhejega:
    Bot USI USER ki khud ki Personal Telegram ID generate karega.
    """
    user_id = update.effective_user.id
    
    # Exact Text Format: 👤 Your ID : <user_id>
    message_text = f"👤 <b>Your ID :</b> <code>{user_id}</code>"
    reply_markup = get_id_keyboard(user_id)

    await update.message.reply_text(
        text=message_text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

async def handle_user_or_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Jab user kisi doosre user ka message/contact forward karega:
    Exact Format: ✅ User ID : <target_id>
    """
    msg = update.message
    if not msg:
        return

    target_id = None

    # Forwarded Message
    if msg.forward_from:
        target_id = msg.forward_from.id
    # Shared Contact
    elif msg.contact:
        target_id = msg.contact.user_id
    # Normal Message (Sender's ID)
    else:
        target_id = update.effective_user.id

    if target_id:
        message_text = f"✅ <b>User ID :</b> <code>{target_id}</code>"
        reply_markup = get_id_keyboard(target_id)

        await msg.reply_text(
            text=message_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

def main():
    # Flask Web Server Parallel Thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Application Setup
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers Registration
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_user_or_forward))

    logger.info("Bot started and ready for users...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
