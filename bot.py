import os
import logging
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

# Token setup directly from Environment Variable (Render compatible)
BOT_TOKEN = os.getenv("8017205070:AAFgbCv6bPfLb-CWCelBW2_S50NYDOIAh2Q")

# Helper to construct stylish response header
def get_user_name(user):
    return user.first_name if user.first_name else "User"

# /start Command Handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = get_user_name(user)

    start_text = f"""╔══════════════════════════════╗
   ⚡ <b>K U S H A L  W E B S</b> ⚡
╚══════════════════════════════╝

👋 <i>Greetings,</i> <b>{name}</b>!

🟢 <b>ACCOUNT STATUS:</b> <code>VERIFIED</code>
💎 <b>TIER:</b> <code>ULTIMATE PREMIUM</code>
✨ <b>ACCESS:</b> <code>UNLIMITED</code>

┌──────────────────────────────┐
│ 🌐 <b>NAVIGATION & MENU</b>       
└──────────────────────────────┘
├ 🆔 /id       — <code>Check User/Chat ID</code>
├ ℹ️ /about    — <code>System Info & Overview</code>
├ ⚙️ /commands — <code>All Commands Directory</code>
├ 🛡️ /status   — <code>Live System Diagnostics</code>
├ 🎁 /premium  — <code>Membership Privilege</code>
└ 💖 /support  — <code>Contact Developer</code>

👇 <b>Select an option below to proceed:</b>"""

    # Telegram Bot API 9.4+ style color attributes included
    keyboard = [
        [
            InlineKeyboardButton("🆔 MY ID", callback_data="cmd_id", style="primary"),
            InlineKeyboardButton("ℹ️ ABOUT", callback_data="cmd_about", style="primary"),
        ],
        [
            InlineKeyboardButton("⚙️ COMMANDS", callback_data="cmd_commands", style="primary"),
            InlineKeyboardButton("🛡️ STATUS", callback_data="cmd_status", style="success"),
        ],
        [
            InlineKeyboardButton("🎁 PREMIUM", callback_data="cmd_premium", style="primary"),
            InlineKeyboardButton("💖 SUPPORT", callback_data="cmd_support", style="danger"),
        ],
        [
            InlineKeyboardButton("📡 OFFICIAL CHANNEL", url="https://t.me/your_channel"),
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

# /id Command
async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    msg = f"""┌──────────────────────────────┐
│ 🆔 <b>IDENTITY CARD</b>
└──────────────────────────────┘
👤 <b>User Name:</b> {user.first_name}
🆔 <b>User ID:</b> <code>{user.id}</code>
💬 <b>Chat ID:</b> <code>{chat.id}</code>"""
    
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /about Command
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """┌──────────────────────────────┐
│ ℹ️ <b>SYSTEM INFORMATION</b>
└──────────────────────────────┘
🌐 <b>Project:</b> KUSHALWEBS Bot Engine
⚡ <b>Version:</b> v3.0 Pro
🔒 <b>Security:</b> End-to-End Encrypted
👑 <b>Developer:</b> @your_username"""
    
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /commands Command
async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """┌──────────────────────────────┐
│ ⚙️ <b>COMMAND DIRECTORY</b>
└──────────────────────────────┘
🔹 /start — Launch / Refresh Dashboard
🔹 /id — Get unique User ID & Chat ID
🔹 /about — View system information
🔹 /commands — View command directory
🔹 /status — Check live system ping
🔹 /premium — Check premium privileges
🔹 /support — Contact support desk"""
    
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /status Command
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """┌──────────────────────────────┐
│ 🛡️ <b>SYSTEM DIAGNOSTICS</b>
└──────────────────────────────┘
✅ <b>Core Engine:</b> ONLINE
🟢 <b>Database:</b> CONNECTED
⚡ <b>Response Speed:</b> ULTRA FAST
🛡️ <b>Protection:</b> ACTIVE"""
    
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /premium Command
async def premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """┌──────────────────────────────┐
│ 🎁 <b>PREMIUM MEMBERSHIP</b>
└──────────────────────────────┘
💎 <b>Plan:</b> VIP Lifetime Unlocked
🔥 <b>Features:</b> Unlimited Speed & Priority Access
🌟 <b>Status:</b> ACTIVE ✅"""
    
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /support Command
async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """┌──────────────────────────────┐
│ 💖 <b>SUPPORT & CONTACT</b>
└──────────────────────────────┘
📩 Need help or custom setups?
👨‍💻 <b>Owner Handle:</b> @your_username
📢 <b>Updates Channel:</b> https://t.me/your_channel"""
    
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# Button Click Router
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    handlers = {
        "cmd_id": id_command,
        "cmd_about": about_command,
        "cmd_commands": commands_command,
        "cmd_status": status_command,
        "cmd_premium": premium_command,
        "cmd_support": support_command
    }

    if query.data in handlers:
        await handlers[query.data](update, context)

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    app = ApplicationBuilder().token(8017205070:AAFgbCv6bPfLb-CWCelBW2_S50NYDOIAh2Q).build()

    # Registering handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("commands", commands_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("premium", premium_command))
    app.add_handler(CommandHandler("support", support_command))
    app.add_handler(CallbackQueryHandler(button_click))

    print("KUSHALWEBS Bot Engine running successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()
