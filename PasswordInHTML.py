import gc
from os import remove as file_remove
from os.path import isfile, isdir
from os import mkdir
from sys import exit as exit_ex
from sys import platform
from time import sleep as time_sleep
from tkinter import Label, TclError, Tk
from tkinter.messagebox import showerror
from tracemalloc import get_traced_memory
from tracemalloc import start as trace_start

from apscheduler.schedulers.background import BackgroundScheduler
from PIL import Image, ImageTk

from run import App, Windows, get_settings, unzip_file, write_dict_in_file
from settings import (LOGGER, clean_after_app, default_settings,
                      path_ico_screen_saver, path_icos_zip,
                      path_to_settings_json, path_to_style, path_to_passwords)


if platform in ['linux']:
    OS = 'Linux'
elif platform in ['win32', 'cygwin']:
    OS = 'Windows'
else:
    showerror(
        'Платформа не поддерживается',
        f'Неподдерживаемая платформа: {platform}\n\nОбратитесь за помощью '
        'к боту VK'
    )

    exit_ex()


class StartApp:
    def __init__(self, preview):
        self.logger = LOGGER('start_app', 'main')

        unzip_file(path_icos_zip, file_name='PassHTML.png', path_extract=path_to_style)
        png_preview_open, png_preview = self.preview_image_open()
        self.preview_image_set(png_preview_open, png_preview, preview)
        preview.update()

        trace_start()
        self.logger.info('Создание задачи scheduler')
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(__scheduler__, 'interval', minutes=1)

        if isfile(path_to_settings_json):
            settings = get_settings()
            first_start = settings['first_start']
        else:
            settings = default_settings
            write_dict_in_file(path_to_settings_json, settings)
            first_start = 1
        auto_update = settings['auto_update']

        unzip_file(path_icos_zip, file_name='LittlePassHTML.ico', path_extract=path_to_style)

        if first_start == 1:
            self.logger.info('Первый запуск')
            preview.destroy()
            done = Windows().person_and_agreement_data()

            if done is True:
                settings['first_start'] = 0
                write_dict_in_file(path_to_settings_json, settings)
        
        if not isdir(path_to_passwords):
            mkdir(path_to_passwords)

        try:
            time_sleep(2)
            self.logger.warning('Закрытие окна первью')
            preview.destroy()
        except TclError:
            pass
        __clean_preview__()

        self.logger.info('Запуск приложения')
        App(auto_update, OS)
        self.logger.info('Закрытие приложения')

        clean_after_app()
    
    def preview_image_open(self):
        """
        Возвращает первью картинку
        """
        try:
            png_preview_open = Image.open(path_ico_screen_saver)
            png_preview = ImageTk.PhotoImage(png_preview_open)
            return png_preview_open, png_preview
        except FileNotFoundError as err:
            self.logger.error(str(err))
            unzip_file(path_icos_zip, file_name='PassHTML.png', path_extract=path_to_style)

    
    @staticmethod
    def preview_image_set(png_preview_open, png_preview, window_preview):
        """
        Устанавливает размеры окна, ставит его по середине, устанавливает
        картинку как фон
        """
        x_img, y_img = png_preview_open.size
        x = (window_preview.winfo_screenwidth() - x_img) // 2
        y = (window_preview.winfo_screenheight() - y_img) // 2
        window_preview.geometry("%ix%i+%i+%i" % (x_img, y_img, x, y))
        Label(window_preview, image=png_preview).pack(side='top')

if __name__ == '__main__':
    if platform not in ['linux', 'win32', 'cygwin']:
        showerror(
            'Платформа не поддерживается',
            f'Неподдерживаемая платформа: {platform}'
        )
        LOGGER('platform', 'main').error(f'{platform} не поддерживается')
        exit_ex()

    LOGGER('platform', 'main').info(f'Запуск на платформе: {platform}')

    def __scheduler__() -> None:
        """
        Функция отвечает за сброс мусора и ведение логгера с информацией об
        этом
        :return:
        """
        scheduler_logger = LOGGER('scheduler', 'main')
        size_last, peak = get_traced_memory()
        size_last = size_last // 1024

        scheduler_logger.warning('Запускаю очситку мусора')
        gc.collect()

        size_now, size_peak = get_traced_memory()
        size_now = size_now // 1024
        size_peak = size_peak // 1024
        scheduler_logger.warning(
            f'Использовалось: {size_last}Mib, Теперь: {size_now}Mib, '
            f'В пике: {size_peak}Mib'
        )
    
    def __clean_preview__():
        if isfile(path_ico_screen_saver):
            file_remove(path_ico_screen_saver)

    preview = Tk()
    preview.overrideredirect(True)

    StartApp(preview)
