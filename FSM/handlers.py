from aiogram.dispatcher import FSMContext
from aiogram import types
from searcher import find_similar_words
import utils



async def search_form(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(WAITING_FOR_NAME=name)
    print(await state.get_data())

    data = await state.get_data()
    tablename = list(data.values())[0]
    search_name = list(data.values())[1]
    tablenameObj = utils.get_model_by_str(tablename)
    obj_list = utils.get_all_(tablenameObj)

    threshold = 3

    if tablename == "color":
        threshold = 0
        
    print(find_similar_words(search_name,obj_list,threshold))

    await state.finish()



    





