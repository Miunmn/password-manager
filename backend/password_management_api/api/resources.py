import hashlib

from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q

from api.models import User, StoredPasswords
from api.AESCipher import AESCipher

import json

class UserManagerView(APIView):
  def get(self, request):
    try:      
      users = User.objects.all()
    except Exception as e:
      return Response(data=f'Error: {e}', status=500)
    return Response(data=users, status=200)

class LoginManagerView(APIView):
  def post(self, request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    username = body['username']
    password = body['password']

    user = User.objects.filter(Q(username=username))
    if len(user) == 0:
      return Response(data="No users found", status=404)

    hashed_password = hashlib.sha256(password + user.salt)
    if user.password == hashed_password:
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