from Crypto.Cipher import AES
from api import AESCipher
from rest_framework.response import Response

from django.db.models import Q

from api.models import StoredPasswords 

import json
"""
def verify_user(request):
    username = request.data['username']
    password = request.data['password']
    color = request.data['color']

    unhashed_key = password + color
    aes = AESCipher(key=unhashed_key)
    encrypted_stored_passwords_obj = StoredPasswords.objects.filter(Q(username=username)).passwords
    decrypted_stored_passwords_obj = aes.decrypt(encrypted_stored_passwords_obj)

    try:
        data = json.loads(decrypted_stored_passwords_obj)
        return Response(data=encrypted_stored_passwords_obj, status=200)
    except Exception as e:
        return Response(data=f'Decryption returned a non-valid JSON object. Error: {e}', status=401)

def security_middleware(get_response):
   # One-time configuration and initialization.

   def middleware(request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.
    
    response = get_response(request)

    # Code to be executed for each request/response after
    # the view is called.

    return response

   return middleware
"""

class CustomMiddleware:
    def __init__(self, get_response):
       self.get_response = get_response

    def verify_user(self, request):
        username = request.data['username']
        password = request.data['password']
        color = request.data['color']

        unhashed_key = password + color
        aes = AESCipher(key=unhashed_key)
        encrypted_stored_passwords_obj = StoredPasswords.objects.filter(Q(username=username)).passwords
        decrypted_stored_passwords_obj = aes.decrypt(encrypted_stored_passwords_obj)

        try:
            data = json.loads(decrypted_stored_passwords_obj)
            return Response(data=encrypted_stored_passwords_obj, status=200)
        except Exception as e:
            return Response(data=f'Decryption returned a non-valid JSON object. Error: {e}', status=401)

    def __call__(self, request):
      print("custom middleware before next middleware/view")
      #response = self.get_response(request)
      response = self.verify_user(request)
      print("custom middleware after response or previous middleware")
      return response
