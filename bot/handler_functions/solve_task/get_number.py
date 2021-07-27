from django.db.models import Subquery
from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import ConversationState, get_state_keyboard
from db.models import Task, TaskAttempt


def get_not_solved_tasks(task_num, tguser):
    solved_tasks = TaskAttempt.objects.filter(
        task__number=task_num,
        user=tguser,
        solved=True
    )
    return Task.objects.filter(
        number=task_num
    ).exclude(
        id__in=Subquery(solved_tasks.values('task__id'))
    ).order_by('?')


def send_task_problem(task, upd, ctx):
    if task.problem_text:
        upd.effective_user.send_message(f"Условие:\n{task.problem_text}")
    else:
        with open(task.problem_pic.path, 'rb') as problem:
            upd.effective_user.send_photo(problem, caption="Условие")
    upd.effective_user.send_message(
        "Присылай ответ текстовым сообщением или нажми /cancel, чтобы вернуться в главное меню",
        reply_markup=get_state_keyboard(ConversationState.SOLVE_TASK_ANSWER, ctx)
    )


def get_number(upd: Update, ctx: CallbackContext):
    number = int(upd.message.text)
    if not (1 <= number <= 19):
        upd.message.reply_text("Такого задания нет, допустимые номера заданий: 1 - 19. Попробуйте еще раз")
        return
    tasks = get_not_solved_tasks(number, ctx.user_data['tguser'])
    if not tasks.exists():
        upd.message.reply_text(
            f"Ты уже решил все задания #{number}. Попробуй решить другие или сбрось учет решенных задач (/reset_solved)"
        )
        # Todo: /reset_solved
        return
    task = tasks.first()
    ctx.user_data['solving_task'] = {
        'task': task,
        'number': number
    }
    send_task_problem(task, upd, ctx)
    return ConversationState.SOLVE_TASK_ANSWER
