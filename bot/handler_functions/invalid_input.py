from telegram import Update
from telegram.ext import CallbackContext


def invalid_input(upd: Update, ctx: CallbackContext):
    upd.message.reply_text("Введены некорректные данные, попробуйте еще раз или /cancel чтобы отменить команду")
