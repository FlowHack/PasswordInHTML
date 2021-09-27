from sys import platform
from tkinter.messagebox import showerror
from sys import exit as exit_ex
from tkinter import Tk, Label
from apscheduler.schedulers.background import BackgroundScheduler
from tracemalloc import get_traced_memory
from tracemalloc import start as trace_start
from settings import LOGGER, path_screen_saver, path_to_style, path_ico_screen_saver
import gc
from run import unzip_file
from PIL import Image, ImageTk
from time import sleep as time_sleep
from os import remove as file_remove

class StartApp:
    def __init__(self, preview):
        self.logger = LOGGER('start_app', 'main')

        unzip_file(path_screen_saver, file_name='play_store_512.png', path_extract=path_to_style)
        png_preview_open, png_preview = self.preview_image_open()
        self.preview_image_set(png_preview_open, png_preview, preview)
        preview.update()

        trace_start()
        self.logger.info('Создание задачи scheduler')
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(__scheduler__, 'interval', minutes=1)

        time_sleep(2)

        __clean_preview__()
    
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
            unzip_file(path_screen_saver, file_name='play_store_512.png', path_extract=path_to_style)

    
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
    OS = 'Linux' if  platform in ['linux'] else 'Windows'
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
        file_remove(path_ico_screen_saver)

    preview = Tk()
    preview.overrideredirect(True)

    StartApp(preview)
