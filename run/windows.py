import hashlib
from sys import exit as exit_ex
from time import time
from tkinter import Text, Tk, Toplevel, filedialog, messagebox, ttk
from tkinter.messagebox import showwarning

from PIL import Image, ImageTk
from run import set_position_window_on_center
from settings import (PERSON_AGREEMENT, path_to_little_ico,
                      path_to_passwords_settings, style)
from settings.encryption import Encryption

from .functions import Passwords, get_settings, write_dict_in_file


def entry_normal(entry):
    style.style_for_normal_entry()
    entry.configure(style='Normal.TEntry')
    entry.update()


def set_warning_entry(entry):
    style.style_for_warning_entry()
    entry.configure(style='Warning.TEntry')
    entry.update()
    entry.after(3000, lambda: entry_normal(entry))


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
        self.parent = parent

        self.window = Toplevel(parent)
        self.window.wm_transient(parent)
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
            self.btn_decode = ttk.Button(
                right_frame_button, text='Декодировать'
            )
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
            self.btn_decode.bind(
                '<Button-1>',
                lambda event: self.decode_columns_values()
            )
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
        if self.edit:
            self.window.title('Редактирование пароля')
        else:
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
        if Encryption().hash_password_decode is not None:
            result = Windows(parent=self.parent).entry_password()
            if not result:
                return

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


class SetEditPasswordDecode:
    def __init__(self, parent, edit=False):
        self.edit = edit
        self.password = None
        self.show = False
        self.parent = parent

        self.window = Toplevel(parent)
        self.window.wm_transient(parent)
        self.initialize_ui()

        left_frame = ttk.Frame(self.window, padding=5)
        left_frame.grid(column=0, row=0, sticky='NSWE')
        if edit:
            old_password_frame = ttk.Frame(left_frame, padding=3)
            old_password_frame.grid(column=0, row=0, sticky='NSE')
            old_password_frame.columnconfigure(0, weight=1)
            old_password_frame.columnconfigure(1, weight=1)
        new_password_frame = ttk.Frame(left_frame, padding=5)
        new_password_frame.grid(column=0, row=1, sticky='NSE')
        new_password_retry_frame = ttk.Frame(left_frame, padding=3)
        new_password_retry_frame.grid(column=0, row=2, sticky='NSE')
        right_frame = ttk.Frame(self.window, padding=5)
        right_frame.grid(column=1, row=0, sticky='NSWE')
        right_frame_button = ttk.Frame(right_frame, padding=1)
        right_frame_button.grid(column=0, row=0, sticky='WE')

        if edit:
            ttk.Label(
                old_password_frame, text='Старый пароль',
                font=('Times New Roman', 12, 'bold italic')
            ).grid(row=0, column=0, sticky='E')
            self.old_entry = ttk.Entry(
                old_password_frame, width=39, font=('Times New Roman', 12),
                show='*'
            )
            self.old_entry.grid(row=0, column=1, sticky='WE', padx=5)
        ttk.Label(
            new_password_frame, text='Новый пароль',
            font=('Times New Roman', 12, 'bold italic')
        ).grid(row=0, column=0, sticky='E')
        self.new_entry = ttk.Entry(
            new_password_frame, width=39, font=('Times New Roman', 12),
            show='*'
        )
        self.new_entry.grid(row=0, column=1, sticky='WE', padx=5)
        ttk.Label(
            new_password_retry_frame, text='Повторите пароль',
            font=('Times New Roman', 12, 'bold italic')
        ).grid(row=0, column=0, sticky='E')
        self.retry_entry = ttk.Entry(
            new_password_retry_frame, width=39, font=('Times New Roman', 12),
            show='*'
        )
        self.retry_entry.grid(row=0, column=1, sticky='WE', padx=5)

        ttk.Button(
            right_frame_button, text='Применить',
            command=lambda: self.add_edit()
        ).grid(column=0, row=0, sticky='WE', pady=2)
        ttk.Button(
            right_frame_button, text='Отменить',
            command=lambda: self.close()
        ).grid(column=0, row=1, sticky='WE')
        ttk.Button(
            right_frame_button, text='Показать',
            command=lambda: self.show_or_not()
        ).grid(column=0, row=2, sticky='WE', pady=2)

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        left_frame.rowconfigure(2, weight=1)
        new_password_frame.columnconfigure(0, weight=1)
        new_password_frame.columnconfigure(1, weight=1)
        new_password_retry_frame.columnconfigure(0, weight=1)
        new_password_retry_frame.columnconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        self.window.bind('<Return>', lambda event: self.add_edit())
        self.window.bind('<Escape>', lambda event: self.close())

    def initialize_ui(self):
        """
        Инициализация окна
        :return:
        """
        style.set_global_style(self.window)

        w = 600
        if self.edit:
            h = 115
        else:
            h = 103
        ico = ImageTk.PhotoImage(Image.open(
            path_to_little_ico
        ))
        if self.edit:
            self.window.title('Редактирование пароля дешифровки')
        else:
            self.window.title('Добавление пароля дешифровки')
        self.window.minsize(w, h)
        self.window.maxsize(w, h)
        set_position_window_on_center(self.window, w, h)
        self.window.tk.call(
            'wm', 'iconphoto', self.window._w, ico
        )

    def show_or_not(self):
        if not self.show:
            if self.edit:
                self.old_entry.configure(show='')
            self.new_entry.configure(show='')
            self.retry_entry.configure(show='')
            self.show = True
        else:
            if self.edit:
                self.old_entry.configure(show='*')
            self.new_entry.configure(show='*')
            self.retry_entry.configure(show='*')
            self.show = False

    def add_edit(self):
        new = self.new_entry.get()
        retry = self.retry_entry.get()
        if self.edit:
            old = self.old_entry.get()
            if len(old) == 0:
                set_warning_entry(self.old_entry)
                return
            if hashlib.md5(bytes(old, 'utf-8')).hexdigest()  \
                    != Encryption().hash_password_decode:
                showwarning(
                    'Неверный пароль',
                    'Введенный вами старый пароль не верный!'
                )
                set_warning_entry(self.old_entry)
                return

        if len(new) == 0:
            set_warning_entry(self.new_entry)
            return
        if len(retry) == 0:
            set_warning_entry(self.retry_entry)
            return

        if new != retry:
            showwarning(
                'Не совпадают пароли!',
                'Новый и повторяющийся пароли не совпадают'
            )
            set_warning_entry(self.new_entry)
            set_warning_entry(self.retry_entry)
            return

        self.password = new
        self.window.destroy()

    def close(self):
        self.password = None
        self.window.destroy()


class ImportPasswords:
    def __init__(self, parent, format_pass=0):
        self.parent = parent
        self.format_pass = format_pass

        self.window = Toplevel(parent)
        self.window.wm_transient(parent)
        self.initialize_ui()

        main_frame = ttk.Frame(self.window)
        main_frame.grid(row=0, column=0, sticky='NSWE')
        object_frame = ttk.Frame(main_frame, padding=5)
        object_frame.grid(row=0, column=0, sticky='NWE', padx=5)
        columns_frame = ttk.Frame(main_frame, padding=5)
        columns_frame.grid(row=1, column=0, sticky='NWE', padx=5)
        import_frame = ttk.Frame(main_frame)
        import_frame.grid(row=2, column=0, sticky='NWE', padx=5, pady=5)

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        object_frame.columnconfigure(0, weight=1)
        object_frame.columnconfigure(1, weight=1)
        columns_frame.columnconfigure(0, weight=1)
        columns_frame.columnconfigure(1, weight=1)
        import_frame.columnconfigure(0, weight=1)

        ttk.Button(
            object_frame, text='Выбрать файл',
            command=lambda: self.get_object()
        ).grid(row=0, column=0, sticky='NWE', pady=5)
        self.entry_object = ttk.Entry(
            object_frame, state='readonly', width=55,
            font=('Times New Roman', 10, 'italic')
        )
        ttk.Label(
            columns_frame,
            text='Введите положение (цифрой, начиная отсчёт колонок с 0) '
            'name, url, username, password через запятую соответственно'
            ', если какой-то колонки нет, то вместо неё "-"',
            font=('Times New Roman', 10, 'italic'), foreground='#FF4600',
            justify='center', wrap=600
        ).grid(row=0, column=0, columnspan=2, pady=3)
        ttk.Label(
            columns_frame,
            text='Колонны:',
            font=('Times New Roman', 13, 'bold italic')
        ).grid(row=1, column=0, sticky='NE')
        self.entry_columns = ttk.Entry(
            columns_frame, width=54,
            font=('Times New Roman', 11, 'italic')
        )
        ttk.Label(
            columns_frame,
            text='Введите разделитель колонок (по умолчанию ",")',
            font=('Times New Roman', 10, 'italic'), foreground='#FF4600',
            justify='center'
        ).grid(row=2, column=0, columnspan=2, pady=3)
        ttk.Label(
            columns_frame, text='Разделитель:',
            font=('Times New Roman', 13, 'bold italic')
        ).grid(row=3, column=0, sticky='NE')
        self.entry_separator = ttk.Entry(
            columns_frame, font=('Times New Roman', 11, 'italic')
        )

        ttk.Button(
            import_frame, text='Импортировать',
            command=lambda: self.import_passwords()
        ).grid(row=0, column=0)

        self.entry_object.grid(row=0, column=1, sticky='NWE', padx=5, pady=5)
        self.entry_columns.grid(row=1, column=1, sticky='NWE', padx=2)
        self.entry_separator.grid(row=3, column=1, sticky='NWE', padx=2)

        self.entry_columns.insert('0', '-,0,1,2')
        self.entry_separator.insert('0', ',')

    def initialize_ui(self):
        """
        Инициализация окна
        :return:
        """
        style.set_global_style(self.window)

        w = 600
        h = 210
        ico = ImageTk.PhotoImage(Image.open(
            path_to_little_ico
        ))
        if self.format_pass == 0:
            self.window.title('Импортирование паролей из csv')
        elif self.format_pass == -1:
            self.window.title('Импортирование паролей из файла')

        self.window.minsize(w, h)
        self.window.maxsize(w, h)
        set_position_window_on_center(self.window, w, h)
        self.window.tk.call(
            'wm', 'iconphoto', self.window._w, ico
        )

    def get_object(self):
        if self.format_pass == 0:
            types = ('csv files', '*.csv')
        if self.format_pass == -1:
            types = ('all files', '*.*')

        file = str(filedialog.askopenfilename(filetypes=[types]))
        if len(file) == '':
            return

        self.entry_object.configure(state='normal')
        self.entry_object.delete('0', 'end')
        self.entry_object.insert('0', file)
        self.entry_object.configure(state='readonly')
        self.entry_object.update()

    def import_passwords(self):
        def val_error_columns_else_int(txt, name_col):
            if txt != '-':
                try:
                    return int(txt)
                except ValueError:
                    messagebox.showerror(
                        'Ошибка',
                        f'Колонка {name_col} названа неверно!\n\nЕсли '
                        'нет такой колонки, то "-"\nИначе укажите '
                        f'номер колонки, начиная с 0\n\nВы назвали {txt}'
                    )
                    return None
            return txt

        path = self.entry_object.get()
        separator = self.entry_separator.get()
        pos_columns = self.entry_columns.get()

        if path == '':
            set_warning_entry(self.entry_object)
            return
        if pos_columns == '':
            set_warning_entry(self.entry_columns)
            return
        if separator == '':
            set_warning_entry(self.entry_separator)
            return

        pos_columns = pos_columns.split(',')
        if len(pos_columns) != 4:
            messagebox.showwarning(
                'Ошибка', 'Вы указали позиции не для всех 4-ех элементов!'
            )
            set_warning_entry(self.entry_columns)
            return
        _name = pos_columns[0]
        _url = pos_columns[1]
        _login = pos_columns[2]
        _password = pos_columns[3]

        _name = val_error_columns_else_int(_name, 'name')
        _url = val_error_columns_else_int(_url, 'url')
        _login = val_error_columns_else_int(_login, 'username')
        _password = val_error_columns_else_int(_password, 'password')
        if None in [_name, _url, _login, _password]:
            return
        if _login == '-' and _password == '-':
            messagebox.showerror(
                'Ошибка',
                'Поля username и password не могут быть оба равны "-"'
            )
            return

        with open(path, 'r', encoding='UTF-8') as file:
            _passwords = [
                item.strip().split(separator) for item in file.readlines()
            ]
            del _passwords[0]

        if _password == '-':
            columns = 'Логин'
        elif _login == '-':
            columns = 'Пароль'
        else:
            columns = 'Логин&&Пароль'

        encryption_class = Encryption()
        columns = encryption_class.encrypt(columns)
        passwords = {}
        k = 0

        for item in _passwords:
            try:
                if _name != '-':
                    name = item[_name]
                else:
                    name = f'import_password_{k}'
                    k += 1
                url = item[_url] if _url != '-' else ''
                if _passwords == '-':
                    value_pass = str(item[_login])
                elif _login == '-':
                    value_pass = str(item[_password])
                else:
                    value_pass = f'{item[_login]}&&{item[_password]}'
            except IndexError:
                continue

            if value_pass == '' or value_pass == '&&':
                continue

            value_pass = encryption_class.encrypt(value_pass)

            passwords[name] = {
                'columns': columns,
                'values': value_pass,
                'url': url
            }

        length = len(passwords)
        if length > 0:
            Passwords().add_password(passwords)

        messagebox.showinfo(
            'Импортировано',
            f'Импортировано {length} паролей.\n\nЕсли кол-во не совпадает '
            'с нужным, занчит при импортировании каких-то паролей'
            ' произошла ошибка! (Возможно были повторяющиеся)'
        )
        self.window.destroy()
        return


class EntryPassword:
    def __init__(self, parent):
        self.result = False
        self.show = False

        self.window = Toplevel(parent)
        self.window.wm_transient(parent)
        self.initialize_ui()

        left_frame = ttk.Frame(self.window, padding=3)
        right_frame = ttk.Frame(self.window, padding=2)
        pass_frame = ttk.Frame(left_frame)
        button_frame = ttk.Frame(right_frame)
        left_frame.grid(row=0, column=0, sticky='NSWE')
        right_frame.grid(row=0, column=1, sticky='NSWE')
        pass_frame.grid(row=0, column=0, sticky='WE')
        button_frame.grid(row=0, column=0, sticky='NSWE')

        ttk.Label(
            pass_frame, text='Пароль дешифровки',
            font=('Times New Roman', 12, 'bold italic')
        ).grid(row=0, column=0, sticky='E')
        self.entry_password = ttk.Entry(
            pass_frame, font=('Times New Roman', 12), width=39,
            show='*'
        )
        self.entry_password.grid(row=0, column=1, sticky='E', padx=5)

        ttk.Button(
            button_frame, text='Применить',
            command=lambda: self.done()
        ).grid(row=0, column=0, sticky='WE', pady=3)
        ttk.Button(
            button_frame, text='Отмена',
            command=lambda: self.close()
        ).grid(row=1, column=0, sticky='WE')
        ttk.Button(
            button_frame, text='Показать',
            command=lambda: self.show_or_not()
        ).grid(row=2, column=0, sticky='WE')

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        self.window.bind('<Return>', lambda event: self.done())
        self.window.bind('<Escape>', lambda event: self.close())

    def initialize_ui(self):
        """
        Инициализация окна
        :return:
        """
        style.set_global_style(self.window)

        w = 600
        h = 103
        ico = ImageTk.PhotoImage(Image.open(
            path_to_little_ico
        ))
        self.window.title('Введите пароль дешифровки')
        self.window.minsize(w, h)
        self.window.maxsize(w, h)
        set_position_window_on_center(self.window, w, h)
        self.window.tk.call(
            'wm', 'iconphoto', self.window._w, ico
        )

    def done(self):
        password = self.entry_password.get()
        password_decode = Encryption().hash_password_decode

        if len(password) == 0:
            set_warning_entry(self.entry_password)
            return

        if hashlib.md5(bytes(password, 'utf-8')).hexdigest()  \
                != password_decode:
            showwarning(
                'Неверный пароль',
                'Вы ввели неверный пароль'
            )
            set_warning_entry(self.entry_password)
            return

        self.result = True
        self.window.destroy()

    def close(self):
        self.result = None
        self.window.destroy()

    def show_or_not(self):
        if self.show:
            self.show = False
            self.entry_password.configure(show='*')
        else:
            self.show = True
            self.entry_password.configure(show='')


class Windows:
    """
    Класс дополнительных окон
    """

    def __init__(self, parent=None):
        self.person_and_agreement_data_window = PersonAndAgreementData
        self._add_password_or_edit = AddPassword
        self.set_edit_password_decode = SetEditPasswordDecode
        self.entry_password_ = EntryPassword
        self.import_passwords = ImportPasswords
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

    def set_or_edit_password_decode(self, edit=False):
        window = self.set_edit_password_decode(self.parent, edit)
        window.window.wait_window()
        password = window.password
        if password is None:
            return False

        passwords_set = Encryption().settings
        passwords_set['password_decode'] =  \
            hashlib.md5(bytes(password, 'utf-8')).hexdigest()
        write_dict_in_file(path_to_passwords_settings, passwords_set)
        return True

    def entry_password(self):
        window = self.entry_password_(self.parent)
        window.window.wait_window()
        return window.result

    def import_passwords_from_file(self, format_pass=0):
        window = self.import_passwords(self.parent, format_pass)
        window.window.wait_window()
        return
