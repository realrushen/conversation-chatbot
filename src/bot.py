#!/usr/bin/env python3

import logging

from google.cloud import dialogflow
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env

# Load environment variables from .env file
env = Env()
env.read_env()

# Constants
LANGUAGE_CODE = 'ru-RU'
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
PROJECT_ID = env.str('PROJECT_ID')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(text='Здравствуйте')




def detect_intent_text(session_id: object, text: object, project_id: str = PROJECT_ID, language_code: str = LANGUAGE_CODE) -> str:
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text

def reply_customer(update: Update, context: CallbackContext) -> None:
    """Reply customer using DialogFlow model"""
    chat_id = update.message.chat_id
    text = update.message.text
    reply = detect_intent_text(session_id=chat_id, text=text)
    update.message.reply_text(reply)



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
