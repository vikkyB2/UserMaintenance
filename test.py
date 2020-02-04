import time   
import mysql.connector 
import hashlib

import zlib

inp = input('Enter something: ')
salt = input('Enter salt ')
dk = hashlib.pbkdf2_hmac('sha256', inp.encode('utf-8'), salt.encode('utf-8'), 100000)
print(dk)


