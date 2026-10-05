import os
import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = {
    "agxamane",
    "amanecommunity",
    "agallzone",
}

TARGET_FILE = "target.json"


def get_target():
    try:
        with open(TARGET_FILE, "r") as f:
            return json.load(f).get("chat_id")
    except Exception:
        return None


def save_target(chat_id):
    with open(TARGET_FILE, "w") as f:
        json.dump({"chat_id": chat_id}, f)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 A M U BOT is running!"
    )


async def settarget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_target(chat_id)

    await update.message.reply_text(
        "✅ AG MINI UNIVERS set as target."
    )


async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post

    if not post:
        return

    username = post.chat.username

    if not username:
        return

    if username.lower() not in {
        x.lower() for x in CHANNELS
    }:
        return

    target = get_target()

    if not target:
        return

    try:
        await context.bot.copy_message(
            chat_id=target,
            from_chat_id=post.chat.id,
            message_id=post.message_id,
        )
    except Exception as e:
        print("Forward error:", e)


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN পাওয়া যায়নি!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("settarget", settarget))

    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST,
            channel_post
        )
    )

    print("🤖 A M U BOT is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
