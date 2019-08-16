# In The name of God
from betterreads import client
from telegram import Bot
from telegram.ext import Updater

from config import Config
from controller.book_controller import BookController
from controller.start_controller import StartController
from loguru import logger
import logging

if __name__ == '__main__':
    logger.info("bot started")
    logging.basicConfig(level=logging.DEBUG)
    goodreads_client = client.GoodreadsClient(client_key=Config.goodi_token, client_secret=Config.goodi_secret)
    bot = Bot(token=Config.bot_token, base_url=Config.base_url, base_file_url=Config.base_file_url)
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher
    StartController(dispatcher, bot)
    BookController(dispatcher, bot, goodreads_client)
    updater.start_polling()
