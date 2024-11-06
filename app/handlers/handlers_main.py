
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import ChatAction # Уведомление о том, что бот пишет ответ


import app.keyboard as kb # Импорт кнопок

router = Router() # Замена dp

class ScheduleStates(StatesGroup):
    MAIN_MENU = State()
    WEEK_SCHEDULE = State()
    TODAY_SCHEDULE = State()
    BACK_WEEK_SCHEDULE = State()
    BACK_TODAY_SCHEDULE = State()
    CLOSE = State()

# Временная база данных (в реальности заменить на полноценную базу)
# users_db = {'123456789': 'admin', '987654321': 'student', '820372096': 'Ruslan', '5866268316': 'Pedik'}  # user_id: role
# # Проверка авторизации
# async def is_authorized(user_id: int, role: str) -> bool:
#     return str(user_id) in users_db or str(role) in users_db

# Команда /start
# @router.message(CommandStart())
# async def cmd_start(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     role = message.from_user.full_name
#     if await (user_id, role):
#         await message.answer(f"Приветствую, {role}")
#         await state.set_state(ScheduleStates.MAIN_MENU)
#         await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
#         await message.answer(f'Выберите расписание:', reply_markup=kb.inline_main)
#     else:
#         await message.answer("У вас нет доступа.")
# Команда /start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    role = message.from_user.full_name

    # Приветствие пользователя
    await message.answer(f"Приветствую, {role}")
    await state.set_state(ScheduleStates.MAIN_MENU)
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await message.answer(f'Выберите расписание:', reply_markup=kb.inline_main)


# # Команда /now
# @router.message(Command('now'))
# async def send_current_class(message: Message):
#     await message.answer("Выберите группу для вывода текущего занятия:", reply_markup=kb.keyboard_today_schedule)


# Команда /help
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('<b>Правила эксплуатации бота расписания для студентов КФУ:</b>'
                         '\n▪️Для просмотра полного расписания введите команду: /start'
                         '\n▪️Чтобы увидеть занятия, которые идут прямо сейчас введите команду: /now'
                         '\n\n<b>Контакты:</b>'
                         'Разработчик - Руслан Мамахаев(<i>@wwdcdev</i>)', parse_mode='html')