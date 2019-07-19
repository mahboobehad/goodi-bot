# In The name of God
from telegram import Bot
from telegram.ext import Updater

from config import Config
from controller.start_controller import StartController

if __name__ == '__main__':
    bot = Bot(token=Config.bot_token, base_url=Config.base_url, base_file_url=Config.base_file_url)
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher
    StartController(dispatcher, bot)
    updater.start_polling()
