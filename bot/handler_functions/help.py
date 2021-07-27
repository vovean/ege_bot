from telegram import Update
from telegram.ext import CallbackContext


def get_help(upd: Update, ctx: CallbackContext):
    upd.effective_user.send_message(
        """
Это бот для решения заданий, посвященных ЕГЭ

/start - начать взаимодействие с ботом, обновить информацию о пользователе (при получении админа), вернуться в главное меню
/cancel - отмена команды, возвращение в главное меню
/reset_solved - сбросить статистику решенных задач (в том числе позволяет перерешать уже решенные задачи)
        """
    )
