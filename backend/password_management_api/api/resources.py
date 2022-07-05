import hashlib

from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q

from backend.password_management_api.models import User

class UserManagerView(APIView):
  def get(self, request):
    try:      
      users = User.objects.all()
    except Exception as e:
      return Response(data=f'Error: {e}', status=500)
    return Response(data=users, status=200)

class LoginManagerView(APIView):
  def post(self, request, format=None):
    username = request.data['username']
    password = request.data['password']

    user = User.objects.filter(Q(username=username))
    if len(user) == 0:
      return Response(data="No users found", status=404)

    hashed_password = hashlib.sha256(password + user.salt)
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
