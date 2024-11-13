from datetime import datetime

from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import Session

from models import Group, Schedule, get_db_session, SessionLocal
from config import ADMINS

router = Router()

class AdminState(StatesGroup):
    ADD_GROUP = State()
    ADD_SCHEDULE_GROUP = State()
    ADD_SCHEDULE_DAY = State()
    ADD_SCHEDULE_DETAILS = State()

# Проверка, является ли пользователь администратором
def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

# Команда для добавления группы
@router.message(Command("add_group"))
async def cmd_add_group(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав для выполнения этой команды.")
        return
    await message.answer("Введите название новой учебной группы:")
    await state.set_state(AdminState.ADD_GROUP)

@router.message(AdminState.ADD_GROUP)
async def process_add_group(message: Message, state: FSMContext):
    group_name = message.text.strip()
    session = get_db_session()
    existing_group = session.query(Group).filter(Group.name == group_name).first()

    if existing_group:
        await message.answer("Группа с таким названием уже существует.")
    else:
        new_group = Group(name=group_name)
        session.add(new_group)
        session.commit()
        await message.answer(f"Группа '{group_name}' успешно добавлена!")
    await state.clear()

# Команда для добавления расписания
@router.message(Command("add_schedule"))
async def cmd_add_schedule(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    session = get_db_session()
    groups = session.query(Group).all()
    if not groups:
        await message.answer("Нет доступных групп. Сначала добавьте группу командой /add_group.")
        return

    keyboard = InlineKeyboardBuilder()
    for group in groups:
        keyboard.button(text=group.name, callback_data=f"select_group:{group.id}")
    await message.answer("Выберите группу для добавления расписания:", reply_markup=keyboard.as_markup())
    await state.set_state(AdminState.ADD_SCHEDULE_GROUP)

@router.callback_query(F.data.startswith("select_group:"))
async def process_select_group(call: CallbackQuery, state: FSMContext):
    group_id = int(call.data.split(":")[1])
    await state.update_data(group_id=group_id)
    await call.message.answer("Введите день недели (например, Понедельник):")
    await state.set_state(AdminState.ADD_SCHEDULE_DAY)

@router.message(AdminState.ADD_SCHEDULE_DAY)
async def process_add_day(message: Message, state: FSMContext):
    day = message.text.strip()
    await state.update_data(day=day)
    await message.answer("Введите расписание в формате:\n<время> - <предмет> - <преподаватель> - <корпус> - <этаж> - <аудитория>")
    await state.set_state(AdminState.ADD_SCHEDULE_DETAILS)

@router.message(AdminState.ADD_SCHEDULE_DETAILS)
async def process_add_schedule_details(message: types.Message, state: FSMContext):
    # Разделяем введённый текст по разделителю " - "
    schedule_data = message.text.split(" - ")

    # Проверка, что введено ровно 6 частей
    if len(schedule_data) != 6:
        await message.answer(
            "Неправильный формат ввода. Убедитесь, что вы ввели данные в формате:\n<время> - <предмет> - <преподаватель> - <корпус> - <этаж> - <аудитория>")
        return

    time, subject, teacher, building, floor, room = schedule_data

    # Проверка формата времени
    if not validate_time_format(time):
        await message.answer("Неправильный формат времени. Используйте формат ЧЧ:ММ (например, 10:00)")
        return

    # Проверка, что корпус, этаж и аудитория являются числами
    if not (building.isdigit() and floor.isdigit() and room.isdigit()):
        await message.answer("Корпус, этаж и аудитория должны быть числами.")
        return

    data = await state.get_data()
    group_id = data['group_id']
    day = data['day']

    # Сохранение данных в БД
    session: Session = get_db_session()
    new_schedule = Schedule(
        group_id=group_id,
        day=day,
        time=time.strip(),
        subject=subject.strip(),
        teacher=teacher.strip(),
        building=int(building.strip()),
        floor=int(floor.strip()),
        room=int(room.strip())
    )
    session.add(new_schedule)
    session.commit()

    await message.answer("Расписание успешно добавлено!")
    await state.clear()


def validate_time_format(time_str: str) -> bool:
    """Проверка, что время задано в формате ЧЧ:ММ"""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# Обработка выбора элемента для редактирования
@router.callback_query(F.data.startswith("edit:"))
async def edit_schedule_item(call: CallbackQuery):
    data = call.data.split(":")
    schedule_id = int(data[1])

    session = SessionLocal()
    item = session.query(Schedule).get(schedule_id)
    if not item:
        await call.message.answer("Элемент расписания не найден.")
        return

    # Запрос новой информации от пользователя
    await call.message.answer(
        f"Текущая запись:\n{item.time} - {item.subject} - {item.teacher} - {item.building} - {item.floor} - {item.room}\n\n"
        "Введите новую информацию в формате:\n"
        "`время, предмет, преподаватель, здание, этаж, аудитория`"
    )
    router.message.register(get_new_schedule_data, F.reply_to_message_id == call.message.message_id, state=schedule_id)


async def get_new_schedule_data(message: Message, schedule_id: int):
    data = message.text.split(", ")
    if len(data) != 6:
        await message.answer("Неверный формат. Попробуйте снова.")
        return

    new_time, new_subject, new_teacher, new_building, new_floor, new_room = data
    session = SessionLocal()
    item = session.query(Schedule).get(schedule_id)

    if item:
        item.time = new_time
        item.subject = new_subject
        item.teacher = new_teacher
        item.building = new_building
        item.floor = new_floor
        item.room = new_room
        session.commit()
        await message.answer("Расписание успешно обновлено.")
    else:
        await message.answer("Ошибка при обновлении расписания.")