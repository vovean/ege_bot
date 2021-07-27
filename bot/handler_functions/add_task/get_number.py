from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from bot.utils import ConversationState


def get_number(upd: Update, ctx: CallbackContext):
    number = int(upd.message.text)
    if not (1 <= number <= 19):
        upd.message.reply_text("Такого задания нет, допустимые номера заданий: 1 - 19. Попробуйте еще раз")
        return
    ctx.user_data['adding_task']['number'] = number
    upd.effective_user.send_message(
        "Отлично, теперь пришли мне условие. Это может быть текст или картинка",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationState.ADD_TASKS_PROBLEM
