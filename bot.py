import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import os
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def gen_numbers_text():
    nums = random.sample(range(1, 16), 15)
    lines = []
    for i in range(0, 15, 4):
        chunk = nums[i:i+4]
        lines.append(" ".join(str(x) for x in chunk))
    return "\n".join(lines)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Kliknij poniżej, żeby wygenerować 15 liczb w losowej kolejności (rzędy po 4):"
    keyboard = [
        [InlineKeyboardButton("Generuj", callback_data="gen")],
        [InlineKeyboardButton("Zamknij", callback_data="close")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "gen":
        txt = gen_numbers_text()
        keyboard = [
            [InlineKeyboardButton("Generuj", callback_data="gen")],
            [InlineKeyboardButton("Zamknij", callback_data="close")]
        ]
        await query.edit_message_text("Liczby w losowej kolejności (rzędy po 4):\n\n" + txt,
                                      reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "close":
        await query.edit_message_text("Zamknięto — jeśli chcesz, kliknij /start, aby zacząć od nowa.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Użyj /start — przycisk Generuj losuje, Zamknij kończy.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot uruchomiony...")
    app.run_polling()

if __name__ == "__main__":
    main()


