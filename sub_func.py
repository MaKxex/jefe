from paginator import Pages
from db.models import *
import db
from utils import get_all_, get_threadList_by, get_all_colors, get_obj_by_str, get_all_table_names
from FSM.states import SearchStates 
    

async def search_(*args):
    #SearchStates.WAITING_FOR_TABLENAME = args [-1]
   # await SearchStates.WAITING_FOR_TABLENAME.set()
    await SearchStates.WAITING_FOR_TABLENAME.set()
    print("ФСМ создался и запихнул туда данные")

async def get_btns(**target):
    return db.gets_(Buttons, **target)


async def emb_list(*args):
    page = Pages()
    page.add_user(get_all_(Embroidery),args[0])
    return page.make_page(args[0])

async def emb_thread_list(*args):
    page = Pages()
    page.add_user(get_threadList_by(embroidery_id=int(args[-1])),args[0])
    return page.make_page(args[0])


async def thread_list(*args):
    page = Pages()
    page.add_user(get_all_colors(), args[0])
    return page.make_page(args[0])
    

async def embroidery_page(*args):
    return get_obj_by_str("embroidery", args[-1]).get_page()


async def color_page(*args):
    return get_obj_by_str("color", args[-1]).get_page()


async def clear_page(*args):
    Pages().remove_user(args[0])

async def page_next(*args):
    page = Pages()
    page.index_increment_plus(args[0])
    return page.make_page(args[0])

async def page_back(*args):
    page = Pages()
    page.index_increment_minus(args[0])
    return page.make_page(args[0])

    


if __name__ == "__main__":
    print(get_all_table_names())


