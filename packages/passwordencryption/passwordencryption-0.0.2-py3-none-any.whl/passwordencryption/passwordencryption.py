#!/usr/bin/env python
#

from cryptography.fernet import Fernet
import sys


class passwordencryption:
  def encrypt(self):
    key = Fernet.generate_key()
    refKey = Fernet(key)
    mypwdbyt = bytes(self, 'utf-8')
    encryptedPWD = refKey.encrypt(mypwdbyt)
    key = key.decode("utf-8")
    encryptedPWD = encryptedPWD.decode("utf-8")
    encryptedpassword = key[:43] + encryptedPWD
    return encryptedpassword


  def decrypt(self):
    key = self[:43] + '='
    key = bytes(key, 'utf-8')
    keytouse = Fernet(key)
    encryptedPWD = self[43:]
    try:
        encryptedPWD =  bytes(encryptedPWD, 'utf-8')
        decryptedPWD = (keytouse.decrypt(encryptedPWD))
        decryptedPWD = decryptedPWD.decode("utf-8")
        decryptedPWD = decryptedPWD.replace(' ', '')
    except:
        decryptedPWD = ('Invalid Encrypted Password')

    return decryptedPWD

