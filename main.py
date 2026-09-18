import os
import logging
import asyncio
import html
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8017205070:AAFgbCv6bPfLb-CWCelBW2_S50NYDOIAh2Q"
OWNER_LINK = "https://t.me/RAHU_LKING89"

# --- FLASK WEB SERVER FOR UPTIMEROBOT ---
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot is Alive 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# --- TELEGRAM BOT HANDLERS ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    name = html.escape(user.first_name if user.first_name else "User")

    welcome_text = f"Welcome, <b>{name}</b>!"

    keyboard = [
        [
            InlineKeyboardButton("👑 Contact Owner", url=OWNER_LINK)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # User profile photos/videos fetch karna
        photos = await context.bot.get_user_profile_photos(user_id=user.id, limit=1)
        if photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
            await context.bot.send_photo(
                chat_id=chat.id,
                photo=file_id,
                caption=welcome_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                welcome_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
    except Exception:
        await update.message.reply_text(
            welcome_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

# Direct Chat ID Command (Only ID output)
async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if update.message:
        await update.message.reply_text(f"<code>{chat.id}</code>", parse_mode="HTML")

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "<b>Help Menu</b>\n\n"
        "• /start — Start Bot\n"
        "• /id — Get Chat ID\n"
        "• /help — Get Support Info"
    )
    keyboard = [[InlineKeyboardButton("👑 Contact Owner", url=OWNER_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=reply_markup)

async def post_init(application):
    # Telegram Side Menu Commands Set Karna
    commands = [
        ("id", "Get Chat ID"),
        ("help", "Help & Support")
    ]
    await application.bot.set_my_commands(commands)

async def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("help", help_command))

    print("Simple Bot Engine Running...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    keep_alive()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.close()
