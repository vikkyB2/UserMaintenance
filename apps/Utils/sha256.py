import hashlib

def hashPinbyKey(pin,salt):
    dk = hashlib.pbkdf2_hmac('sha256', pin.encode('utf-8'), salt.encode('utf-8'), 100000)
    hashpin = dk.hex()
    return hashpin