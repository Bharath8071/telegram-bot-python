# Telegram Chatbot

A beginner-friendly Telegram bot built with Python using python-telegram-bot.
The bot responds to messages, handles commands, and can be easily extended.

## Table of Contents

- [Features](features)
- [Tech Stack](tech-stack)
- [Installation](installation)
- [Project Working](project-working)
- [Configuration](configuration)
- [License](license)

## Features
- Responds to /start and /help commands
- Easy to extend with custom commands
- Beginner-friendly setup

## Tech Stack
- Python 3.9+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot?utm_source=chatgpt.com)

## Installation
**Follow these steps to set up the Telegram bot on your local machine:**
1. Clone the repository
```
    Download the project to your computer using Git:

      git clone https://github.com/YourUsername/telegram-chatbot.git

      cd telegram-chatbot
```

2) Install Python dependencies
```
   Make sure you have Python 3.9+ installed. Then install the required packages:

      pip install -r requirements.txt
```

3) Create your private configuration file
```
   Copy the template configuration file to a new file named `config.py`:

      cp config_template.py config.py
```
4) Open config.py and add your Telegram bot token and bot name:
```
      BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

      BOT_NAME = "YourBot"
```
5) Run the bot

   Start the bot with:

6) python main.py

   Your bot should now be live on Telegram and ready to respond to commands.

## Project Working

The bot works as follows:

1. Bot Setup

    - Connects to Telegram via Bot API using your token.

2. Message Handling

    - Listens for user messages in real-time.

    - Responds to commands like `/start`, `/help`, `/bye`.

3. Private Config

    - Your real `config.py` contains the token and bot name.
    - `.gitignore` ensures it is never pushed to GitHub.

## Configuration

- config_template.py → included in the repo, safe for public

- config.py → your private config, never push

- Example config.py content:

## License

This project is licensed under the MIT License. See the LICENSE file for details.
