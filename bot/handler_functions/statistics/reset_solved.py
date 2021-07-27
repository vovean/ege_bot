from telegram import Update
from telegram.ext import CallbackContext

from db.models import TaskAttempt


def reset_solved(upd: Update, ctx: CallbackContext):
    user = ctx.user_data['tguser']
    TaskAttempt.objects.filter(user=user).delete()
    upd.effective_user.send_message("Статистика решенных заданий была сброшена. Теперь можно решить все задачи заново")
