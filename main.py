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
    # Render default PORT environment variable use karega
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# --- TELEGRAM BOT HANDLERS ---
def get_user_name(user):
    raw_name = user.first_name if user.first_name else "User"
    return html.escape(raw_name)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = get_user_name(user)

    start_text = (
        f"👑 <b>JOY WEBS</b> 👑\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ Hello, <b>{name}</b>!\n\n"
        f"✅ You are now <b>verified</b>.\n"
        f"💎 Premium access <b>unlocked</b>.\n"
        f"🔥 Enjoy the full experience!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ <b>Quick Access</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 /id — GET YOUR CHAT ID\n"
        f"ℹ️ /about — ABOUT THIS BOT\n"
        f"⚙️ /commands — FULL COMMAND LIST\n"
        f"🛡️ /status — BOT STATUS\n"
        f"🎁 /premium — PREMIUM INFO\n"
        f"💖 /support — CONTACT OWNER\n\n"
        f"✨ <i>Tap a button below to begin</i> 👇"
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
            InlineKeyboardButton("📣 CHANNEL", url="https://t.me/your_channel"),
            InlineKeyboardButton("👑 OWNER", url="https://t.me/your_username"),
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
        f"🆔 <b>IDENTITY DETAILS</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Name:</b> {get_user_name(user)}\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
        f"💬 <b>Chat ID:</b> <code>{chat.id}</code>"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"ℹ️ <b>SYSTEM INFORMATION</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🌐 <b>Project:</b> JOY WEBS Bot Engine\n"
        f"⚡ <b>Version:</b> v3.0 Pro\n"
        f"🔒 <b>Security:</b> End-to-End Encrypted\n"
        f"👑 <b>Developer:</b> @your_username"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"⚙️ <b>COMMAND DIRECTORY</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔹 /start — Launch Dashboard\n"
        f"🔹 /id — Get User & Chat ID\n"
        f"🔹 /about — System Info\n"
        f"🔹 /commands — Command Directory\n"
        f"🔹 /status — System Status\n"
        f"🔹 /premium — Premium Info\n"
        f"🔹 /support — Contact Support"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"🛡️ <b>SYSTEM DIAGNOSTICS</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ <b>Engine:</b> ONLINE\n"
        f"🟢 <b>Database:</b> CONNECTED\n"
        f"⚡ <b>Speed:</b> ULTRA FAST"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    handlers = {
        "cmd_id": id_command,
        "cmd_about": about_command,
        "cmd_commands": commands_command,
        "cmd_status": status_command,
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
    app.add_handler(CallbackQueryHandler(button_click))

    print("JOY WEBS Bot Engine running successfully!")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Web server start
    keep_alive()
    
    # Telegram Bot start
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.close()
