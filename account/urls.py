from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name="account_home"),
  path('logout/', views.logout, name="account_logout"),
  path('posts/', views.posts, name="account_posts"),
  path('posts/new', views.new_post, name="account_new_post"),
  path('posts/<int:post_id>/edit', views.edit_post, name="account_edit_post"),
  path('categories/', views.categories, name="account_categories"),
  path('categories/<int:cat_id>', views.category, name="account_category"),
]