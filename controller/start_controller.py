# In the name of God
from telegram import Bot, Update
from telegram.ext import ConversationHandler, CommandHandler, RegexHandler, Dispatcher

from view.constant_messages import Keyboard
from view.start_view import StartView


class StartController:
    def __init__(self, dispatcher: Dispatcher, bot: Bot):
        self.view = StartView(bot)
        self.dispatcher = dispatcher
        self.conversation_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start),
                          RegexHandler(pattern=Keyboard.main_menu, callback=self.main_menu)
                          ],
            states={},
            fallbacks={}
        )
        self.dispatcher.add_handler(self.conversation_handler)
        self.user_data = {}

    def add_user_data(self, user_id, key, value):
        if not user_id in self.user_data.keys():
            self.user_data[user_id] = {key: value}
        else:
            self.user_data[user_id].update({key: value})

    def start(self, bot: Bot, update: Update):
        chat_id = update.effective_chat.id
        self.view.send_start_message(chat_id)

    def main_menu(self, bot: Bot, update: Update):
        chat_id = update.effective_chat.id
        self.view.send_main_menu(chat_id)
