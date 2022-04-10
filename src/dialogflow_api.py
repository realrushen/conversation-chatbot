from dataclasses import dataclass

from environs import Env
from google.cloud import dialogflow
from google.cloud.dialogflow_v2.types import session as gcd_session

env = Env()
env.read_env()

LANGUAGE_CODE = 'ru-RU'
PROJECT_ID = env.str('PROJECT_ID')


@dataclass
class Reply:
    text: str
    is_fallback: bool


def detect_intent(session_id: int, text: str, project_id: str = PROJECT_ID,
                  language_code: str = LANGUAGE_CODE) -> gcd_session.DetectIntentResponse:
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

    return response


def get_reply(text: str, session_id: int) -> Reply:
    """Reply using DialogFlow model"""
    response = detect_intent(session_id=session_id, text=text)
    return Reply(
        text=response.query_result.fulfillment_text,
        is_fallback=response.query_result.intent.is_fallback,
    )
