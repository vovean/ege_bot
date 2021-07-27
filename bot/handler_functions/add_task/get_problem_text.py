from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import ConversationState


def get_problem_text(upd: Update, ctx: CallbackContext):
    problem = upd.message.text
    ctx.user_data['adding_task']['problem_text'] = problem
    upd.effective_user.send_message(
        "Отлично! Теперь отправь ответ на задачу текстовым сообщением"
    )
    return ConversationState.ADD_TASKS_ANSWER
