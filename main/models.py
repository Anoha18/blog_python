from django.db import models
from account.models import User
from django.contrib.sessions.models import Session

# Create your models here.
class Category(models.Model):
  name = models.TextField()
  description = models.TextField()
  brief = models.TextField()

class Post(models.Model):
  title = models.TextField()
  body = models.TextField()
  image = models.TextField(null=False, default='')
  creator = models.ForeignKey(User, on_delete=models.PROTECT)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(blank=False)
  deleted = models.BooleanField(default=False, blank=False)
  category = models.ForeignKey(Category, on_delete=models.PROTECT)

class Comment(models.Model):
  text = models.TextField()
  creator = models.ForeignKey(User, on_delete=models.PROTECT)
  parent_id = models.BigIntegerField(null=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(blank=False, null=True)
  deleted = models.BooleanField(default=False, blank=False)

class Post_views(models.Model):
  session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=False, null=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)