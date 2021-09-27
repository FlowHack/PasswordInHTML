from typing import Union

import clipboard
import zipfile

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
