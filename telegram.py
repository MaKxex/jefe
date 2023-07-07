import logging

from aiogram import Bot, Dispatcher, executor, md, types
from aiogram.types import InlineKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import re

from config import TOKEN
import sub_func
from sub_func import *

import upload_emb
import locales as locale


from FSM.handlers import *
from FSM.states import *

api = Bot(token = TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(api, storage=MemoryStorage())

image_base= -900601494

logging.basicConfig(level=logging.INFO)


def generate_btns(BtnsList:list, args="None"):
    markup = InlineKeyboardMarkup(resize_keyboard=True)

    for btnObj in sorted(BtnsList, key=lambda x: x.pr):
        if btnObj.show_on == "true":
            arg = btnObj.args
            if btnObj.args == "None" or btnObj.args == None:
                arg = args
            markup.insert(
                KeyboardButton(text=locale.get_("ru", btnObj.link_to + "_btn"), callback_data=f"{btnObj.link_to}|{btnObj.f_name}|{arg}")
                )

    return markup

async def custom_exec(func_name, *args):
    print(func_name)
    print(args)
    try:
        return await getattr(sub_func, func_name)(*args)
    except TypeError as e:
        print(e)
        return await getattr(sub_func, func_name)

@dp.message_handler(commands=["start"])
async def start(message):
    await main(message)



@dp.message_handler(commands=["upload_emb"])
async def start(message):
    upload_emb.upload()

@dp.message_handler(commands=["main"])
async def main(message):
    btns_list = await get_btns(sub="main")
    message = await message.reply(text="asd", reply_markup = generate_btns(btns_list))



    
@dp.message_handler(regexp=r"/\b(" + "|".join(re.escape(word) for word in get_all_table_names()) + r"\w*)+\d+\b")
async def regex(message):
    table, id = re.findall(r'[A-Za-z]+|\d+', message.text)
    obj = get_obj_by_str(table,id=id)

    data = obj.get_page()

    msg = locale.get_("ru", table + "_msg")
    btns = await get_btns(sub=table)

    try:
        if obj.photo_link != "None":
            photo = await api.download_file(obj.photo_link)
            await api.send_photo(image_base,photo)
    except AttributeError:
        pass

    await api.send_message(message.chat.id,text=msg.format(*data), reply_markup=generate_btns(btns,id))

@dp.callback_query_handler()
async def callback_handler(callback_query: types.CallbackQuery):

    await api.answer_callback_query(callback_query.id)
    #print(callback_query)
    message = callback_query.message

    sub, func, args = callback_query.data.split("|") 
    #print(sub, func, args)

    chat_id = callback_query.message.chat.id
    #print("---------------------------")
    
    #print(sub)
    msg = locale.get_("ru", sub + "_msg")
    btns = await get_btns(sub=sub)
    dynamic_text = ""

    args = args.split(",")

    if msg == None:
        msg = ""
    
    if args == "None":
        args = None

    if func != "None":
        dynamic_text = await custom_exec(func, callback_query.from_user.id,api,*args)
        if dynamic_text == None:
            dynamic_text = ""

    #print(dynamic_text)
    await api.edit_message_text(text=msg.format(*dynamic_text), chat_id=chat_id, message_id=message.message_id,reply_markup=generate_btns(btns,*args))

@dp.callback_query_handler(state="*")
async def FSM_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await api.answer_callback_query(callback_query.id)
    sub, func, args = callback_query.data.split("|") 
    print(sub,func,args)
    state_name = (await state.get_state()).split(":")[1]
    async with state.proxy() as state_data:
        state_data[state_name] = args

    await SearchStates.next()

dp.register_message_handler(search_form, state=SearchStates.WAITING_FOR_NAME.state)




executor.start_polling(dp, skip_updates=True)


# @dp.message_handler(content_types=types.ContentType.PHOTO)
# async def handle_photo(message: types.Message):
#     # gettedFile = await api.get_file(message.photo[-1].file_id)
#     # path = gettedFile.file_path
#     # print(path)
#     for x in range(0,10):
#         photo = await api.download_file(f"photos/file_{x}.jpg")
#         message = await api.send_photo(image_base, photo)



# @dp.message_handler(commands=["test"])
# async def start(message):
#     with open("image.png", "rb") as f:
#         photo = await api.send_photo(image_base,f)
#         gettedFile = await api.get_file(photo.photo[-1].file_id)
#         path = gettedFile.file_path

#         photo = await api.download_file(path)
#         await api.send_photo(image_base,photo)
#         #print(photo.photo[-1])
        

# @dp.message_handler(commands=["test2"])
# async def start(message):

#     photo = await api.download_file("/photos/file_1.jpg")
#     await api.send_photo(image_base,photo)

