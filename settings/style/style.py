from tkinter.ttk import Style

from _tkinter import TclError
from settings import path_to_main_style

DEFAULT_STYLE = 'awdark'
BUTTON_BACKGROUND = '#6D6D6D'
light_theme = {
    'font-color': '#494949',
    'back-color': '#DBDBDB',
    'back_card_color': '#f1efef'
}

dark_theme = {
    'font-color': '#DBDBDB',
    'back-color': '#494949',
    'back_card_color': '#292929'
}

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

def style_for_ok_and_close_btn() -> None:
    """
    Функция создания стилей для кнопок Ок и Отмена
    :return:
    """
    style = Style()
    style.map("OK.TButton",
              foreground=[
                  ('pressed', 'white'), ('active', 'green')
              ],
              background=[
                  ('pressed', '#5CFF5D'),
                  ('active', '#A5FF99'),
                  ('!disabled', BUTTON_BACKGROUND)
              ],
              )
    style.map(
        'Close.TButton',
        foreground=[('pressed', 'black'), ('active', '#B20007')],
        background=[('pressed', '#B20007'), ('active', '#FFA3B5')]
    )


def style_for_warning_entry() -> None:
    """
    Функция создания стиля для пустого Entry
    :return:
    """
    style = Style()
    try:
        style.element_create('plain.field', 'from', 'clam')
    except TclError as error:
        if str(error) == 'Duplicate element plain.field':
            pass
    style.layout('Warning.TEntry',
                 [('Entry.plain.field', {'children': [(
                     'Entry.background', {'children': [(
                         'Entry.padding', {'children': [(
                             'Entry.textarea', {'sticky': 'nswe'})],
                             'sticky': 'nswe'})], 'sticky': 'nswe'})],
                     'border': '2', 'sticky': 'nswe'})])
    style.configure('Warning.TEntry', fieldbackground='#FFA3AD', foreground='#191C1D')


def style_for_normal_entry() -> None:
    """
    Функция создания стиля для пустого Entry
    :return:
    """
    style = Style()
    try:
        style.element_create('plain.field', 'from', 'clam')
    except TclError as error:
        if str(error) == 'Duplicate element plain.field':
            pass
    style.layout('Normal.TEntry',
                 [('Entry.plain.field', {'children': [(
                     'Entry.background', {'children': [(
                         'Entry.padding', {'children': [(
                             'Entry.textarea', {'sticky': 'nswe'})],
                             'sticky': 'nswe'})], 'sticky': 'nswe'})],
                     'border': '2', 'sticky': 'nswe'})])
    style.configure('Warning.TEntry', fieldbackground='#191C1D', foreground='#FFFFFF')
