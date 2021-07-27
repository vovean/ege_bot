from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from bot.utils import get_state_keyboard, ConversationState
from db.models import TGUser


def start(upd: Update, ctx: CallbackContext):
    tguser = TGUser.objects.filter(telegram_id=upd.effective_user.id)
    if tguser.exists():
        ctx.user_data['tguser'] = tguser.first()
        upd.effective_user.send_message(
            'Привет! С возвращением!',
            reply_markup=get_state_keyboard(ConversationState.MAIN_MENU, ctx)
        )
        return ConversationState.MAIN_MENU
    upd.effective_user.send_message(
        'Привет! Представься, пожалуйста, как тебя зовут?',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationState.REGISTER
