import random
_h = {
    '1': 'WD',
    '2': 'ED',
    '3': 'AD',
    '4': 'KD',
    '5': 'SD',
    '6': 'ZD',
    '7': 'MD',
    '8': 'OD',
    '9': 'FD',
    '0': 'TD'
}
_sp = 'D'
def generate_key(length):
    return ''.join(random.choice('0123456789') for _ in range(length))
def random_obfuscation(data: str) -> str:
    return ''.join(random.choice(['|', ';', '$', '%', '&', '*','      ']) + char for char in data)
def Devil(text: str):
    _out = []
    key = generate_key(len(text))
    for i, char in enumerate(text):
        encrypted_char = ord(char) ^ ord(key[i % len(key)])
        _out.append(str(encrypted_char))
    encoded_output = []
    for num in _out:
        for digit in num:
            if digit in _h:
                encoded_output.append(_h[digit])
            else:
                raise ValueError(f"Unsupported digit: {digit}")
        encoded_output.append(_sp)
    for digit in key:
        if digit in _h:
            encoded_output.append(_h[digit])
        else:
            raise ValueError(f"Unsupported key digit: {digit}")
    encoded_output.append(_sp)
    final_output = ''.join(encoded_output)
    obfuscated_output = random_obfuscation(final_output)
    return obfuscated_output.encode('utf-8')
def Nasr(text: bytes):
    obfuscated_text = text.decode('utf-8')
    cleaned_text = ''.join([char for char in obfuscated_text if char.isalnum() or char == _sp])
    _ts = ''
    _d = []
    key = ""
    lis = cleaned_text.split(_sp)
    key_segment = lis[-2]
    for io in key_segment.split("D"):
        for im, ip in _h.items():
            if ip == io + "D":
                key += im
    for segment in lis[:-2]:
        for io in segment.split('D'):
            for im, ip in _h.items():
                if ip == io + 'D':
                    _ts += im
        _ts += ','
    for i in _ts.split(','):
        if len(i) >= 1:
            original_char = chr(int(i) ^ ord(key[len(_d) % len(key)]))
            _d.append(original_char)
    exec(''.join(_d))