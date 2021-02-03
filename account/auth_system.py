from django.contrib.auth.backends import ModelBackend
from .models import User

class AuthSystem(ModelBackend):
  def authenticate(self, request, login, password, **kwargs):
    user = User.objects.get(login=login)
    isValidPassword = user.check_password(password)
    if isValidPassword is False:
      return None
    return user

  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
