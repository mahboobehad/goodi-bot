# In the name of God
from telegram import Bot, Update
from telegram.ext import ConversationHandler, CommandHandler, RegexHandler, Dispatcher

from controller.bot_states import BotStates
from view.constant_messages import Keyboard
from view.start_view import StartView


class StartController:
    def __init__(self, dispatcher: Dispatcher, bot: Bot):
        self.view = StartView(bot)
        self.dispatcher = dispatcher
        self.conversation_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={BotStates.MENU: [RegexHandler(pattern=Keyboard.main_menu, callback=self.main_menu)]},
            fallbacks={}, allow_reentry=True)
        self.dispatcher.add_handler(self.conversation_handler)
        self.dispatcher.add_handler(RegexHandler(pattern=Keyboard.main_menu, callback=self.main_menu))

    def start(self, bot: Bot, update: Update):
        chat_id = update.effective_chat.id
        self.view.send_start_message(chat_id)
        return BotStates.MENU

    def main_menu(self, bot: Bot, update: Update):
        chat_id = update.effective_chat.id
        self.view.send_main_menu(chat_id)
        return ConversationHandler.END
