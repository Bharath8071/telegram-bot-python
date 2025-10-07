from typing import Final
from  telegram import Update 
from telegram.ext import Application,CommandHandler,MessageHandler,filters, ContextTypes
import random

# Import config.py if exists, otherwise exit
if not os.path.exists("config.py"):
    print("Please create a config.py from config_template.py with your BOT_TOKEN")
    exit(1)

from config import BOT_TOKEN, BOT_NAME
TOKEN: Final = BOT_TOKEN
BOT_USERNAME: Final = BOT_NAME

async def start_command(update:Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello! hi i think you also was very board as like me.')   

async def help_command(update:Update,context: ContextTypes.DEFAULT_TYPE):
    random_set = random.choice([True, False])
    if random_set == True :
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
        
    else: help_text="sorry!! no time"
    
    await update.message.reply_text(f'{help_text}')

async def bye_command(update:Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'bye!! see you later')
    exit(0)

def handle_response (text):
    user_input = text.lower()

    if 'hello' in  user_input:
        return 'Hey there!'
    if 'how are you' in  user_input:
        return 'I am good!'
    
    return 'I do not understand what you wrote'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print("stating....")
    app = Application.builder().token(TOKEN).build()


    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('bye',bye_command))
   # app.add_handler(MessageHandler(filters.text,handle_message))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print("poling.....")

    app.run_polling(poll_interval=3)
