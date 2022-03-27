#!/usr/bin/env python3

import logging
import random

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

# Load environment variables
from src.dialogflow_api import detect_intent

env = Env()
env.read_env()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Constants
VK_BOT_TOKEN = env.str('VK_BOT_TOKEN')
RANDOM_ID = random.randint(1, 1000)


def reply_customer(event, vk_api):
    """
    Reply customer using DialogFlow model.
    Do nothing if intent was not recognized
    """
    user_id = event.user_id
    text = event.text
    intent = detect_intent(session_id=user_id, text=text)

    if not intent.is_fallback:
        vk_api.messages.send(
            user_id=user_id,
            message=intent.fulfilment_text,
            random_id=RANDOM_ID
        )


def main():
    vk_session = vk.VkApi(token=VK_BOT_TOKEN)
    vk_api = vk_session.get_api()
    longpolling = VkLongPoll(vk_session)
    for event in longpolling.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_customer(event, vk_api)


if __name__ == "__main__":
    main()
