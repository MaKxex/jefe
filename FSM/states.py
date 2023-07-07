from aiogram.dispatcher.filters.state import StatesGroup, State


class SearchStates(StatesGroup):
    WAITING_FOR_TABLENAME = State()
    WAITING_FOR_NAME = State()