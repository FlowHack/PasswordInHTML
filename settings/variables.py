from os import getcwd
from os.path import join as path_join

path = getcwd()
path_to_settings = path_join(path, 'settings')
path_screen_saver = path_join(path_to_settings, 'PassHTMLicos.zip')
path_to_style = path_join(path_to_settings, 'style')
path_ico_screen_saver = path_join(path_to_style, 'play_store_512.png')
path_to_main_style = path_join(path_to_style, 'awthemes-10.2.0')