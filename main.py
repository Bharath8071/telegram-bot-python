# main.py
import os
import random
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, Dispatcher

# --- Environment variables ---
TOKEN = os.getenv("BOT_TOKEN")  # Telegram bot token
BOT_USERNAME = '@summa_oru_bot'
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")  # Render HTTPS URL

if not TOKEN or not RENDER_URL:
    raise RuntimeError("BOT_TOKEN or RENDER_EXTERNAL_URL not set!")

WEBHOOK_URL = f"{RENDER_URL}/webhook"

# --- Flask app ---
app = Flask(__name__)

# --- Telegram bot application ---
application = Application.builder().token(TOKEN).build()


# --- Command handlers ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I think you’re as bored as me 😄")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_set = random.choice([True, False])
    help_text = (
        "Hi! I can respond to simple messages like:\n"
        "- 'hello' → I will say hi back!\n"
        "- 'how are you' → I will tell you how I am.\n"
        "- 'i love python' → I will reply with a fun message.\n\n"
        "You can also use these commands:\n"
        "/start → Greet the bot\n"
        "/bye → Say goodbye to the bot\n"
        "/stop → Stop the bot (admin only)"
    ) if random_set else "Sorry!! no time 😅"
    await update.message.reply_text(help_text)


async def bye_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bye!! See you later 👋")


def handle_response(text: str) -> str:
    text = text.lower()
    if "hello" in text:
        return "Hey there!"
    if "how are you" in text:
        return "I am good!"
    return "I do not understand what you wrote 🤔"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = handle_response(update.message.text)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# --- Add handlers ---
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("bye", bye_command))
application.add_handler(MessageHandler(filters.TEXT, handle_message))
application.add_error_handler(error)


# --- Flask webhook route ---
@app.route("/webhook", methods=["POST"])
def webhook():
    """Receive updates from Telegram"""
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"


# --- Flask root route (optional) ---
@app.route("/")
def index():
    return "Telegram bot is running on Render!"


# --- Set webhook on startup ---
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")


# --- Start Flask app ---
if __name__ == "__main__":
    import asyncio

    # Set webhook before running Flask
    asyncio.run(set_webhook())

    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
