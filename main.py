import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# Credentials
TELEGRAM_BOT_TOKEN = "8830057135:AAGhA-W170Cy36x0fG1bCbW2G2ySntxZIx0"
FIVESIM_API_KEY = "wk5Yk_VDunn1Nrnt72JbJ9nZNdQt6yqTx6uZUA3MkrjRCiEzA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"🤖 **Welcome to OTP Bot!**\n\n"
        f"🆔 User ID: `{user.id}`\n"
        f"👤 Name: {user.full_name}\n\n"
        f"নিচের মেনু থেকে আপনার সার্ভিস নির্বাচন করুন:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📱 Get Number", callback_data='get_number')],
        [InlineKeyboardButton("💰 Balance & Profile", callback_data='profile')],
        [InlineKeyboardButton("💬 Support", callback_data='support')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'get_number':
        keyboard = [
            [InlineKeyboardButton("📌 WhatsApp", callback_data='service_wa')],
            [InlineKeyboardButton("✈️ Telegram", callback_data='service_tg')],
            [InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')]
        ]
        await query.message.edit_text("⚙️ **সার্ভিস নির্বাচন করুন:**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        
    elif query.data == 'profile':
        headers = {'Authorization': f'Bearer {FIVESIM_API_KEY}', 'Accept': 'application/json'}
        response = requests.get('https://5sim.net/v1/user/profile', headers=headers)
        
        balance_info = "⚠️ Unable to fetch balance."
        if response.status_code == 200:
            data = response.json()
            balance_info = f"💰 **5SIM Balance:** {data.get('balance', 0)} RUB"
            
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')]]
        await query.message.edit_text(f"👤 **Profile Info**\n\n{balance_info}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'main_menu':
        await start(update, context)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()
