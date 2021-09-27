from os.path import isfile
from settings import path_to_passwords_settings
from run import get_dict_from_json_file, write_dict_in_file

ENCRYPTION_ALPHABET = '''a 0 @ p а п я Щ С ! 1 A q б р А Ъ " 2 B r в с Б Ы # 3 C s г т В Ь $ 4 D t д у Г Э % 5 E u е ф Д Ю & 6 F v ё х Е Я ' 7 G w ж ц Ё И ( 8 H x з ч Ж Й ) 9 I y и ш З К * : J z й щ У Л + ; K { к ъ Ф М , < L \ | л ы Х Н Т - = M } м ь Ц О . > N ~ н э Ч П / ? O — о ю Ш Р'''

class Encryption:
    def __init__(self):
        if not isfile(path_to_passwords_settings):
            self.create_passwords_settings()

        settings = get_dict_from_json_file(path_to_passwords_settings)
        
        self.alphabet, self.step = settings['alphabet'], settings['step']
        self.reversed_alphabet = {}
        for number, symbol in settings['reversed_alphabet'].items():
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

    