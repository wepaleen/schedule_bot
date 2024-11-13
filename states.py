from aiogram.fsm.state import State, StatesGroup

class ScheduleStates(StatesGroup):
    MAIN_MENU = State()
    SELECT_GROUP = State()
    SELECT_DAY = State()
    ADD_SCHEDULE = State()
    EDIT_SCHEDULE = State()
    VIEW_SCHEDULE = State()