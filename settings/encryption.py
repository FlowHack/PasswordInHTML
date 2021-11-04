from os.path import isfile

from run import get_dict_from_json_file, write_dict_in_file
from settings import path_to_passwords_settings

ENCRYPTION_ALPHABET = '''Й Ц У К Е Н Г Ш Щ З Х Ъ Ё Ф Ы В А П Р О Л Д Ж Э Я Ч С М И Т Ь Б Ю й ц у к е н г ш щ з х ъ ё ф ы в а п р о л д ж э я ч с м и т ь б ю Q W E R T Y U I O P A S D F G H J K L Z X C V B N M q w e r t y u i o p a s d f g h j k l z x c v b n m 0 1 2 3 4 5 6 7 8 9 ^ @ ! 1 " # $ % & ' ( ) * : + ; { , < \ | - = } . > ~ / ? — _ [ ]'''

class Encryption:
    def __init__(self):
        if not isfile(path_to_passwords_settings):
            self.create_passwords_settings()

        self.settings = get_dict_from_json_file(path_to_passwords_settings)
        
        if 'password_decode' in list(self.settings.keys()):
            self.hash_password_decode = self.settings['password_decode']
        else:
            self.hash_password_decode = None
        self.alphabet, self.step = self.settings['alphabet'], self.settings['step']
        self.reversed_alphabet = {}
        for number, symbol in self.settings['reversed_alphabet'].items():
            self.reversed_alphabet[int(number)] = symbol
    
    @staticmethod
    def create_passwords_settings():
        from random import randint, shuffle

        alphabet = ENCRYPTION_ALPHABET.split() + [' ']
        shuffle(alphabet)

        encrypt_alphabet = {}
        reversed_encrypt_alphabet = {}
        for i in range(len(alphabet)):
            symbol = alphabet[i]
            encrypt_alphabet[symbol] = i
            reversed_encrypt_alphabet[i] = symbol
        

        step = randint(randint(-30, -1), randint(1, 55))

        settings = {
            'step': step,
            'alphabet': encrypt_alphabet,
            'reversed_alphabet': reversed_encrypt_alphabet
        }
        write_dict_in_file(path_to_passwords_settings, settings)

        return settings
    
    def encrypt(self, text: str):
        encrypt_text = ''
        for symbol in text:
            number_symbol = self.alphabet[symbol] + self.step
            while number_symbol > len(self.alphabet)-1:
                number_symbol -= len(self.alphabet)
            while number_symbol < 0:
                number_symbol += len(self.alphabet)
            encrypt_text += self.reversed_alphabet[number_symbol]
        
        return encrypt_text
    
    def decryption(self, text: str):
        decryption_text = ''
        for symbol in text:
            number_symbol = self.alphabet[symbol] - self.step
            while number_symbol < len(self.alphabet) - 1:
                number_symbol += len(self.alphabet)
            while number_symbol > len(self.alphabet) - 1:
                number_symbol -= len(self.alphabet)
            decryption_text += self.reversed_alphabet[number_symbol]
        
        return decryption_text
