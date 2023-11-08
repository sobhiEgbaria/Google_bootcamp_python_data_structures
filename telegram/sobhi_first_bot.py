import logging
import requests
import json

from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    Updater,
)

import bot_settings

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def age_of_celb(name):
    api_url = f"https://api.api-ninjas.com/v1/celebrity?name={name}"

    response = requests.get(
        api_url, headers={"X-Api-Key": "K7HUfTzDONfdXWfbw5qAYg==iC2g5EcqOJfP9Yg9"}
    )
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
    else:
        print("Error:", response.status_code, response.text)
    return data[0]["age"]


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    context.bot.send_message(chat_id=chat_id, text="hi this is sobhi from home")


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    response = text.replace("7", "💣")
    context.bot.send_message(chat_id=update.message.chat_id, text=age_of_celb(response))


my_bot = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
my_bot.dispatcher.add_handler(CommandHandler("start", start))
my_bot.dispatcher.add_handler(MessageHandler(Filters.text, respond))

logger.info("* Start polling...")
my_bot.start_polling()  # Starts polling in a background thread.
my_bot.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
