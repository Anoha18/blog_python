from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name="account_home"),
  path('logout/', views.logout, name="account_logout"),
  path('posts/', views.posts, name="account_posts"),
  path('posts/new', views.new_post, name="account_new_post"),
  path('categories/', views.categories, name="account_categories")
]