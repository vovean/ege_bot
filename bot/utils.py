from datetime import datetime
from enum import Enum

from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackContext


class ConversationState(Enum):
    REGISTER = 1
    MAIN_MENU = 2
    ADD_TASKS_NUMBER = 3
    ADD_TASKS_PROBLEM = 4
    ADD_TASKS_ANSWER = 5
    ADD_TASKS_LINK = 6
    ADD_TASKS_NEXT_STEP = 7
    SOLVE_TASK_ANSWER = 8


TASKS_COUNT = 19
TASKS = [list(map(str, range(1, 20)[i: i + 5])) for i in range(0, TASKS_COUNT + 1, 5)]


def get_main_kb(admin: bool):
    return ReplyKeyboardMarkup([
        *TASKS,
        ['Статистика'] if not admin else ['Статистика', 'Добавить задание']
    ])


def get_only_tasks_kb(*_):
    return ReplyKeyboardMarkup([
        *TASKS
    ])


def get_add_task_after_add_kb(*_):
    return ReplyKeyboardMarkup([
        ['В главное меню', 'Добавить еще задание']
    ])


def get_solve_task_kb(*_):
    return ReplyKeyboardMarkup([
        ['Другая задача']
    ])


def get_state_keyboard(state, ctx: CallbackContext):
    is_admin = ctx.user_data['tguser'].is_admin if 'tguser' in ctx.user_data else False
    return {
        ConversationState.MAIN_MENU: get_main_kb,
        ConversationState.ADD_TASKS_NUMBER: get_only_tasks_kb,
        ConversationState.ADD_TASKS_NEXT_STEP: get_add_task_after_add_kb,
        ConversationState.SOLVE_TASK_ANSWER: get_solve_task_kb
    }[state](is_admin)


def get_filename_to_save(user_id, task_number, extension):
    return f'{task_number}_{user_id}_{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}.{extension}'
