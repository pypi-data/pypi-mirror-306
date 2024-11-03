
import random
_h={
'1':'WI',
'2':'EI',
'3':'AI',
'4':'KI',
'5':'SI',
'6':'ZI',
'7':'MI',
'8':'OI',
'9':'DI',
'0':'TI'
}
_sp='L'

def dump(text:str):
    _tre=[]
    _out=[]
    key=random.randint(1,100)
    for i in list(text):
        _tre.append(str(ord(i)+key))
    for i in _tre:
        for i in list(i):
            _out.append(_h[i])
        _out.append(_sp)
    for x in str(key):
        _out.append(_h[x])
    _out.append(_sp)
    return ''.join(_out).encode('utf-8')

def load(text:bytes):
    _ts=''
    _d=[]
    key=""
    lis=text.decode('utf-8').split('L')
    for x in lis[-2]:
        for io in x.split("I"):
            for im,ip in _h.items():
                if ip==io+"I":
                    key+=im
    lis.remove(lis[-2])
    for i in lis:
        for io in i.split('I'):
            for im,ip in _h.items():
                if ip==io+'I':
                    _ts+=im
        _ts+=','
    for i in _ts.split(','):
        if len(i)>=1:
            _d.append(chr(int(i)-int(key)))
    exec(''.join(_d))


