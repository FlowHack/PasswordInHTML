import subprocess
import tempfile
import zipfile
from json import dump as dump_json
from json import dumps as dumps_json
from json import load as load_json
from json import loads as loads_json
from os import system as os_system
from os.path import isfile
from os.path import join as path_join
from shutil import rmtree
from tkinter import filedialog, messagebox
from tkinter.messagebox import askyesnocancel, showerror, showinfo, showwarning
from typing import Union

import clipboard
import requests
import winshell
from requests.exceptions import ConnectionError
from win32com.client import Dispatch

from settings import (LOGGER, REPO_BRANCH_UPDATER, REPO_URL_UPDATER,
                      REPO_URL_VERSION, UPDATE_LINUX, UPDATE_WIN, VERSION,
                      clean_after_app, path, path_app_win,
                      path_to_passwords_json, path_to_settings_json,
                      path_to_updater, path_to_version)


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
            write_dict_in_file(path_to_passwords_json, {})

        self.passwords_dict, self.name_passwords = self.get_passwords()

    def add_password(self, password):
        self.passwords_dict.update(password)
        sorted_passwords = dict(
            sorted(self.passwords_dict.items(), key=lambda x: x[0])
        )
        write_dict_in_file(path_to_passwords_json, sorted_passwords)

    def edit_password(self, password, name):
        del self.passwords_dict[name]
        self.add_password(password)

    def get_passwords(self):
        passwords_dict = get_dict_from_json_file(path_to_passwords_json)
        name_passwords = list(passwords_dict.keys())

        return passwords_dict, name_passwords

    def delete_password(self, name):
        del self.passwords_dict[name]

        write_dict_in_file(path_to_passwords_json, self.passwords_dict)
        self.passwords_dict, self.name_passwords = self.get_passwords()

    def delete_all_passwords(self):
        self.passwords_dict = {}

        write_dict_in_file(path_to_passwords_json, self.passwords_dict)
        self.passwords_dict, self.name_passwords = self.get_passwords()


def update_app(os_name: str) -> None:
    """
    Скачивание программы обновления и запуск обновлений
    :param os_name: имя OS
    :return:
    """
    logger = LOGGER('update', 'main')
    logger.info(f'Клонируем проект {os_name}')

    response = requests.get(REPO_URL_UPDATER)

    with tempfile.TemporaryFile() as file:
        file.write(response.content)
        with zipfile.ZipFile(file) as fzip:
            fzip.extractall(path)

    if os_name == 'Windows':
        command = path_join(path_to_updater, UPDATE_WIN)
        subprocess.Popen(command, cwd=path_to_updater)
        clean_after_app()

    if os_name == 'Linux':
        os_system(f'chmod -R 775 {path_to_updater}')

        showwarning(
            'Обновление',
            'Для обновления вам нужно перейти в папку '
            f'\"{REPO_BRANCH_UPDATER}\", которая '
            'появилась у вас в корне программы и запустить файл '
            f'{UPDATE_LINUX}.\n\nИзвините за предоставленные неудобства.'
        )
        clean_after_app()


def check_update(os_name: str, call: bool = False) -> None:
    """
    Проверка наличия обновлений
    :param os_name: имя OS
    :param call: булево принудительно ли отправлен запрос на проверку
    обновлений default: False
    :return:
    """
    version = path_join(path_to_version, 'version.txt')
    logger = LOGGER('update', 'main')

    try:
        logger.info('Клонируем version')
        response = requests.get(REPO_URL_VERSION)

        with tempfile.TemporaryFile() as file:
            file.write(response.content)
            with zipfile.ZipFile(file) as fzip:
                fzip.extractall(path)

    except ConnectionError as error:
        logger.error(
            f'Произошла ошибка при клонировании проекта {error}'
        )
        if call is True:
            showerror(
                'Невозможно выполнить обновление',
                f'Ваша версия: {VERSION}\n\nПлохое подключение к интернету. '
                'Мы не смогли выполнить обновление.\n\nВы можете скачать '
                'новую версию самостоятельно, либо рассказать об ошибке '
                'в боте ВК'
            )

        return

    with open(version, 'r', encoding='utf-8') as file:
        file = file.readline().strip().split('&')

    rmtree(path_to_version, ignore_errors=True, onerror=None)

    version = file[0].strip()
    v_int = [int(item) for item in version.split('.')]
    version_old = [item for item in VERSION.split('.')]
    v_old_int = [int(item) for item in version_old]
    info = file[1].replace('\\n', '\n')

    condition_1 = v_int[0] > v_old_int[0]
    condition_2 = v_int[0] >= v_old_int[0] and v_int[1] > v_old_int[1]
    condition_3 = \
        v_int[0] >= v_old_int[0] and v_int[1] >= v_old_int[1] and \
        v_int[2] > v_old_int[2]
    need_update = (False, True)[condition_1 or condition_2 or condition_3]

    if (call is True) and (need_update is False):
        showinfo(
            'Обновление не требуется',
            'Обновление не требуется\n\nУстановлена актуальная версия:'
            f' {VERSION}'
        )

    if need_update is True:
        answer = askyesnocancel(
            'Требуется обновление',
            f'Выпущена новая версия: {version}\n\n{info}\n\nДа-Будет '
            'установлено обновление\nНет-Обновление будет отложено'
            '\nОтмена-Будет отменена автоматическая проверка обновлений'
        )

        if answer is False:
            return
        if answer is None:
            logger.info('Отмена автообновлений')
            settings = get_settings()
            settings['auto_update'] = 0
            write_dict_in_file(path_to_settings_json, settings)
            return
        if answer is True:
            try:
                update_app(os_name)
            except ConnectionError as error:
                logger.error(
                    f'Невозможно обновиться {os_name} -> {error}'
                )
                showerror(
                    'Невозможно выполнить обновление',
                    f'Ваша версия: {VERSION}\n\nПлохое подключение к '
                    'интернету. Мы не смогли выполнить обновление.'
                    '\n\nВы можете скачать новую версию '
                    'самостоятельно, либо рассказать об ошибке в боте ВК'
                )


def import_passwords(encryption):
    path = str(
        filedialog.askopenfilename(
            filetypes=[('passinhtml files', '*.passinhtml')]
        )
    )
    if path == '':
        return

    with open(path, 'r', encoding='UTF-8') as file:
        passwords = file.readlines()

    encryption = encryption()
    import_passwords = {}

    for item in passwords:
        item = item.strip()
        if len(item) < 1:
            continue

        item = item.split('&&separator&&')

        columns = encryption.encrypt(item[1])
        values = encryption.encrypt(item[2])
        url = item[3]

        import_passwords[item[0]] = {
            'columns': columns,
            'values': values,
            'url': url
        }

    length = len(import_passwords)
    if length > 0:
        Passwords().add_password(import_passwords)

    messagebox.showinfo(
        'Импортировано',
        'Ваши пароли успешно импортированы!\n\nСоветуем удалить файл '
        f'passinhtml\n\nВсего импортировано: {length}'
    )
    return


def export_passwords(encryption):
    path = str(
        filedialog.asksaveasfilename(
            initialfile='PassInHTML_export.passinhtml',
            filetypes=[('passinhtml files', '*.passinhtml')]
        )
    )
    if path == '':
        return

    path_split = path.split('.')
    if path_split[-1] != 'passinhtml':
        path += '.passinhtml'

    all_passwords = Passwords().passwords_dict
    text = ''
    encryption = encryption()

    for name, item in all_passwords.items():
        columns = encryption.decryption(item['columns'])
        values = encryption.decryption(item['values'])
        url = item['url']

        text += f'{name}&&separator&&{columns}&&separator&&{values}'  \
            f'&&separator&&{url}\n'

    write_file(path, text)
    showinfo(
        'Готово',
        'Экспорт успешно завершён!\n\nУбедительная просьба не хранить '
        'этот файл в свободном доступе, так как в нём ваши пароли не '
        'защищены!'
    )
    return


def create_shortcut_win(need=False):
    desktop = winshell.desktop()
    path_desktop = path_join(desktop, 'PasswordInHTML.lnk')
    target = path_app_win
    wDir = path
    icon = path_app_win

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path_desktop)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()

    if need:
        showinfo('Удачно', 'Ярлык удачно создан!')
