from django.db import models
from account.models import User

# Create your models here.
class Category(models.Model):
  name = models.TextField()
  description = models.TextField()
  brief = models.TextField()

class Post(models.Model):
  title = models.TextField()
  body = models.TextField()
  creator = models.ForeignKey(User, on_delete=models.PROTECT)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(blank=False)
  deleted = models.BooleanField(default=False, blank=False)
  category = models.ForeignKey(Category, on_delete=models.PROTECT)