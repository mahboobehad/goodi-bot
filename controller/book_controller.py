# In the name of God
from telegram import Update, Bot
from telegram.ext import ConversationHandler, MessageHandler, RegexHandler, Filters
from betterreads import client

from config import Config
from controller.bot_states import BotStates
from controller.start_controller import StartController
from view.book_view import BookView
from view.constant_messages import Keyboard


class BookController(StartController):
    def __init__(self, dispatcher, bot, goodreads_client: client.GoodreadsClient):
        StartController.__init__(self, dispatcher, bot)
        self.view = BookView(bot)
        self.conversation_handler = ConversationHandler(
            entry_points=[RegexHandler(pattern=Keyboard.search_book, callback=self.search_book)],
            states={BotStates.BOOK_INFO: [MessageHandler(filters=Filters.text, callback=self.get_book_info)],
                    BotStates.NEXT_SEARCH_RESULT: [
                        RegexHandler(pattern=Keyboard.next_page, callback=self.get_book_info)]
                    },
            fallbacks={})
        self.dispatcher.add_handler(self.conversation_handler)
        self.goodreads_client = goodreads_client

    def search_book(self, update: Update):
        chat_id = update.effective_chat.id
        self.view.send_search_message(chat_id)
        return BotStates.BOOK_INFO

    def get_book_info(self, update: Update):
        chat_id = update.effective_chat.id
        search_query = update.effective_message.text
        books = self.goodreads_client.search_books(search_query)
        index = 1
        if books:
            self.view.send_book_search_result(chat_id, books, index)
        else:
            self.view.send_search_failed(chat_id)
