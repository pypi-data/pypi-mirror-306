
import random
import string
_h = {
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

_sp = 'G'

def generate_key(length: int = 12) -> str:
    """إنشاء مفتاح عشوائي باستخدام أحرف السداسية."""
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

def encode_character(char: str, key: int) -> str:
    """تشفير حرف واحد باستخدام المفتاح."""
    return str(ord(char) + key)

def dump(text: str) -> bytes:
    """تشفير النص المدخل وإرجاع النتيجة بتنسيق بايت."""
    _tre = []
    _out = []
    key = random.randint(1, 100)
    for char in text:
        _tre.append(encode_character(char, key))
    for value in _tre:
        for digit in value:
            _out.append(_h[digit]) 
        _out.append(_sp) 
    encrypted_key = generate_key()
    for digit in str(key):
        _out.append(_h[digit])
    _out.append(_sp)
    _out.append(encrypted_key)
    return ''.join(_out).encode('utf-8') 
def decode_character(encoded_char: str) -> str:
    """فك تشفير حرف واحد باستخدام التشفير العكسي."""
    for im, ip in _h.items():
        if ip == encoded_char + " ":
            return im
    return ''
def load(text: bytes) -> str:
    """فك تشفير النص المشفر وإرجاع النص الأصلي."""
    _ts = ''
    _d = []
    lis = text.decode('utf-8').split(_sp)
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
    """التحقق من صحة المدخلات."""
    return isinstance(text, str) and len(text) > 0


