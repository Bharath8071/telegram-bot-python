from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask, request
import os, random

TOKEN: Final = os.getenv("BOT_TOKEN")  # safer than hardcoding
BOT_USERNAME: Final = '@summa_oru_bot'

# --- Telegram Handlers ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I think you’re as bored as me 😄")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_set = random.choice([True, False])
    if random_set:
        help_text = (
            "Hi! I can respond to simple messages like:\n"
            "- 'hello' → I will say hi back!\n"
            "- 'how are you' → I will tell you how I am.\n"
            "- 'i love python' → I will reply with a fun message.\n\n"
            "You can also use these commands:\n"
            "/start → Greet the bot\n"
            "/bye → Say goodbye to the bot\n"
            "/stop → Stop the bot (admin only)"
        )
    else:
        help_text = "Sorry!! no time 😅"

    await update.message.reply_text(help_text)

async def bye_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bye!! See you later 👋")

def handle_response(text: str) -> str:
    text = text.lower()
    if 'hello' in text:
        return 'Hey there!'
    if 'how are you' in text:
        return 'I am good!'
    return 'I do not understand what you wrote 🤔'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = handle_response(text)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# --- Flask App for Render ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"


# --- Telegram Bot Setup ---
application = Application.builder().token(TOKEN).build()

application.add_handler(CommandHandler('start', start_command))
application.add_handler(CommandHandler('help', help_command))
application.add_handler(CommandHandler('bye', bye_command))
application.add_handler(MessageHandler(filters.TEXT, handle_message))
application.add_error_handler(error)

# --- Start Webhook ---
if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))
    URL = f"https://{os.environ.get('RENDER_EXTERNAL_URL')}/webhook"

    # set webhook dynamically on startup
    import asyncio
    async def set_webhook():
        await application.bot.set_webhook(URL)
        print(f"Webhook set to {URL}")

    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=PORT)
