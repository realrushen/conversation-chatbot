import argparse
import logging
from dataclasses import dataclass
from pprint import pprint

import requests
from environs import Env
from google.cloud import dialogflow

env = Env()
env.read_env()

PROJECT_ID = env.str('PROJECT_ID')

logger = logging.getLogger(__name__)


@dataclass
class Intent:
    name: str
    questions: list[str]
    answer: str


def create_intent(project_id: str, display_name: str,
                  training_phrases_parts: list[str], message_texts: list[str]) -> None:
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    logger.info('Intent created: %s' % response)


def is_json(url: str) -> bool:
    response = requests.head(url, allow_redirects=True)
    response.raise_for_status()
    header = response.headers
    content_type = header.get('content-type')

    return 'json' in content_type


def get_intents(url: str) -> list[Intent]:
    intents = []
    if is_json(url):
        intents_dict: dict = requests.get(url).json()
        for intent_name, intent_contents in intents_dict.items():
            intent_questions = intent_contents['questions']
            intent_answer = intent_contents['answer']
            intent = Intent(name=intent_name, questions=intent_questions, answer=intent_answer)
            intents.append(intent)
    logger.info('Found %d intents', len(intents))
    return intents


def main() -> None:
    parser = argparse.ArgumentParser(description='Script to learn DialogFlow model')
    parser.add_argument('url', type=str, help='Url to json file with learning data')
    parser.add_argument('-d', '--debug', action='store_true', help='Runs script with logging level DEBUG')
    args = parser.parse_args()

    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging_level
    )

    intents = get_intents(args.url)

    for intent in intents:
        create_intent(
            project_id=PROJECT_ID,
            display_name=intent.name,
            training_phrases_parts=intent.questions,
            message_texts=[intent.answer]
        )


if __name__ == '__main__':
    main()
