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

# --- HELPER FUNCTION FOR USER DATA ---
def get_user_details(user, chat):
    first_name = html.escape(user.first_name) if user.first_name else "N/A"
    last_name = html.escape(user.last_name) if user.last_name else ""
    full_name = f"{first_name} {last_name}".strip()
    username = f"@{user.username}" if user.username else "N/A"
    
    return full_name, username, chat.id

# --- TELEGRAM BOT HANDLERS ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    full_name, username, chat_id = get_user_details(user, chat)

    welcome_text = (
        f"𝙃𝙚𝙮 {full_name} 𝙬𝙚𝙡𝙘𝙤𝙢𝙚 𝙆𝙪𝙨𝙝𝙖𝙡 𝙙𝙖𝙩𝙖\n\n"
        f"𝙗𝙤𝙩 𝙪𝙨𝙚𝙙 𝙛𝙤𝙧 𝙘𝙝𝙖𝙩 𝙄𝘿 𝙖𝙣𝙮 𝙥𝙧𝙤𝙗𝙡𝙚𝙢 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙖𝙙𝙢𝙞𝙣 𝙩𝙝𝙖𝙣𝙠𝙨\n\n"
        f"𝙛𝙤𝙧 𝙨𝙪𝙥𝙥𝙤𝙧𝙩\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>NAME:</b> {full_name}\n"
        f"🌐 <b>USERNAME:</b> {username}\n"
        f"🆔 <b>CHAT ID:</b> <code>{chat_id}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )

    # VIP Styled Buttons Layout
    keyboard = [
        [
            InlineKeyboardButton(" 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝘼𝘿𝙈𝙄𝙉 ", url=OWNER_LINK)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
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

# Direct Chat ID Command
async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if update.message:
        await update.message.reply_text(f"<code>{chat.id}</code>", parse_mode="HTML")

async def post_init(application):
    await application.bot.delete_my_commands()
    
    commands = [
        ("start", "Start Bot"),
        ("id", "Get Chat ID")
    ]
    await application.bot.set_my_commands(commands)

async def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("id", id_command))

    print("Kushal Data VIP Bot Engine Running...")
    
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
