from tkinter.ttk import Style

from _tkinter import TclError

from settings import path_to_main_style

DEFAULT_STYLE = 'awdark'

def set_global_style(parent: object) -> None:
    """
    Функция утановки стиля для окна
    :param parent: объект окна
    :return:
    """
    default_style = DEFAULT_STYLE

    try:
        parent.tk.call('lappend', 'auto_path', f'{path_to_main_style}')
        parent.tk.call('package', 'require', DEFAULT_STYLE)
    except TclError as error:
        if str(error) == 'can\'t find package awdark':
            default_style = 'alt'

    style = Style()
    style.theme_use(default_style)