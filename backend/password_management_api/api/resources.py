from rest_framework.views import APIView
from rest_framework.response import Response

class LoginMangerView(APIView):
  def post(self, request, format=None):
    return Response(data='Logged in!', status=200)
