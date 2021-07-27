from telegram import Update
from telegram.ext import CallbackContext

from bot.handler_functions.solve_task.get_number import get_not_solved_tasks, send_task_problem
from bot.utils import ConversationState


def another_task(upd: Update, ctx: CallbackContext):
    task = ctx.user_data['solving_task']['task']
    tasks = get_not_solved_tasks(
        ctx.user_data['solving_task']['number'], ctx.user_data['tguser']
    ).exclude(id=task.id)
    if not tasks.exists():
        upd.effective_user.send_message("Других заданий этого номера нет")
    else:
        task = tasks.first()
        ctx.user_data['solving_task'].update({
            'task': task
        })
    send_task_problem(task, upd, ctx)
    return ConversationState.SOLVE_TASK_ANSWER
