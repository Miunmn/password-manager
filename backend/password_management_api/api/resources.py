import hashlib
import string
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *

from django.db.models import Q

from api.models import User, StoredPasswords
from api.AESCipher import AESCipher

import json
from django.http import JsonResponse
# class UserManagerView(APIView):
#   def get(self, request):
#     try:      
#       users = User.objects.all().values()
#     except Exception as e:
#       return Response(data=f'Error: {e}', status=500)
#     user_list = list(users)
#     return JsonResponse({"dataList": json.dumps(user_list)}) 


class SignUpView(APIView):
  def post(self, request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    username = body.get('username', None)
    password = body.get('password', None)
    salt = ''.join(random.choice(string.digits) for i in range(10)) 
    
    # salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    salt_encoded = salt.encode('utf-8')

    hashed_password = hashlib.sha256(password + salt_encoded)
    print(salt, hashed_password)

    new_user = User(username=username, salt=salt, password=hashed_password.hexdigest())
    try:
      new_user.save()
    except Exception as es:
      return Response(data="Error al guardar nuevo usuario", status=404)
    return Response(data=[], status=200)

class LoginManagerView(APIView):
  def post(self, request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    username = body.get('username', None)
    password = body.get('password', None)

    try:
      user = User.objects.filter(username=username)
    except e as Exception:
      print(e)
      return Response(data="Error while retrieving username", status=404)

    if len(user) == 0:
      return Response(data="No users found", status=404)

    user = user.first()
    user_salt = user.salt
    salt = user_salt.encode('utf-8')
    password = password.encode('utf-8')
    
    hashed_password = hashlib.sha256(password + salt)

    print(user.password, hashed_password.hexdigest() )
    if user.password == hashed_password.hexdigest():
      return Response(data='Logged in!', status=200)

    return Response(data="Incorrect credentials", status=401)

def modify_passwords(username, color, obj=None, delete=False):
    aes = AESCipher(key=username+color)
    encrypted_passwords = StoredPasswords.objects.filter(Q(username=username)).passwords
    decrypted_passwords = aes.decrypt(encrypted_passwords)
    decrypted_passwords = json.loads(decrypted_passwords)
    if not delete:
      decrypted_passwords.update(obj)
    else:
      decrypted_passwords.pop(obj)
    decrypted_passwords = json.dumps(decrypted_passwords)
    return aes.encrypt(decrypted_passwords)
  
class PasswordsManagerView(APIView):
  def post(self, request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    username = body['username'] 
    site = body['site']
    password = body['password']
    color = body['color']

    if request.data['action'] == 'add':
      obj = {'site': site, 'password': password}

      encrypted_passwords = modify_passwords(username, color, obj)

      try:
        StoredPasswords.objects.filter(Q(username=username)).update(passwords=encrypted_passwords)
        return Response(data="Added", status=200)
      except Exception as e:
        return Response(data=f"Error: {e}", status=500)

    elif request.data['action'] == 'get':
      body_unicode = request.body.decode('utf-8')
      body = json.loads(body_unicode)

      username = body['username'] 
      site = body['site']
      password = body['password']
      color = body['color']

      passwords = StoredPasswords.objects.filter(Q(username=username))
      return Response(data=passwords, status=200)
  
  def put(self, request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    username = body['username'] 
    site = body['site']
    password = body['password']
    color = body['color']

    obj = {'site': site, 'password': password}

    encrypted_passwords = modify_passwords(username, color, obj)

    try:
      StoredPasswords.objects.filter(Q(username=username)).update(passwords=encrypted_passwords)
      return Response(data="Updated", status=200)
    except Exception as e:
      return Response(data=f"Error: {e}", status=500)
  
  def delete(self, request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    username = body['username'] 
    site = body['site']
    color = body['color']

    encrypted_passwords = modify_passwords(username, color, site)

    try:
      StoredPasswords.objects.filter(Q(username=username)).update(passwords=encrypted_passwords)
      return Response(data="Deleted", status=200)
    except Exception as e:
      return Response(data=f"Error: {e}", status=500)