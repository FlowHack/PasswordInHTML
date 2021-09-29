import os
from sys import exit as exit_ex
from time import time
from tkinter import Text, Tk, Toplevel, messagebox, ttk
from tkinter.messagebox import showwarning

from PIL import Image, ImageTk

from run import set_position_window_on_center
from settings import PERSON_AGREEMENT, path_to_little_ico, style
from settings.encryption import Encryption

from .functions import Passwords, get_settings


class PersonAndAgreementData:
    """
    Класс отвечающий за окно персонального соглашения и лицензионного
    """

    def __init__(self):
        self.start_function_time = time()
        self.agreement = False
        self.lose_agreement_count: int = 0

        self.agreement_window = Tk()
        self.initialize_ui()

        main_frame = ttk.Frame(self.agreement_window, padding=10)
        main_frame.pack(side='top', fill='both', expand=True)

        text = Text(main_frame, wrap='word', width=71, height=14)
        text.insert(1.0, PERSON_AGREEMENT)
        text.grid(row=0, column=0, sticky='NSEW', columnspan=2)

        btn_agreement = ttk.Button(main_frame, text='Принять')
        btn_agreement.grid(row=1, column=0, sticky='EW', pady=5)
        ttk.Button(
            main_frame, text='Отмена', command=exit_ex
        ).grid(row=1, column=1, sticky='EW')

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        btn_agreement.bind(
            '<Button-3>', lambda event: self.done_agreement()
        )
        btn_agreement.bind(
            '<Button-1>', lambda event: self.lose_agreement()
        )

    def initialize_ui(self):
        """
        Инициализация окна
        :return:
        """
        style.set_global_style(self.agreement_window)
        style.style_for_ok_and_close_btn()
        style.style_for_warning_entry()

        w = 600
        h = 300
        ico = ImageTk.PhotoImage(Image.open(
            path_to_little_ico
        ))
        self.agreement_window.title('Пользовательское соглашение!')
        set_position_window_on_center(self.agreement_window, w, h)
        self.agreement_window.tk.call(
            'wm', 'iconphoto', self.agreement_window._w, ico
        )
        self.agreement_window.protocol('WM_DELETE_WINDOW', exit_ex)

    def done_agreement(self):
        """
        Обработка нажатия
        :return:
        """
        self.agreement = True
        self.agreement_window.destroy()

    def lose_agreement(self):
        """
        Шуточная обработка неправильного подтверждения прочтения
        :return:
        """
        if self.lose_agreement_count == 0:
            messagebox.showinfo(
                'Прочтите пользовательское соглашение!',
                'Вы не прочитали соглашение!'
            )
            self.lose_agreement_count = 1
        elif self.lose_agreement_count == 1:
            messagebox.showinfo(
                'Прочтите пользовательское соглашение!',
                'Вы не собираетесь читать пользовательское '
                'соглашение?!\n\nЯ всё же настаиваю на его прочтении! '
            )
            self.lose_agreement_count = 2
        elif self.lose_agreement_count == 2:
            lose_time = time() - self.start_function_time
            messagebox.showwarning(
                'Прочтите пользовательское соглашение!',
                f'Я придумал! Буду считать сколько времени вы тратите '
                f'впустую.\nНа данный момент вы потратили '
                f'{lose_time:.0f}сек.\n\nПрочитайте пользовательское '
                f'соглашение! '
            )
            self.lose_agreement_count = 3
        else:
            lose_time = time() - self.start_function_time
            messagebox.showwarning(
                'Прочтите пользовательское соглашение!',
                f'На данный момент вы потратили {lose_time:.0f}сек.\n\nНе '
                f'тратьте своё время просто так. Прочитайте '
                f'пользовательское соглашение! '
            )

class AddPassword:
    def __init__(self, parent, edit, name):
        self.password = None
        self.edit = edit
        self.name = name
        self.decode = False

        self.window = Toplevel(parent)
        self.initialize_ui()

        left_frame = ttk.Frame(self.window, padding=5, borderwidth=1)
        left_frame_name = ttk.Frame(left_frame, padding=1)
        left_frame_top = ttk.Frame(left_frame, padding=1)
        left_frame_average = ttk.Frame(left_frame, padding=1)
        left_frame_bottom = ttk.Frame(left_frame, padding=1)
        right_frame = ttk.Frame(self.window, padding=5, borderwidth=1)
        right_frame_button = ttk.Frame(right_frame)
        left_frame.grid(column=0, row=0, sticky='NSWE')
        left_frame_name.grid(column=0, row=0, sticky='NSE')
        left_frame_top.grid(column=0, row=1, sticky='NSE')
        left_frame_average.grid(column=0, row=2, sticky='NSE')
        left_frame_bottom.grid(column=0, row=3, sticky='NSE')
        right_frame.grid(column=1, row=0, sticky='NSWE')
        right_frame_button.grid(column=0, row=0, sticky='WE')

        ttk.Label(
            left_frame_name, text='Название', font=('Times New Roman', 12)
        ).grid(row=0, column=0, sticky='E')
        self.entry_name = ttk.Entry(
            left_frame_name, width=50, font=('Times New Roman', 12)
        )
        ttk.Label(
            left_frame_top, text='Необязательно',
            font=('Times New Roman', 9), foreground='#FF4600'
        ).grid(row=0, column=0, columnspan=2)
        ttk.Label(
            left_frame_top, text='Ссылка', font=('Times New Roman', 12)
        ).grid(row=1, column=0, sticky='E')
        self.entry_url = ttk.Entry(
            left_frame_top, width=50, font=('Times New Roman', 12)
        )
        ttk.Label(
            left_frame_average, text='Введите названия колонок через &&', 
            font=('Times New Roman', 9), foreground='#FF4600'
            ).grid(row=0, column=0, columnspan=2)
        ttk.Label(
            left_frame_average, text='Колонки', font=('Times New Roman', 12)
        ).grid(row=1, column=0, sticky='E')
        self.entry_columns = ttk.Entry(
            left_frame_average, width=50, font=('Times New Roman', 12)
        )
        ttk.Label(
            left_frame_bottom, text='Введите значения колонок через &&', 
            font=('Times New Roman', 9), foreground='#FF4600'
            ).grid(row=0, column=0, columnspan=2)
        ttk.Label(
            left_frame_bottom, text='Значения', font=('Times New Roman', 12)
        ).grid(row=1, column=0, sticky='E')
        self.entry_values = ttk.Entry(
            left_frame_bottom, width=50, font=('Times New Roman', 12)
        )
        if edit:
            self.btn_decode = ttk.Button(right_frame_button, text='Декодировать')
            btn_add = ttk.Button(right_frame_button, text='Редактировать')
        else:
            btn_add = ttk.Button(right_frame_button, text='Добавить')
        btn_cancel = ttk.Button(right_frame_button, text='Отмена')

        self.entry_name.grid(row=0, column=1, sticky='WE', padx=4)
        self.entry_url.grid(row=1, column=1, sticky='WE', padx=4)
        self.entry_columns.grid(row=1, column=1, sticky='WE', padx=4)
        self.entry_values.grid(row=1, column=1, sticky='WE', padx=4)
        if edit:
            self.btn_decode.grid(row=0, column=0, sticky='WE')
            btn_add.grid(row=1, column=0, sticky='WE', pady=3)
            btn_cancel.grid(row=2, column=0, sticky='WE')
        else:
            btn_add.grid(row=0, column=0, sticky='WE', pady=3)
            btn_cancel.grid(row=1, column=0, sticky='WE')

        self.window.columnconfigure(0, weight=5)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        left_frame.rowconfigure(2, weight=1)
        left_frame.rowconfigure(3, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)


        self.completetion_entry_columns()

        btn_cancel.bind('<Button-1>', lambda event: self.close())
        btn_add.bind('<Button-1>', lambda event: self.add_password())
        if edit:
            self.btn_decode.bind('<Button-1>', lambda event: self.decode_columns_values())
            self.entry_columns.configure(state='readonly')
            self.entry_values.configure(state='readonly')
        self.window.bind('<Return>', lambda event: self.add_password())
        self.window.bind('<Escape>', lambda event: self.close())
    
    def initialize_ui(self):
        """
        Инициализация окна
        :return:
        """
        style.set_global_style(self.window)

        w = 600
        h = 200
        ico = ImageTk.PhotoImage(Image.open(
            path_to_little_ico
        ))
        self.window.title('Добавление пароля')
        self.window.minsize(w, h)
        self.window.maxsize(w, h)
        set_position_window_on_center(self.window, w, h)
        self.window.tk.call(
            'wm', 'iconphoto', self.window._w, ico
        )
    
    def close(self):
        self.password = None
        self.window.destroy()
    
    def completetion_entry_columns(self):
        if self.edit:
            password = Passwords().passwords_dict[self.name]

            self.entry_name.insert(0, self.name)
            self.entry_url.insert(0, password['url'])
            self.entry_columns.insert(0, password['columns'])
            self.entry_values.insert(0, password['values'])
        else:
            settings = get_settings()
            self.entry_columns.insert(0, settings['default_columns'])
    
    def decode_columns_values(self):
        columns = self.entry_columns.get()
        values = self.entry_values.get()

        encryption = Encryption()
        columns = encryption.decryption(columns)
        values = encryption.decryption(values)

        self.entry_columns.configure(state='normal')
        self.entry_values.configure(state='normal')
        self.entry_columns.delete(0, 'end')
        self.entry_values.delete(0, 'end')
        self.entry_columns.insert(0, columns)
        self.entry_values.insert(0, values)
        self.btn_decode.destroy()

        self.decode = True
    
    def add_password(self):
        def entry_normal(entry):
            style.style_for_normal_entry()
            entry.configure(style='Normal.TEntry')
            entry.update()
        
        def set_warning_entry(entry):
            style.style_for_warning_entry()
            entry.configure(style='Warning.TEntry')
            entry.update()
            entry.after(3000, lambda: entry_normal(entry))

        name = self.entry_name.get()
        if name in Passwords().name_passwords and not self.edit:
            showwarning(
                'Есть с таким именем',
                'Запись с таким именем уже имеется!'
            )
            return

        url = self.entry_url.get()
        _columns = self.entry_columns.get()
        _values = self.entry_values.get()
        if self.edit and self.decode is False:
            encrypt = Encryption()
            _columns = encrypt.decryption(_columns)
            _values = encrypt.decryption(_values)

        columns = _columns.split('&&')
        values = _values.split('&&')

        if len(name) == 0:
            set_warning_entry(self.entry_name)
            return
        if len(columns) == 1 and columns[0] == '':
            set_warning_entry(self.entry_columns)
            return
        if len(values) == 1 and values[0] == '':
            set_warning_entry(self.entry_values)
            return
        
        if len(columns) != len(values):
            showwarning(
                'Неверное значение',
                'Количество колонок не соответствует количеству значений'    
            )
            set_warning_entry(self.entry_columns)
            set_warning_entry(self.entry_values)
            return
        
        encryptyon_func = Encryption()
        columns = encryptyon_func.encrypt(_columns)
        values = encryptyon_func.encrypt(_values)

        self.password = {
            name: {
                'columns': columns,
                'values': values,
                'url': url
            } 
        }
        self.window.destroy()

class Windows:
    """
    Класс дополнительных окон
    """

    def __init__(self, parent=None):
        self.person_and_agreement_data_window = PersonAndAgreementData
        self._add_password_or_edit = AddPassword
        self.parent = parent

    def person_and_agreement_data(self):
        """
        Функция запуска окна лицензионного соглашения и получения из него
        данных
        :return:
        """
        window = self.person_and_agreement_data_window()
        window.agreement_window.wait_window()

        return window.agreement
    
    def add_password_or_edit(self, edit=False, name=False):
        window = self._add_password_or_edit(self.parent, edit, name)
        window.window.wait_window()
        password = window.password
        if password is None:
            return False
        
        if edit:
            Passwords().edit_password(password, name)
        else:
            Passwords().add_password(password)
        return True
