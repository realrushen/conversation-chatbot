#!/usr/bin/env python3
import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from src.dialogflow_api import get_reply
from src.log_handlers import TelegramChatHandler

# Load environment variables from .env file
env = Env()
env.read_env()

# Constants
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
LOGS_BOT_TOKEN = env.str('LOGS_BOT_TOKEN')
CHAT_ID_FOR_LOGS = env.str('CHAT_ID_FOR_LOGS')
DEBUG = env.int('DEBUG')

logger = logging.getLogger(__name__)


def reply_customer(update: Update, context: CallbackContext) -> None:
    """Reply customer using DialogFlow model"""
    chat_id = update.message.chat_id
    text = update.message.text
    reply = get_reply(text=text, session_id=chat_id)
    update.message.reply_text(reply.text)


def log_error(update: Update, context: CallbackContext) -> None:
    """Log exception while handling update"""
    logger.exception(context.error)


def main() -> None:
    """Start the bot."""
    # Enable logging
    if DEBUG:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging_level
    )
    telegram_handler = TelegramChatHandler(token=LOGS_BOT_TOKEN, chat_id=CHAT_ID_FOR_LOGS)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    telegram_handler.setFormatter(formatter)
    logger.addHandler(telegram_handler)
    # Bot initialisation
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_customer))
    dispatcher.add_error_handler(log_error)
    logger.info('Telegram support bot started')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
