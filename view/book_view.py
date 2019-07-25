# In the name of God
from typing import List

from betterreads.book import GoodreadsBook
from telegram import Bot, ReplyKeyboardMarkup, parsemode

from config import Config
from view.constant_messages import Keyboard, CommonStrings, ratings


class BookView:
    search_title = "برای جستجو می‌توانید *عنوان،‌ نام نویسنده یا ISBN کتاب* را وارد کنید."
    search_result_title = "نتیجهٔ جستجو: "
    book_detail = "{index}-" + " [{title}](send:{book_index}) " + CommonStrings.new_line + \
                  "نویسنده(ها): {author} " + CommonStrings.new_line + "امتیاز: {rating}" + CommonStrings.double_new_line
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

        for book in sorted(books[index: index + Config.max_per_page], key=lambda b: b.average_rating):
            text += self.book_detail.format(index=index + 1,
                                            rating=ratings[int(book.average_rating)],
                                            title=book.title,
                                            book_index=index + 1,
                                            author="-".join(str(author) for author in book.authors)+".")
            index += 1

        book_btns = []
        if index != len(books):
            book_btns.append([Keyboard.next_page])

        book_btns.append([Keyboard.main_menu])
        reply_markup = ReplyKeyboardMarkup(keyboard=book_btns)
        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup,
                              parse_mode=parsemode.ParseMode.MARKDOWN)

    def send_search_failed(self, chat_id):
        keyboard = [[Keyboard.main_menu]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
        self.bot.send_message(chat_id=chat_id, text=self.not_found, reply_markup=reply_markup)

    def send_book_detail(self, chat_id, book: GoodreadsBook):
        text = self.book_caption.format(book.title, ratings[int(book.average_rating)], book.description)
        keyboard = [[Keyboard.main_menu]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
