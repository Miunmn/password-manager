
from django.urls import path
from . import resources


urlpatterns = [
  path('authorization/login/', resources.LoginMangerView.as_view()),
]