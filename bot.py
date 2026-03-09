import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 68700299

NAME, LEVEL = range(2)

levels = [["A1-A2"], ["B1-B2"], ["B2+"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ism familiyangizni kiriting:")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    keyboard = ReplyKeyboardMarkup(levels, resize_keyboard=True)

    await update.message.reply_text(
        "Ingliz tili darajangizni tanlang:",
        reply_markup=keyboard
    )

    return LEVEL


async def get_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data["name"]
    level = update.message.text
    username = update.message.from_user.username

    if username:
        username = "@" + username
    else:
        username = "username yo'q"

    text = f"""
Yangi foydalanuvchi:

Ism: {name}
Level: {level}
Username: {username}
"""

    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

    await update.message.reply_text(
        "Ro'yxatdan o'tdingiz.\nYangiliklar uchun kanal:\nhttps://t.me/TedxYazyavan"
    )

    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_level)],
        },
        fallbacks=[],
    )

    app.add_handler(conv)

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
