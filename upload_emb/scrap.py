#utf-8
#TODO
# В данный момент создаются копии вышивок, 
# то есть при каждом запуске одни и те же вышивки закидываются в базу
# Исправить данный момент, чтобы автоматизировать добавление вышивок в базу


import os 
from db import database
from db import models
from .utils import *

def record_embroidery_to_db():
    for emb_filepath in get_all_jef_paths():
        k=1
        path = os.path.split(emb_filepath)
        name = os.path.splitext((os.path.split(emb_filepath)[1]))[0]
        size = calculate_size(emb_filepath)
        rel_path = os.path.relpath(path[0],dir_path)

        Emb = database.add_(models.Embroidery, {"name": name, "height": size[1], "width": size[0],"photo_link": "None", "rel_path": rel_path})
        if os.path.exists(path[0] + "\\" + name + ".txt"):
            threadList = record_ThreadList(path[0] + "\\" + name)

            for lenght, colorRaw in zip(threadList[0],threadList[1]):
                color_id = colorRaw[-5:]
                color_name = colorRaw.split(",")[1]
                color_lenght = lenght
                # print(color_id, color_name, color_lenght)

                database.add_(models.Color, {"id":color_id, "catalog_id": 1, "name":color_name})
                database.add_(models.Thread, {"color_id": color_id, "embroidery_id": Emb.id,"index":k, "length":color_lenght})
                k+= 1


def upload():
    database.create_tables() # 
    record_embroidery_to_db()


if __name__ == "__main__":
    database.create_tables() # 
    record_embroidery_to_db()


