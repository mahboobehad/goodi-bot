# In the name of God
from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, RegexHandler, Filters
from betterreads import client

from controller.bot_states import BotStates
from controller.start_controller import StartController
from view.book_view import BookView
from view.constant_messages import Keyboard, CommonRegexes


class BookController(StartController):
    def __init__(self, dispatcher, bot, goodreads_client: client.GoodreadsClient):
        StartController.__init__(self, dispatcher, bot)
        self.view = BookView(bot)
        self.conversation_handler = ConversationHandler(
            entry_points=[RegexHandler(pattern=Keyboard.search_book, callback=self.search_book), ],
            states={BotStates.BOOK_INFO: [MessageHandler(filters=Filters.text, callback=self.get_book_info)],
                    BotStates.SHOW_BOOK: [
                        MessageHandler(filters=Filters.text, callback=self.show_book_detail)]
                    },
            fallbacks={})
        self.dispatcher.add_handler(self.conversation_handler)
        self.goodreads_client = goodreads_client

    def search_book(self, bot, update: Update):
        chat_id = update.effective_chat.id
        self.view.send_search_message(chat_id)
        return BotStates.BOOK_INFO

    def get_book_info(self, bot, update: Update):
        chat_id = update.effective_chat.id
        search_query = update.effective_message.text
        books = self.goodreads_client.search_books(search_query)
        index = 1
        if books:
            self.add_user_data(chat_id, "books", books)
            self.view.send_book_search_result(chat_id, books, index)
            return BotStates.SHOW_BOOK
        else:
            self.view.send_search_failed(chat_id)
            return ConversationHandler.END

    def show_book_detail(self, bot, update):
        chat_id = update.effective_chat.id
        book_title = update.effective_message.text
        book = list(filter(lambda b: b.title == book_title, self.get_user_data(chat_id, "books")))[0]
        self.view.send_book_detail(chat_id, book)
        return ConversationHandler.END
