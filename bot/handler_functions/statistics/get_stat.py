from django.db.models import Sum
from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import TASKS_COUNT
from db.models import TaskAttempt, Task


def get_stat(upd: Update, ctx: CallbackContext):
    tguser = ctx.user_data['tguser']
    msg = ""
    for task_num in range(1, TASKS_COUNT + 1):
        tasks = Task.objects.filter(number=task_num)
        attempts = TaskAttempt.objects.filter(task__in=tasks, user=tguser)
        total_tasks = tasks.count()
        total_attempts = attempts.aggregate(Sum('attempts_count'))['attempts_count__sum'] or 0
        correct_attempts = attempts.filter(solved=True).count()
        try:
            correct_percent = correct_attempts / total_attempts * 100
        except ZeroDivisionError:
            correct_percent = 0
        msg += f"#{task_num}:\n" \
               f"\tДоступно заданий: {total_tasks}\n" \
               f"\tОтправлено решений: {total_attempts}\n" \
               f"\tИз них правильных {correct_attempts} ({correct_percent:.1f}%)\n" \
               f"\tИтого решено: {correct_attempts} / {total_tasks}\n\n"
    upd.effective_user.send_message(msg)
