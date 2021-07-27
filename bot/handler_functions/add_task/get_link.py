from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import get_state_keyboard, ConversationState
from db.models import Task


def get_link(upd: Update, ctx: CallbackContext):
    link = upd.message.text.strip()
    ctx.user_data['adding_task']['link_to_lesson'] = link
    Task.objects.create(**ctx.user_data['adding_task'])
    upd.effective_user.send_message(
        "Отлично! Добавили задание в базу. Что хочешь делать дальше?",
        reply_markup=get_state_keyboard(ConversationState.ADD_TASKS_NEXT_STEP, ctx)
    )
    return ConversationState.ADD_TASKS_NEXT_STEP
