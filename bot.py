import os
import threading
import logging
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Single Hardcoded Token
BOT_TOKEN = "8017205070:AAFgbCv6bPfLb-CWCelBW2_S50NYDOIAh2Q"

# Flask Server for UptimeRobot Ping
server = Flask(__name__)

@server.route('/')
def home():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)

def get_id_keyboard(user_id: int):
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"📋 {user_id}",
                callback_data=f"copy_{user_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Share ID ↗️",
                switch_inline_query=f"{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = f"👤 <b>Your ID :</b> <code>{user_id}</code>"
    reply_markup = get_id_keyboard(user_id)

    await update.message.reply_text(
        text=message_text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

async def handle_user_or_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    target_id = None

    if msg.forward_from:
        target_id = msg.forward_from.id
    elif msg.contact:
        target_id = msg.contact.user_id
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
    # Keep-alive Flask Web Server Thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Telegram Bot Application Setup
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_user_or_forward))

    logger.info("Bot starting with web service...")
    app.run_polling()

if __name__ == "__main__":
    main()
