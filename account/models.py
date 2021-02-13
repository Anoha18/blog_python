from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .user_manager import UserManager
from django.contrib.sessions.models import Session


# Create your models here.
class User(AbstractBaseUser):
  first_name = models.TextField()
  last_name = models.TextField(blank=False, null=True)
  login = models.TextField(unique=True)
  password = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(blank=False)
  deleted = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False, null=False)

  USERNAME_FIELD = 'login'
  REQUIRED_FIELDS = ['first_name']

  objects = UserManager()

  def __str__ (self):
    return self.login

  class Meta:
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'

class User_sessions(models.Model):
  session = models.ForeignKey(Session, on_delete=models.CASCADE, null=False, blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
  active = models.BooleanField(default=True, null=False, blank=False)
  created_at = models.DateTimeField(auto_now=True, null=False, blank=False)
  closed_at = models.DateTimeField(null=True)