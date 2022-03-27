from environs import Env
from google.cloud import dialogflow

# Load environment variables
env = Env()
env.read_env()

# Constants
LANGUAGE_CODE = 'ru-RU'
PROJECT_ID = env.str('PROJECT_ID')


def detect_intent(session_id: object, text: object, project_id: str = PROJECT_ID,
                  language_code: str = LANGUAGE_CODE):
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

    return response.query_result.intent

