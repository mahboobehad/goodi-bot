# In the name of God
from telegram import Bot, ReplyKeyboardMarkup

from view.constant_messages import Keyboard


class StartView:
    start_message = "سلام! من یک بات متصل به goodreads هستم. فعلا می‌تونی با من در بین کتاب‌ها جستجو کنی."
    main_menu_title = "یکی از گزینه‌های زیر رو انتخاب کن!"
    def __init__(self, bot:Bot):
        self.bot = bot

    def send_start_message(self, chat_id):
        reply_keyboard = [[Keyboard.main_menu]]
        reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
        self.bot.send_message(chat_id=chat_id, text=self.start_message, reply_markup=reply_markup)

    def send_main_menu(self, chat_id):
        reply_keyboard = [[Keyboard.search_book]]
        reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
        self.bot.send_message(chat_id=chat_id, text=self.main_menu_title, reply_markup=reply_markup)
