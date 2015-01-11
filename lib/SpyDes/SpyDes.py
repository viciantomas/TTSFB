#   SpyDes: Simplified pyDes
#   Copyright 2015 Štefan Uram
#   This file is part of TTSFB.

import SpyDes.pyDes as pyDes
import hashlib

def valid_key(key):
    key = str(key)
    key = hashlib.md5(str.encode(key)).digest()
    return key


def encrypt(key, string):
    string = str.encode(string)
    encrypted_string = pyDes.triple_des(valid_key(key)).encrypt(string, padmode=2)
    return encrypted_string

def decrypt(key, string):
    decrypted_string = pyDes.triple_des(valid_key(key)).decrypt(string, padmode=2)
    return decrypted_string.decode("utf-8")