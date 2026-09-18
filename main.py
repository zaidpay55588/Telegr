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
    CallbackQueryHandler,
    ContextTypes,
)

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8017205070:AAFgbCv6bPfLb-CWCelBW2_S50NYDOIAh2Q"

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

# --- HELPER FUNCTION ---
def get_user_name(user):
    return html.escape(user.first_name if user.first_name else "User")

# --- TELEGRAM BOT HANDLERS ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = get_user_name(user)

    start_text = (
        f"<tg-emoji emoji-id='5368324170671202286'>👑</tg-emoji> <b>JOY WEBS</b> <tg-emoji emoji-id='5368324170671202286'>👑</tg-emoji>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<tg-emoji emoji-id='5368324170671202286'>✨</tg-emoji> Hello, <b>{name}</b>!\n\n"
        f"<tg-emoji emoji-id='5368324170671202286'>✅</tg-emoji> Status: <b>VERIFIED</b>\n"
        f"<tg-emoji emoji-id='5368324170671202286'>💎</tg-emoji> Access: <b>UNLOCKED</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<tg-emoji emoji-id='5368324170671202286'>⚙️</tg-emoji> Select an option below:"
    )

    keyboard = [
        [
            InlineKeyboardButton("🆔 MY ID", callback_data="cmd_id"),
            InlineKeyboardButton("ℹ️ ABOUT", callback_data="cmd_about"),
        ],
        [
            InlineKeyboardButton("⚙️ COMMANDS", callback_data="cmd_commands"),
            InlineKeyboardButton("🛡️ STATUS", callback_data="cmd_status"),
        ],
        [
            InlineKeyboardButton("💖 SUPPORT", callback_data="cmd_support"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            start_text,
            parse_mode="HTML",
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    msg = (
        f"<tg-emoji emoji-id='5368324170671202286'>🆔</tg-emoji> <b>IDENTITY DETAILS</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<tg-emoji emoji-id='5368324170671202286'>👤</tg-emoji> <b>Name:</b> {get_user_name(user)}\n"
        f"<tg-emoji emoji-id='5368324170671202286'>🆔</tg-emoji> <b>User ID:</b> <code>{user.id}</code>\n"
        f"<tg-emoji emoji-id='5368324170671202286'>💬</tg-emoji> <b>Chat ID:</b> <code>{chat.id}</code>"
    )
    
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"<tg-emoji emoji-id='5368324170671202286'>ℹ️</tg-emoji> <b>SYSTEM INFORMATION</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<tg-emoji emoji-id='5368324170671202286'>🌐</tg-emoji> <b>Project:</b> JOY WEBS\n"
        f"<tg-emoji emoji-id='5368324170671202286'>👑</tg-emoji> <b>Owner:</b> @RAHU_LKING89"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"<tg-emoji emoji-id='5368324170671202286'>⚙️</tg-emoji> <b>COMMANDS LIST</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<tg-emoji emoji-id='5368324170671202286'>🔹</tg-emoji> /start — Start Bot\n"
        f"<tg-emoji emoji-id='5368324170671202286'>🔹</tg-emoji> /id — Check ID\n"
        f"<tg-emoji emoji-id='5368324170671202286'>🔹</tg-emoji> /about — About System\n"
        f"<tg-emoji emoji-id='5368324170671202286'>🔹</tg-emoji> /commands — Command List\n"
        f"<tg-emoji emoji-id='5368324170671202286'>🔹</tg-emoji> /status — Bot Status\n"
        f"<tg-emoji emoji-id='5368324170671202286'>🔹</tg-emoji> /support — Contact Support"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"<tg-emoji emoji-id='5368324170671202286'>🛡️</tg-emoji> <b>SYSTEM STATUS</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<tg-emoji emoji-id='5368324170671202286'>✅</tg-emoji> <b>Engine:</b> ONLINE\n"
        f"<tg-emoji emoji-id='5368324170671202286'>🟢</tg-emoji> <b>Status:</b> ACTIVE"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"      <tg-emoji emoji-id='5368324170671202286'>💖</tg-emoji> <b>SUPPORT CENTER</b> <tg-emoji emoji-id='5368324170671202286'>💖</tg-emoji>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<tg-emoji emoji-id='5368324170671202286'>✨</tg-emoji> Need help? We're here for you!\n\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n"
        f"<tg-emoji emoji-id='5368324170671202286'>👑</tg-emoji> Owner: @RAHU_LKING89\n"
        f"<tg-emoji emoji-id='5368324170671202286'>📣</tg-emoji> Channel: @RAHU_LKING89\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("👑 OWNER", url="https://t.me/RAHU_LKING89"),
            InlineKeyboardButton("📣 CHANNEL", url="https://t.me/RAHU_LKING89")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML", reply_markup=reply_markup, disable_web_page_preview=True)
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML", reply_markup=reply_markup, disable_web_page_preview=True)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    handlers = {
        "cmd_id": id_command,
        "cmd_about": about_command,
        "cmd_commands": commands_command,
        "cmd_status": status_command,
        "cmd_support": support_command,
    }

    if query.data in handlers:
        await handlers[query.data](update, context)

async def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("commands", commands_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("support", support_command))
    app.add_handler(CallbackQueryHandler(button_click))

    print("JOY WEBS Bot Engine Running...")
    
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
