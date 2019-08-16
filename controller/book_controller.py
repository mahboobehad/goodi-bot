# In the name of God

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, RegexHandler, Filters
from betterreads import client

from config import Config
from controller.bot_states import BotStates
from controller.start_controller import StartController
from view.book_view import BookView
from view.constant_messages import Keyboard, CommonRegexes


class BookController(StartController):
    def __init__(self, dispatcher, bot, goodreads_client: client.GoodreadsClient):
        StartController.__init__(self, dispatcher, bot)
        self.view = BookView(bot)
        self.conversation_handler = ConversationHandler(
            entry_points=[RegexHandler(pattern=Keyboard.search_book, callback=self.search_book, pass_user_data=True)],
            states={BotStates.BOOK_INFO: [MessageHandler(filters=Filters.text, callback=self.get_book_info,
                                                         pass_user_data=True)],
                    BotStates.SHOW_BOOK: [RegexHandler(pattern=CommonRegexes.numbers, callback=self.show_book_detail,
                                                       pass_user_data=True),
                                          RegexHandler(pattern=Keyboard.next_page, callback=self.get_book_info,
                                                       pass_user_data=True)]
                    },
            fallbacks={}, allow_reentry=True)

        self.dispatcher.add_handler(self.conversation_handler)
        self.goodreads_client = goodreads_client

    def search_book(self, bot, update: Update, user_data):
        chat_id = update.effective_chat.id
        user_data['index'] = None
        self.view.send_search_message(chat_id)
        return BotStates.BOOK_INFO

    def get_book_info(self, bot, update: Update, user_data):
        chat_id = update.effective_chat.id
        search_query = update.effective_message.text
        index = user_data['index']
        if not index:
            index = 0
            books = self.goodreads_client.search_books(search_query)
            user_data['books'] = books

        books = user_data['books']
        if books:
            self.view.send_book_search_result(chat_id, books, index)
            index += Config.max_per_page
            user_data['index'] = index
            return BotStates.SHOW_BOOK
        else:
            self.view.send_search_failed(chat_id)
            return ConversationHandler.END

    def show_book_detail(self, bot, update, user_data):
        chat_id = update.effective_chat.id
        book_index = int(update.effective_message.text) - 1
        book = user_data['books'][book_index]
        self.view.send_book_detail(chat_id, book)
        return ConversationHandler.END
