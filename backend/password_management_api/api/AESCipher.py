from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import base64
from django.db.models import Q

class AESCipher:
    def __init__(self, key): 
      self.bs = 16
      self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
      raw = self._pad(raw)
      iv = Random.new().read(16)
      cipher = AES.new(self.key, AES.MODE_CBC, iv)
      return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
      enc = base64.b64decode(enc)
      iv = enc[:16]
      cipher = AES.new(self.key, AES.MODE_CBC, iv)
      return self._unpad(cipher.decrypt(enc[16:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
