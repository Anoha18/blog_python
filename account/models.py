from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .user_manager import UserManager


# Create your models here.
class User(AbstractBaseUser):
  first_name = models.TextField()
  last_name = models.TextField(blank=False, null=True)
  login = models.TextField(unique=True)
  password = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(blank=False)
  deleted = models.BooleanField(default=False)

  USERNAME_FIELD = 'login'
  REQUIRED_FIELDS = ['first_name']

  objects = UserManager()

  def __str__ (self):
    return self.first_name

  class Meta:
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'


