from aiogram.dispatcher import FSMContext
from aiogram import types



async def search_form(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(WAITING_FOR_NAME=name)


    print(await state.get_data())