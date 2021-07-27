from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.utils import get_state_keyboard, ConversationState


def next_step(upd: Update, ctx: CallbackContext):
    text = upd.message.text
    if text == 'В главное меню':
        upd.effective_user.send_message(
            "Окей, возвращаю в главное меню",
            reply_markup=get_state_keyboard(ConversationState.MAIN_MENU, ctx)
        )
        return ConversationHandler.END
    else:
        upd.effective_user.send_message(
            "Какое задание ты хочешь добавить?",
            reply_markup=get_state_keyboard(ConversationState.ADD_TASKS_NUMBER, ctx)
        )
        ctx.user_data['adding_task'] = dict()
        return ConversationState.ADD_TASKS_NUMBER
