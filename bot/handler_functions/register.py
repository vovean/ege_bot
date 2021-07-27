from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import get_state_keyboard, ConversationState
from db.models import TGUser


def register(upd: Update, ctx: CallbackContext):
    name = upd.message.text.strip()
    if '\n' in name:
        upd.message.reply_text("Имя должно состоять из одной строки. Пожалуйста, попробуйте еще раз")
        return
    if len(name) > 60:
        upd.message.reply_text("Имя не должно быть длиннее 60 символов. Пожалуйста, попробуйте еще раз")
        return
    tguser = TGUser.objects.create(telegram_id=upd.effective_user.id, name=name)
    ctx.user_data['tguser'] = tguser
    upd.effective_user.send_message(
        f"Привет, {name}! Теперь можешь приступать к заданиям",
        reply_markup=get_state_keyboard(ConversationState.MAIN_MENU, ctx)
    )
    return ConversationState.MAIN_MENU
