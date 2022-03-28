from dataclasses import dataclass

from environs import Env
from google.cloud import dialogflow
from google.cloud.dialogflow_v2.types import session as gcd_session

# Load environment variables
env = Env()
env.read_env()

# Constants
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


def create_reply(response: gcd_session.DetectIntentResponse) -> Reply:
    """Creates reply object"""
    reply_text: str = response.query_result.fulfillment_text
    is_fallback: bool = response.query_result.intent.is_fallback

    return Reply(text=reply_text, is_fallback=is_fallback)


def get_reply(text: str, session_id: int) -> Reply:
    response = detect_intent(session_id=session_id, text=text)
    reply = create_reply(response)
    return reply
