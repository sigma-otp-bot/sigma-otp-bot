import os
import requests
from flask import Flask
from threading import Thread
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, filters, ContextTypes

# --- Render Keep-Alive Server ---
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot is running perfectly!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app_web.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Credentials
TELEGRAM_BOT_TOKEN = "8830057135:AAGhA-W170Cy36x0fG1bCbW2G2ySntxZIx0"
FIVESIM_API_KEY = "wk5Yk_VDunn1Nrnt72JbJ9nZNdQt6yqTx6uZUA3MkrjRCiEzA"

# --- /start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f" (@{user.username})" if user.username else ""
    
    welcome_text = (
        f"👍 **Welcome to Premium OTP Bot!**\n\n"
        f"🆔 **Your ID:** `{user.id}`\n"
        f"👤 **Name:** 💖 \"{user.full_name}\"{username}\n\n"
        f"Please select an option from the menu below:\n"
        f"⬇️⬇️⬇️⬇️⬇️⬇️⬇️"
    )

    # Permanent Reply Keyboard (Bottom Layout)
    reply_keyboard = [
        [KeyboardButton("💬 Get Number"), KeyboardButton("📈 Traffic")],
        [KeyboardButton("💰 Wallet"), KeyboardButton("🏆 Top Users")],
        [KeyboardButton("🎧 Support"), KeyboardButton("💰 Refer & Earn")],
        [KeyboardButton("💳 Bulk Number")]
    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# --- Reply Menu Click Handler ---
async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💬 Get Number":
        services_text = "⚙️ **Select a service:**"
        inline_keyboard = [
            [InlineKeyboardButton("🅿️ Paypal", callback_data='srv_paypal')],
            [InlineKeyboardButton("📌 Whatsapp", callback_data='srv_wa')],
            [InlineKeyboardButton("✈️ Telegram", callback_data='srv_tg')],
            [InlineKeyboardButton("🍎 Apple", callback_data='srv_apple')],
            [InlineKeyboardButton("🚘 Uber", callback_data='srv_uber')],
            [InlineKeyboardButton("💬 Discord", callback_data='srv_discord')]
        ]
        await update.message.reply_text(services_text, reply_markup=InlineKeyboardMarkup(inline_keyboard), parse_mode='Markdown')

    elif text == "💰 Wallet":
        headers = {'Authorization': f'Bearer {FIVESIM_API_KEY}', 'Accept': 'application/json'}
        balance_info = "⚠️ Unable to fetch balance."
        try:
            res = requests.get('https://5sim.net/v1/user/profile', headers=headers)
            if res.status_code == 200:
                balance_info = f"💰 **5SIM Balance:** {res.json().get('balance', 0)} RUB"
        except Exception:
            pass
        
        await update.message.reply_text(f"👤 **Profile & Balance Info**\n\n{balance_info}", parse_mode='Markdown')

    elif text in ["📈 Traffic", "🏆 Top Users", "🎧 Support", "💰 Refer & Earn", "💳 Bulk Number"]:
        await update.message.reply_text(f"⚙️ **{text}** অপশনটি শীঘ্রই যুক্ত করা হচ্ছে!")

# --- Inline Button Callback Handler ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # When a service is selected -> Show Countries
    if query.data.startswith('srv_'):
        countries_text = "🌍 **Select a country:**"
        country_keyboard = [
            [InlineKeyboardButton("🇻🇪 Venezuela", callback_data='cnt_venezuela'), InlineKeyboardButton("🇧🇴 Bolivia", callback_data='cnt_bolivia')],
            [InlineKeyboardButton("🇰🇭 Cambodia", callback_data='cnt_cambodia'), InlineKeyboardButton("🇪🇬 Egypt", callback_data='cnt_egypt')],
            [InlineKeyboardButton("🇳🇬 Nigeria", callback_data='cnt_nigeria'), InlineKeyboardButton("🇵🇭 Philippines", callback_data='cnt_philippines')],
            [InlineKeyboardButton("🔙 Back to Services", callback_data='back_to_services')]
        ]
        await query.message.edit_text(countries_text, reply_markup=InlineKeyboardMarkup(country_keyboard), parse_mode='Markdown')

    elif query.data == 'back_to_services':
        services_text = "⚙️ **Select a service:**"
        inline_keyboard = [
            [InlineKeyboardButton("🅿️ Paypal", callback_data='srv_paypal')],
            [InlineKeyboardButton("📌 Whatsapp", callback_data='srv_wa')],
            [InlineKeyboardButton("✈️ Telegram", callback_data='srv_tg')],
            [InlineKeyboardButton("🍎 Apple", callback_data='srv_apple')],
            [InlineKeyboardButton("🚘 Uber", callback_data='srv_uber')],
            [InlineKeyboardButton("💬 Discord", callback_data='srv_discord')]
        ]
        await query.message.edit_text(services_text, reply_markup=InlineKeyboardMarkup(inline_keyboard), parse_mode='Markdown')

    elif query.data.startswith('cnt_'):
        country_name = query.data.replace('cnt_', '').capitalize()
        status_text = (
            f"✅ **PAYPAL** - {country_name}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⏳ **Waiting for OTP...**\n"
            f"(Auto-expiry: 25m)\n"
        )
        action_keyboard = [
            [InlineKeyboardButton("📋 +584167884757", callback_data='copy_num')],
            [InlineKeyboardButton("🔄 Change", callback_data='change_num'), InlineKeyboardButton("👀 OTP", callback_data='check_otp')],
            [InlineKeyboardButton("🔙 Back", callback_data='back_to_services')]
        ]
        await query.message.edit_text(status_text, reply_markup=InlineKeyboardMarkup(action_keyboard), parse_mode='Markdown')

if __name__ == '__main__':
    keep_alive()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()
