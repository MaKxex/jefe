from db import db
from db.models import *


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


def make_page(data, page_index=0):
    i = 50
    output = ""

    for index in range(i):
        output += data[index].row_in_array()

    return output


def get_obj_by_str(tableName: str, id):
    print(type(Embroidery))
    return db.get_by_str(tableName, id)
    

def search(table, target):
    pass


def emb_array(**kwargs):
    return make_page(get_all_(Embroidery))

def thread_script(**kwargs):
    return make_page(get_all_colors(),1)


if __name__ == "__main__":
    #thread_script()
    print(get_all_table_names())
    # emb = get_embroidery_by(name="birka")
    # print(get_threadList_by(embroidery_hash=emb.hash))

    

    #get_btn(sub = "main")
    # get_threadList_by()

