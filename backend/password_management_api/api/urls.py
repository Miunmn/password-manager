from django.urls import path
from . import resources

urlpatterns = [
  path('authorization/login', resources.LoginManagerView.as_view()),
  path('passwords', resources.PasswordsManagerView.as_view())
]