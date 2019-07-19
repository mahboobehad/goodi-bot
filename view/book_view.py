# In the name of God
from typing import List

from betterreads.book import GoodreadsBook
from telegram import Bot, ReplyKeyboardMarkup

from view.constant_messages import Keyboard, CommonStrings, ratings


class BookView:
    search_title = "برای جستجو می‌توانید *عنوان،‌ نام نویسنده یا ISBN کتاب* را وارد کنید."
    search_result_title = "نتیجهٔ جستجو: "
    book_detail = " {}-عنوان کتاب:" + CommonStrings.new_line + "[{}]({}) " + CommonStrings.new_line + "نویسنده: *{}* " + CommonStrings.new_line + "امتیاز: *{}*" + CommonStrings.double_new_line
    not_found = "کتابی با مشخصاتی که وارد کردید پیدا نشد."

    def __init__(self, bot: Bot):
        self.bot = bot

    def send_search_message(self, chat_id):
        keyboard = [[Keyboard.main_menu]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
        self.bot.send_message(chat_id=chat_id, text=self.search_title, reply_markup=reply_markup)

    def send_book_search_result(self, chat_id, books: List[GoodreadsBook], index):
        text = self.search_result_title + CommonStrings.double_new_line

        for book in sorted(books, key=lambda b: b.average_rating):
            curr_text = self.book_detail.format(index, book.title, index - 1,book.authors[0],
                                                ratings[int(book.average_rating)])
            text += curr_text
            index += 1

        keyboard = [[Keyboard.main_menu]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def send_search_failed(self, chat_id):
        keyboard = [[Keyboard.main_menu]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
        self.bot.send_message(chat_id=chat_id, text=self.not_found, reply_markup=reply_markup)
