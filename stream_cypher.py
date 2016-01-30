from random import *

def encode(key, msg):
    seed(key)
    out = [chr((ord(char) - 97 + randint(0,10000)) % 26 + 97)  for char in msg]
    return "".join(out)

def decode(key, msg):
    seed(key)
    out = [chr((ord(char) - 97 - randint(0,10000)) % 26 + 97)  for char in msg]
    return "".join(out)

'''
Using a seed as the key, messages are encoded using the randint method
'''
