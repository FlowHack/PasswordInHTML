from gc import enable
from os.path import isfile
from settings.encryption import Encryption
from sys import exit as exit_ex
from tkinter import Listbox, TclError, Tk, ttk, IntVar

from PIL import Image, ImageTk

from run import unzip_file
from run.windows import Windows
from settings import *

from .functions import Passwords, check_update, get_settings, set_position_window_on_center, update_app, write_dict_in_file
from .html_generate import generate_template


class App(Tk):
    """
    Класс отвечающий за запуск главного окна и его создание
    """

    def __init__(self, auto_update, OS):
        """
        Создание главного окна, вкладок и управление функциями
        :param update: нужно ли проверить обновление
        :param OS_NAME: имя операционной системы
        :return
        """
        super().__init__()
        self.OS = OS
        self.app_ico = self.get_app_ico()
        self.initialize_ui()

        notebook = ttk.Notebook(self)
        self.main = ttk.Frame(notebook, padding=15)
        self.settings = ttk.Frame(notebook)
        notebook.add(self.main, text='Пароли')
        notebook.add(self.settings, text='Настройки')
        notebook.pack(expand=True, fill='both')

        self.update()
        self.build()

        if auto_update == 1:
            LOGGER('update', 'master').info('Начинаем процесс проверки обновлений')
            check_update(os_name=self.OS)

        self.mainloop()
    
    @staticmethod
    def get_app_ico():
        """
        Функция получения всех иконок в случае ошибки запустится проверка
        иконок
        :return: Словарь {имя: переменная готовой иконки}
        """
        if not isfile(path_to_little_ico):
            unzip_file(
                path_icos_zip, file_name='LittlePassHTML.ico', 
                path_extract=path_to_style
                )
        little_phtml_ico = ImageTk.PhotoImage(Image.open(
            path_to_little_ico
        ))

        return {
            'LittlePassHTML_ico': little_phtml_ico
        }

    def initialize_ui(self):
        """
        Функция настройки окна пограммы
        :return:
        """
        self.title('PasswordInHTML')
        self.tk.call('wm', 'iconphoto', self._w, self.app_ico['LittlePassHTML_ico'])
        style.set_global_style(self)
        w = 800
        h = 400
        set_position_window_on_center(self, width=w, height=h)
        self.minsize(w, h)
        self.maxsize(w, h)
        self.protocol('WM_DELETE_WINDOW', clean_after_app)
    
    def build(self):
        self.generate_main()
        self.build_settings()
        self.update()
    
    def build_settings(self):
        theme_frame = ttk.Frame(self.settings)
        theme_frame.grid(row=0, column=0, sticky='NWE', padx=5)
        password_frame = ttk.Frame(self.settings)
        password_frame.grid(row=1, column=0, sticky='NWE', padx=5, pady=5)
        update_frame = ttk.Frame(self.settings)
        update_frame.grid(row=2, column=0, sticky='NWE', padx=5)
        load_frame = ttk.Frame(self.settings)
        load_frame.grid(row=0, column=1, padx=8, sticky='NWE')

        self.loading_set = ttk.Label(
            load_frame, text='Изменение', font=('Times New Roman', 13, 'bold italic'),
            foreground='#00FF74'
        )
        self.loading_set.grid(row=0, column=0, sticky='WE')
        self.loading_set.grid_remove()

        ttk.Label(
            theme_frame, text='Тема оформления',
            font=('Times New Roman', 13, 'bold italic')
        ).grid(row=0, column=0, sticky='NE')
        self.theme_var = IntVar()
        settings = get_settings()
        if settings['theme'] == style.dark_theme:
            self.theme_var.set(1)
        else:
            self.theme_var.set(0)
        theme_light = ttk.Radiobutton(
            theme_frame, text='Светлая', value=0, variable=self.theme_var
        )
        theme_dark = ttk.Radiobutton(
            theme_frame, text='Темная', value=1, variable=self.theme_var
        )

        theme_light.grid(row=0, column=1, sticky='WN', padx=10)
        theme_dark.grid(row=0, column=2, sticky='WN')

        if Encryption().hash_password_decode is None:
            ttk.Button(
                password_frame, text='Установить пароль для дешифровки',
                command=lambda: self.add_edit_password_decript()
            ).grid(row=0, column=0, sticky='NWE')
        else:
            ttk.Button(
                password_frame, text='Сменить пароль для дешифровки',
                command=lambda: self.add_edit_password_decript(edit=True)
            ).grid(row=0, column=0, sticky='NWE')
            ttk.Button(
                password_frame, text='Удалить пароль для дешифровки',
                command=lambda: self.delete_password_decode()
            ).grid(row=0, column=1, sticky='NWE', padx=5)
        
        ttk.Label(
            update_frame, text='Автообновление', 
            font=('Times New Roman', 13, 'bold italic')
        ).grid(row=0, column=0, sticky='WN')
        self.auto_update_var = IntVar()
        settings = get_settings()
        if settings['auto_update'] == 1:
            self.auto_update_var.set(1)
        else:
            self.auto_update_var.set(0)
        autoupdate_on = ttk.Radiobutton(
            update_frame, text='Включено', value=1, variable=self.auto_update_var
        )
        autoupdate_off = ttk.Radiobutton(
            update_frame, text='Отключено', value=0, variable=self.auto_update_var
        )
        ttk.Button(
            update_frame, text='Проверить наличие обновления',
            command=lambda: check_update(os_name=self.OS, call=True),
            cursor='exchange' 
        ).grid(row=0, column=3, sticky='W', padx=5)
        autoupdate_on.grid(row=0, column=1, sticky='NW', padx=5)
        autoupdate_off.grid(row=0, column=2, sticky='NW')

        theme_light.bind('<Button-1>', lambda event: self.click_to_radio_theme())
        theme_dark.bind('<Button-1>', lambda event: self.click_to_radio_theme())
        autoupdate_on.bind('<Button-1>', lambda event: self.click_to_radio_auto_update())
        autoupdate_off.bind('<Button-1>', lambda event: self.click_to_radio_auto_update())

        self.settings.columnconfigure(0, weight=1)
        load_frame.rowconfigure(0, weight=1)

    def click_to_radio_auto_update(self):
        var = self.auto_update_var.get()
        settings = get_settings()

        if var == 0:
            self.auto_update_var.set(1)
            self.loading_set.grid()
            self.loading_set.after(4000, lambda: self.loading_set.grid_remove())
            settings['auto_update'] = 1
            write_dict_in_file(path_to_settings_json, settings)
        else:
            self.auto_update_var.set(0)
            self.loading_set.grid()
            self.loading_set.after(4000, lambda: self.loading_set.grid_remove())
            settings['auto_update'] = 0
            write_dict_in_file(path_to_settings_json, settings)       
    
    def add_edit_password_decript(self, edit=False):
        Windows(self).set_or_edit_password_decode(edit)
        self.build_settings()
    
    def delete_password_decode(self):
        if Encryption().hash_password_decode is not None:
            result = Windows(parent=self).entry_password()
            if not result:
                return
        
        settings = Encryption().settings
        del settings['password_decode']
        write_dict_in_file(path_to_passwords_settings, settings)
        self.build_settings()
    
    def click_to_radio_theme(self):
        var = self.theme_var.get()
        settings = get_settings()

        if var == 0:
            self.theme_var.set(1)
            self.loading_set.grid()
            self.loading_set.after(4000, lambda: self.loading_set.grid_remove())
            settings['theme'] = style.dark_theme
            write_dict_in_file(path_to_settings_json, settings)
        else:
            self.theme_var.set(0)
            self.loading_set.grid()
            self.loading_set.after(4000, lambda: self.loading_set.grid_remove())
            settings['theme'] = style.light_theme
            write_dict_in_file(path_to_settings_json, settings)
    
    def generate_main(self):
        top_frame = ttk.Frame(self.main, padding=2)
        left_frame = ttk.Frame(self.main, relief='solid', borderwidth=1, padding=5)
        right_frame = ttk.Frame(self.main, padding=5)
        right_top_frame = ttk.Frame(right_frame)
        right_center_frame = ttk.Frame(right_frame)
        right_bottom_frame = ttk.Frame(right_frame)
        top_frame.grid(row=0, column=0, columnspan=2, sticky='WE', pady=2, padx=3)
        left_frame.grid(row=1, column=0, sticky='NSWE', padx=3, pady=3)
        right_frame.grid(row=1, column=1, sticky='NSWE', padx=3, pady=3)
        right_top_frame.grid(row=0, column=0, sticky='WE')
        right_center_frame.grid(row=1, column=0, sticky='WE')
        right_bottom_frame.grid(row=2, column=0, sticky='WE')     

        self.search = ttk.Entry(top_frame, width=73, font=('Times New Roman', 12))
        btn_search = ttk.Button(top_frame, text='Найти')
        btn_throw_off = ttk.Button(top_frame, text='Сбросить')
        self.list_password = Listbox(
            left_frame, borderwidth=1, height=11, width=62,
            cursor='dot', font=('Times New Roman', 15)
        )
        generate = ttk.Button(right_top_frame, text='Генерировать', width=13, cursor='star')
        add = ttk.Button(right_center_frame, text='Добавить', width=13, cursor='plus')
        self.edit = ttk.Button(
            right_center_frame, text='Редактировать', width=13, cursor='pencil', state='disable'
        )
        self.delete = ttk.Button(
            right_bottom_frame, text='Удалить', width=13, cursor='circle', state='disable'
        )
        self.delete_all = ttk.Button(
            right_bottom_frame, text='Удалить все', width=13, cursor='pirate'
        )

        self.search.grid(row=0, column=0)
        btn_search.grid(row=0, column=1, padx=4)
        btn_throw_off.grid(row=0, column=2, )
        self.list_password.grid(row=0, column=0, sticky='NSWE')
        generate.grid(row=0, column=0, sticky='NWE')
        add.grid(row=1, column=0, sticky='NWE')
        self.edit.grid(row=2, column=0, sticky='NWE', pady=3)
        self.delete.grid(row=3, column=0, sticky='NWE')
        self.delete_all.grid(row=4, column=0, sticky='NWE', pady=3)

        right_frame.rowconfigure(0, weight=2)
        right_frame.rowconfigure(1, weight=2)
        right_frame.rowconfigure(2, weight=2)

        self.completetion_into_listbox()

        self.list_password.bind('<<ListboxSelect>>', lambda event: self.enable_button_touch())
        self.list_password.bind('<Double-Button-1>', lambda event: self.edit_password())
        self.list_password.bind('<Delete>', lambda event: self.delete_password())
        self.delete.bind('<Button-1>', lambda event: self.delete_password())
        self.delete_all.bind('<Button-1>', lambda event: self.delete_all_passwords())
        add.bind('<Button-1>', lambda event: self.add_password())
        self.edit.bind('<Button-1>', lambda event: self.edit_password())
        btn_search.bind('<Button-1>', lambda event: self.completetion_into_listbox(True))
        btn_throw_off.bind('<Button-1>', lambda event: self.throw_off())
        generate.bind('<Button-1>', lambda event: generate_template())
    
    def update_list(self):
        self.list_password.delete(0, 'end')
        self.completetion_into_listbox()
        self.disable_button_touch()
    
    def enable_button_touch(self):
        passwords = Passwords()

        if len(passwords.name_passwords) > 0:
            self.edit.configure(state='enable')
            self.delete.configure(state='enable')
    
    def disable_button_touch(self):
        self.edit.configure(state='disable')
        self.delete.configure(state='disable')
    
    def throw_off(self):
        self.search.delete(0, 'end')
        self.completetion_into_listbox()
    
    def completetion_into_listbox(self, search=False):
        self.list_password.delete(0, 'end')
        self.disable_button_touch()
        passwords = sorted(Passwords().name_passwords)

        if search is not False:
            fraze = self.search.get()

            k = 0
            for i in range(len(passwords)):
                name_password = passwords[i]
                if fraze in name_password:
                    self.list_password.insert(k, name_password)
                    k += 1
            
            if k == 0:
                self.list_password.insert(k, 'Ничего не найдено')
            return

        for i in range(len(passwords)):
            name_password = passwords[i]
            self.list_password.insert(i, name_password)
    
    def delete_password(self):
        if Encryption().hash_password_decode is not None:
            result = Windows(parent=self).entry_password()
            if not result:
                return

        name = self.get_record()
        if name is None:
            return
        Passwords().delete_password(name)
        self.update_list()
    
    def delete_all_passwords(self):
        if Encryption().hash_password_decode is not None:
            result = Windows(parent=self).entry_password()
            if not result:
                return

        Passwords().delete_all_passwords()
        self.update_list()

    def get_record(self):
        try:
            cure = self.list_password.curselection()
            return self.list_password.get(cure)
        except TclError:
            self.disable_button_touch()
            return
    
    def add_password(self):
        windows = Windows(self)
        windows.add_password_or_edit()
        self.update_list()
    
    def edit_password(self):
        name = self.get_record()
        if name is None:
            return 

        if Encryption().hash_password_decode is not None:
            result = Windows(parent=self).entry_password()
            if not result:
                return
        
        windows = Windows(self)
        windows.add_password_or_edit(edit=True, name=name)
        self.update_list()
