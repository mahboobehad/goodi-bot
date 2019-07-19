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
    book_caption = '''
    عنوان کتاب: *{}*
    امتیاز کتاب: {} 
    معرفی:
{}
    '''

    def __init__(self, bot: Bot):
        self.bot = bot

    def send_search_message(self, chat_id):
        keyboard = [[Keyboard.main_menu]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
        self.bot.send_message(chat_id=chat_id, text=self.search_title, reply_markup=reply_markup)

    def send_book_search_result(self, chat_id, books: List[GoodreadsBook], index):
        text = self.search_result_title + CommonStrings.double_new_line

        book_btns = []
        for book in sorted(books, key=lambda b: b.average_rating):
            book_btns.append([book.title])

        book_btns.append([Keyboard.main_menu])
        reply_markup = ReplyKeyboardMarkup(keyboard=book_btns)
        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def send_search_failed(self, chat_id):
        keyboard = [[Keyboard.main_menu]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
        self.bot.send_message(chat_id=chat_id, text=self.not_found, reply_markup=reply_markup)

    def send_book_detail(self, chat_id, book: GoodreadsBook):
        text = self.book_caption.format(book.title, ratings[int(book.average_rating)], book.description)
        keyboard = [[Keyboard.main_menu]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
