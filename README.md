# Conversation ChatBot

![support-bot](https://user-images.githubusercontent.com/58989626/161416694-df986533-b7b4-4eae-8c35-3bbcaacf9e12.gif)

This project developed using [Python 3.9](https://www.python.org/downloads/release/python-390/) and
[DialogFlow](https://cloud.google.com/dialogflow/docs/) - natural language understanding platform that makes it easy to
design and integrate a conversational user interface.

This repository contains two bots. One for popular [Russsian Social Network VKontakte](https://vk.com/) and second
for [Telegram Messanger](https://telegram.org/). 

## How to Install and Run

Make sure you have installed [Python 3.9](https://www.python.org/downloads/release/python-390/)
and [poetry](https://python-poetry.org/docs/#installation)

1. Clone repository

```shell
git clone https://github.com/realrushen/conversation-chatbot.git
```

2. Init virtual environment and install dependencies

```shell
poetry install
```

3. Set environment variables from section bellow
4. Train DialogFlow model using `/src/learn.py` script from this repo. Detailed instructions see below.
5. Activate virtual environment and Run bots

```shell
poetry shell
python3 ./src/telegram_bot.py
python3 ./src/vk_bot.py
```

## Environment Variables

This environment variables are required to run bots:

* `DEBUG` - true/false to eneble/disable debug log messages.
* `LOGS_BOT_TOKEN` - telegram bot token that sends log messages. To register your bot you need register it with
  [BotFather](https://telegram.me/BotFather). It looks like this `958423683:AAEAtJ5Lde5YYfu8GldVhSG`.
* `CHAT_ID_FOR_LOGS` - chat_id in Telegram where you want to receive log massages.
* `TELEGRAM_BOT_TOKEN` - main telegram bot token to communicate with your customers.
* `VK_BOT_TOKEN` - same for vk.com.
* `GOOGLE_APPLICATION_CREDENTIALS` - absolute path to your DialogFlow credentials json file. Detailed
  instructions [here](https://cloud.google.com/dialogflow/es/docs/quick/setup).
* `PROJECT_ID` - project name from DialogFlow panel.

## Training DialogFlow model

Make sure you set environment `PROJECT_ID` and `GOOGLE_APPLICATION_CREDENTIALS` variables

1. Prepare data and generate json file with structure you can see below:

```json
{
  "intent_name1": {
    "answer": "answer1",
    "questions": [
      "question1",
      "question2",
      "question3"
    ]
  },
  "intent_name2": {
    "answer": "answer2",
    "questions": [
      "question4",
      "question5",
      "question6"
    ]
  }
}
```

2. Start model training using python script learn.py

```shell
python3 ./src/learn.py https://link.to/file.json
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
