from Crypto.Cipher import AES
import hashlib
from api import AESCipher

# def security_middleware(get_response):
#   # One-time configuration and initialization.

#   def middleware(request):
#     # Code to be executed for each request before
#     # the view (and later middleware) are called.

#     key = hashlib.sha256(request.data['password'] + request.data['color'])
#     aes = AESCipher(key=key)

#     response = get_response(request)

#     # Code to be executed for each request/response after
#     # the view is called.

#     return response

#   return middleware

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
      print("custom middleware before next middleware/view")
      response = self.get_response(request)
      print("custom middleware after response or previous middleware")
      return response
