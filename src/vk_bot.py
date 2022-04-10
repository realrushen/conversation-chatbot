#!/usr/bin/env python3

import logging
import random

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_api import get_reply
from log_handlers import TelegramChatHandler

env = Env()
env.read_env()

# Constants
VK_BOT_TOKEN = env.str('VK_BOT_TOKEN')
LOGS_BOT_TOKEN = env.str('LOGS_BOT_TOKEN')
CHAT_ID_FOR_LOGS = env.int('CHAT_ID_FOR_LOGS')
DEBUG = env.bool('DEBUG')

logger = logging.getLogger(__name__)


def reply_customer(event, vk_api):
    """
    Reply customer using DialogFlow model.
    Do nothing if intent was not recognized.
    """
    user_id = event.user_id
    text = event.text
    reply = get_reply(text=text, session_id=user_id)

    if not reply.is_fallback:
        vk_api.messages.send(
            user_id=user_id,
            message=reply.text,
            random_id=random.randint(1, 1000)
        )
    else:
        logger.debug('FALLBACK intent on "%s"' % text)


def start_polling():
    """Starts long polling to VK API"""
    vk_session = vk.VkApi(token=VK_BOT_TOKEN)
    vk_api = vk_session.get_api()
    longpolling = VkLongPoll(vk_session)
    logger.info('VK support bot started')

    for event in longpolling.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply_customer(event, vk_api)
        except Exception as e:
            logger.error(e)


def main():
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

    start_polling()
    logger.info('VK support bot stopped')


if __name__ == "__main__":
    main()
