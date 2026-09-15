import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Aapka Telegram Bot Token
BOT_TOKEN = "8017205070:AAFgbCv6bPfLb-CWCelBW2_S50NYDOIAh2Q"


def get_id_keyboard(user_id: int):
    """
    Screenshot jaisa exact layout:
    1. Pehla Blue Highlight Button -> ID copy format
    2. Doosra Red Highlight Button -> Direct Share ID inline action
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
                text="Share ID ↗️",
                switch_inline_query=f"{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Har user ke liye unki apni personal ID dikhayega"""
    user_id = update.effective_user.id
    message_text = f"👤 <b>Your ID :</b> <code>{user_id}</code>"
    reply_markup = get_id_keyboard(user_id)

    await update.message.reply_text(
        text=message_text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


async def handle_user_or_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forwarded message, shared contact, ya direct user profile share handle karne ke liye"""
    msg = update.message
    target_id = None

    # Forward kiye gaye message se ID nikalne ke liye
    if msg.forward_from:
        target_id = msg.forward_from.id
    # Share kiye gaye contact se ID nikalne ke liye
    elif msg.contact:
        target_id = msg.contact.user_id
    # Direct message bhejne wale user ki ID
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
    # Multi-user Async Application build
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers Registration
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_user_or_forward))

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()