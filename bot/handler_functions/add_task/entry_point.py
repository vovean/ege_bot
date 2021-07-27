from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.utils import ConversationState, get_state_keyboard


def entry_point(upd: Update, ctx: CallbackContext):
    if not ctx.user_data['tguser'].is_admin:
        return ConversationHandler.END
    upd.effective_user.send_message(
        "Какое задание ты хочешь добавить?",
        reply_markup=get_state_keyboard(ConversationState.ADD_TASKS_NUMBER, ctx)
    )
    ctx.user_data['adding_task'] = dict()
    return ConversationState.ADD_TASKS_NUMBER
