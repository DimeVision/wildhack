from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminFSM(StatesGroup):
    title = State()
    description = State()
    photo = State()

