import zipfile
from json import dump as dump_json
from json import dumps as dumps_json
from json import load as load_json
from json import loads as loads_json
from os.path import isfile
from typing import Union

import clipboard

from settings import path_to_passwords, path_to_settings_json, path_to_passwords_json, default_passwords


def set_position_window_on_center(parent, width: int, height: int) -> None:
    """
    Функция установки окна по середине окна
    :param parent: объект окна, которое нужно расположить посередине
    :param width: параметр длины окна
    :param height: параметр высоты окна
    :return:
    """
    sw = parent.winfo_screenwidth()
    sh = parent.winfo_screenheight()
    x = (sw - width) / 2
    y = (sh - height) / 2
    parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

def copy_in_clipboard(widget: object, value: Union[int, str]) -> None:
    """
    Функция управляющая наполнением буфера обмена
    :param widget: виджет от лица которого будет происходить копирование
    :param value: строковое значение, которое надо скопировать
    :return:
    """
    widget.clipboard_clear()
    widget.clipboard_append(value)

def paste_into_widget(widget: object, text=False) -> None:
    """
    Функция управляющая наполнением из буфера обмена
    :param widget: виджет в который вставить объект
    :param text: Текстовое ли поле
    :return:
    """
    txt = clipboard.paste()

    if text is True:
        widget.insert(1.0, txt)
        return

    widget.insert(0, txt)

def time_now() -> float:
    from time import localtime, mktime
    local_time = localtime()
    time = mktime(local_time)

    return time

def unzip_file(path, file_name=None, all=False, path_extract=None):
    zip_file = zipfile.ZipFile(path, 'r')

    if all:
        zip_file.extractall(path=path_extract)
        return
    
    zip_file.extract(file_name, path=path_extract)

def read_file(path):
    with open(path, 'r', encoding='UTF-8') as file:
        text = file.read().strip()
    
    return text

def write_file(path, text):
    with open(path, 'w', encoding='UTF-8') as file:
        file.write(text.strip())

def get_dict_from_json(text):
    return loads_json(text)

def get_dict_from_json_file(path):
    with open(path, 'r', encoding='UTF-8') as file:
        return load_json(file)


def get_json_from_dict(object):
    return dumps_json(object, indent=4, ensure_ascii=False)

def write_dict_in_file(path, object):
    with open(path, 'w', encoding='UTF-8') as file:
        dump_json(object, file, ensure_ascii=False, indent=4)

def get_settings():
    return get_dict_from_json_file(path_to_settings_json)

class Passwords:
    def __init__(self):
        if not isfile(path_to_passwords_json):
            write_dict_in_file(path_to_passwords_json, default_passwords)
        
        self.passwords_dict, self.name_passwords = self.get_passwords()
    
    def get_passwords(self):
        passwords_dict = get_dict_from_json_file(path_to_passwords_json)
        name_passwords = list(passwords_dict.keys())

        return passwords_dict, name_passwords
    
    def delete_password(self, name):
        del self.passwords_dict[name]

        write_dict_in_file(path_to_passwords_json, self.passwords_dict)
        self.passwords_dict, self.name_passwords = self.get_passwords()
    
    def delete_all_passwords(self):
        self.passwords_dict = default_passwords

        write_dict_in_file(path_to_passwords_json, self.passwords_dict)
        self.passwords_dict, self.name_passwords = self.get_passwords()
