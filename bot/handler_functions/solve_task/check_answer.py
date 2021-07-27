from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.utils import get_state_keyboard, ConversationState
from db.models import TaskAttempt


def check_answer(upd: Update, ctx: CallbackContext):
    ans = upd.message.text.strip()
    correct = ans == ctx.user_data['solving_task']['task'].answer
    attempt, created = TaskAttempt.objects.get_or_create(
        user=ctx.user_data['tguser'],
        task=ctx.user_data['solving_task']['task']
    )
    attempt.attempts_count += 1
    if not correct:
        link = attempt.task.link_to_lesson
        upd.message.reply_text(
            f"Не правильно, попробуй еще раз (или /cancel чтобы вернуться в главное меню)\n"
            f"Ты можешь найти разбор здесь {link}" if link != '-' else ""
        )
        attempt.save()
        return
    attempt.solved = True
    attempt.save()
    upd.effective_user.send_message(
        "Правильно! Какое задание ты хочешь решить дальше?",
        reply_markup=get_state_keyboard(ConversationState.MAIN_MENU, ctx)
    )
    return ConversationHandler.END
