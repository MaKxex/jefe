import db.database as db
from db.models import *

from paginator.page import Pages


def get_all_colors(**target):
    return db.gets_(Color, **target)

def get_all_(table, **target):
    return db.gets_(table,**target)

def get_threadList_by(**target):
    return db.gets_(Thread, **target)

def get_embroidery_by(**target):
    return db.get_(Embroidery, **target)

def get_btns(**target):
    return db.gets_(Buttons, **target)

def get_all_table_names():
    return [cls.__table__.name for cls in Base.__subclasses__()]


def get_obj_by_str(tableName: str, id):
    print(type(Embroidery))
    return db.get_by_str(tableName, id)
    

def emb_list(*args):
    page = Pages()
    page.add_user(get_all_(Embroidery),args[0])
    return page.make_page(args[0])

def emb_thread_list(*args):
    page = Pages()
    page.add_user(get_threadList_by(embroidery_id=int(args[1])),args[0])
    return page.make_page(args[0])


def thread_list(*args):
    page = Pages()

    page.add_user(get_all_colors(), args[0])

    return page.make_page(args[0])
    

def embroidery_page(*args):
    return get_obj_by_str("embroidery", args[1]).get_page()



def clear_page(*args):
    Pages().remove_user(args[0])

def page_next(*args):
    page = Pages()
    page.index_increment_plus(args[0])
    return page.make_page(args[0])

def page_back(*args):
    page = Pages()
    page.index_increment_minus(args[0])
    return page.make_page(args[0])

    


if __name__ == "__main__":
    print(get_all_table_names())


