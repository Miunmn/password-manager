from Crypto.Cipher import AES
import hashlib
import base64
from django.db.models import Q
from api.resources import User
class AESCipher:

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw, request):
      username = request.data['username']

      raw = self._pad(raw)
      iv = User.objects.filter(Q(username=username))[0].iv
      cipher = AES.new(self.key, AES.MODE_CBC, iv)
      return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc, request):
      username = request.data['username']

      enc = base64.b64decode(enc)
      iv = User.objects.filter(Q(username=username))[0].iv
      cipher = AES.new(self.key, AES.MODE_CBC, iv)
      return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
