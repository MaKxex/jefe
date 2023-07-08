import pyembroidery
import glob
import os
import db
from db.models import *

dir_path = r"C:\Users\Makxex\Desktop\MOT\MOT-EMBF\jefs"


def get_all_colors(**target):
    return db.gets_(Color, **target)

def get_all_(table, **target):
    return db.gets_(table,**target)

def get_threadList_by(**target):
    return db.gets_(Thread, **target)

def get_embroidery_by(**target):
    return db.get_(Embroidery, **target)

def get_embroiderys_by(**target):
    return db.gets_(Embroidery, **target)


def get_all_table_names():
    return [cls.__table__.name for cls in Base.__subclasses__()]


def get_model_by_str(tableName:str):
    return db.get_model_by_str(tableName)

def get_obj_by_str(tableName: str, id):
    print(type(Embroidery))
    return db.get_by_str(tableName, id)


def get_color_hex_by_id(id):
    with open("catalog\marathonVol3.csv", encoding="utf-8") as f:
        catalog = f.readlines()

        for color in catalog:
            color_data = color.split(",")
            if color_data[1][-4] == id:
                return color_data[1][3]


def calculate_path_length(file_path):
    units_per_meter = 5965
    # Загружаем файл вышивки
    pattern = pyembroidery.read(file_path)
    # Переменная для хранения общей длины пути в метрах
    path_length_meters = 0

    threads_lenght = []
    # Проходимся по всем стежкам в файле вышивки
    for i in range(len(pattern.stitches) - 1):
        # Получаем координаты текущего и следующего стежка
        current_stitch = pattern.stitches[i]
        next_stitch = pattern.stitches[i + 1]

        # Вычисляем расстояние между текущим и следующим стежком в единицах файла
        distance_units = ((next_stitch[0] - current_stitch[0]) ** 2 + (next_stitch[1] - current_stitch[1]) ** 2) ** 0.5

        # Преобразуем расстояние в метры
        distance_meters = distance_units / units_per_meter

        # Увеличиваем общую длину пути в метрах
        path_length_meters += distance_meters

        if current_stitch[2] == 5 or i == len(pattern.stitches) - 2:
            threads_lenght.append(round(path_length_meters, 1))
            path_length_meters = 0


    #print(len(pattern.stitches))
    # Возвращаем общую длину пути в метрах
    return threads_lenght

def calculate_size(file_path):
    pattern = pyembroidery.read(file_path)
    bounds = pattern.bounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    
    return width / 10, height /10


def get_all_jef_paths():
    jefs = []
    txts = []
    for filename in glob.glob(dir_path +'/**/*.jef', recursive=True):
        jefs.append(filename)
        if os.path.exists(os.path.splitext(filename)[0] + ".txt"):
            txts.append(os.path.splitext(filename)[0] + ".txt")
    return jefs
    
def get_colors(filename):
    with open(filename, "r" , encoding="utf-16-le") as t:

        return t.readlines()[2:]


def record_ThreadList(filename):
    path_length = calculate_path_length(filename + ".jef")
    colors =  get_colors(filename + ".txt")

    return path_length, colors


if __name__ == "__main__":
    pass

    
