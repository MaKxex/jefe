from aiogram import Bot, Dispatcher, executor, md, types
from aiogram.types import InlineKeyboardMarkup, KeyboardButton
from config import TOKEN
from sub_func import *
import sub_func
import re
from locales import get_locale as locale

api = Bot(token = TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(api)

image_base= -900601494


class Pages(object):
    i = 50
    next = KeyboardButton(locale.get_("ru", "page_next_btn"))
    back = KeyboardButton(locale.get_("ru", "page_back_btn"))

    def __init__(self, data: list, page_index = 0):
        self.data = data
        self.index = page_index
        self.output = ""

    def get_page(self):
        for obj in self.data:
            print(obj)





def generate_btns(BtnsList:list):
    markup = InlineKeyboardMarkup(resize_keyboard=True)

    #TODO Сделать систему приоритета и фигню для растановки кнопок

    for btnObj in BtnsList:
        if btnObj.show_on == "true":
            markup.insert(
                KeyboardButton(text=locale.get_("ru", btnObj.link_to + "_btn"), callback_data=f"{btnObj.link_to}|{btnObj.f_name}|{btnObj.args}")
                )

    return markup

@dp.message_handler(regexp=r"/\b(" + "|".join(re.escape(word) for word in get_all_table_names()) + r"\w*)+\d+\b")
async def regex(message):
    table, id = re.findall(r'[A-Za-z]+|\d+', message.text)
    obj = get_obj_by_str(table,id=id)
    print(obj)
    data = obj.get_page()
    print(table)
    msg = locale.get_("ru", table + "_msg")
    btns = get_btns(sub=table)
    print(btns)
    #print(msg.format("hehe",123,123))
    #print(msg.format(*data))

    if obj.photo_link != "None":
        photo = await api.download_file(obj.photo_link)
        await api.send_photo(image_base,photo)

    print(generate_btns(btns))

    await api.send_message(message.chat.id,text=msg.format(*data), reply_markup=generate_btns(btns))



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

@dp.message_handler(commands=["start"])
async def start(message):
    await main(message)
@dp.message_handler(commands=["main"])
async def main(message):
    btns_list = get_btns(sub="main")
    message = await message.reply(text="asd", reply_markup = generate_btns(btns_list))



def custom_exec(func_name, *args):
    print(args)
    try:
        return getattr(sub_func, func_name)(*args)
    except TypeError as e:
        return getattr(sub_func, func_name)

@dp.callback_query_handler()
async def callback_handler(callback_query: types.CallbackQuery):

    await api.answer_callback_query(callback_query.id)
    print(callback_query)

    message = callback_query.message

    sub, func, args = callback_query.data.split("|") 
    print(sub, func,args)

    chat_id = callback_query.message.chat.id
    msg = locale.get_("ru", sub + "_msg")
    btns = get_btns(sub=sub)
    
    dynamic_text = ""

    if func != "None":
        dynamic_text = custom_exec(func, *args.split(","))()
    
    await api.edit_message_text(text=msg + dynamic_text, chat_id=chat_id, message_id=message.message_id,reply_markup=generate_btns(btns))

    
    


executor.start_polling(dp, skip_updates=True)