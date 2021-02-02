from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime

class UserManager(BaseUserManager):
  def create_user(self, firstname, login, password):
    if not login or not firstname or not password:
      raise ValueError('Not found login or firstname or password')

    user = self.model(
      first_name = firstname,
      login = login,
      updated_at = datetime.now()
    )

    user.set_password(password)
    user.save(using=self._db)

    return user