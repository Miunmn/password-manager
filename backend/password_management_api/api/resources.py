import hashlib
import string
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *

from django.db.models import Q

from api.models import User

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

    new_user = User(username=username, salt=salt, password=hashed_password)
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

    if user.password == hashed_password:
      return Response(data='Logged in!', status=200)

    return Response(data="Incorrect credentials", status=401)
  

class PasswordsManagerView(APIView):
  def post(self, request, format=None):

    if request.data['action'] == 'add':
      #add password to django's database
      site = request.data['site']
      password = request.data['password']
      obj = {'site': site, 'password': password}
      return Response(data="Added", status=200)

    elif request.data['action'] == 'get_stored_passwords':
      data = {}
      #get passwords
        #token based application
        #return encrypted passwords
      return Response(data=data, status=200)
  
  def put(self, request, format=None):
    return Response(data="SIU", status=200)
  
  def delete(self, request, format=None):
    return Response(data="Deleted", status=200)
