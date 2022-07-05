from Crypto.Cipher import AES
from api import AESCipher
from rest_framework.response import Response
from django.db.models import Q
from api.models import StoredPasswords 
from django.http import HttpResponseForbidden
import json

class CustomMiddleware:
    def __init__(self, get_response):
       self.get_response = get_response

    def verify_user(self, request):
        if request.method != "POST":
            return request
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        username = body.get('username', None)
        password = body.get('password', None)
        color = body.get('color', None)

        if color is None:
            return request

        try:
            unhashed_key = password + color
            aes = AESCipher(key=unhashed_key)
            encrypted_stored_passwords_obj = StoredPasswords.objects.filter(Q(username=username)).passwords
            decrypted_stored_passwords_obj = aes.decrypt(encrypted_stored_passwords_obj)
            data = json.loads(decrypted_stored_passwords_obj)
            return request
        except Exception as e:
            print('Error:', e)
            return HttpResponseForbidden()

    def __call__(self, request):
    #   verification = self.verify_user(request)
      response = self.get_response(request)
      return response
