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

BOT_TOKEN = os.getenv("8017205070:AAFgbCv6bPfLb-CWCelBW2_S50NYDOIAh2Q")

# /start Command Handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name if user.first_name else "User"

    start_text = f"""━━━━━━━━━━━━━━━━━━━━━━━
      👑  <b>KUSHALWEBS</b>  👑
━━━━━━━━━━━━━━━━━━━━━━━

✨ Hello, <b>{first_name}</b>!

✅ You are now <b>verified</b>.
💎 Premium access <b>unlocked</b>.
🔥 Enjoy the full experience!

┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
⚙️ <b>Quick Access</b>
┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
  🆔 /id       — ɢᴇᴛ ʏᴏᴜʀ ᴄʜᴀᴛ ɪᴅ
  ℹ️ /about    — ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ
  ⚙️ /commands — ꜰᴜʟʟ ᴄᴏᴍᴍᴀɴᴅ ʟɪꜱᴛ
  🛡️ /status   — ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ
  🎁 /premium  — ᴘʀᴇᴍɪᴜᴍ ɪɴꜰᴏ
  💖 /support  — ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ

✨ Tap a button below to begin 👇"""

    # Inline Keyboard Layout
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
            InlineKeyboardButton("📣 CHANNEL", url="https://t.me/your_channel"),  # Apne channel ka link daalein
            InlineKeyboardButton("👑 OWNER", url="https://t.me/your_username"),   # Apne username ka link daalein
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        start_text,
        parse_mode="HTML",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# /id Command
async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    msg = f"🆔 <b>Your User ID:</b> <code>{user_id}</code>\n💬 <b>Chat ID:</b> <code>{chat_id}</code>"
    
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /about Command
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "ℹ️ <b>About KUSHALWEBS Bot</b>\n\nThis bot provides premium services and features for users."
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /commands Command
async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """⚙️ <b>Available Commands:</b>

/start - Restart the bot
/id - Get your User & Chat ID
/about - About this bot
/commands - List all commands
/status - Check bot status
/premium - Premium membership details
/support - Contact bot owner"""
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /status Command
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🛡️ <b>Bot Status:</b> Operational & Running smoothly! ✅"
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /premium Command
async def premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🎁 <b>Premium Status:</b> Unlocked! You have full access to all features. 💎"
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# /support Command
async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "💖 <b>Support:</b> Contact owner for help: @your_username"
    if update.message:
        await update.message.reply_text(msg, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.reply_text(msg, parse_mode="HTML")

# Button Click Handler
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cmd_id":
        await id_command(update, context)
    elif query.data == "cmd_about":
        await about_command(update, context)
    elif query.data == "cmd_commands":
        await commands_command(update, context)
    elif query.data == "cmd_status":
        await status_command(update, context)

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers Registration
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("commands", commands_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("premium", premium_command))
    app.add_handler(CommandHandler("support", support_command))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
