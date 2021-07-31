from django.core.files.base import ContentFile
from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import ConversationState, get_filename_to_save


def get_problem_pic(upd: Update, ctx: CallbackContext):
    attachment = upd.message.effective_attachment
    if isinstance(attachment, list):
        attachment = attachment[-1]
    tg_file = attachment.get_file()
    file = tg_file.download_as_bytearray()
    dj_file = ContentFile(
        bytes(file),
        name=get_filename_to_save(upd.effective_user.id, ctx.user_data['adding_task']['number'],
                                  tg_file.file_path.split('.')[-1])
    )
    ctx.user_data['adding_task']['problem_pic'] = dj_file
    upd.effective_user.send_message(
        "Отлично! Теперь отправь ответ на задачу текстовым сообщением"
    )
    return ConversationState.ADD_TASKS_ANSWER
