import os
from sys import exit as exit_ex
from time import time
from tkinter import Text, Tk, messagebox, ttk

from PIL import ImageTk

from run import set_position_window_on_center
from settings import PERSON_AGREEMENT, path_to_little_ico, style


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
        FPVK = ImageTk.PhotoImage(
            file=path_to_little_ico
        )
        self.agreement_window.title('Пользовательское соглашение!')
        set_position_window_on_center(self.agreement_window, w, h)
        self.agreement_window.tk.call(
            'wm', 'iconphoto', self.agreement_window._w, FPVK
        )
        self.agreement_window.protocol("WM_DELETE_WINDOW", exit_ex)

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

class Windows:
    """
    Класс дополнительных окон
    """

    def __init__(self):
        self.person_and_agreement_data_window = PersonAndAgreementData

    def person_and_agreement_data(self):
        """
        Функция запуска окна лицензионного соглашения и получения из него
        данных
        :return:
        """
        window = self.person_and_agreement_data_window()

        window.agreement_window.wait_window()

        return window.agreement
