#!/usr/bin/env python3

import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables from .env file
from src.dialogflow_api import detect_intent

env = Env()
env.read_env()

# Constants
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(text='Здравствуйте')


def reply_customer(update: Update, context: CallbackContext) -> None:
    """Reply customer using DialogFlow model"""
    chat_id = update.message.chat_id
    text = update.message.text
    intent = detect_intent(session_id=chat_id, text=text)
    update.message.reply_text(intent.fulfillment_text)


def main() -> None:
    """Start the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_customer))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
