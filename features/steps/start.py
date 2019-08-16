# In the name of God

from unittest.mock import Mock

from behave import given, when, then

from controller.bot_states import BotStates
from controller.start_controller import StartController


@given('a bot and update from server')
def step_impl(context):
    context.bot = Mock()
    context.update = Mock()
    context.dispatcher = Mock()
    context.start_controller = StartController(dispatcher=context.dispatcher, bot=context.bot)


@when('user send /start')
def step_impl(context):
    context.first_step = context.start_controller.start(context.bot, context.update)
    print(f"first step return value is {context.first_step}")


@then('send main menu')
def step_impl(context):
    assert context.first_step == BotStates.MENU
