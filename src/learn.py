from dataclasses import dataclass

import requests
from environs import Env
from google.cloud import dialogflow

# Load environment variables from .env file
env = Env()
env.read_env()

PROJECT_ID = env.str('PROJECT_ID')


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

    print("Intent created: {}".format(response))


def is_json(url: str) -> bool:
    response = requests.head(url, allow_redirects=True)
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
    return intents


def main() -> None:
    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    intents = get_intents(url)
    if not intents:
        return
    for intent in intents:
        create_intent(
            project_id=PROJECT_ID,
            display_name=intent.name,
            training_phrases_parts=intent.questions,
            message_texts=[intent.answer]
        )


if __name__ == '__main__':
    main()
