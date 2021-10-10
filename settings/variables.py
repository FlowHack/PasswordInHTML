from os import getcwd
from os.path import join as path_join

VERSION = '1.0.3'

UPDATE_WIN = 'updater.exe'
UPDATE_LINUX = 'updater.sh'
REPO_URL_VERSION = 'https://github.com/FlowHack/PasswordInHTML/archive/refs/heads/version.zip'
REPO_URL_UPDATER = 'https://github.com/FlowHack/PasswordInHTML/archive/refs/heads/updater.zip'
REPO_BRANCH_VERSION = 'PasswordInHTML-version'
REPO_BRANCH_UPDATER = 'PasswordInHTML-updater'
REPO_BRANCH_MASTER = 'PasswordInHTML-master'

path = getcwd()
path_to_version = path_join(path, REPO_BRANCH_VERSION)
path_to_updater = path_join(path, REPO_BRANCH_UPDATER)
path_to_settings = path_join(path, 'settings')
path_icos_zip = path_join(path_to_settings, 'PassHTMLicos.zip')
path_to_style = path_join(path_to_settings, 'style')
path_ico_screen_saver = path_join(path_to_style, 'PassHTML.png')
path_to_main_style = path_join(path_to_style, 'awthemes-10.2.0')
path_to_settings_json = path_join(path_to_settings, 'settings.json')
path_to_little_ico = path_join(path_to_style, 'LittlePassHTML.ico')
path_to_static = path_join(path_to_settings, 'static')
path_to_passwords = path_join(path_to_settings, 'passwords')
path_to_passwords_settings = path_join(path_to_passwords, 'passwords.settings')
path_to_passwords_json = path_join(path_to_passwords, 'passwords.json')
path_to_html = path_join(path_to_passwords, 'PasswordsInHTML.html')

default_settings = {
    'first_start': 1,
    'auto_update': 1,
    'theme': {
        'font-color': '#494949',
        'back-color': '#DBDBDB',
        'back_card_color': '#f1efef'
    },
    'default_columns': 'Логин&&Пароль'
}


PERSON_AGREEMENT = """
Нажимая кнопку "Принять", вы соглашаетесь с тем, что за все действия в программе несёте ответственность только вы.
Нажимая кнопку "Принять", вы соглашаетесь с тем, что все ваши действия в программе обдуманны.
Нажимая кнопку "Принять", вы соглашаетесь с тем, что запрещены догадки и бездоказательственные обвинения программы, а также её автора за причинённые неполадки или утечку данных по вине пользователя.
Нажимая кнопку "Принять", вы соглашаетесь с тем, что автор не несёт ответственности за модифицированный или перепакованный исполняемый файл, за любые случаи, которые затрагивают целостность исполняемого файла, а также любой вред причинённый программой посредством редактирования содержимого её папки.
Нажимая кнопку "Принять", вы соглашаетесь с тем, что автор не несёт ответственность за утерю ваших данных по вине пользователя.

Только в случае полного понимания всего вышеописанного, нажмите правой кнопкой мыши на кнопку "Принять". Это сообщение показывается только один раз.
"""
