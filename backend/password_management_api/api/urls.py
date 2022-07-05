import hashlib
import base64
from Crypto.Cipher import AES

from django.urls import path
from django.db.models import Q

from backend.password_management_api.models import User
from . import resources

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

def simple_middleware(get_response):
  # One-time configuration and initialization.

  def middleware(request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.

    key = hashlib.sha256(request.data['password'] + request.data['color'])
    aes = AESCipher(key=key)

    response = get_response(request)

    # Code to be executed for each request/response after
    # the view is called.

    return response

  return middleware


urlpatterns = [
  path('authorization/login/', resources.LoginManagerView.as_view()),
  path('passwords', resources.PasswordsManagerView.as_view())
]