#!/usr/bin/env python3

import logging
import random

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from src.dialogflow_api import get_reply

# Load environment variables
env = Env()
env.read_env()

# Constants
VK_BOT_TOKEN = env.str('VK_BOT_TOKEN')
DEBUG = env.int('DEBUG')

# Enable logging
if DEBUG:
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging_level
)

logger = logging.getLogger(__name__)



def reply_customer(event, vk_api):
    """
    Reply customer using DialogFlow model.
    Do nothing if intent was not recognized
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


def main():
    vk_session = vk.VkApi(token=VK_BOT_TOKEN)
    vk_api = vk_session.get_api()
    longpolling = VkLongPoll(vk_session)
    for event in longpolling.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_customer(event, vk_api)


if __name__ == "__main__":
    main()
