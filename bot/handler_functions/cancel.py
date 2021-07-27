from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import get_state_keyboard, ConversationState


def cancel(upd: Update, ctx: CallbackContext):
    upd.effective_user.send_message("Окей, возвращаю тебя в главное меню",
                                    reply_markup=get_state_keyboard(ConversationState.MAIN_MENU, ctx))
    return ConversationState.MAIN_MENU
