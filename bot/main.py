import os

import django

from settings.settings import TG_TOKEN

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from telegram.ext import Updater, Dispatcher, CommandHandler, ConversationHandler, MessageHandler, \
    Filters, PicklePersistence

from bot.utils import ConversationState
from bot.handler_functions import start, register, cancel, add_task, invalid_input, solve_task, statistics, get_help

persistence = PicklePersistence(filename='saved_state.pickle')
updater = Updater(token=TG_TOKEN, persistence=persistence)
dispatcher: Dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
cancel_handler = CommandHandler('cancel', cancel)
reset_solved_handler = CommandHandler('reset_solved', statistics.reset_solved)
help_handler = CommandHandler('help', get_help)
invalid_input_handler = MessageHandler(Filters.all & ~Filters.regex("/cancel"), invalid_input)

add_task_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("Добавить задание"), add_task.entry_point)],
    states={
        ConversationState.ADD_TASKS_NUMBER: [MessageHandler(Filters.regex(r'\d+'), add_task.get_number)],
        ConversationState.ADD_TASKS_PROBLEM: [
            MessageHandler(Filters.text & ~Filters.command, add_task.get_problem_text),
            MessageHandler(Filters.document.image, add_task.get_problem_pic)
        ],
        ConversationState.ADD_TASKS_ANSWER: [MessageHandler(Filters.text & ~Filters.command, add_task.get_answer)],
        ConversationState.ADD_TASKS_LINK: [MessageHandler(Filters.text & ~Filters.command, add_task.get_link)],
        ConversationState.ADD_TASKS_NEXT_STEP: [
            MessageHandler(Filters.regex(r"(В главное меню|Добавить еще задание)"), add_task.next_step)
        ]
    },
    fallbacks=[
        start_handler,
        reset_solved_handler,
        cancel_handler,
        help_handler,
        invalid_input_handler
    ],
    map_to_parent={
        ConversationHandler.END: ConversationState.MAIN_MENU,
        ConversationState.MAIN_MENU: ConversationState.MAIN_MENU
    }
)

solve_task_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r'\d+'), solve_task.get_number)],
    states={
        ConversationState.SOLVE_TASK_ANSWER: [
            MessageHandler(Filters.regex("Другая задача"), solve_task.another_task),
            MessageHandler(Filters.text & ~Filters.command, solve_task.check_answer),
        ]
    },
    fallbacks=[
        start_handler,
        reset_solved_handler,
        cancel_handler,
        help_handler,
        invalid_input_handler
    ],
    map_to_parent={
        ConversationHandler.END: ConversationState.MAIN_MENU,
        ConversationState.MAIN_MENU: ConversationState.MAIN_MENU
    }
)

get_stat_handler = MessageHandler(Filters.regex("Статистика"), statistics.get_stat)

handlers = [
    ConversationHandler(
        entry_points=[start_handler],
        states={
            ConversationState.REGISTER: [MessageHandler(Filters.text, register)],
            ConversationState.MAIN_MENU: [
                add_task_handler,
                solve_task_handler,
                get_stat_handler
            ]
        },
        fallbacks=[
            cancel_handler,
            start_handler,
            reset_solved_handler,
            help_handler,
            invalid_input_handler
        ],
        name="global_conversation", persistent=True
    )
]

for h in handlers:
    dispatcher.add_handler(h)

updater.start_polling()
