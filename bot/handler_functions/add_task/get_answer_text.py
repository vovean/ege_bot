from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import ConversationState


def get_answer(upd: Update, ctx: CallbackContext):
    ans = upd.message.text.strip()
    ctx.user_data['adding_task']['answer'] = ans
    upd.effective_user.send_message(
        "Отлично, теперь отправь ссылку на урок, где объясняется это задание "
        "(или \"-\", если ссылки нет)"
    )
    return ConversationState.ADD_TASKS_LINK
